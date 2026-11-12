"""Dependency-free request validators for the ML service."""

import os

ALLOWED_AUDIO_EXTENSIONS = frozenset({'wav', 'mp3', 'flac', 'ogg', 'm4a', 'webm'})


def allowed_audio_file(filename, allowed_extensions=ALLOWED_AUDIO_EXTENSIONS):
    """Return True when ``filename`` ends in a supported audio extension."""
    if not filename or '.' not in filename:
        return False

    extension = filename.rsplit('.', 1)[-1].lower()
    normalized = {ext.lower().lstrip('.') for ext in allowed_extensions}
    return extension in normalized


def is_downloadable_model(path):
    """Return True when the weights file exists on disk."""
    return bool(path) and os.path.exists(path)
