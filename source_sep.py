import os
from spleeter.separator import Separator
import toml

# Load configuration file 
config = toml.load("config.toml")

# Set input audio folder filepath
input_folder = config["paths"]["preprocess_s2_folder"]

# Create output directory to store separated audio files
output_folder = config["paths"]["stem_separated_output_folder"]
os.makedirs(output_folder, exist_ok=True)

def separate_audio(input_files_folder, output_folder): 
    # Initialze the separator model (2, 4, or 5 stems)
    separator = Separator('spleeter:4stems')

    # These are the supported file audio formats
    supported_formats = {'.WAV', '.MP3', '.FLAC', '.OGG', '.M4A'}

    # Iterate through all the files in the input files folder
    for file in os.listdir(input_files_folder):   # os.listdir() returns a list of all entries in a given directory
        file_path = os.path.join(input_files_folder, file)

        # Check if folder entry is a file (not folder) and if it has the proper file extension
        if os.path.isfile(file_path) and any(file.upper().endswith(extension) for extension in supported_formats):
            try: 
                # Stem separation of each file if it is a proper audio file
                print(f'Processing: {file}')
                separator.separate_to_file(file_path, output_folder)   # store output files in specified output folder
                print(f'Stem separation completed successfully for: {file}')
                
            except Exception as e: 
                print(f'Error while processing {file}: {e}')   # throws error which Python will generate if there is one (that I didn't plan for)
        else:
            print(f'Skipping non-audio file: {file}')   # skips any non-audio file
    
    # Print statement when all files have been separated
    print('All files have been processed and separated!')
    


if __name__ == '__main__':
    separate_audio(input_folder, output_folder)