import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
import os
from bulbmanager import BulbManager
import datetime

bm = BulbManager()
def start_speech_transcription():
    # This function opens an audio stream to capture voice input and sends it off to Google to interpret.
    # Uses the speech_recognition module by Anthony Zhang (Uberi).

    # Remember to add sound after recog.adjust_for_ambient_noise... indicates you can start speaking.
    # Maybe make it only adjust the ambient noise once at startup? Otherwise it might derp up if starting while
    # someone is talking.

    # Setting up speech recognition objects.
    recog = sr.Recognizer()
    mic = sr.Microphone()
    
    activate = AudioSegment.from_wav("../resources/Nova_Activated.wav")
    error = AudioSegment.from_wav("../resources/Nova_Error.wav")
    with mic as source:
        # Adjusts sensitivity of microphone depending on background noise.
        print("Adjusting sensitivity to negate background noise.")
        recog.adjust_for_ambient_noise(source)
        
        # Play 'listening' sound.
        bm.activeLight()
        play(activate-20)
        
        # Records audio data for sending to Google services.
        print("Listening to command.")
        audioData = recog.listen(source)
        print("Stopped listening.")
        bm.normalLight()
        try:
            # Sends request to Google's speech recognition API. If all goes well, value is returned.
            voiceInput = recog.recognize_google(audioData)
            print(voiceInput)
            return voiceInput
        except:
            # Print to console in event of recognition failure.
            print('Something went wrong!')

def say(voiceoutput):
    print(voiceoutput)
    if not os.path.isfile('spokenaudio/'+voiceoutput+'.mp3'):
        tts = gTTS(voiceoutput)
        tts.save('spokenaudio/'+voiceoutput+'.mp3')
        
    audio = AudioSegment.from_mp3('spokenaudio/'+voiceoutput+'.mp3')
    play(audio-20)

def localise(datetime):
    return datetime + datetime.timedelta(hours=8)

def tomorrow():
    return datetime.datetime.now() + datetime.timedelta(days=1)