import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import toml 

config = toml.load("config.toml")
stem1_path = config["paths"]["stem1"]
stem2_path = config["paths"]["stem2"]

def find_spectral_overlap(stem1_path, stem2_path, threshold):
    # Load audio files
    stem1, sr = librosa.load(stem1_path, sr=44100)
    stem2, sr = librosa.load(stem2_path, sr=44100) 

    # Compute STFTs
    S1 = np.abs(librosa.stft(stem1, n_fft=2048, hop_length=512))
    S2 = np.abs(librosa.stft(stem2, n_fft=2048, hop_length=512))

    # Normalize both spectrograms to 0–1
    S1 /= np.max(S1)
    S2 /= np.max(S2)

    # Multiply to find overlap — high when both are strong
    overlap = S1 * S2
    print(overlap)

    # Optional: mask regions with strong overlap
    mask = overlap > threshold

    # Visualization of spectral overlap across select time window
    hop_length = 512
    start_time = 0   
    end_time = 20
    t_start = int((start_time* sr) / hop_length)
    t_end = int((end_time * sr) / 512)
    overlap_window = overlap[:, t_start:t_end]
    plt.figure(figsize=(12, 6))
    librosa.display.specshow(overlap_window, sr=sr, hop_length=512, y_axis='log', x_axis='time', cmap='plasma')
    plt.title(f'Spectral Overlap From {start_time}s to {end_time}s')
    plt.colorbar(format='%0.2f')
    plt.savefig('over_lapping_normalized_spectrogram_window.png')
    plt.show()

    # Visualization of spectral overlap across full song duration 
    plt.figure(figsize=(12, 6))
    librosa.display.specshow(overlap, sr=sr, hop_length=512, y_axis='log', x_axis='time', cmap='plasma')
    plt.title('Spectral Overlap Between Drum & Guitar Stems')
    plt.colorbar(format='%0.2f')
    plt.savefig('overlapping_normalized_spectrogram_full.png')
    plt.show()

if __name__ == '__main__': 
    find_spectral_overlap(stem1_path, stem2_path, 0.5)
