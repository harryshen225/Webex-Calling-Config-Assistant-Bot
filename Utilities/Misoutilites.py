import time
import json

def current_time():
    return time.strftime("%I:%M %p %A")

def extractAAIdName(message):
    return json.dumps([{"value": item["id"], "title": item["name"]} for item in message])
