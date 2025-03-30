# Start adding to this when progress is made
Cmd + Shift + v to preview this markdown document.

## Python script notes
### Python file versions
*source_sepV2.py* removes the lines of code that generate individual output files for each input file because *separator.separate_to_file* automatically does this - it was redundant.

## Python library notes
### Librosa
Librosa is a library for music and audio analysis, providing tools for loading audio files, feature extraction, TD and FD proessing, and visualization.  I use Librosa for setting the sampling rate of audio files to Spleeter's required 44.1 kHz.

### bit_depth.py
This script isn't actually able to convert bit depth. I could spend more time on this, but I think ffmpeg is structured in a way that doesn't let it convert bit depths with the way my pre-processing script is written. It could also be that the *pcm_s24le* acodec (audio coder/decoder) doesn't allow conversion the way I'm trying to do it. 

### RAM usage of pre-trained separator models
The solid-state drive (SSD), or hard disk drive (HHD), is the non-volatile memory that stores your computers information (e.g., files) when it is powered off. Bits, 0s and 1s, are individually stored in memory cells, which are small electronic circuits whose voltage levels indicate the type of bit being stored. A high voltage state would indicate a 1 bit for example. A processor is the mechanism that assigns the memory cells their individual states and it is the way in which the states are organized that constructs memory of specific signals/information.  

[*Specific to Graham*] Go to __Activity Monitor__ and then __Memory__. Run the driver script and watch Python use up to 6 GB RAM MEM. Spleeter models use a lot of memory and TensorFlow creates multiple background processes leading to memory leaks, which are events where memory is lost because the program fails to deallocate memory. When a program needs to store data, it requests memory from the OS and this memory is allocated to the program. Once the program is done using using that memory, it should release it back to the OS, which is the process of deallocation (or freeing memory). When the program fails to deallocate the memory given to it, memory leaks occur. 

When you run the Spleeter models, TensorFlow leads the called model into RAM. After processing a file, that model still remains in your RAM, which is massive, so further additions to RAM could quickly eat up most of your RAM. TensorFlow does not free its tensors adn models automatically. The biggest issue comes when you are *separating multiple files in sequence*. Spleeter processes each file and stores the chunks of intermediate tensors in memory without clearing memory. I noticed that the second audio file always struggles to process in terms of speed, and it's likely because a large part of availble RAM has been used and little memory is free for further computations. 

TensorFlow's [tf.keras.backend.clear_session()](https://www.tensorflow.org/api_docs/python/tf/keras/backend/clear_session) describes the need to call this when specifically creating multiple models in a loop. Keras manages a global state containing information about the model and its API, so creating many models in a loop will consume an increasing amount of memory over time. Calling clear_session() releases the global state and avoids clutter from old models and layers, freeing up memory. 

## Theorems
### Nyquist-Shannon sampling theorem
The Nyquist-Shannon samplinng theorem is a principle in digital signal processing that establishes the relationship between a signal's frequency range (bandwidth) and the sample rate required to avoid aliasing (a type of distortion where lower frequencies are artificially generated due to poor sampling). The theorem states that a signal's saVmpling rate must be at least twice the bandwidth of the signal.  
  
  __Nyquist-Shannon sampling theorem__ $$f_{SR} \geq 2f_{BW} $$  
  
Generally, audio tracks are sampled at 44.1 kHz. This is because humans' audible frequency range is generally 20 - 20,000 Hz. Using the Nyquist-Shannonn theorem,  
  
  $$ f_{SR} \geq 2f_{BW} = 2(20,000) = 40 kHz $$
    
Anti-aliasing filters require a frequency buffer above the Nyquist limit (40 kHz), and 44.1 kHz became the practical sampling rate for audio instruments in the industry.  

### Bit Depth
Bit depth in digital imaging refers to how many bits are used to represent the color of a single pixel. Thus, higher bit depths generally result in richer, more accurate images.  

In audio, bit depth refers to how many bits are used to represent a single audio sample. A sample is a single value representing the amplitude of an audio signal, so by increasing the sample's bit depth, you have more bits to quantify the amplitude, leading to higher resolution when describing the exact magnitude of the signal at the sample's moment in time.  

When you take an existing audio file and increase its bit depth, you're only adding zeros to the sample's bit-representation (also calledd bit padding). This doesn't improve sound quality, it only makes the file bigger. However, when you apply audio processing tools (e.g., use Spleeter) to the file, you may introduce rounding errors. By bit padding, you add in a buffer for precision and reduce the rounding error effects. 

### Pulse Code Modulation (PCM)
ADD THEORY TO THIS LATER...  
PCM is a standard method for converting analog audio signals to digital audio signals *without compression*, meaning PCM is a raw, uncompressed format. WAV files are PCM formatted, which is what Spleeter expects when separating an audio file.  

A common bit depth is 16-bit, which Spleeter might work best with, but I'm not sure. If the bit depth is incompatible with Spleeter's model, then the conversion process (if there is one) or inalignment might affect sound quality. That's a hypothesis. 