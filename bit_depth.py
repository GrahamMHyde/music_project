import pre_processing
import os, subprocess 
import toml

# Load configuration file
config = toml.load("config.toml")

# Define folder paths
s1_input_folder = config["paths"]["audio_folder"]
s1_output_folder = config["paths"]["preprocess_s1_folder"]
s2_output_folder = config["paths"]["preprocess_s2_folder"]
s3_input_folder = s2_output_folder
s3_output_folder = config["paths"]["preprocess_s3_folder"]

# Create output folders
os.makedirs(s1_output_folder, exist_ok=True)
os.makedirs(s2_output_folder, exist_ok=True)
os.makedirs(s3_output_folder, exist_ok=True)  

# Stage 1: Convert to WAV
pre_processing.convert_to_wav(s1_input_folder, s1_output_folder)

# Stage 2: Resample audio
pre_processing.convert_audio(s1_output_folder, s2_output_folder)

def convert_bit_depth(input_folder, output_folder):
    bit_depth = 's24'
    # Iterate over input files and increase their bit depths
    for file in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file)
        output_file = os.path.join(output_folder, os.path.splitext(file)[0] + '_final.wav')

        # Skip over the output folder that's going to store these resampled files
        if not os.path.isfile(file_path):
            continue

        print(f"Processing file: {file_path}...")

        # Run bash command to increase input files' bit depths
        command = ["ffmpeg", "-i", file_path, '-acodec', f'pcm_{bit_depth}le', output_file]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Print the result of ffmpeg command to debug if anything went wrong
        if result.returncode != 0:
            print(f"Error during conversion of {file}: {result.stderr}")
        else:
            print(f"Successfully converted {file_path} to {output_file}")

# Run bit depth function
convert_bit_depth(s3_input_folder, s3_output_folder)