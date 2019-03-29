#! /usr/bin/env python
# Naive Online Voice Assistant - NOVA

import sys
sys.path.append('../modules')
sys.path.append('../extensions')

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

config = configparser.ConfigParser()
config.read('config.ini')

if not config.has_section('Nova'):
        config['Nova'] = {'wit_api_key': 'ADD_API_KEY_HERE'}
        config.write(open('config.ini', 'a'))

wit_api_key = config['Nova']['wit_api_key']

witClient = Wit(wit_api_key)

bm = BulbManager()

interrupted = False
playing = False

extensions = ['spotify', 'weather']
loaded_extensions = []
extension_objects = []


for i in extensions:
    temp_ext_object = __import__(str(i)).Extension()
    if temp_ext_object.extName == 'Spotify':
        sp = temp_ext_object
    extension_objects.append(temp_ext_object)

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
        if type(i.intent) is list:
            for intent in i.intent:
                if witResponse['entities']['intent'][0]['value'] == intent:
                    i.parse(witResponse, intent)
        else:
            if witResponse['entities']['intent'][0]['value'] == i.intent:
                    i.parse(witResponse, i.intent)

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
