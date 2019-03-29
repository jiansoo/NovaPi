# DarkSky Extension v1 for Nova
# Author: Jian Soo
# Dependencies: ForecastIOPy

# Add /modules as a path variable
import sys
sys.path.append('../modules')

# Import modules
from forecastiopy import *
import configparser
config = configparser.ConfigParser()
import os
from utils import *
import herepy
import random
import dateutil.parser
import datetime
from wit import Wit

class Extension:
    # Standard extension class variables
    
    # Name of extension - used to make config file field.
    extName = 'DarkSkyWeather'
    
    # Settings to store in config; use dictionary format.
    # Values can be referenced to as config[<extension name>][<key>].
    extSettings = {
    'dsw_api_key':'ADD_API_KEY_HERE', 
    'herepy_app_id': 'ADD_API_KEY_HERE', 
    'herepy_app_code': 'ADD_API_KEY_HERE'
    }
        
    extIntent = ['findWeather', 'findRainChance']
    
    # Config file heavy lifting:
    
    # Check if config file has the extension's section. If not, adds it in with default values defined above.
    config.read('config.ini')
    
    if not config.has_section(extName):
        config[extName] = extSettings
        config.write(open('config.ini', 'a'))
    # Beyond this point are extension-specific class variables:
    dsw_apiKey = config[extName]['dsw_api_key']

    herepy_appId = config[extName]['herepy_app_id']
    herepy_appCode = config[extName]['herepy_app_code']

    # Extension methods
    def __init__(self):
        self.intent = Extension.extIntent
    
    def getForecaster(self, location):
        # Get coordinates from address.
        geocoderApi = herepy.GeocoderApi(Extension.herepy_appId, Extension.herepy_appCode)
        jsonResponse = geocoderApi.free_form(location)
        coords = jsonResponse.as_dict()['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]

        # Making ForecastIO object from coordinates.
        return ForecastIO.ForecastIO(Extension.dsw_apiKey, units=ForecastIO.ForecastIO.UNITS_SI, lang=ForecastIO.ForecastIO.LANG_ENGLISH, latitude=coords['Latitude'], longitude=coords['Longitude'])
        
    def summaryInDays(self, location, days):
        forecaster = self.getForecaster(location)
        currently = FIOCurrently.FIOCurrently(forecaster)
        hourly = FIOHourly.FIOHourly(forecaster)
        daily = FIODaily.FIODaily(forecaster)

        # Gives summary of current weather conditions.
        if days == 0:
            targetDay = {'summary': hourly.summary, 'icon': hourly.icon}
            speech = hourly.summary
            # Say current temperature and humidity.
            speechCurrently = 'At ' + ' '.join(location) + ' it is currently ' + str(round(currently.temperature,1)) + ' degrees Celsius, with ' + str(round(currently.humidity*100)) + ' percent humidity.'
            say(speechCurrently)
    
        elif days <= daily.days():
            targetDay = daily.get_day(days)
            speech = targetDay['summary']
        
        elif days > daily.days(): 
            say('Please ask for a day less than 7 days in the future.')
            return
        
        elif days < 0:
            say('Weather history is currently not supported.')
            return
        
        
        # Say current summary.
        say(speech)

        if targetDay['icon'] == 'clear-day':
            opinion = ["A nice clear day.",
            "Looks like the sun is out.",
            "No clouds, no rain. Looks like it's going to be a nice sunny day.",
            "Perfect weather for the beach!",
            "Clear days like this are a real blessing.",
            "Looks like it's clear and blue skies today."
            ]
        elif targetDay['icon'] == 'clear-night':
            opinion = ["A nice clear night.",
            "Looks like the stars are out.",
            "Get a good look at the moon.",
            "The sky is pretty. Have a look.",
            "No clouds. Maybe you can see the stars.",
            "Perfect weather for some starseeing."
            ]
        elif targetDay['icon'] == 'rain':
            opinion = ["If you're going out, bring an umbrella!",
            "Cloudy and watery skies. Take an umbrella!",
            "Not a good day for outdoor activities.",
            "A bit of rain every once in a while never hurt anybody.",
            "I'm thinking an umbrella's what you need.",
            "Hope the rain isn't too heavy.",
            "Don't forget to take your umbrella!"
            ]
        elif targetDay['icon'] == 'snow':
            opinion = ["Perfect weather for a snowman.",
            "Good day if you want to go for a ski!",
            "It will be snowing, so wear some layers! It's going to be cold.",
            "Somehow, the word snow seems to ring a bell...",
            "It's a happy and snowy day."
            ]
        elif targetDay['icon'] == 'sleet':
            opinion = ["Oh, sleet. Never trust a cross between snow and rain.",
            "Sleet, huh? Pack an umbrella.",
            "Don't forget your umbrella!",
            "Some interesting weather we have today.",
            "Rain and snow together, huh? Good luck with that."
            ]
        elif targetDay['icon'] == 'wind':
            opinion = ["It's a windy day, so enjoy the breeze!",
            "Enjoy the breeze!",
            "The weather will blow you away! Ha ha.",
            "It's going to be a breezy day.",
            "Perfect weather to do some sailing!",
            "Perfect weather to play with a kite."
            ]
        elif targetDay['icon'] == 'fog':
            opinion = ["Can't see much in this weather...",
            "Kinda spooky, isn't it?",
            "Perfect weather for some ghost stories.",
            "Visibility's going to be bad today.",
            "I haven't the foggiest idea about what the weather will bring. Ha ha."
            ]
        elif targetDay['icon'] == 'cloudy':
            opinion = ["The clouds are out. Hopefully it won't rain.",
            "Cloudy days are quite pleasant, aren't they?",
            "Perfect weather for some sports.",
            "Perfect weather for some exercise. How about a run?",
            "Nice and cloudy weather. Have some fun."
            ]
        elif targetDay['icon'] == 'partly-cloudy-day':
            opinion = ["Looks like the clouds are out.",
            "Cloudy and sunny; the perfect mix.",
            "Not too sunny, not too overcast. A nice day, for sure.",
            "A good day for some sports.",
            "A good day to go out for a run.",
            "It's a good day for some outdoor activities."
            ]

        elif targetDay['icon'] == 'partly-cloudy-night':
            opinion = ["You won't be able to see many stars.",
            "A cloudy night... spooky, isn't it?",
            "And the moon was a ghostly galleon among the cloudy sky.",
            "Tonight's weather is kind of poetic.",
            "A cloudy night sky dotted with stars is good too.",
            "The sky's looking spooky."
            ]

        else:
            opinion = ["Have a nice day!",
        "Have a good day!"
            ]

        # Give a quip based on the weather status.
        say(random.choice(opinion))

    def rainChance(self, location, day):
        # Method to find rain chance given ForecastIO object.
        forecaster = self.getForecaster(location)
        daily = FIODaily.FIODaily(forecaster)
        
        # Checks if requested day falls within data in ForecastIO object.
        if day <= daily.days():
            rainprob = daily.get_day(day)['precipProbability']*100
            if day == 0:
                rainString = 'There is a ' + str(rainprob) + ' percent chance it will rain today.' 
            elif day == 1:
                rainString = 'There is a ' + str(rainprob) + ' percent chance it will rain tomorrow.'
            elif day == 2:
                rainString = 'There is a ' + str(rainprob) + ' percent chance it will rain the day after tomorrow.'
            else:
                rainString = 'There is a ' + str(rainprob) + ' percent chance it will rain in ' + str(day) + ' days.'
        elif day < 0:
            # Todo... add Time Machine feature from ForecastIO.
            say('Weather history is currently not supported.')
            return
        else:
            say('You can request weather information up to 7 days in the future.')
            return

        say(rainString)

    # General 'parse' command: interprets voice input 
    def parse(self, witResponse, intent):
        # Load intent information from json.

        # Location = (resolved) location
        # Time = datetime object of target time

        location = witResponse['entities']['location'][0]['value']
        
        # Try interpreting response as single datetime object.
        # If input such as 'this weekend' is used, wit.ai returns a range... which throws an error here.
        try:
            time = witResponse['entities']['datetime'][0]['value']
        except:
            # If you say 'this weekend', we take the average between the to and from datetimes.
            timeTo = witResponse['entities']['datetime'][0]['to']['value']
            timeFrom = witResponse['entities']['datetime'][0]['from']['value']
            # Parse time to datetime format and find midpoint. a + (b - a)/2
            time = dateutil.parser.parse(timeFrom, ignoretz=True) + (dateutil.parser.parse(timeTo, ignoretz=True)-dateutil.parser.parse(timeFrom, ignoretz=True))/2

        # Find delta in days from current date to requested date.
        dayDelta = (dateutil.parser.parse(time, ignoretz=True)-datetime.datetime.now()+datetime.timedelta(days=1)).days
        
        # Invokes methods depending on detected intent.
        if intent == 'findWeather':
            self.summaryInDays(location, dayDelta)
        elif intent == 'findRainChance':
            self.rainChance(location, dayDelta)