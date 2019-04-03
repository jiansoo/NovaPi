# <Extension Name> <Version Number> for Nova
# Author: <Name>
# Dependencies: <Dependencies>

# Import modules here
import sys
import configparser

# Add /modules as a path variable
sys.path.append('../modules')

# Import modules
config = configparser.ConfigParser()

class Extension:
    # Standard extension class variables

    # Name of extension - used to make config file field.
    extName = 'EXTENSION_NAME_HERE'

    # Settings to store in config; use dictionary format.
    # Values can be referenced to as config[<extension name>][<key>].
    extSettings = {
        'variable1': 'ADD_VAR',
        'variable2': 'ADD_VAR',
    }

    # If your extension uses 1 intent, you can make it a string instead of an array.
    extIntent = ['INTENT1', 'INTENT2']

    # Config file heavy lifting:

    # Check if config file has the extension's section. If not, adds it in with default values defined above.
    config.read('config.ini')

    if not config.has_section(extName):
        config[extName] = extSettings
        config.write(open('config.ini', 'a'))

    # Here are extension-specific class variables:
    
    #   token = sp.util_prompt_for_token('wafAfawf')

    # Extension methods here:
    def __init__(self):
        self.intent = Extension.extIntent

    # When your extension's intent is matched, the parse command will be invoked.
    # The Wit.AI response is passed as an argument as well as your intent as a string.
    def parse(self, witResponse, intent):
        # Invokes methods depending on detected intent.

        if intent == 'drinkDrink':
            pass
        elif intent == 'eatFood':
            pass
