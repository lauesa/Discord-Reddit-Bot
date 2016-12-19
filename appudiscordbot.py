import random, sys, os, math, time, datetime, re, urllib.request, asyncio
import discord
import pytz
import praw
import traceback
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from discord.ext import commands

blacklist = []
animeKeyWords = {}
mangaKeyWords = {}
path = 'C:/Users/Deepak/Desktop/pyscripts/discordbot/'

bot = commands.Bot(command_prefix='ap:', description='test')
# @bot.command()
# async def add(left : int, right : int):
#     """Adds two numbers together."""
#     await bot.say(left + right)
@bot.command(pass_context=True)
async def follow(ctx):
    f = open('%susers/allusers.txt' % path, 'r+')
    all = f.read().strip()
    if all != '':
        users = all.split(',')
    else:
        users = []
    if ctx.message.author.id not in users:
        users.append(ctx.message.author.id)
        f.seek(0)
        f.truncate()
        for i in users:
            f.write(i + ',')
        keywords = open('%susers/user%s.txt' % (path, ctx.message.author.id), 'w+')
        keywords.write(ctx.message.author.id + '\n----' + '----Blacklist----\nrecommend, recommendation, recomend, recommendations, suggest, suggestion, sugest, suggestions\n\n----Anime----\n\n----Manga----\n\n----End----')
        keywords.close()
        await bot.say(ctx.message.author.mention + ' **You are now subscribed to the manga/anime notifier feed.** Your following list is empty so use ``ap:add`` to add the manga and anime you want to follow and ``ap:list`` to see your current list. Use ``ap:commands`` for more commands.')
    else:
        await bot.say(ctx.message.author.mention + 'You are **already subscribed** to the notifier. Do ``ap:list`` to see your current list. Do ``ap:commands`` to see other commands.')
    f.close()

@bot.command(pass_context=True)
async def unfollow(ctx):
    f = open('%susers/allusers.txt' % path, 'r+')
    all = f.read().strip()
    if all != '':
        users = all.split(',')
    else:
        users = []
    if ctx.message.author.id in users:
        users.remove(ctx.message.author.id)
        f.seek(0)
        f.truncate()
        if users != ['']:
            for i in users:
                if i is not '':
                    f.write(i + ',')
        else:
            pass
        os.remove('%susers/user%s.txt' % (path, ctx.message.author.id))
        await bot.say(ctx.message.author.mention + ' You have unsubscribed from the manga/anime notifier feed. Use ``ap:follow`` to resubscribe if you\'d like. **Note: your list has been deleted** so if you subscribe again, you must remake your list.')
    else:
        await bot.say(ctx.message.author.mention + 'You are already unsubscribed from the notifier.')
    f.close()

@bot.command(pass_context=True)
async def list(ctx):
    f = open('%susers/allusers.txt' % path, 'r+')
    all = f.read().strip()
    if all != '':
        users = all.split(',')
    else:
        users = []
    if ctx.message.author.id not in users:
        await bot.say(ctx.message.author.mention + ' You are not subscribed to the notifier. Do ``ap:follow`` to subscribe and start adding anime/manga to follow.')
    else:
        await bot.say(ctx.message.author.mention)
        for i in listKeyWords(ctx.message.author.id):
            await bot.say('```' + i + '```')

@bot.command(pass_context=True)
async def add(ctx):
    toFollow = ctx.message.content
    msg = ctx.message.author.mention + '**Error** Something went wrong. Are you using the command right? Example use: ``ap:add anime One Punch Man S2 - opm s2, opm season 2, one punch man season 2``'
    try:
        toFollow = ctx.message.content.split('ap:add')[1].strip()
        if addKeyWords(toFollow, ctx.message.author.id) is True:
            await bot.say(ctx.message.author.mention + 'Successfully added ``%s`` to ``%s``. View your list with ``ap:list``.' % (toFollow.split(' ', 1)[1].strip(), toFollow.split(' ', 1)[0].strip()))
        else:
            await bot.say(msg)
    except Exception as e:
        await bot.say(msg)

@bot.command(pass_context=True)
async def remove(ctx):
    toUnfollow = ctx.message.content
    msg = ctx.message.author.mention + '**Error** Something went wrong. Are you using the command right? Example use: ``ap:remove anime One Punch Man S2``'
    try:
        toUnfollow = ctx.message.content.split('ap:remove')[1].strip()
        if removeKeyWords(toUnfollow, ctx.message.author.id) is True:
            await bot.say(ctx.message.author.mention + 'Successfully removed ``%s`` from ``%s``. View your list with ``ap:list``.' % (toUnfollow.split(' ', 1)[1].strip(), toUnfollow.split(' ', 1)[0].strip()))
        else:
            await bot.say(msg)
    except Exception as e:
        await bot.say(msg)
@bot.command(pass_context=True)
async def settings(ctx):
    await bot.say(ctx.message.author.mention + ' settings')
@bot.command(pass_context=True)
async def commands(ctx):
    await bot.say(ctx.message.author.mention +  '\n**Bot commands:**\n\n``ap:info`` - Get bot info and current settings. \n\n``ap:settings <subreddit1>, <subreddit2>, ...`` - [WORK IN PROGRESS] Set the settings file. Ex: ``ap:settings anime, manga`` \n\n``ap:list`` - Get current keywords list. \n\n``ap:add <subreddit> name = kw1, kw2, ...`` - Add keywords for the specified sub to the list. Ex: ``ap:add anime Steins;Gate = steins;gate, s;g, okabe, kurisu`` \n\n``ap:remove <subreddit> name`` - Remove keywords for the specified sub from the list. Ex: ``ap:remove anime Hunter x Hunter``')

# @client.event
# async def on_message(message):
#     if message.content.lower().startswith('test'):
#         tag = message.content.split('test', 1)[1].strip()
#         #with urllib.request.urlopen("http://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=100&tags=" + tag.replace(" ", "_")) as response:
#             #match = response.read()
#         #matches = re.findall(re.escape('file_url="') + '(.*?)' + re.escape('" '), str(match))
#         #rand = random.randrange(0, len(matches))
#         await client.send_message(message.channel, message.author.mention)
#     if message.content.lower().startswith('stop'):
#         # redditor.message('Bot paused', 'Bot has been paused. [Manage server.](https://cloud.digitalocean.com/droplets/33441368/graphs)')
#         while pause() == False:
#             time.sleep(5)
#     if message.content.lower().startswith('appu: !'):
#         client.send_message(message.channel, message.author.mention + currentRun())
#     if message.content.lower().startswith('appu: list'):
#         client.send_message(message.channel, message.author.mention + ' list of keywords')
#     if message.content.lower().startswith('appu: add:'):
#         client.send_message(message.channel, message.author.mention + ' add')
#     if message.content.lower().startswith('appu: remove:'):
#         client.send_message(message.channel, message.author.mention + ' remove')
#     if message.content.lower().startswith('appu: settings:'):
#         client.send_message(message.channel, message.author.mention + ' settings')
#     if message.content.lower().startswith('appu: commands') or message.content.lower().startswith('appu: cmds') or message.content.lower().startswith('appu: help'):
#         client.send_message(message.channel, message.author.mention + ' ```Bot commands', '`ap:info` - Get bot info and current settings. \n\n `ap:settings: <subreddit1>, <subreddit2>, ...` - [WORK IN PROGRESS] Set the settings file. `Ex: ap:settings: anime, manga` \n\n `ap:list` - Get current keywords list. \n\n `ap:add: <subreddit> name = kw1, kw2, ...` - Add keywords for the specified sub to the list. `Ex: ap:add: anime Steins;Gate = steins;gate, s;g, okabe, kurisu` \n\n `ap:remove: <subreddit> name` Remove keywords for the specified sub from the list. `Ex: ap:remove: anime Hunter x Hunter` \n\n `clear-log` - Clear log file.```')

start_time = time.time()
failCount = 0
tz = pytz.timezone('US/Eastern')

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

def pause():
    return True

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
    kw = open('%susers/user%s.txt' % (path, msg), 'rU')
    msg = ''
    kw.readline()
    kw.readline()
    kw.readline()
    kw2 = kw.read()
    part = int(math.ceil(len(kw2) / 1900))
    kw4 = [kw2[i:i+1900] for i in range(0, len(kw2), 1900)]
    allWords = []
    for i,blocks in enumerate(kw4):
        msg += 'List of keywords: %s of %s\n' % (i+1, part)
        for b in blocks.split('\n'):
            msg += b + '\n'
        info = 'Bot keyword info'
        allWords.append(msg)
        #redditor.message('%s pt. %s' % (info, i+1), msg)
        msg = ''
    kw.close()
    return allWords

def addKeyWords(word, user):
    afds = open('%susers/user%s.txt' % (path, user), 'rU')
    aorm = word.split(' ', 1)[0].strip()
    title = word.split(' ', 1)[1].strip()
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
                    afds = open('%susers/user%s.txt' % (path, user), 'w')
                    afds.writelines(data)
                    afds.close()
    else:
        afds.close()
        return False
    return True

def removeKeyWords(word, user):
    afds = open('%susers/user%s.txt' % (path, user), 'r')
    aorm = word.split(' ', 1)[0].strip()
    title = word.split(' ', 1)[1].strip()
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
                    afds = open('%susers/user%s.txt' % (path, user), 'w')
                    afds.truncate()
                    afds.writelines(data)
                    afds.close()
    else:
        afds.close()
        return False
    return True

@bot.event
async def on_ready():
    allcheck = []
    loopCount = 0
    allcheckcount = 0
    checked = []
    hits = 0
    userFollows = {}
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
            @bot.command(pass_context=True)
            async def info(ctx):
                await bot.say(ctx.message.author.mention + currentRun(allcheckcount, hits, loopCount))
            if len(checked) >= 80:
                checked = checked[40:]
            for users in os.listdir('users'):
                if users == 'allusers.txt':
                    continue
                print(users)
                with open('%susers/%s' % (path, users), 'r') as stuff:
                    str1 = stuff.readline()
                    if '----disable----' in str1:
                        continue
                    currUser = str1.strip()
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
                userFollows[currUser] = [animeKeyWords, mangaKeyWords]
            settings = open('settings.txt', 'r')
            msg = ''
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
                    alertUsers = []
                    for eachUser in userFollows.items():
                        for anime in eachUser[1][0].items():
                            key_words = any(string in op_title for string in anime[1])
                            if submission.id not in checked and key_words:
                                alertUsers.append(eachUser[0].strip())
                                msg = '\n%s related thread: "%s"\n%s in %s' % (anime[0], (submission.title[:50] + '..') if len(submission.title) > 50 else submission.title, submission.shortlink, errorCatch)
                                hits += 1
                    allmentions = ''
                    for i in alertUsers:
                        temp = await bot.get_user_info(i)
                        allmentions += temp.mention + ' '
                    if msg != '':
                        await bot.send_message(discord.Object(id='259921092586504202'), allmentions + msg)
                        checked.append(submission.id)
                await asyncio.sleep(4)
            msg = ''
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
                    alertUsers = []
                    for eachUser in userFollows.items():
                        for manga in eachUser[1][1].items():
                            key_words = any(string in op_title for string in manga[1])
                            if submission.id not in checked and key_words:
                                alertUsers.append(eachUser[0].strip())
                                msg = '\n%s related thread: "%s"\n%s in %s' % (manga[0], (submission.title[:50] + '..') if len(submission.title) > 50 else submission.title, submission.shortlink, errorCatch)
                                hits += 1
                    allmentions = ''
                    for i in alertUsers:
                        temp = await bot.get_user_info(i)
                        allmentions += temp.mention + ' '
                    if msg != '':
                        await bot.send_message(discord.Object(id='259921092586504202'), allmentions + msg)
                        checked.append(submission.id)
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