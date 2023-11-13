import scipy.io.wavfile

import pyaudio
from datetime import datetime as dt
import sys
import wave
import numpy as np
FILENAME = f"./logging/{sys.argv[1]}_n_back_output.wav"
def update_wav(audio):
    result = []
    '''
    for index in range(0, len(audio), 2):
        value = int.from_bytes(audio[index:index+2], 'big')
        result.append(value)'''
    #print("hi")
    result = np.frombuffer(audio,dtype=np.int16)
    #print(result)
    #print(np.asarray(result, dtype=np.int16))
    #numpy_data = numpy.array(audio, dtype=float)
    scipy.io.wavfile.write(FILENAME, 44100, result)#np.asarray(result, dtype=np.int16))

def testFkt():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 1
    

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    # for i in range(0, int(fs / chunk * seconds)):
    #     data = stream.read(chunk)
    #     frames.append(data)
    #wf = wave.open(filename, 'wb')
    #wf.close()
    while True:
        try:
            data = stream.read(chunk)
            frames.append(data)
            for i in range(0, int(fs / chunk * seconds)):
                data = stream.read(chunk)
                frames.append(data)
            update_wav(b"".join(frames))
           # rf = wave.open(filename, 'rb')
           # dat = rf.readframes(1000000000000000)
           # rf.close()
           # wf = wave.open(filename, 'wb')
           # wf.setnchannels(channels)
           # wf.setsampwidth(p.get_sample_size(sample_format))
           # wf.setframerate(fs)
           # wf.writeframes(b''.join([dat,data]))
           # wf.close()
        except Exception as e:
            print("kjdhsgfkjhdfskgjh")
            # Stop and close the stream 
            stream.stop_stream()
            stream.close()
            # Terminate the PortAudio interface
            p.terminate()
            print(e)

            break

if __name__ == '__main__':
    testFkt()