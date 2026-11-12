import os
import random
import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from flask import Flask, jsonify, request
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename

from config import config
from preprocessing import generate_spectrogram, preprocess_input_audio
from validators import allowed_audio_file

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = config.MAX_UPLOAD_BYTES

_model = None


def get_model():
    """Load the Keras model on first use.

    Loading lazily means the service can start (and answer /api/health)
    even when the weights file has not been downloaded yet.
    """
    global _model
    if _model is None:
        if not os.path.exists(config.MODEL_PATH):
            raise RuntimeError(f'Model not found at {config.MODEL_PATH}')
        _model = load_model(config.MODEL_PATH)
    return _model


# Function to make prediction
def predict_audio(audio_path):
    processed_audio = preprocess_input_audio(audio_path)
    prediction = get_model().predict(processed_audio)
    prediction_score = float(prediction[0][0])
    classification = 'Real' if prediction_score > 0.5 else 'Fake'
    spectrogram_path = generate_spectrogram(audio_path, config.UPLOAD_FOLDER)
    return classification, prediction_score, spectrogram_path


@app.route('/api/health', methods=['GET'])
def health_check():
    """Liveness probe that also reports whether weights are installed."""
    return jsonify({
        'status': 'UP',
        'service': 'Deepfake Speech Detection ML Service',
        'model_present': os.path.exists(config.MODEL_PATH),
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """Classify an uploaded audio clip as real or deepfake.

    Expects multipart form data with a single ``file`` field.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_audio_file(file.filename, config.ALLOWED_AUDIO_EXTENSIONS):
        return jsonify({
            'error': 'Unsupported audio format',
            'allowed': sorted(config.ALLOWED_AUDIO_EXTENSIONS),
        }), 400

    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    filename = secure_filename(file.filename)
    audio_path = os.path.join(config.UPLOAD_FOLDER, f'{uuid.uuid4().hex}_{filename}')
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
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not config.TRANSCRIBE_API_URL or not config.TRANSCRIBE_API_TOKEN:
        return jsonify({'error': 'Transcription provider is not configured'}), 503

    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)

    headers = {
        'Authorization': f'Bearer {config.TRANSCRIBE_API_TOKEN}',
        'Content-Type': 'audio/wav',
    }
    with open(file_path, 'rb') as f:
        response = requests.post(config.TRANSCRIBE_API_URL, headers=headers, data=f)

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


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
