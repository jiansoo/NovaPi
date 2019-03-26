# Spotify Extension v1 for Nova
# Author: Jian Soo
# Dependencies: SpotiPy

# Add /modules as a path variable
import sys
sys.path.append('../modules')

# Import modules
import spotipy.util as util
import spotipy as spotipy
import sharedvalues as sv
import configparser
config = configparser.ConfigParser()
import os
from utils import say


class Extension:
    # Standard extension class variables
    
    # Name of extension - used to make config file field.
    extName = 'Spotify'
    
    # Settings to store in config; use dictionary format.
    # Values can be referenced to as config[<extension name>][<key>].
    extSettings = {'client_id': 'ADD_CLIENT_ID_HERE',
                 'client_secret': 'ADD_CLIENT_SECRET_HERE'}
        
    extOperative = 'play'
    
    # Config file heavy lifting:
    
    # Check if config file has the extension's section. If not, adds it in with default values defined above.
    config.read('config.ini')
    
    if not config.has_section(extName):
        config[extName] = extSettings
        config.write(open('config.ini', 'a'))
    
    # Beyond this point are extension-specific class variables
    scope = 'playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private streaming ugc-image-upload user-follow-modify user-follow-read user-library-read user-library-modify user-read-private user-read-birthdate user-read-email user-top-read user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played'

    token = util.prompt_for_user_token('jiansoo', scope, config['Spotify']['client_id'],
                                       config['Spotify']['client_secret'],
                                       redirect_uri='http://localhost/')

    sp = spotipy.client.Spotify(auth=token)
    
    # Extension methods
    def __init__(self):
        self.operative = Extension.extOperative

    def startPlayback(self):
        print('Started playback')
        self.sp.start_playback()

    def stopPlayback(self):
        self.sp.pause_playback()

    def searchTrack(self, sterm):
        uri_list = []
        result = self.sp.search(sterm, type='track')
        result_uri = result['tracks']['items'][0]['uri']
        print(result_uri)
        uri_list.append(result_uri)
        self.sp.start_playback(uris=uri_list)

    def searchPlaylist(self, sterm):
        result = self.sp.search(sterm, type='playlist')
        result_uri = result['playlists']['items'][0]['uri']
        print(result_uri)
        self.sp.start_playback(context_uri=result_uri)
    
    # General 'parse' command: interprets voice input 
    def parse(self, command):
        # Play music
        if command[0] == 'music':
            say('Playing music.')
            self.startPlayback()
            sv.playing = True
            
        # Play playlist ...
        elif command[0] == 'playlist':
            searchterm = ' '.join(command[1:])
            say('Playing' + searchterm)
            self.searchPlaylist(searchterm)
            sv.playing = True
        
        # Play ... playlist
        elif command[-1] == 'playlist':
            searchterm = ' '.join(command[:-1])
            say('Playing' + searchterm)
            self.searchPlaylist(searchterm)
            sv.playing = True
        
        # Play ...
        else:
            searchterm = ' '.join(command)
            say('Playing' + searchterm)
            self.searchTrack(searchterm)
            sv.playing = True