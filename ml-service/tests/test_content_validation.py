"""Tests for content-based audio validation (no ML dependencies required)."""

import io
import wave

import pytest

import app as app_module
from validators import allowed_audio_content, detect_audio_type


def make_wav_bytes(sample_rate=8000, duration=0.05):
    """Return a small, valid mono 16-bit PCM WAV file as bytes."""
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b'\x00\x00' * int(sample_rate * duration))
    return buffer.getvalue()


@pytest.mark.parametrize(
    ('filename', 'payload'),
    [
        ('clip.wav', make_wav_bytes()),
        ('song.mp3', b'ID3\x04\x00\x00\x00\x00\x00\x00'),
        ('voice.flac', b'fLaC\x00\x00\x00\x22'),
        ('note.ogg', b'OggS\x00\x02\x00\x00'),
        ('record.m4a', b'\x00\x00\x00\x18ftypM4A\x00\x00\x00\x00'),
        ('meeting.webm', b'\x1aE\xdf\xa3\x00\x00\x00\x00\x42\x82\x84webm'),
    ],
)
def test_allowed_audio_content_accepts_supported_formats(filename, payload):
    assert allowed_audio_content(io.BytesIO(payload), filename) is True


@pytest.mark.parametrize(
    ('filename', 'payload'),
    [
        ('fake.wav', b'This is plain text, not an audio file.\n'),
        ('fake.mp3', b'\x00\x01\x02\x03unknown binary content'),
        ('clip.mp3', make_wav_bytes()),
        ('clip.webm', b'ID3\x04\x00\x00\x00\x00\x00\x00'),
        ('clip.txt', make_wav_bytes()),
    ],
)
def test_allowed_audio_content_rejects_unknown_or_mismatched_content(filename, payload):
    assert allowed_audio_content(io.BytesIO(payload), filename) is False


def test_detect_audio_type_reports_container_and_mime():
    detected = detect_audio_type(io.BytesIO(make_wav_bytes()))

    assert detected is not None
    assert detected.extension == 'wav'
    assert detected.mime in {'audio/wav', 'audio/x-wav'}


def test_detect_audio_type_returns_none_for_unknown_content():
    assert detect_audio_type(io.BytesIO(b'not audio')) is None
    assert detect_audio_type(io.BytesIO(b'')) is None


def test_stream_position_is_restored_after_inspection():
    stream = io.BytesIO(make_wav_bytes())
    stream.seek(5)

    assert allowed_audio_content(stream, 'clip.wav') is True
    assert stream.tell() == 5

    detected = detect_audio_type(stream)
    assert detected is not None
    assert stream.tell() == 5


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(
        app_module,
        'predict_audio',
        lambda path: ('Real', 0.91, 'uploads/spectrogram.png'),
    )
    # Signal validation is covered separately and needs the audio stack.
    monkeypatch.setattr(app_module, 'validate_audio_signal', lambda *args, **kwargs: None)
    application = app_module.create_app({
        'TESTING': True,
        'UPLOAD_FOLDER': str(tmp_path),
    })
    return application.test_client()


def test_predict_rejects_text_file_renamed_to_wav(client):
    response = client.post(
        '/api/predict',
        data={'file': (io.BytesIO(b'This is not audio.\n'), 'renamed.wav')},
    )

    assert response.status_code == 400
    assert response.get_json() == {
        'error': 'File content is not a supported audio format',
        'code': 'INVALID_AUDIO_CONTENT',
    }


def test_predict_accepts_valid_wav_content(client):
    response = client.post(
        '/api/predict',
        data={'file': (io.BytesIO(make_wav_bytes()), 'clip.wav')},
    )

    assert response.status_code == 200
    assert response.get_json()['classification'] == 'Real'
