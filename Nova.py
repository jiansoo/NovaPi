#! /usr/bin/env python
# Naive Online Voice Assistant - NOVA

import sys
sys.path.append('modules')
sys.path.append('extensions')

from utils import *

import sharedvalues as sv
import snowboydecoder

import signal
import importlib
import spotipywrapper as spw
import os
from bulbmanager import BulbManager
from weather import returnForecast
import datetime

bm = BulbManager()
sp = spw.SpotifyWrapper()

interrupted = False
playing = False

extensions = ['spotify']
loaded_extensions = []
extension_objects = []

for i in extensions:
    extension_objects.append(__import__(str(i)).Extension())

print(extension_objects)

def signal_handler(*args):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def ascertain_command():
    try:
        sp.stopPlayback()
    except:
        sv.playing = False
    voiceInput = 'Play music'
    if voiceInput == None:
        print('No speech detected.')
        if sv.playing:
            sp.startPlayback()
        return
    
    voiceInput = voiceInput.lower()
    
    for i in extension_objects:
        print(find_and_split(voiceInput,i.operative))
        if find_and_split(voiceInput,i.operative) is not None:
            i.parse(find_and_split(voiceInput,i.operative))

    elif 'good morning' == voiceInput:
        say('Good morning, Jian.')
        
    if sv.playing:
        sp.startPlayback()

bm.normalLight()

detector = snowboydecoder.HotwordDetector('NovaWebcam.pmdl', sensitivity=0.8)
print('Listening for hotword.')
detector.start(detected_callback=ascertain_command,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()

ascertain_command()
