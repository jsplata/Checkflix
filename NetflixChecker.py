import re
import requests
import json
import discord
from validator_collection import checkers

#Launching client
client = discord.Client()
#Logging
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
#On message
@client.event
async def on_message(message):
    #check if message is calling for the bot
    if message.content.startswith('-check'):
        #strip the -check command and check for the movie/show name
        user_string = message.content.split("-check ",1)[1]
        #send a request to the API with the parameters given by the user
        url = "https://unogsng.p.rapidapi.com/search"
        query_string = {"query":user_string}
        #add keys from config file
        with open('config.json', 'r') as config:
            data = config.read()
            obj = json.loads(data)
            headers = {
                'x-rapidapi-key': obj['RAPIDAPI_KEY'],
                'x-rapidapi-host': obj['RAPIDAPI_HOST']
            }
        #get the API response
        response = requests.request("GET", url, headers=headers, params=query_string)
        #take only the first result from the API        
        parsed = json.loads(response.text)['results'][0]
        #place the synopsis in the description
        description = parsed['synopsis'].replace('&#39;',"'")
        #process the country list
        obj = {k.strip('"'): v.strip('"') for k, v in [p.split(':') for p in parsed['clist'].split(',')]}
        #add the country list to the description
        description = description + '\n\n Available in: ' + str(list(obj.values())).strip('[').strip(']').replace("'","")
        #create the embed from different items from the response
        embed = discord.Embed(title=parsed['title'] + ' (click to watch)', url='https://www.netflix.com/title/' + str(parsed['nfid']), description=description, color=0xFF5733)
        #check whether a movie has a poster link, if it has, show it
        if(checkers.is_url(parsed['poster'])):
            embed.set_image(url=parsed['poster'])
        await message.channel.send(embed = embed)
#Loading token into client
with open('config.json', 'r') as config:
    data = config.read()
    obj = json.loads(data) 
client.run(obj['TOKEN'])
