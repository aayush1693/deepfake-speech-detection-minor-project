"""Tests for audio duration and signal-quality validation.

These tests are skipped when the audio stack (soundfile/librosa) is unavailable.
"""

import io

import pytest

import app as app_module
from validators import (
    AudioSignalError,
    AudioSignalResult,
    validate_audio_signal,
)

try:
    import librosa  # noqa: F401,E402
    import numpy as np  # noqa: E402
    import soundfile as sf  # noqa: E402
except ImportError:
    librosa = None
    np = None
    sf = None

pytestmark = pytest.mark.skipif(
    librosa is None or np is None or sf is None,
    reason='soundfile/librosa are required for signal validation tests',
)

SAMPLE_RATE = 16000
TONE_HZ = 440


def write_tone(path, duration=1.0, amplitude=0.5):
    """Write a mono sine WAV and return its path as a string."""
    times = np.linspace(0.0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    samples = amplitude * np.sin(2 * np.pi * TONE_HZ * times)
    sf.write(path, samples.astype(np.float32), SAMPLE_RATE)
    return str(path)


def write_silence(path, duration=1.0):
    """Write a mono silent WAV and return its path as a string."""
    samples = np.zeros(int(SAMPLE_RATE * duration), dtype=np.float32)
    sf.write(path, samples, SAMPLE_RATE)
    return str(path)


def test_valid_sine_is_accepted(tmp_path):
    path = write_tone(tmp_path / 'tone.wav')

    result = validate_audio_signal(path)

    assert isinstance(result, AudioSignalResult)
    assert result.duration == pytest.approx(1.0, abs=0.01)
    assert result.rms > 0.1


def test_silent_audio_is_rejected(tmp_path):
    path = write_silence(tmp_path / 'silent.wav')

    with pytest.raises(AudioSignalError) as exc:
        validate_audio_signal(path)

    assert isinstance(exc.value, ValueError)
    assert exc.value.code == 'AUDIO_SILENT'


def test_near_silent_audio_is_rejected(tmp_path):
    path = write_tone(tmp_path / 'quiet.wav', amplitude=1e-5)

    with pytest.raises(AudioSignalError) as exc:
        validate_audio_signal(path)

    assert exc.value.code == 'AUDIO_SILENT'


def test_non_finite_samples_are_rejected(monkeypatch):
    samples = np.full(SAMPLE_RATE, np.nan, dtype=np.float32)
    monkeypatch.setattr(librosa, 'load', lambda *args, **kwargs: (samples, SAMPLE_RATE))

    with pytest.raises(AudioSignalError) as exc:
        validate_audio_signal('non-finite.wav')

    assert exc.value.code == 'AUDIO_SILENT'


def test_short_audio_is_rejected(tmp_path):
    path = write_tone(tmp_path / 'short.wav', duration=0.1)

    with pytest.raises(AudioSignalError) as exc:
        validate_audio_signal(path)

    assert exc.value.code == 'AUDIO_TOO_SHORT'


def test_long_audio_is_rejected_with_custom_limit(tmp_path):
    path = write_tone(tmp_path / 'long.wav', duration=2.0)

    with pytest.raises(AudioSignalError) as exc:
        validate_audio_signal(path, max_seconds=1.0)

    assert exc.value.code == 'AUDIO_TOO_LONG'


def test_environment_defaults_are_used(tmp_path, monkeypatch):
    path = write_tone(tmp_path / 'tone.wav', duration=1.0)
    monkeypatch.setenv('MIN_AUDIO_SECONDS', '2.0')

    with pytest.raises(AudioSignalError) as exc:
        validate_audio_signal(path)

    assert exc.value.code == 'AUDIO_TOO_SHORT'


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(
        app_module,
        'predict_audio',
        lambda path: ('Real', 0.91, 'uploads/spectrogram.png'),
    )
    application = app_module.create_app({
        'TESTING': True,
        'UPLOAD_FOLDER': str(tmp_path),
    })
    return application.test_client()


def post_file(client, path, filename):
    with open(path, 'rb') as audio_file:
        return client.post(
            '/api/predict',
            data={'file': (io.BytesIO(audio_file.read()), filename)},
        )


def test_predict_rejects_silent_audio(client, tmp_path):
    path = write_silence(tmp_path / 'silent.wav')

    response = post_file(client, path, 'silent.wav')

    assert response.status_code == 422
    assert response.get_json()['code'] == 'AUDIO_SILENT'


def test_predict_rejects_short_audio(client, tmp_path):
    path = write_tone(tmp_path / 'short.wav', duration=0.1)

    response = post_file(client, path, 'short.wav')

    assert response.status_code == 422
    assert response.get_json()['code'] == 'AUDIO_TOO_SHORT'


def test_predict_accepts_tone_after_signal_check(client, tmp_path):
    path = write_tone(tmp_path / 'tone.wav')

    response = post_file(client, path, 'tone.wav')

    assert response.status_code == 200
    assert response.get_json()['classification'] == 'Real'
