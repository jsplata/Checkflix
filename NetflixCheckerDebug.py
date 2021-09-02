import requests
import json
import discord

def search_title(search_string):
    url = "https://unogsng.p.rapidapi.com/search"
    query_string = {"query":search_string}

    with open('config.json', 'r') as config:
        data = config.read()
        obj = json.loads(data)
        headers = {
        'x-rapidapi-key': obj['RAPIDAPI_KEY'],
        'x-rapidapi-host': obj['RAPIDAPI_HOST']
        }
    response = requests.request("GET", url, headers=headers, params=query_string)
    return response.text

search_string = input('Please write the title you are looking for: ')
print(search_title(search_string))