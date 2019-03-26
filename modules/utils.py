import speech_recognition as sr
import nltk
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
    
    activate = AudioSegment.from_wav("/home/pi/Desktop/NovaPi/resources/Nova_Activated.wav")
    error = AudioSegment.from_wav("/home/pi/Desktop/NovaPi/resources/Nova_Error.wav")
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

def find_and_split(full, search):
    # This function is quite important... it looks for commands in input and parses them to find the command arguments.
    # Functioning is quite simple, though.

    # Create WhitespaceTokeniser object to perform tokenisation.
    whitespaceTokeniser = nltk.tokenize.WhitespaceTokenizer()

    # 'Tokenise' voice input according to whitespace. In other words, make it into an array.
    tokenise_input = whitespaceTokeniser.tokenize(full)

    # Searching for term in tokenised input... Lazy, but it works.
    
    # Special case for extensions with multiple operatives
    if type(search) is list:
        for term in search:
            for i in range(len(tokenise_input)):
                # If the search is positive, sends back the term and all words after it. Simple array slice.
                if term == tokenise_input[i]:
                    command_contents = tokenise_input[i+1:]
                    return command_contents, term
        # If there's no matching term, return None.
        return None
    
    else:
        for i in range(len(tokenise_input)):
            # If the search is positive, sends back the term and all words after it. Simple array slice.
            if search == tokenise_input[i]:
                command_contents = tokenise_input[i+1:]
                return command_contents

        # If there's no matching term, return None.
        return None

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