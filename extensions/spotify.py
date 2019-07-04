# Spotify Extension v1 for Nova
# Author: Jian Soo
# Dependencies: SpotiPy

# Add /modules as a path variable (Optional, only needed if you are trying to run the extension without running NOVA)
# sys.path.append('fullpath to NOVA directory')

# Import modules
import spotipy.util as util
import spotipy as spotipy
import configparser
config = configparser.ConfigParser()
import os
from utils import say, print_warn, print_debug


class Extension:
    # Standard extension class variables
    
    # Name of extension - used to make config file field.
    extName = 'Spotify'
    
    # Settings to store in config; use dictionary format.
    # Values can be referenced to as config[<extension name>][<key>].
    extSettings = {
        'user_id': 'ADD_USER_ID_HERE',
        'client_id': 'ADD_CLIENT_ID_HERE', 
        'client_secret': 'ADD_CLIENT_SECRET_HERE'
        }
        
    extIntent = ['playMusic', 'playPlaylist']
    
    # Config file heavy lifting:
    
    # Check if config file has the extension's section. If not, adds it in with default values defined above.
    config.read('config.ini')
    
    if not config.has_section(extName):
        config[extName] = extSettings
        config.write(open('config.ini', 'a'))
    
    # Beyond this point are extension-specific class variables
    scope = 'playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private streaming ugc-image-upload user-follow-modify user-follow-read user-library-read user-library-modify user-read-private user-read-birthdate user-read-email user-top-read user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played'

    token = util.prompt_for_user_token(config['Spotify']['user_id'], scope, config['Spotify']['client_id'],
                                       config['Spotify']['client_secret'],
                                       redirect_uri='http://localhost/')

    sp = spotipy.client.Spotify(auth=token)
    
    # Extension methods
    def __init__(self):
        self.intent = Extension.extIntent

    def startPlayback(self):
        # Starts playback on current active device.
        self.sp.start_playback()
        os.environ['playing'] = 'True'

    def stopPlayback(self):
        # Stops playback on current active device.
        self.sp.pause_playback()

    def searchTrack(self, sterm):
        # Searches Spotify database for song URIs, and then starts playback.
        uri_list = []
        result = self.sp.search(sterm, type='track')
        result_uri = result['tracks']['items'][0]['uri']
        print_debug('Track URI '+ result_uri)
        uri_list.append(result_uri)
        return uri_list

    def searchPlaylist(self, sterm):
        # Searches Spotify database for playlist URIs, and then starts playback.
        result = self.sp.search(sterm, type='playlist')
        result_uri = result['playlists']['items'][0]['uri']
        print_debug('Playlist URI ' + result_uri)
        return result_uri
    
    # General 'parse' command: interprets voice input 
    def parse(self, witResponse, intent):
        # Invokes methods depending on detected intent.

        # Track - track/playlist name
        # Artist - artist
        # Intent - detected intent by wit.ai model
        os.environ['playing'] = 'True'
        if intent == 'playMusic':
            track = witResponse['entities']['track'][0]['value']
            artist = witResponse['entities']['artist'][0]['value']
            self.sp.start_playback(uris=self.searchTrack(track + ' ' + artist))
                
        elif intent == 'playPlaylist':
            playlist = witResponse['entities']['track'][0]['value']
            self.sp.start_playback(context_uri=self.searchPlaylist(playlist))
            
        return
        
