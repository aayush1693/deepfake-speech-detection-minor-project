"""Audio preprocessing shared by the API routes and the offline Colab flow."""

import os
import uuid

SAMPLE_RATE = 16000
N_MFCC = 13
INPUT_SIZE = (128, 128)


def preprocess_input_audio(audio_path):
    """Turn an audio file into the (1, 128, 128, 3) tensor the model expects."""
    # Imported lazily so the module can be imported without the audio stack.
    import librosa
    import numpy as np

    audio, sr = librosa.load(audio_path, sr=SAMPLE_RATE)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=N_MFCC)
    mfcc_resized = np.resize(mfcc, INPUT_SIZE)
    mfcc_3d = np.stack((mfcc_resized,) * 3, axis=-1)
    return np.array([mfcc_3d])


def generate_spectrogram(audio_path, output_dir='.'):
    """Render a log-frequency spectrogram and return the file path.

    A unique filename is used so concurrent requests cannot overwrite each
    other's image.
    """
    # Imported lazily so the module can be imported without the plotting stack.
    import librosa
    import librosa.display
    import matplotlib

    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    audio, sr = librosa.load(audio_path, sr=SAMPLE_RATE)
    figure = plt.figure(figsize=(10, 4))
    try:
        db = librosa.amplitude_to_db(np.abs(librosa.stft(audio)), ref=np.max)
        librosa.display.specshow(db, sr=sr, x_axis='time', y_axis='log')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Spectrogram')

        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'spectrogram_{uuid.uuid4().hex}.png')
        figure.savefig(output_path)
    finally:
        plt.close(figure)

    return output_path
