#! /usr/bin/env python
# Naive Online Voice Assistant - NOVA

import sys

# Add /modules and /extensions as path variables
sys.path.append('../modules')
sys.path.append('../extensions')

# Import block
from wit import Wit
from utils import *
import sharedvalues as sv
import snowboydecoder
import signal
import importlib
import os
from bulbmanager import BulbManager
from weather import returnForecast
import datetime
import configparser

# Check for Nova entry in the config file. 
# If none exists, makes one with the placeholder values.
config = configparser.ConfigParser()
config.read('config.ini')

if not config.has_section('Nova'):
        config['Nova'] = {'wit_api_key': 'ADD_API_KEY_HERE'}
        config.write(open('config.ini', 'a'))

# Setup Wit.ai client.
wit_api_key = config['Nova']['wit_api_key']
witClient = Wit(wit_api_key)

# Todo - possibly make BulbManager into an extension? Maybe have it as an extension and a module as well.
bm = BulbManager()

# If set to true, Snowboy hotword detector stops.
interrupted = False

# Add extension Python file names here to load them.
extensions = ['spotify', 'weather']
loaded_extensions = []
extension_objects = []

# Loads extensions into extension_objects array. 
# Loads Spotify extension into variable sp.
for i in extensions:
    ext_object = __import__(str(i)).Extension()
    if ext_object.extName == 'Spotify':
        sp = ext_object
    extension_objects.append(ext_object)

# Sets interrupted to True when interrupt is detected.
def signal_handler(*args):
    global interrupted
    interrupted = True

# Getter function for interrupted variable.
def interrupt_callback():
    global interrupted
    return interrupted

# Main function invoked by hotword detection.
def ascertain_command():
    # Tries to stop playback of music. 
    # If error is returned, no active device (nothing is playing).
    # As such, playing is set to false.
    try:
        sp.stopPlayback()
    except:
        sv.playing = False
    
    # Ask Google-san to transcribe voice input to text format.
    voiceInput = start_speech_transcription()

    # If the voiceInput is None, presume false alarm.
    # Should be a better way to handle this...
    if voiceInput == None:
        print('No speech detected.')
        if sv.playing:
            sp.startPlayback()
        return
    
    # Sends transcribed voice input off to my Wit.ai model.
    witResponse = witClient.message(voiceInput)

    # Iterates through extension objects, and checks if any intents match the one returned by Wit.
    for i in extension_objects:
        if type(i.intent) is list:
            for intent in i.intent:
                if witResponse['entities']['intent'][0]['value'] == intent:
                    # If the intent matches, the parse command is invoked with the witResponse object and the detected intent.
                    # Waaaay better than my if-tree method.
                    i.parse(witResponse, intent)
        else:
            if witResponse['entities']['intent'][0]['value'] == i.intent:
                    i.parse(witResponse, i.intent)

    # If the music was playing beforehand, try to start playback up again.
    # ... and if it fails, Playing is set to false.
    try:
        sp.startPlayback()
    except:
        sv.playing = False

bm.normalLight()

# If it detects a Ctrl+C, makes interrupted = True.
signal.signal(signal.SIGINT, signal_handler)

# Setting up hotword detection with PMDL file.
# Change sensitivity at your own leisure - and make a PMDL file for your device for the best results.
detector = snowboydecoder.HotwordDetector('NovaWebcam.pmdl', sensitivity=0.8)

print('Started listening for hotword.')

# Starting detector.
detector.start(detected_callback=ascertain_command,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

# Gracefully kills detector if Ctrl+C is detected.
detector.terminate()

