import gradio as gr
import teonsorflw as tf
import numpy as np
import librosa
import matplotlib.pyplot as plt
import librosa.display
from tensorflow.keras.models import load_model



# Load the trained model
model = load_model('deepfake_audio_detection_model.h5')

# Function to preprocess input audio
def preprocess_input_audio(audio_path):
    audio, sr = librosa.load(audio_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    mfcc_resized = np.resize(mfcc, (128, 128))
    mfcc_3d = np.stack((mfcc_resized,)*3, axis=-1)
    return np.array([mfcc_3d])

# Function to generate spectrogram
def generate_spectrogram(audio_path):
    audio, sr = librosa.load(audio_path, sr=16000)
    plt.figure(figsize=(10, 4))
    D = librosa.amplitude_to_db(np.abs(librosa.stft(audio)), ref=np.max)
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.savefig('spectrogram.png')
    plt.close()
    return 'spectrogram.png'

# Function to make prediction
def predict_audio(audio_path):
    processed_audio = preprocess_input_audio(audio_path)
    prediction = model.predict(processed_audio)
    prediction_score = prediction[0][0]
    classification = 'Real' if prediction_score > 0.5 else 'Fake'
    spectrogram_path = generate_spectrogram(audio_path)
    return classification, prediction_score, spectrogram_path

# Main function to test the model in Colab
def main():
    # Test with a sample audio file
    sample_audio_path = '/content/recording13014.wav_norm_mono.wav'
    classification, prediction_score, spectrogram_path = predict_audio(sample_audio_path)
    print(f"Classification: {classification}")
    print(f"Prediction Score: {prediction_score}")
    ipd.display(ipd.Audio(sample_audio_path)) # Use ipd.display to play audio
    img = plt.imread(spectrogram_path)
    plt.imshow(img)
    plt.axis('off')
    plt.show()

# Run the main function
main()