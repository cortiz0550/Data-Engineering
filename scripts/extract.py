import requests
import json
import os

def load_config(path):
    with open(path, 'r') as json_file:
        config = json.load(json_file)
    print(config)
    
path = os.getcwd()
load_config(path + "\\config\\qualtrics_config.json")