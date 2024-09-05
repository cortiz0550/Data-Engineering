import requests
import json

def load_config(path):
    with open(path, 'r') as json_file:
        config = json.load(json_file)
    
    print(config)

load_config("C:\\Users\\E33100\\OneDrive - SRI International\\My Stuff\\Me\\PD\\Data-Engineering\\config\\qualtrics_config.json")    