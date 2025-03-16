import librosa
import soundfile as sf
import subprocess
import os
import json

#  -----  STAGE 1: FILE TYPE CONVERSION TO .WAV  -----

# Any general input file is likely not a .wav file, which librosa requires for resampling.
# This function runs a bash command to extract the audio stream from any file and 
# create a .wav file with it.
def convert_to_wav(input_folder, output_folder):
    # Iterate through all files in the input files folder
    for file in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file)

        # Run this bash command to check if the audio file is already .wav type
        command_check = [
            "ffprobe", "-v", "error", "-select_streams", "a:0", 
            "-show_entries", "format=format_name", "-of", "json", file_path
            ]
        result = subprocess.run(command_check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        file_info = json.loads(result.stdout)
            
        # If the file format is .wav already, skip conversion
        if file_info.get("format", {}).get("format_name") == "wav":
            print(f"File {file_path} is already a WAV file. Skipping conversion.")
            continue   # Exit function and skip to next input file

        # Defining output file path for the command below, which extracts the 
        # audio stream from any file and converts it to .wav
        output_file = os.path.join(output_folder, os.path.splitext(file)[0] + '_s1.wav')
        """ 
        ffmpeg:   software designed to handle multi-media files; used for digital signal processing
        -vn:   disables video processing
        - acodec pcm_s16le:   specifies the audio coder/decoder shoudl be PCM with 16-bit signed little-endian encoding (WAV files)...
        - ar 44100:   sets sample rate to 44.1 kHz
        -ac 2:   ensures stereo output (2 channels)
        """
        command = [ 
            'ffmpeg', '-i', file_path, '-vn', '-acodec', 'pcm_s24le', '-ar', 
            '44100', '-ac', '2', output_file
        ]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


#  -----  STAGE 2: RESAMPLE CONVERTED AUDIO FILES  -----

# This function sets the sampling rate to 44.1 kHz for Spleeter's separator models
# and outputs the converted files
def convert_audio(input_folder, output_folder):   
    """
    librosa.load() takes an audio file and resamples it to the 
    specified sampling rate (target_sr). To preserve native sr set 
    sr = None; the default sr is 22050 Hz.

    The default sr for all audio files is generally 44100, but more
    importantly Spleeter only accepts this sr, so this is a check to
    ensure the expected sr is correct and eliminates backend resampling.
    """
    for file in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file)
        output_file = os.path.join(output_folder, os.path.splitext(file)[0] + '_s2.wav')

        # Skip over the output folder that's going to store these resampled files
        if not os.path.isfile(file_path):
            continue

        # Use librosa library to resample audio files to 44.1 kHz 
        try: 
            data, sr = sf.read(file_path, dtype='float32')  # Returns 1) audio time series array & 2) sampling rate of the array
            data_441k = librosa.resample(data, orig_sr=sr, target_sr=44100)
            sf.write(output_file, data_441k, 44100)

        except Exception as e: 
            print(f'Error in resampling stage: {e}')


# Main function
def main(): 
    # Define folder paths
    s1_input_folder = '/Users/grahamhyde/Downloads/folder/Music_Project/test_audio_files'
    s1_output_folder = '/Users/grahamhyde/Downloads/folder/Music_Project/preprocessing_output'
    s2_output_folder = '/Users/grahamhyde/Downloads/folder/Music_Project/preprocessing_output/resampled_output'

    # Create output folders
    os.makedirs(s1_output_folder, exist_ok=True)
    os.makedirs(s2_output_folder, exist_ok=True)

    # Stage 1: Convert to WAV
    convert_to_wav(s1_input_folder, s1_output_folder)

    # Stage 2: Resample audio
    convert_audio(s1_output_folder, s2_output_folder)


# This ensures the script runs when executed directly, but not when imported as a module
if __name__ == "__main__":
    main()
