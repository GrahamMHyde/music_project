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