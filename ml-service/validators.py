"""Request validators for the ML service.

Content and filename checks stay dependency-free. Audio signal checks import
librosa lazily so validator-only tests do not need the audio stack.
"""

import os
from collections import namedtuple

import filetype

ALLOWED_AUDIO_EXTENSIONS = frozenset({'wav', 'mp3', 'flac', 'ogg', 'm4a', 'webm'})

DEFAULT_MIN_AUDIO_SECONDS = 0.5
DEFAULT_MAX_AUDIO_SECONDS = 30.0
DEFAULT_MIN_RMS = 1e-4
TARGET_SAMPLE_RATE = 16000

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


AudioSignalResult = namedtuple('AudioSignalResult', ['duration', 'rms'])


class AudioSignalError(ValueError):
    """ValueError carrying a stable code for a signal-quality failure."""

    def __init__(self, code, message):
        super().__init__(code)
        self.code = code
        self.reason = code
        self.message = message
        self.detail = message


def _limit(value, env_name, default):
    if value is not None:
        return float(value)
    return float(os.getenv(env_name, default))


def validate_audio_signal(
    path,
    min_seconds=None,
    max_seconds=None,
    min_rms=None,
):
    """Check duration, finite samples and loudness for an audio file.

    Audio is loaded as mono at 16 kHz. Raises :class:`AudioSignalError`, a
    ``ValueError`` subclass, with ``AUDIO_TOO_SHORT``, ``AUDIO_TOO_LONG`` or
    ``AUDIO_SILENT`` as its code. Returns an :class:`AudioSignalResult` for a
    valid clip.
    """
    # Imported lazily so importing this module never requires the audio stack.
    import librosa
    import numpy as np

    minimum = _limit(min_seconds, 'MIN_AUDIO_SECONDS', DEFAULT_MIN_AUDIO_SECONDS)
    maximum = _limit(max_seconds, 'MAX_AUDIO_SECONDS', DEFAULT_MAX_AUDIO_SECONDS)
    rms_floor = _limit(min_rms, 'MIN_RMS', DEFAULT_MIN_RMS)

    samples, sample_rate = librosa.load(path, sr=TARGET_SAMPLE_RATE, mono=True)
    samples = np.asarray(samples, dtype=np.float32)

    if not np.all(np.isfinite(samples)):
        raise AudioSignalError('AUDIO_SILENT', 'Audio contains non-finite samples')

    duration = float(samples.size) / float(sample_rate)
    if duration < minimum:
        raise AudioSignalError(
            'AUDIO_TOO_SHORT',
            f'Audio is too short: minimum duration is {minimum:g} seconds',
        )
    if duration > maximum:
        raise AudioSignalError(
            'AUDIO_TOO_LONG',
            f'Audio is too long: maximum duration is {maximum:g} seconds',
        )

    rms = float(np.sqrt(np.mean(np.square(samples)))) if samples.size else 0.0
    if rms < rms_floor:
        raise AudioSignalError(
            'AUDIO_SILENT',
            f'Audio is silent: RMS {rms:.3g} is below the minimum {rms_floor:g}',
        )

    return AudioSignalResult(duration=duration, rms=rms)


def is_downloadable_model(path):
    """Return True when the weights file exists on disk."""
    return bool(path) and os.path.exists(path)
