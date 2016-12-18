import random
import sys
import os
import json
from discord.ext import commands
import discord
import re
import urllib.request
import asyncio
#http = new HttpClient()

client = discord.Client()

@client.event
async def on_message(message):
    if message.content.startswith('test'):
        tag = message.content.split('test', 1)[1].strip()
        #with urllib.request.urlopen("http://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=100&tags=" + tag.replace(" ", "_")) as response:
            #match = response.read()
        #matches = re.findall(re.escape('file_url="') + '(.*?)' + re.escape('" '), str(match))
        #rand = random.randrange(0, len(matches))
        await client.send_message(message.channel, message.author.mention)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run('MjU5OTE3Njk0MzE5NDYwMzUy.Cze6TQ.00RvXhRokiMeuBKRF7qzjnolRj0')
