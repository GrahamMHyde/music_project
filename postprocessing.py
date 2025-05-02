import numpy as np
from scipy.signal import butter, sosfilt
import soundfile as sf
import librosa
import matplotlib.pyplot as plt 
import noisereduce as nr
from pedalboard import Pedalboard, HighpassFilter, LowpassFilter, Compressor, Gain, Reverb
import os
import toml
import spectrogram_plotter 

# Load configuration file 
config = toml.load("config.toml")

# Set filepaths
input_path = config["paths"]["postprocess_input_file"]
output_path = config["paths"]["postprocess_output_file"]

# Flags
apply_test_tone = False
apply_noise_reduce = False
apply_low_pass = False
apply_spec_window = False

# ================= APPLY POST-PROCESSING TECHNIQUES ==========================

# Test tone for clearest tuning effects 
def generate_sine_wave(frequency=440.0, duration=2.0, rate=44100):
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    return tone.astype(np.float32), rate

def load_audio(filepath, sr=44100):
    data, rate = librosa.load(filepath, sr=sr)
    # data = data.astype(np.float32)
    print(f'Input data length: {len(data)}, dtype: {data.dtype}')
    return data, rate

def apply_noise_reduction(data, rate, prop_decrease=0.3):
    noise_clip = data[0:int(0.5 * rate)]  # first 0.5s as noise
    return nr.reduce_noise(y=data, sr=rate, y_noise=noise_clip, prop_decrease=prop_decrease, stationary=True)

def apply_eq_compression_reverb(data, rate, apply_low_pass):
    print(f"Data shape before effects: {data.shape}, dtype: {data.dtype}")

    # Lowpass butter filter (sos = second order sections, Wn = cutoff frequency [Hz])
    if apply_low_pass: 
        print('Applying lowpass butter filter...')
        lowpass_sos = butter(N=8, Wn=600, btype='low', fs=rate, output='sos')
        if data.ndim == 2:
            filtered = np.stack([sosfilt(lowpass_sos, data[:,ch]) for ch in range(data.shape[1])], axis=-1)
        else: 
            filtered = sosfilt(lowpass_sos, data)   # filter data using second-order sections
    else: 
        # Skip low_pass filter, rename data
        filtered = data

    # Tweak the degree of gain, compression, and reverb along with high/lowpass filters
    # Warning: Filter effects are gentle and not strict - use butter filter for stricter filtering
    board = Pedalboard([
        HighpassFilter(cutoff_frequency_hz=5),   # Remove mud
        # LowpassFilter(cutoff_frequency_hz=800), # Remove harshness
        Gain(gain_db=1.0),                        # Slight boost
        Compressor(threshold_db=-10, ratio=6.0, attack_ms=5, release_ms=20),
        Reverb(room_size=0.05, damping=0.7, wet_level=0.03),  # Subtle space
    ])

    processed = board(filtered, rate)
    print(f"Shape after pedalboard: {processed.shape}")
    return processed

# ================ SAVE PROCESSED AUDIO FILE / MAIN FUNCTION =================

def save_audio(filepath, processed, rate):
    dirnam = os.path.dirname(filepath)
    os.makedirs(dirnam, exist_ok=True)
    print(f"Processed data shape: {processed.shape}, dtype: {processed.dtype}, max amplitude: {np.max(np.abs(processed)):.2f}")
    sf.write(filepath, processed, rate)

def main(input_path, output_path, apply_test_tone, apply_noise, apply_low_pass, apply_spec_window):
    # Generate test tone for emphasized post-processing effects
    # Good for evaluating effects on pedalboard
    if apply_test_tone:
        print('Generating test tone...')
        data, rate = generate_sine_wave(frequency=440, duration=2.0)
    else: 
        # Load audio file
        print("Loading audio...")
        data, rate = load_audio(input_path)

    # Apply noise reduction
    if apply_noise_reduce:
        print("Applying noise reduction...")
        data = apply_noise_reduction(data, rate)
    else: 
        print('Skipping noise reduction...')

    # Apply EQ and compressionn (Pedalboard)
    print("Applying EQ, compression, de-essing, and reverb...")
    processed = apply_eq_compression_reverb(data, rate, apply_low_pass)

    # Generate and plot spectrogram
    print('Plotting spectrogram...')
    S_dB = spectrogram_plotter.spectrogram(processed, rate)

    # Generate specific spectrogram window
    if apply_spec_window: 
        print('Generating time window spectrogram...')
        start_time = 13
        end_time = 20
        spectrogram_plotter.plot_spectrogram_window(S_dB, sr=rate, hop_length=128, start_time=start_time, end_time=end_time)

    # Save post-processed audio file
    print(f"Saving to {output_path}")
    save_audio(output_path, processed, rate)
    print("Done!")


if __name__ == "__main__":
    main(input_path, output_path, apply_test_tone, apply_noise_reduce, 
         apply_low_pass, apply_spec_window)
