import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Runtime configuration, overridable through environment variables."""

    # Model
    MODEL_PATH = os.getenv('MODEL_PATH', 'deepfake_audio_detection_model.h5')

    # Uploads
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_UPLOAD_BYTES = int(os.getenv('MAX_UPLOAD_BYTES', 20 * 1024 * 1024))
    ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'flac', 'ogg', 'm4a', 'webm'}

    # Signal quality
    MIN_AUDIO_SECONDS = float(os.getenv('MIN_AUDIO_SECONDS', '0.5'))
    MAX_AUDIO_SECONDS = float(os.getenv('MAX_AUDIO_SECONDS', '30.0'))
    MIN_RMS = float(os.getenv('MIN_RMS', '1e-4'))

    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

    # Optional transcription provider
    TRANSCRIBE_API_URL = os.getenv('TRANSCRIBE_API_URL', '')
    TRANSCRIBE_API_TOKEN = os.getenv('TRANSCRIBE_API_TOKEN', '')


config = Config()
