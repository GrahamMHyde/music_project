import librosa 
import numpy as np
import matplotlib.pyplot as plt 

def spectrogram(processed, rate):
    # Compute short time Fourier transform - computes DFT over short overlapping windows
    S = np.abs(librosa.stft(processed))

    # Compute RMS from the spectrogram
    rms = librosa.feature.rms(S=S)[0]  # Extract magnitude of frequency of short ([1] extracts phase information)

    # Time axis for RMS
    frames = range(len(rms))
    t_rms = librosa.frames_to_time(frames, sr=rate)

    # Plot spectrogram
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                            y_axis='log', x_axis='time', sr=rate)
    plt.title('Log-frequency Spectrogram (dB)')
    plt.colorbar(format='%+2.0f dB')

    # Plot RMS energy
    plt.subplot(2, 1, 2)
    plt.plot(t_rms, rms, color='r')
    plt.title('RMS Energy (Loudness Estimate)')
    plt.ylabel('RMS Amplitude of Digital Signal')
    plt.xlabel('Time (s)')
    plt.tight_layout()
    plt.show(block=False)
    plt.savefig('spectrogram_rms_plot.png')

    S_dB = librosa.amplitude_to_db(S, ref=np.max)
    return S_dB   # return spectrogram object in dB

def plot_spectrogram_window(S_dB, sr, hop_length, start_time, end_time):
    # Calculate the time array in seconds
    times = librosa.frames_to_time(np.arange(S_dB.shape[1]), sr=sr, hop_length=hop_length)
    
    # Find frame indices corresponding to the desired time window
    start_idx = np.searchsorted(times, start_time)
    end_idx = np.searchsorted(times, end_time)

    # Slice the spectrogram
    S_dB_window = S_dB[:, start_idx:end_idx]
    time_window = times[start_idx:end_idx]

    # Plot the zoomed spectrogram
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_dB_window, x_axis='time', y_axis='log', sr=sr,
                             hop_length=hop_length, cmap='magma', 
                             x_coords=time_window)
    plt.colorbar(format='%+2.0f dB')
    plt.title(f'Spectrogram Window: {start_time}s to {end_time}s')
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.tight_layout()
    plt.show(block=False)
    plt.savefig('spectrogram_window.png')