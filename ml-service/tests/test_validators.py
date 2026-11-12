"""Tests for the audio upload validators (no ML dependencies required)."""

import pytest

from validators import ALLOWED_AUDIO_EXTENSIONS, allowed_audio_file, is_downloadable_model


@pytest.mark.parametrize(
    'filename',
    ['clip.wav', 'CLIP.WAV', 'song.mp3', 'voice.flac', 'note.ogg', 'record.m4a', 'meeting.webm'],
)
def test_allowed_audio_file_accepts_supported_formats(filename):
    assert allowed_audio_file(filename) is True


@pytest.mark.parametrize(
    'filename',
    ['clip.txt', 'video.mp4', 'song', '', 'clip.wav.exe', 'archive.zip'],
)
def test_allowed_audio_file_rejects_other_files(filename):
    assert allowed_audio_file(filename) is False


def test_allowed_extensions_are_normalised():
    assert allowed_audio_file('clip.WAV', {'.WAV'}) is True


def test_model_presence_check(tmp_path):
    weights = tmp_path / 'model.h5'
    assert is_downloadable_model(str(weights)) is False
    weights.write_bytes(b'not-a-real-model')
    assert is_downloadable_model(str(weights)) is True
    assert is_downloadable_model('') is False


def test_extension_set_is_not_empty():
    assert len(ALLOWED_AUDIO_EXTENSIONS) >= 3
