#! /usr/bin/env python
# Naive Online Voice Assistant - NOVA

import sys
sys.path.append('modules')
sys.path.append('extensions')

from wit import Wit

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

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

if not config.has_section('Nova'):
        config['Nova'] = {'wit_api_key': 'ADD_API_KEY_HERE'}
        config.write(open('config.ini', 'a'))

wit_api_key = config['Nova']['wit_api_key']

witClient = Wit(wit_api_key)

bm = BulbManager()
sp = spw.SpotifyWrapper()

interrupted = False
playing = False

extensions = ['spotify', 'weather']
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
    
    witResponse = witClient.message(voiceInput)

    if 'good morning' == voiceInput:
        say('Good morning, Jian.')
    
    for i in extension_objects:
        if type(i.extIntent) is list:
            for intent in i.extIntent:
                if witResponse['entities']['intent'][0]['value'] == intent:
                    i.parse(witResponse, intent)
        else:
            if witResponse['entities']['intent'][0]['value'] == i.extIntent:
                    i.parse(witResponse, i.extIntent)

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
