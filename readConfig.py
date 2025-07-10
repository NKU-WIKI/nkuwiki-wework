import json

def readConfig():
    with open('config.json', 'r', encoding='utf-8') as json_file:
        config = json.load(json_file)
    return config