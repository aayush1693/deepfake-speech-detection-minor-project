"""Dependency-free request validators for the ML service."""

import os

import filetype

ALLOWED_AUDIO_EXTENSIONS = frozenset({'wav', 'mp3', 'flac', 'ogg', 'm4a', 'webm'})

# The content type detected for each extension. filetype reports M4A files
# either as their own type or as MP4, because M4A is an MP4 container.
AUDIO_CONTENT_EXTENSIONS = {
    'wav': frozenset({'wav'}),
    'mp3': frozenset({'mp3'}),
    'flac': frozenset({'flac'}),
    'ogg': frozenset({'ogg'}),
    'm4a': frozenset({'m4a', 'mp4'}),
    'webm': frozenset({'webm'}),
}

HEADER_SIZE = 8192


def allowed_audio_file(filename, allowed_extensions=ALLOWED_AUDIO_EXTENSIONS):
    """Return True when ``filename`` ends in a supported audio extension."""
    if not filename or '.' not in filename:
        return False

    extension = filename.rsplit('.', 1)[-1].lower()
    normalized = {ext.lower().lstrip('.') for ext in allowed_extensions}
    return extension in normalized


def detect_audio_type(file_stream, size=HEADER_SIZE):
    """Detect the container type from the first ``size`` bytes of a stream.

    The original stream position is restored afterwards so the upload can
    still be saved by Flask. Returns ``None`` for empty or unknown content.
    """
    if file_stream is None or not hasattr(file_stream, 'read'):
        return None

    try:
        position = file_stream.tell()
        file_stream.seek(0)
    except (AttributeError, OSError):
        position = None

    try:
        header = file_stream.read(size)
    finally:
        if position is not None:
            try:
                file_stream.seek(position)
            except (AttributeError, OSError):
                pass

    if not isinstance(header, (bytes, bytearray)) or not header:
        return None

    return filetype.guess(header)


def allowed_audio_content(file_stream, filename, allowed_extensions=ALLOWED_AUDIO_EXTENSIONS):
    """Return True when stream content is supported audio matching ``filename``.

    This complements :func:`allowed_audio_file` by rejecting renamed files and
    content whose detected container contradicts the extension.
    """
    if isinstance(file_stream, str) and hasattr(filename, 'read'):
        file_stream, filename = filename, file_stream

    if not allowed_audio_file(filename, allowed_extensions):
        return False

    extension = filename.rsplit('.', 1)[-1].lower()
    expected_extensions = AUDIO_CONTENT_EXTENSIONS.get(extension)
    if not expected_extensions:
        return False

    detected = detect_audio_type(file_stream)
    return detected is not None and detected.extension in expected_extensions


# Descriptive aliases for callers that prefer the "validate" wording.
validate_audio_content = allowed_audio_content
detect_audio_content = detect_audio_type


def is_downloadable_model(path):
    """Return True when the weights file exists on disk."""
    return bool(path) and os.path.exists(path)
