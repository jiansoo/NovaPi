import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
import os
from bulbmanager import BulbManager
import datetime

bm = BulbManager()

def print_debug(message):
    print('\033[0;37;43m DEBUG \033[0m ' + message)
    return
    
def print_warn(message):
    print('\033[0;37;41m WARNG \033[0m ' + message)
    return

def print_output(message):
    print('\033[0;37;45m OUTPT \033[0m ' + message)
    return

def start_speech_transcription():
    # This function opens an audio stream to capture voice input and sends it off to Google to interpret.
    # Uses the speech_recognition module by Anthony Zhang (Uberi).

    # Remember to add sound after recog.adjust_for_ambient_noise... indicates you can start speaking.
    # Maybe make it only adjust the ambient noise once at startup? Otherwise it might derp up if starting while
    # someone is talking.

    # Setting up speech recognition objects.
    recog = sr.Recognizer()
    mic = sr.Microphone()
    
    activate = AudioSegment.from_wav("./resources/Nova_Activated.wav")
    error = AudioSegment.from_wav("./resources/Nova_Error.wav")
    with mic as source:
        # Adjusts sensitivity of microphone depending on background noise.
        print_debug("Adjusting sensitivity to negate background noise. ")
        recog.adjust_for_ambient_noise(source)
        
        # Play 'listening' sound.
        bm.activeLight()
        play(activate-2)
        
        # Records audio data for sending to Google services.
        print_debug("Listening to command.")
        audioData = recog.listen(source)
        print_debug("Stopped listening.")
        bm.normalLight()
        try:
            # Sends request to Google's speech recognition API. If all goes well, value is returned.
            voiceInput = recog.recognize_google(audioData)
            print_debug('Transcribed \''+ voiceInput + '\'')
            return voiceInput
        except sr.UnknownValueError:
            # Return None if there's nothing that's been said.
            return None

def say(voiceoutput):
    print_output(voiceoutput)
    if not os.path.isfile('./resources/spokenaudio/'+voiceoutput+'.mp3'):
        tts = gTTS(voiceoutput)
        tts.save('./resources/spokenaudio/'+voiceoutput+'.mp3')
        
    audio = AudioSegment.from_mp3('./resources/spokenaudio/'+voiceoutput+'.mp3')
    play(audio-2)

def localise(datetime):
    return datetime + datetime.timedelta(hours=8)

def tomorrow():
    return datetime.datetime.now() + datetime.timedelta(days=1)

def setplayingtrue():
    os.environ['playing'] = True

def setplayingfalse():
    os.environ['playing'] = False