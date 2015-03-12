# -*- coding: utf-8 -*-

import pygame as pg
import numpy as np
from math import *
import pyaudio

#FUNCTIONS USED ELSEWHERE TO DEAL WITH SOUND

pg.mixer.init(44100)


def make_sound(duration=2.,freq=440.,pan=(1.,1.),attack=.1,decay=.5):
    #Create a pure tone at a given frequency
    mixer_freq=44100
    pan=np.array(pan) #left-right balance

    steps=int(duration*mixer_freq)
    snd_puls=2*pi*freq
    amp=5000

    def vamp(i):
        #modulated amplitude for attack and decay
        t=(i+.5)/mixer_freq
        return amp/(1.+ (attack/t)**2 + (decay/(duration-t))**2 )

    snd_array=np.array([pan*vamp(i)*cos(i*snd_puls/mixer_freq) for i in range(steps)])
    snd=pg.sndarray.make_sound(snd_array.astype("int16"))
    return snd


def record(duration = 5.):
    #Record stereo sound, blocking all processes
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100


    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    #print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    #print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()
    return frames,CHANNELS,p.get_sample_size(FORMAT),RATE

def save(duration,filename="output.wav"):
    #Record sound from microphone and save it to a file
    import wave
    frames,CHANNELS,SAMPLEWIDTH,RATE=record(duration)
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(SAMPLEWIDTH)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def decode(in_data, channels):
    #No credit here, found on StackOverflow
    """
    Convert a byte stream into a 2D numpy array with
    shape (chunk_size, channels)

    Samples are interleaved, so for a stereo stream with left channel
    of [L0, L1, L2, ...] and right channel of [R0, R1, R2, ...], the output
    is ordered as [L0, R0, L1, R1, ...]
    """
    # TODO: handle data type as parameter, convert between pyaudio/numpy types
    result = np.fromstring(in_data, dtype=np.int16)

    chunk_length = len(result) / channels
    assert chunk_length == int(chunk_length)

    result = np.reshape(result, (chunk_length, channels))
    return result


def encode(signal):
    #No credit here, found on StackOverflow
    """
    Convert a 2D numpy array into a byte stream for PyAudio

    Signal should be a numpy array with shape (chunk_size, channels)
    """
    interleaved = signal.flatten()

    # TODO: handle data type as parameter, convert between pyaudio/numpy types
    out_data = interleaved.astype(np.int16).tostring()
    return out_data

def record_array(duration):
    #Record from microphone then output a Numpy array
    frames,channels,samplewidth,rate=record(duration)
    return decode(''.join(frames),channels )


def spectrogram(fig,samples, binsize=2**12, colormap="jet"):
    # Plot spectrogram into fig, from array samples

    from scipy.fftpack import rfft
    spec=[]
    for i in range(len(samples)/binsize ):
        spec.append(rfft((samples[i*binsize:(i+1)*binsize]))[:600] )
    spec=np.array(spec,dtype='float')
    spec = 20.*np.log10(np.abs(spec)/10e-6)

    ax = fig.gca()
    #ax.set_yscale('log')
    ax.imshow(spec.T, origin="lower", aspect="auto", cmap=colormap, interpolation="none")

    return
