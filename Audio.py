from pytube import YouTube
import os
import time
import pandas as pd
from scipy.io.wavfile import read
import numpy as np


def get_audio_from_link(link: str, rickroll: bool):

    # Initialize the pytube interface and fetch the audio
    print('Connecting to Youtube server...')
    stream = YouTube(link).streams.get_audio_only()
    print('Connected!')

    # Download the audio and convert from mp4 to wav using ffmpeg
    audioName = '"' + stream.default_filename + '"'
    stream.download()
    print('Downloading...')
    time.sleep(1)
    cmd = f'ffmpeg -i {audioName} "{audioName[1:len(audioName) - 4]}wav"'
    os.system(cmd)

    # Remove the unneeded mp4 file
    os.remove(audioName[1:len(audioName) - 1])

    fileName = f'{audioName[1:len(audioName) - 4]}wav'
    soundFile = read(fileName)
    soundWaves = soundFile[1]
    amplitudes = list()
    frequencies = list()

    time.sleep(1)
    for soundWave in soundWaves:
        amplitudes.append(soundWave[0])
        frequencies.append(soundWave[1])

    val = 0
    if (rickroll):
        val = 1
    os.remove(fileName)
    return (amplitudes,frequencies, val)