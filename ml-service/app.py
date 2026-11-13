import os
import random
import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Blueprint, Flask, current_app, has_app_context, jsonify, request
from werkzeug.utils import secure_filename

from config import config
from validators import allowed_audio_file

_model = None


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
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_audio_file(file.filename, current_app.config['ALLOWED_AUDIO_EXTENSIONS']):
        return jsonify({
            'error': 'Unsupported audio format',
            'allowed': sorted(current_app.config['ALLOWED_AUDIO_EXTENSIONS']),
        }), 400

    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
    filename = secure_filename(file.filename)
    audio_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'], f'{uuid.uuid4().hex}_{filename}'
    )
    file.save(audio_path)

    try:
        classification, confidence, spectrogram_path = predict_audio(audio_path)
    except RuntimeError as exc:
        return jsonify({'error': str(exc)}), 503
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
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not current_app.config['TRANSCRIBE_API_URL'] or not current_app.config['TRANSCRIBE_API_TOKEN']:
        return jsonify({'error': 'Transcription provider is not configured'}), 503

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
        return jsonify({'error': 'Transcription failed'}), 500

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
    app.register_blueprint(api)
    return app


app = create_app()


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
