# DarkSky Extension v1 for Nova
# Author: Jian Soo
# Dependencies: ForecastIOPy

# Add /modules as a path variable
import sys
sys.path.append('../modules')

# Import modules
from forecastiopy import *
import sharedvalues as sv
import configparser
config = configparser.ConfigParser()
import os
from utils import say


class Extension:
    # Standard extension class variables
    
    # Name of extension - used to make config file field.
    extName = 'DarkSkyWeather'
    
    # Settings to store in config; use dictionary format.
    # Values can be referenced to as config[<extension name>][<key>].
    extSettings = {'api_key':'ADD_API_KEY_HERE'}
        
    extOperative = 'weather'
    
    # Config file heavy lifting:
    
    # Check if config file has the extension's section. If not, adds it in with default values defined above.
    config.read('config.ini')
    
    if not config.has_section(extName):
        config[extName] = extSettings
        config.write(open('config.ini', 'a'))
    
    # Beyond this point are extension-specific class variables:
    apiKey = config[extName]['api_key']

    # Extension methods
    def __init__(self):
        self.operative = Extension.extOperative
        
    def summary(location):
        fHandler = ForecastIO.ForecastIO(apiKey, location[0], location[1])
    # General 'parse' command: interprets voice input 
    def parse(self, command):
        if command[0] == 'like' and command[1] == 'in':
            summary(command[2:])
        # Play mus

Extension()