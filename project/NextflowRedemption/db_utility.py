import jsonpickle
from django.conf import settings
import nextflow

files = ["pipeline", "template", "user"]

def load(from_file):
    if (from_file in files):
        with open( str(settings.BASE_DIR)  + '/' + str(from_file)  + '.json', 'r') as f:
            from_file = f.read()
            if (from_file != ""):
                return jsonpickle.decode(from_file) 
            else:
                return []

def save(to_file, objects):
    if (to_file in files):
        json = jsonpickle.encode([ob for ob in objects])

        with open( str(settings.BASE_DIR)  + '/' + str(to_file)  + '.json', 'w') as f:
            f.write(json)

