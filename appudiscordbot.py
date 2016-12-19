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

import time
import datetime
import pytz
import praw
import smtplib
import math
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from discord.ext import commands

blacklist = []
animeKeyWords = {}
mangaKeyWords = {}
print('sadflkjdhsaf')

client = discord.Client()
bot = commands.Bot(command_prefix='ap:', description='test')
# @bot.command()
# async def add(left : int, right : int):
#     """Adds two numbers together."""
#     await bot.say(left + right)

@bot.command(pass_context=True)
async def list(ctx):
    await bot.say(ctx.message.author.mention + ' list')

@bot.command(pass_context=True)
async def add(ctx):
    await bot.say(ctx.message.author.mention + ' add')

@bot.command(pass_context=True)
async def remove(ctx):
    await bot.say(ctx.message.author.mention + ' remove')
@bot.command(pass_context=True)
async def settings(ctx):
    await bot.say(ctx.message.author.mention + ' settings')
@bot.command(pass_context=True)
async def commands(ctx):
    await bot.say(ctx.message.author.mention +  '```Bot commands:\n\nstop - Stop sending all notifications. \n\nstart - If stopped, resume notifier. \n\n! - Get bot info and current settings. \n\nsettings: <subreddit1>, <subreddit2>, ... - Set the settings file. Ex: settings: anime, manga \n\nlist - Get current keywords list. \n\nadd: <subreddit> ---- name = kw1, kw2, ... - Add keywords for the specified sub to the list. Ex: add: anime ---- Steins;Gate = steins;gate, s;g, okabe, kurisu \n\nremove: <subreddit> ---- name - Remove keywords for the specified sub from the list. Ex: remove: anime ---- Hunter x Hunter```')

@client.event
async def on_message(message):
    if message.content.lower().startswith('test'):
        tag = message.content.split('test', 1)[1].strip()
        #with urllib.request.urlopen("http://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=100&tags=" + tag.replace(" ", "_")) as response:
            #match = response.read()
        #matches = re.findall(re.escape('file_url="') + '(.*?)' + re.escape('" '), str(match))
        #rand = random.randrange(0, len(matches))
        await client.send_message(message.channel, message.author.mention)
    if message.content.lower().startswith('stop'):
        # redditor.message('Bot paused', 'Bot has been paused. [Manage server.](https://cloud.digitalocean.com/droplets/33441368/graphs)')
        while pause() == False:
            time.sleep(5)
    if message.content.lower().startswith('appu: !'):
        client.send_message(message.channel, message.author.mention + currentRun())
    if message.content.lower().startswith('appu: list'):
        client.send_message(message.channel, message.author.mention + ' list of keywords')
    if message.content.lower().startswith('appu: add:'):
        client.send_message(message.channel, message.author.mention + ' add')
    if message.content.lower().startswith('appu: remove:'):
        client.send_message(message.channel, message.author.mention + ' remove')
    if message.content.lower().startswith('appu: settings:'):
        client.send_message(message.channel, message.author.mention + ' settings')
    if message.content.lower().startswith('appu: commands') or message.content.lower().startswith('appu: cmds') or message.content.lower().startswith('appu: help'):
        client.send_message(message.channel, message.author.mention + ' ```Bot commands', '`stop` - Stop sending all notifications. \n\n `start` - If stopped, resume notifier. \n\n `!` - Get bot info and current settings. \n\n `settings: <subreddit1>, <subreddit2>, ...` - Set the settings file. `Ex: settings: anime, manga` \n\n `list` - Get current keywords list. \n\n `add: <subreddit> ---- name = kw1, kw2, ...` - Add keywords for the specified sub to the list. `Ex: add: anime ---- Steins;Gate = steins;gate, s;g, okabe, kurisu` \n\n `remove: <subreddit> ---- name` - Remove keywords for the specified sub from the list. `Ex: remove: anime ---- Hunter x Hunter` \n\n `clear-log` - Clear log file.```')

start_time = time.time()
failCount = 0
tz = pytz.timezone('US/Eastern')

def pause():
    return True


def currentRun(allcheck, hits, loops):
    seconds = time.time() - start_time
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    temp = open('settings.txt', 'r').readlines()
    currRun = '```Bot has been running for: %s days, %s hours, %s minutes, and %s seconds\n\nLinks checked: %s\nHits: %s\nItterations without fail: %s\nCurrent settings:\n' % (int(days), int(hours), int(minutes), int(seconds), allcheck, hits, loops)
    for i in temp:
        currRun += '    ' + i
    currRun += '\n\n' + 'Available settings: anime, questions, manga, steinsgate```'
    info = 'Bot is running'
    return currRun

def changeSettings(word):
    try:
        temp = []
        if ',' in word:
            temp = word[9:].strip().split(',')
        else:
            temp.append(word[9:].strip())
        for i,b in enumerate(temp):
            temp[i] = temp[i].strip() + '\n'
        setfile = open('settings.txt', 'w')
        setfile.truncate()
        setfile.writelines(temp)
        setfile.close()
        setfile = open('settings.txt', 'r').read()
        currentRun()
    except Exception as e:
        pass
        #redditor.message('Settings update failed', 'Could not update settings file with `%s` Error thrown: `%s`' % (word, e))



def listKeyWords(msg):
    kw = open('keywords.txt', 'rU')
    kw2 = kw.read()
    part = int(math.ceil(len(kw2) / 5000))
    kw4 = [kw2[i:i+5000] for i in range(0, len(kw2), 5000)]
    for i,blocks in enumerate(kw4):
        msg += 'List of keywords: %s of %s \n\n' % (i+1, part+1)
        for b in blocks.split('\n'):
            msg += '    ' + b + '\n'
        info = 'Bot keyword info'
        #redditor.message('%s pt. %s' % (info, i+1), msg)
        msg = ''
    kw.close()

def addKeyWords(word):
    afds = open('keywords.txt', 'r')
    try:
        temp = word.split('add:', 1)[1].lstrip()
        aorm = temp.split('----', 1)[0].strip()
        title = temp.split('----', 1)[1].strip()
        title2 = title.split('=', 1)[0].strip()
        keys = title.split('=', 1)[1].strip()
        data = afds.readlines()
        afds.close()
        if aorm.lower() == 'anime' or aorm.lower() == 'manga':
            for i,d in enumerate(data):
                if '----' in d:
                    if aorm.lower() in d.lower():
                        c = 0
                        while data[i+c] != '\n':
                            c += 1
                        data[i+c] = title2 + ' = ' + keys + '\n' + data[i+c]
                        afds = open('keywords.txt', 'w')
                        afds.writelines(data)
                        afds.close()
                        listKeyWords('Added `%s = %s` to `%s`\n\n' % (title2, keys, aorm.lower()))
        else:
            #redditor.message('Keyword addition failed', 'Unable to add `%s` to `%s`' % (title, aorm.lower()))
            afds.close()
    except Exception as e:
        #traceback.print_exc()
        #redditor.message('Keyword addition failed', 'Something went wrong when tokenizing: `%s` Error thrown: `%s`' % (word, e))
        afds.close()

def removeKeyWords(word):
    afds = open('keywords.txt', 'r')
    try:
        temp = word.split('remove:', 1)[1].lstrip()
        aorm = temp.split('----', 1)[0].strip()
        title = temp.split('----', 1)[1].strip()
        data = afds.readlines()
        afds.close()
        if aorm.lower() == 'anime' or aorm.lower() == 'manga':
            for i,d in enumerate(data):
                if '----' in d:
                    if aorm.lower() in d.lower():
                        c = 0
                        while title.lower().strip() != data[i+c].lower().split(' = ', 1)[0].strip():
                            c += 1
                        data[i+c] = ''
                        afds = open('keywords.txt', 'w')
                        afds.truncate()
                        afds.writelines(data)
                        afds.close()
                        listKeyWords('Removed `%s` from `%s`\n\n' % (title, aorm.lower()))
        else:
            listKeyWords('Keyword removal failed. Could not find `%s` in `%s`\n\n' % (title, aorm.lower()))
            afds.close()
    except Exception as e:
        #traceback.print_exc()
        listKeyWords('Keyword removal failed. Syntax error/word not found for: `%s` Error thrown: `%s`\n\n' % (word, e))
        afds.close()

@bot.event
async def on_ready():
    allcheck = []
    loopCount = 0
    allcheckcount = 0
    checked = []
    hits = 0
    while True:
        failCount = 0
        #try:
        print('-----------')
        r = praw.Reddit(client_id='736Wc6N44ZYyxA',
                             client_secret='HSZQv9Bkh1SOEBESiXbU6lpPYOw',
                             password='appu2844',
                             user_agent='Related Submissions by /u/appu1232',
                             username='appubot')
        errorCatch = ''
        while True:
            loopCount += 1

            str1 = '+'
            currentRun(allcheckcount, hits, loopCount)
            print(checked)
            @bot.command(pass_context=True)
            async def info(ctx):
                await bot.say(ctx.message.author.mention + currentRun(allcheckcount, hits, loopCount))
            if len(checked) >= 80:
                checked = checked[40:]
            with open('keywords.txt', 'r') as stuff:
                while str1 != '':
                    str1 = stuff.readline()
                    if '----Blacklist----' in str1:
                        str1 = stuff.readline()
                        if ', ' in str1:
                            lstr2 = str1.strip().split(', ')
                            for word in lstr2:
                                blacklist.append(word)
                        else:
                            blacklist.append(str1.strip())
                    if '----Anime----'  in str1:
                        while str1 != '':
                            str1 = stuff.readline()
                            str2 = str1.strip().split(' = ', 1)
                            if str2[0] == '':
                                break
                            temp = []
                            if ', ' in str2[1]:
                                lstr2 = str2[1].lstrip().split(', ')
                                for word in lstr2:
                                    temp.append(word)
                                animeKeyWords[str2[0]] = temp
                            else:
                                temp.append(str2[1].lstrip())
                                animeKeyWords[str2[0]] = temp
                    if '----Manga----'  in str1:
                        while str1 != '':
                            str1 = stuff.readline()
                            str2 = str1.strip().split(' = ', 1)
                            if str2[0] == '':
                                break
                            temp = []
                            if ', ' in str2[1]:
                                lstr2 = str2[1].lstrip().split(', ')
                                for word in lstr2:
                                    temp.append(word)
                                mangaKeyWords[str2[0]] = temp
                            else:
                                temp.append(str2[1].lstrip())
                                mangaKeyWords[str2[0]] = temp
            settings = open('settings.txt', 'r')
            inbox = praw.models.Inbox(r, [])
            msgs = inbox.unread(limit=1).__iter__()
            for words in msgs:
                words.mark_read()
                if words.body.lower().startswith('stop'):
                    #redditor.message('Bot paused', 'Bot has been paused. [Manage server.](https://cloud.digitalocean.com/droplets/33441368/graphs)')
                    while pause() == False:
                        time.sleep(5)
                if words.body.lower().startswith('!'):
                    currentRun()
                if words.body.lower().startswith('list'):
                    listKeyWords('')
                if words.body.lower().startswith('add:'):
                    addKeyWords(words.body)
                if words.body.lower().startswith('remove:'):
                    removeKeyWords(words.body)
                if words.body.lower().startswith('settings:'):
                    changeSettings(words.body)
                if words.body.lower().startswith('commands') or words.body.lower().startswith('cmds') or words.body.lower().startswith('help'):
                    #redditor.message('Bot commands', '`stop` - Stop sending all notifications. \n\n `start` - If stopped, resume notifier. \n\n `!` - Get bot info and current settings. \n\n `settings: <subreddit1>, <subreddit2>, ...` - Set the settings file. `Ex: settings: anime, manga` \n\n `list` - Get current keywords list. \n\n `add: <subreddit> ---- name = kw1, kw2, ...` - Add keywords for the specified sub to the list. `Ex: add: anime ---- Steins;Gate = steins;gate, s;g, okabe, kurisu` \n\n `remove: <subreddit> ---- name` - Remove keywords for the specified sub from the list. `Ex: remove: anime ---- Hunter x Hunter` \n\n `clear-log` - Clear log file.')
                    pass
                if words.body.lower().startswith('clear-log'):
                    pass
                    #redditor.message('Bot log', 'Log has been cleared.')
            msgs = None
            f = settings.read()
            settings.close()
            if 'anime' in f:
                errorCatch = '/r/anime'
                subreddit = r.subreddit('anime')
                for submission in subreddit.new(limit=8):
                    op_title = submission.title.lower()
                    if submission.id not in allcheck:
                        if len(allcheck) == 40 and ('anime' in f or 'questions' in f):
                            allcheck = [allcheck[-1]] + allcheck[:-1]
                            allcheck[0] = submission.id
                            allcheckcount += 1
                        if len(allcheck) != 40 and ('anime' in f or 'questions' in f):
                            allcheck.append(submission.id)
                            allcheckcount += 1
                    blacklist_words = any(string in op_title for string in blacklist)
                    if blacklist_words and submission.id not in checked:
                        checked.append(submission.id)
                    for anime in animeKeyWords.items():
                        key_words = any(string in op_title for string in anime[1])
                        if submission.id not in checked and key_words:
                            msg = '%s related thread: %s in %s' % (anime[0], submission.shortlink, errorCatch)
                            info = (submission.title[:50] + '..') if len(submission.title) > 50 else submission.title
                            #stuff = discord.Server()
                            await bot.send_message(discord.Object(id='259921092586504202'), msg)
                            #redditor.message('%s' % info, msg)
                            checked.append(submission.id)
                            hits += 1
                await asyncio.sleep(4)
            if 'manga' in f:
                errorCatch = '/r/manga'
                subreddit = r.subreddit('manga')
                for submission in subreddit.new(limit=8):
                    op_title = submission.title.lower()
                    if submission.id not in allcheck:
                        if len(allcheck) == 40 and 'manga' in f:
                            allcheck = [allcheck[-1]] + allcheck[:-1]
                            allcheck[0] = submission.id
                            allcheckcount += 1
                        if len(allcheck) != 40 and 'manga' in f:
                            allcheck.append(submission.id)
                            allcheckcount += 1
                    blacklist_words = any(string in op_title for string in blacklist)
                    if blacklist_words and submission.id not in checked:
                        checked.append(submission.id)
                    for manga in mangaKeyWords.items():
                        key_words = any(string in op_title for string in manga[1])
                        if submission.id not in checked and key_words:
                            msg = '[%s related thread](%s) in %s' % (manga[0], submission.shortlink, errorCatch)
                            info = (submission.title[:50] + '..') if len(submission.title) > 50 else submission.title
                            #redditor.message('%s' % info, msg)
                            checked.append(submission.id)
                            hits += 1
                await asyncio.sleep(4)
            if loopCount > 10:
                failCount = 0
        # except Exception as e:
        #     try:
        #         if failCount <= 4:
        #             failCount += 1
        #             try:
        #                 #traceback.print_exc()
        #                 time.sleep(5)
        #                 #redditor.message('Bot crashed', 'Failed at loop %d in %s block. Error: `%s` Attempting to restart in 2 minutes. [Manage server.](https://cloud.digitalocean.com/droplets/33441368/graphs)' % (loopCount, errorCatch, str(e)))
        #                 #logger('--------CRASHED--------\n')
        #                 #logger('Crashed during loop. Sent Reddit message. Attempting to restart in 2 minutes. Error: %s %s\n' % (str(e), failCount))
        #                 time.sleep(120)
        #             except Exception as g:
        #                 pass
        #                 #sendEmail(300, 'Bot crashed', 'Restarting postponed 5 minutes. [Manage server.](https://cloud.digitalocean.com/droplets/33441368/graphs)')
        #                 #logger('--------CRASHED--------\n')
        #                 #logger('Crashed trying to send exception message. Sent email. Attempting to restart in 30 minutes. Error: %s\n' % str(g))
        #         else:
        #             failCount += 1
        #             try:
        #                 pass
        #                 #redditor.message('Bot has crashed too many times', 'Restarting postponed for 30 mins. [Manage server.](https://cloud.digitalocean.com/droplets/33441368/graphs)')
        #             except:
        #                 pass
        #             #sendEmail(1800, 'Bot crashed too many times', 'Restarting postponed 30 minutes. [Manage server.](https://cloud.digitalocean.com/droplets/33441368/graphs)')
        #             #logger('--------CRASHED--------\n')
        #             #logger('Crashing during loop too much. Sent Reddit message and email. Attempting to restart in 30 minutes. Error: %s\n' % str(e))
        #             failCount = 0
        #     except Exception as f:
        #         if failCount > 4:
        #             #logger('######## Crashing too much, sleeping for 5 minutes. ########\n\n')
        #             failCount = 0
        #             time.sleep(300)
        #         else:
        #             failCount += 1
        #             #logger('--------CRASHED--------\n')
        #             #logger('Crashed at exception handler. Error: %s %s\n' % (f, failCount))

bot.run('MjU5OTE3Njk0MzE5NDYwMzUy.Cze6TQ.00RvXhRokiMeuBKRF7qzjnolRj0')