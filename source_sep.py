import os
from spleeter.separator import Separator
import gc
import tensorflow as tf
import subprocess 

def separate_audio(input_files_folder, output_folder): 
    # These are the supported file audio formats
    supported_formats = {'.WAV', '.MP3', '.FLAC', '.OGG', '.M4A'}

    # Iterate through all the files in the input files folder
    for file in os.listdir(input_files_folder):   # os.listdir() returns a list of all entries in a given directory
        file_path = os.path.join(input_files_folder, file)

        # Check if folder entry is a file (not folder) and if it has the proper file extension
        if os.path.isfile(file_path) and any(file.upper().endswith(extension) for extension in supported_formats):
            try: 
                print(f'Processing: {file}')

                # Initialze the separator model (2, 4, or 5 stems)
                separator = Separator('spleeter:4stems')

                # Perform source separation
                separator.separate_to_file(file_path, output_folder)   # store output files in specified output folder
                print(f'Stem separation completed successfully for: {file}')

                # Free memory after audio file is processed/separated
                del separator   # delete separator instance
                tf.keras.backend.clear_session()   # clear tensorflow session 
                gc.collect()   # collect garbage
                
            except Exception as e: 
                print(f'Error while processing {file}: {e}')   # throws error which Python will generate if there is one (that I didn't plan for)
        else:
            print(f'Skipping non-audio file: {file}')   # skips any non-audio file
    
    # Print statement when all files have been separated
    print('All files have been processed and separated!')