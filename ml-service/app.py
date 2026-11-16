import os
import random
import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Blueprint, Flask, abort, current_app, has_app_context, jsonify, request
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from config import config
from validators import allowed_audio_content, allowed_audio_file, validate_audio_signal

_model = None

FORM_MIMETYPES = frozenset({'multipart/form-data', 'application/x-www-form-urlencoded'})
SIGNAL_ERROR_MESSAGES = {
    'AUDIO_TOO_SHORT': 'Audio is too short',
    'AUDIO_TOO_LONG': 'Audio is too long',
    'AUDIO_SILENT': 'Audio is silent or below the minimum signal level',
}


def error_response(message, code, status):
    """Return a JSON error envelope with a stable machine-readable code."""
    return jsonify({'error': message, 'code': code}), status


def validate_upload_request():
    """Enforce the upload limit and reject non-form request bodies."""
    limit = current_app.config.get('MAX_CONTENT_LENGTH')
    if limit is not None and request.content_length is not None and request.content_length > limit:
        raise RequestEntityTooLarge()

    if request.mimetype and request.mimetype not in FORM_MIMETYPES:
        abort(415, description='Unsupported media type: expected multipart/form-data')


def handle_bad_request(error):
    message = getattr(error, 'description', None) or 'Bad request'
    return error_response(message, 'BAD_REQUEST', 400)


def handle_not_found(error):
    return error_response('Resource not found', 'NOT_FOUND', 404)


def handle_method_not_allowed(error):
    return error_response('Method not allowed', 'METHOD_NOT_ALLOWED', 405)


def handle_request_entity_too_large(error):
    limit = current_app.config.get('MAX_CONTENT_LENGTH')
    if limit is None:
        limit = current_app.config.get('MAX_UPLOAD_BYTES')
    return error_response(
        f'Payload too large: upload exceeds MAX_UPLOAD_BYTES ({limit} bytes)',
        'PAYLOAD_TOO_LARGE',
        413,
    )


def handle_unsupported_media_type(error):
    message = getattr(error, 'description', None) or 'Unsupported media type'
    return error_response(message, 'UNSUPPORTED_MEDIA_TYPE', 415)


def handle_internal_server_error(error):
    original = getattr(error, 'original_exception', None)
    current_app.logger.error(
        'Unhandled error processing %s %s',
        request.method,
        request.path,
        exc_info=original if original is not None else True,
    )
    return error_response('Internal server error', 'INTERNAL_SERVER_ERROR', 500)


def get_model():
    """Load the Keras model on first use.

    Loading lazily means the service can start (and answer /api/health)
    even when the weights file has not been downloaded yet. The TensorFlow
    import lives here so the app can be imported without the ML stack.
    """
    global _model
    if _model is None:
        model_path = current_app.config['MODEL_PATH'] if has_app_context() else config.MODEL_PATH
        if not os.path.exists(model_path):
            raise RuntimeError(f'Model not found at {model_path}')

        from tensorflow.keras.models import load_model

        _model = load_model(model_path)
    return _model


# Function to make prediction
def predict_audio(audio_path):
    # Imported lazily: librosa/matplotlib are only needed for predictions.
    from preprocessing import generate_spectrogram, preprocess_input_audio

    model = get_model()
    processed_audio = preprocess_input_audio(audio_path)
    prediction = model.predict(processed_audio)
    prediction_score = float(prediction[0][0])
    classification = 'Real' if prediction_score > 0.5 else 'Fake'
    spectrogram_path = generate_spectrogram(audio_path, current_app.config['UPLOAD_FOLDER'])
    return classification, prediction_score, spectrogram_path


api = Blueprint('api', __name__)


@api.route('/api/health', methods=['GET'])
def health_check():
    """Liveness probe that also reports whether weights are installed."""
    return jsonify({
        'status': 'UP',
        'service': 'Deepfake Speech Detection ML Service',
        'model_present': os.path.exists(current_app.config['MODEL_PATH']),
    })


@api.route('/api/predict', methods=['POST'])
def predict():
    """Classify an uploaded audio clip as real or deepfake.

    Expects multipart form data with a single ``file`` field.
    """
    validate_upload_request()

    if 'file' not in request.files:
        return error_response('No file provided', 'BAD_REQUEST', 400)

    file = request.files['file']
    if file.filename == '':
        return error_response('No file selected', 'BAD_REQUEST', 400)

    if not allowed_audio_file(file.filename, current_app.config['ALLOWED_AUDIO_EXTENSIONS']):
        payload = {
            'error': 'Unsupported audio format',
            'code': 'BAD_REQUEST',
            'allowed': sorted(current_app.config['ALLOWED_AUDIO_EXTENSIONS']),
        }
        return jsonify(payload), 400

    if not allowed_audio_content(
        file.stream, file.filename, current_app.config['ALLOWED_AUDIO_EXTENSIONS']
    ):
        return error_response(
            'File content is not a supported audio format', 'INVALID_AUDIO_CONTENT', 400
        )

    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
    filename = secure_filename(file.filename)
    audio_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'], f'{uuid.uuid4().hex}_{filename}'
    )
    file.save(audio_path)

    try:
        try:
            validate_audio_signal(
                audio_path,
                min_seconds=current_app.config['MIN_AUDIO_SECONDS'],
                max_seconds=current_app.config['MAX_AUDIO_SECONDS'],
                min_rms=current_app.config['MIN_RMS'],
            )
        except ValueError as exc:
            code = getattr(exc, 'code', None) or str(exc)
            if code not in SIGNAL_ERROR_MESSAGES:
                raise
            message = getattr(exc, 'message', None) or SIGNAL_ERROR_MESSAGES[code]
            return error_response(message, code, 422)

        classification, confidence, spectrogram_path = predict_audio(audio_path)
    except RuntimeError as exc:
        return error_response(str(exc), 'SERVICE_UNAVAILABLE', 503)
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

    return jsonify({
        'classification': classification,
        'confidence': round(confidence, 4),
        'spectrogram': spectrogram_path,
    })


# Transcription endpoint
@api.route('/transcribe', methods=['POST'])
def transcribe_audio():
    validate_upload_request()

    if 'file' not in request.files:
        return error_response('No file provided', 'BAD_REQUEST', 400)

    file = request.files['file']
    if file.filename == '':
        return error_response('No file selected', 'BAD_REQUEST', 400)

    if not current_app.config['TRANSCRIBE_API_URL'] or not current_app.config['TRANSCRIBE_API_TOKEN']:
        return error_response('Transcription provider is not configured', 'SERVICE_UNAVAILABLE', 503)

    # Imported lazily so the rest of the service does not depend on requests.
    import requests

    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)

    headers = {
        'Authorization': f"Bearer {current_app.config['TRANSCRIBE_API_TOKEN']}",
        'Content-Type': 'audio/wav',
    }
    with open(file_path, 'rb') as f:
        response = requests.post(current_app.config['TRANSCRIBE_API_URL'], headers=headers, data=f)

    if response.status_code != 200:
        return error_response('Transcription failed', 'INTERNAL_SERVER_ERROR', 500)

    transcription = response.json().get('transcription', '')
    return jsonify({'transcription': transcription})


# Two-step verification
def send_otp(email):
    sender = os.getenv('MAIL_USERNAME')
    password = os.getenv('MAIL_PASSWORD')
    if not sender or not password:
        raise RuntimeError('MAIL_USERNAME and MAIL_PASSWORD must be configured')

    otp = random.randint(100000, 999999)
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = email
    msg['Subject'] = 'Your OTP Code'
    body = f'Your OTP code is {otp}'
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(os.getenv('MAIL_HOST', 'smtp.outlook.com'), int(os.getenv('MAIL_PORT', 587)))
    server.starttls()
    server.login(sender, password)
    text = msg.as_string()
    server.sendmail(sender, email, text)
    server.quit()

    return otp


def create_app(config_object=None):
    """Build a Flask app with the default config and optional overrides."""
    app = Flask(__name__)
    app.config.from_object(config)

    if config_object is not None:
        if isinstance(config_object, dict):
            app.config.update(config_object)
        else:
            app.config.from_object(config_object)

    app.config['MAX_CONTENT_LENGTH'] = app.config['MAX_UPLOAD_BYTES']

    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(404, handle_not_found)
    app.register_error_handler(405, handle_method_not_allowed)
    app.register_error_handler(413, handle_request_entity_too_large)
    app.register_error_handler(RequestEntityTooLarge, handle_request_entity_too_large)
    app.register_error_handler(415, handle_unsupported_media_type)
    app.register_error_handler(500, handle_internal_server_error)

    app.register_blueprint(api)
    return app


app = create_app()


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
