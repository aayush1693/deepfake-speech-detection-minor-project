"""Shape checks for the MFCC preprocessing pipeline.

Skipped automatically when the audio stack (librosa/numpy) is unavailable.
"""

import numpy as np
import pytest

pytest.importorskip('librosa', reason='librosa is required for audio preprocessing tests')

import soundfile as sf  # noqa: E402

from preprocessing import INPUT_SIZE, SAMPLE_RATE, preprocess_input_audio  # noqa: E402


@pytest.fixture()
def tone_file(tmp_path):
    """1 second of a 440 Hz sine wave, written as 16-bit mono WAV."""
    t = np.linspace(0, 1.0, SAMPLE_RATE, endpoint=False)
    audio = 0.5 * np.sin(2 * np.pi * 440 * t).astype(np.float32)
    path = tmp_path / 'tone.wav'
    sf.write(path, audio, SAMPLE_RATE)
    return str(path)


def test_preprocess_returns_batched_rgb_tensor(tone_file):
    batch = preprocess_input_audio(tone_file)

    assert batch.shape == (1, INPUT_SIZE[0], INPUT_SIZE[1], 3)
    assert batch.dtype == np.float32 or batch.dtype == np.float64


def test_preprocess_is_deterministic(tone_file):
    first = preprocess_input_audio(tone_file)
    second = preprocess_input_audio(tone_file)

    np.testing.assert_allclose(first, second)
