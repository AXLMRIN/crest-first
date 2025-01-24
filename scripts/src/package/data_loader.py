# Third parties

# Native

# Custom

# Classes

# Functions
from json import load

#===============================================================================

def load_JSON_parameters(
        filenames : dict, FOLDERNAME : str = 'scripts/plotlyThemes/'
        ) -> dict:
    """Conveniently load a bunch of json files
    Given a dictionnary [key, filename] it returns a dictionnary [key, content]"""

    parameters = {}

    for key in filenames : 
        with open(FOLDERNAME + filenames[key], "r") as file:
            parameters[key] = load(file)
    
    return parameters