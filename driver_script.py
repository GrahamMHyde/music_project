# Use this script to separate songs you want to separate; store them all in one folder. 
# Place songs in the "audio folder" designated in the config file and this driver script
# will modules to preprocess and separate stems.

import pre_processing
import source_sep
import memory_stats
import toml
import os
import time

# Start timer to track runtime performance
start_time = time.perf_counter()

# Function to create new output folders so you don't have to delete previous runs
def generate_new_folder(current_folder, subfolder=""): 
    index = 1
    while True: 
        if subfolder:   # needed for stage 2 of preprocessing script
            new_folder = os.path.join(current_folder, f'{subfolder}_run{index}')
        else: 
            new_folder = f'{current_folder}_run{index}'

        if not os.path.exists(new_folder):   # if current created folder exists (run1 already stored), increase index
            os.makedirs(new_folder)   # if runX isn't in file directory, create new output folder
            return new_folder
        index += 1

def main(config_path):
    # Load configuration files
    config = toml.load('config.toml')

    # Input and output folders for preprocessing 
    input_folder_PP = config["paths"]["audio_folder"]
    s1_output_folder = generate_new_folder(config["paths"]["preprocess_s1_folder"])
    s2_output_folder = generate_new_folder(s1_output_folder, "resampled_output")

    # Grab system utilization data - monitor processes, resources
    memory_stats.log_memory_stats(filename="start_sys_data.txt")

    # Preprocess song
    pre_processing.preprocess_audio(input_folder_PP, s1_output_folder, s2_output_folder) 

    # Output folder for separator model
    output_folder_sep = generate_new_folder(config["paths"]["stem_separated_output_folder"])

    # Make directory for stem separator output 
    os.makedirs(output_folder_sep, exist_ok=True)

    # Separate stems
    model = 'spleeter:4stems'
    source_sep.separate_audio(s2_output_folder, output_folder_sep, model)

    # Display program runtime
    stop_time = time.perf_counter()
    runtime = stop_time - start_time 
    if runtime >= 60: 
        min = int(runtime // 60)
        sec = runtime % 60 
        print(f'Program runtime: {min} minutes {sec:1f} seconds')
    else: 
        print(f'Program runtime: {runtime:.4f} seconds')

if __name__ == '__main__':
    config_path = "config.toml"
    main(config_path)