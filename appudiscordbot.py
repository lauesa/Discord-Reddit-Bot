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
path = 'C:/Users/Appu/Desktop/pyscripts/'

bot = commands.Bot(command_prefix='ap:', description='test')

@bot.command(pass_context=True)
async def follow(ctx):
    sub = ctx.message.content.split('follow', 1)[1].strip()
    f = open('%susers/allusers.txt' % path, 'r+')
    all = f.read().strip()
    if all:
        users = all.split(',')
        users = users[:-1]
    else:
        users = []
    if ctx.message.author.id not in users:
        users.append(ctx.message.author.id)
        f.seek(0)
        f.truncate()
        for i in users:
            f.write(i + ',')
        f.close()
        if sub:
            try:
                try:
                    name = ctx.message.mentions[0]
                    toFollow = name.id
                except IndexError:
                    server = ctx.message.server
                    try:
                        name = discord.Server.get_member_named(server, sub)
                    except:
                        await bot.say('Could not find the user\'s list. They might not be subscribed.')
                        return
                    toFollow = name.id
                g = open('%susers/user%s.txt' % (path, toFollow), 'r')
                copy = g.read()
                g.close()
                paste = open('%susers/user%s.txt' % (path, ctx.message.author.id), 'w+')
                paste.write(copy)
                paste.seek(0)
                paste.write(ctx.message.author.id)
                paste.close()
                await bot.say('Subscribed and imported %s\'s list. Do ``ap:list`` to view list.' % name)
            except Exception as e:
                traceback.print_exc()
                if e == IndexError:
                    await bot.say('Not a valid argument. Example use: ``ap:follow`` or ``ap:follow appu1232#2569`` (You don\'t need to tag them)' % toFollow)
                else:
                    await bot.say('Could not find the user\'s list. They might not be subscribed.')
        else:
            keywords = open('%susers/user%s.txt' % (path, ctx.message.author.id), 'w+')
            keywords.write(ctx.message.author.id + '\nNotif location: ' + ctx.message.author.id + '\n----Blacklist----\nrecommend, recommendation, recomend, recommendations, suggest, suggestion, sugest, suggestions\n\n----Anime----\n\n----Manga----\n\n----End----')
            keywords.close()
            await bot.say('**You are now subscribed to the manga/anime notifier feed.** Your following list is empty so use ``ap:add`` to add the manga and anime you want to follow and ``ap:list`` to see your current list. Use ``ap:commands`` for more commands.')
    else:
        # if sub:
        #     await merge/follow
        await bot.say('You are **already subscribed** to the notifier. Do ``ap:list`` to see your current list. Do ``ap:commands`` to see other commands.')
        f.close()

@bot.command(pass_context=True)
async def unfollow(ctx):
    f = open('%susers/allusers.txt' % path, 'r+')
    all = f.read().strip()
    if all:
        users = all.split(',')
    else:
        users = []
    if ctx.message.author.id in users:
        users.remove(ctx.message.author.id)
        f.seek(0)
        f.truncate()
        if users != ['']:
            for i in users:
                if i:
                    f.write(i + ',')
        else:
            pass
        os.remove('%susers/user%s.txt' % (path, ctx.message.author.id))
        await bot.say('You have unsubscribed from the manga/anime notifier feed. Use ``ap:follow`` to resubscribe if you\'d like. **Note: your list has been deleted** so if you subscribe again, you must remake your list.')
    else:
        await bot.say('You are already unsubscribed from the notifier.')
    f.close()

@bot.command(pass_context=True)
async def location(ctx):
    if not isFollowing(ctx.message.author.id):
        await bot.say('Use ``ap:follow`` first to subscribe to the bot. Do ``ap:commands`` for more help')
    else:
        try:
            sub = ctx.message.content.split('location', 1)[1].strip()
            f = open('%susers/user%s.txt' % (path, ctx.message.author.id), 'r+')
            content = f.readlines()
            if sub.lower() == 'here':
                content[1] = 'Notif location: %s\n' % str(ctx.message.channel.id)
            elif sub.lower() == 'dm':
                content[1] = 'Notif location: %s\n' % ctx.message.author.id
            else:
                channel = ctx.message.raw_channel_mentions
                if channel != []:
                    content[1] = 'Notif location: %s\n' % str(channel[0])
                else:
                    await bot.say('Invalid location. Ex: ``ap:location dm`` Possible locations:\n``ap:location dm`` - Direct message you\n``ap:location here`` - This channel\n``ap:location #channel`` - Other channel on this server')
                    return
            f.seek(0)
            f.truncate()
            for i in content:
                f.write(i)
            f.close()
            await bot.say('Successfully set location. Sent a test message to specified location.')
            if bot.get_channel(content[1][16:].strip()):
                await bot.send_message(discord.Object(id=content[1][16:].strip()), 'This is where you will recieve notifications.')
            else:
                await bot.send_message(discord.User(id=content[1][16:].strip()), 'This is where you will recieve notifications.')
        except:
            traceback.print_exc()
            await bot.say('Please specify a location. Ex: ``ap:location dm`` Possible locations:\n``ap:location dm`` - Direct message you\n``ap:location here`` - This channel\n``ap:location #channel`` - Other channel on this server')


@bot.command(pass_context=True)
async def on(ctx):
    if not isFollowing(ctx.message.author.id):
        await bot.say('Use ``ap:follow`` first to subscribe to the bot. Do ``ap:commands`` for more help')
    else:
        f = open('%susers/user%s.txt' % (path, ctx.message.author.id), 'r+')
        content = f.read()
        if content.startswith('--disable--'):
            content = content[11:]
            f.seek(0)
            f.truncate()
            f.write(content)
        f.close()
        await bot.say('Notifications have been enabled for you. Use ``ap:off`` to disable notifications.')

@bot.command(pass_context=True)
async def off(ctx):
    if not isFollowing(ctx.message.author.id):
        await bot.say('Use ``ap:follow`` first to subscribe to the bot. Do ``ap:commands`` for more help')
    else:
        f = open('%susers/user%s.txt' % (path, ctx.message.author.id), 'r+')
        content = f.read()
        f.seek(0)
        f.write('--disable--' + content)
        f.close()
        await bot.say('Notifications have been disabled for you. Use ``ap:on`` to enable notifications.')

@bot.command(pass_context=True)
async def list(ctx):
    sub = ctx.message.content.split('list', 1)[1].strip()
    f = open('%susers/allusers.txt' % path, 'r+')
    all = f.read().strip()
    if all:
        users = all.split(',')
    else:
        users = []
    if sub:
        try:
            try:
                toFollow = ctx.message.mentions[0]
                await bot.say('**%s\'s list:**' % str(toFollow))
                toFollow = toFollow.id
            except IndexError:
                server = ctx.message.server
                try:
                    toFollow = discord.Server.get_member_named(server, sub).id
                    temp = await bot.get_user_info(toFollow)
                except:
                    await bot.say('Could not find the user\'s list. They might not be subscribed.')
                    return
                await bot.say('**%s\'s list:**' % temp)
        except Exception as e:
            traceback.print_exc()
            if e == IndexError:
                await bot.say('Not a valid argument. Example use: ``ap:follow`` or ``ap:follow appu1232#2569`` (You don\'t need to tag them)' % toFollow)
            else:
                await bot.say('Could not find the user\'s list. They might not be subscribed.')
                return
        list = listKeyWords(str(toFollow))
        if len(list) > 2:
            await bot.say('List is very large. Sending via DM so chat doesn\'t get cluttered.')
            for i in list:
                await bot.send_message(discord.User(id=ctx.message.author.id), '```%s```' % i)
        else:
            for i in list:
                await bot.say('```%s```' % i)

    else:
        if ctx.message.author.id not in users:
            await bot.say('You are not subscribed to the notifier. Do ``ap:follow`` to subscribe and start adding anime/manga to follow.')
        else:
            list = listKeyWords(ctx.message.author.id)
            if len(list) > 2:
                await bot.say('List is very large. Sending via DM so chat doesn\'t get cluttered.')
                for i in list:
                    await bot.send_message(discord.User(id=ctx.message.author.id), '```%s```' % i)
            else:
                for i in list:
                    await bot.say('```%s```' % i)

@bot.command(pass_context=True)
async def add(ctx):
    if not isFollowing(ctx.message.author.id):
        await bot.say('Use ``ap:follow`` first to subscribe to the bot. Do ``ap:commands`` for more help')
    else:
        msg = '**Error** Something went wrong. Are you using the command right? Example uses: ``ap:add manga One Piece`` or ``ap:add manga Kaguya Wants to Be Confessed to = Kaguya wants, kaguya-sama wants`` or ``ap:add -a anime One Punch Man S2 = opm s2, opm season 2, one punch man season 2``'
        try:
            toFollow = ctx.message.content.split('ap:add')[1].strip()
            if addKeyWords(toFollow, ctx.message.author.id) == True:
                await bot.say('Successfully added ``%s`` to ``%s``. View your list with ``ap:list``.' % (toFollow.split(' ', 1)[1].strip(), toFollow.split(' ', 1)[0].strip()))
            else:
                await bot.say(msg)
        except Exception as e:
            traceback.print_exc()
            await bot.say(msg)

@bot.command(pass_context=True)
async def remove(ctx):
    msg = '**Error** Something went wrong. Are you using the command right? Example use: ``ap:remove anime One Punch Man S2``'
    try:
        toUnfollow = ctx.message.content.split('ap:remove')[1].strip()
        if removeKeyWords(toUnfollow, ctx.message.author.id) == True:
            await bot.say('Successfully removed ``%s`` from ``%s``. View your list with ``ap:list``.' % (toUnfollow.split(' ', 1)[1].strip(), toUnfollow.split(' ', 1)[0].strip()))
        else:
            await bot.say(msg)
    except Exception as e:
        traceback.print_exc()
        await bot.say(msg)

@bot.command(pass_context=True)
async def commands(ctx):
    await bot.say('\n**Bot commands:**\n\n``ap:follow`` or ``ap:follow person`` - Subscribe to the bot. This means you can start adding and removing manga and anime. Optionally, put a person username (doesn\'t have to be a mention) to import their list.\n\n``ap:unfollow`` - Unsubscribe from the bot. You will not receive any more notifications. Warning: this deletes your list.\n\n``ap:list`` or ``ap:list person`` - Get your current keywords list or seomeone else\'s.\n\n``ap:add subreddit name`` or ``ap:add subreddit name = keyword1, keyword2, ...``  or ``ap:add -a subreddit name = keyword1, keyword2, ...`` - Add an anime or manga to follow. <subreddit> can be either ``anime`` or ``manga``. <name> is the title of the anime/manga. Optionally, add keywords to specify more in case you think it could be posted under different titles (like japanese title vs. english titles). Using the ``-a`` flag gives you notifications on all threads posted about your anime/manga, not just episode/chapter updates. Leave it out to recieve only episode/chapter updates. Ex: ``ap:add anime Little With Academia`` or ``ap:add -a manga Boku no Hero = boku no hero academia, my hero academia``\n\n``ap:remove subreddit name`` - Remove keywords for the specified sub from the list. Ex: ``ap:remove anime Hunter x Hunter``\n\n``ap:location dm/channel`` - Where to get notifications. ``dm`` for direct message, ``here`` for current channel or ``#channel_name`` for another channel. Default after you follow is ``dm``\n\n``ap:off`` - Turn off all notifications for you. Useful if you want to stop notifications temporarily but don\'t want to delete your list.\n\n``ap:on`` - Turn on notifications if off.\n\n``ap:info`` - Get bot info and current settings.')

start_time = time.time()
tz = pytz.timezone('US/Eastern')

def isFollowing(msg):
    f = open('%susers/allusers.txt' % path, 'r+')
    all = f.read().strip()
    if all:
        users = all.split(',')
        users = users[:-1]
    else:
        users = []
    if msg not in users:
        return False
    return True

def currentRun(allcheck, hits, notifssent, loops):
    seconds = time.time() - start_time
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    temp = open('settings.txt', 'r').readlines()
    currRun = '```Bot has been running for: %s days, %s hours, %s minutes, and %s seconds\n\nLinks checked: %s\nHits: %s\nNotifications sent: %s\nItterations without fail: %s\nCurrent settings:\n' % (int(days), int(hours), int(minutes), int(seconds), allcheck, hits, notifssent, loops)
    for i in temp:
        currRun += '    ' + i
    currRun += '\n\n' + 'Available settings: anime, manga```'
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
        traceback.print_exc()
        pass



def listKeyWords(msg):
    kw = open('%susers/user%s.txt' % (path, msg), 'rU')
    msg = ''
    kw.readline()
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
        allWords.append(msg)
        msg = ''
    kw.close()
    return allWords

def addKeyWords(word, user):
    afds = open('%susers/user%s.txt' % (path, user), 'rU')
    if word.split(' ', 1)[0].strip() == '-a':
        aorm = word.split(' ', 2)[1].strip()
        title = word.split(' ', 2)[2].strip()
        allthreads = True
    else:
        aorm = word.split(' ', 1)[0].strip()
        title = word.split(' ', 1)[1].strip()
        allthreads = False
    if '=' not in title:
        title2 = title.strip()
        keys = title.lower().strip()
    else:
        title2 = title.split('=', 1)[0].strip()
        keys = title.split('=', 1)[1].lower().strip()
    if keys.endswith(','):
        keys = keys[:-1]
    data = afds.readlines()
    afds.close()
    if aorm.lower() == 'anime' or aorm.lower() == 'manga':
        for i,d in enumerate(data):
            if '----' in d:
                if aorm.lower() in d.lower():
                    c = 0
                    while data[i+c] != '\n':
                        c += 1
                    if allthreads:
                        title2 = '[All Threads] ' + title2
                    else:
                        if aorm.lower() == 'anime':
                            title2 = '[Episodes Only] ' + title2
                        else:
                            title2 = '[Chapters Only] ' + title2
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
                    line = '----End----'
                    while title.lower().strip() != line:
                        c += 1
                        if data[i+c].startswith('[All Threads]'):
                            line = data[i+c][14:].lower().split(' = ', 1)[0].strip()
                        elif data[i+c].startswith('[Episodes Only]') or data[i+c].startswith('[Chapters Only]'):
                            line = data[i+c][16:].lower().split(' = ', 1)[0].strip()
                    data[i+c] = ''
                    afds = open('%susers/user%s.txt' % (path, user), 'w')
                    afds.truncate()
                    afds.writelines(data)
                    afds.close()
    else:
        afds.close()
        return False
    return True

@bot.command(pass_context=True)
async def info(ctx):
    run = run = open('current_run', 'r')
    info = run.readlines()
    await bot.say(currentRun(info[0], info[1], info[2], info[3]))

async def checker():
    allcheck = []
    loopCount = 0
    allcheckcount = 0
    checked = []
    hits = 0
    notifssent = 0
    failCount = 0
    userFollows = {}

    while True:
        try:
            if failCount > 5:
                time.sleep(20)
            #traceback.print_exc()
            r = praw.Reddit(client_id='LBfKLnsNZwuPlA',
                                 client_secret='oHeIsPqIM8t4xw3MJki9qEXcg-4',
                                 password='appu2844',
                                 user_agent='Related Submissions by /u/appu1232',
                                 username='appubot2')
            failCount = 0
            while True:
                loopCount += 1
                userFollows.clear()
                if len(checked) >= 80:
                    checked = checked[40:]
                for users in os.listdir('users'):
                    animeKeyWords = {}
                    mangaKeyWords = {}
                    if users == 'allusers.txt':
                        continue
                    with open('%susers/%s' % (path, users), 'r') as stuff:
                        str1 = stuff.readline()
                        if '--disable--' in str1:
                            continue
                        currUser = str1.strip()
                        str1 = stuff.readline()
                        while str1 != '':
                            if 'Notif location: ' in str1:
                                notif = str1.split('Notif location: ')[1].strip()
                            str1 = stuff.readline()
                            if '----Blacklist----' in str1:
                                str1 = stuff.readline()
                                if ',' in str1:
                                    lstr2 = str1.strip().split(',')
                                    for word in lstr2:
                                        blacklist.append(word.strip())
                                else:
                                    blacklist.append(str1.strip())
                            if '----Anime----' in str1:
                                while str1 != '':
                                    str1 = stuff.readline()
                                    str2 = str1.strip().split(' = ', 1)
                                    if str2[0] == '':
                                        break
                                    temp = []
                                    if ',' in str2[1]:
                                        lstr2 = str2[1].lstrip().split(',')
                                        for word in lstr2:
                                            temp.append(word.strip())
                                        animeKeyWords[str2[0]] = temp
                                    else:
                                        temp.append(str2[1].lstrip())
                                        animeKeyWords[str2[0]] = temp
                            if '----Manga----' in str1:
                                while str1 != '':
                                    str1 = stuff.readline()
                                    str2 = str1.strip().split(' = ', 1)
                                    if str2[0] == '':
                                        break
                                    temp = []
                                    if ',' in str2[1]:
                                        lstr2 = str2[1].lstrip().split(',')
                                        for word in lstr2:
                                            temp.append(word.strip())
                                        mangaKeyWords[str2[0]] = temp
                                    else:
                                        temp.append(str2[1].lstrip())
                                        mangaKeyWords[str2[0]] = temp
                    userFollows[currUser] = [animeKeyWords, mangaKeyWords, notif]
                settings = open('settings.txt', 'r')
                msg = ''
                f = settings.read()
                settings.close()
                if 'anime' in f:
                    errorCatch = '/r/anime'
                    subreddit = r.subreddit('anime')
                    for submission in subreddit.new(limit=8):
                        if submission.id in checked:
                            continue
                        op_title = submission.title.lower()
                        if submission.id not in allcheck:
                            if len(allcheck) == 40 and ('anime'):
                                allcheck = [allcheck[-1]] + allcheck[:-1]
                                allcheck[0] = submission.id
                                allcheckcount += 1
                            if len(allcheck) != 40 and ('anime'):
                                allcheck.append(submission.id)
                                allcheckcount += 1
                        blacklist_words = any(string in op_title for string in blacklist)
                        if blacklist_words and submission.id not in checked:
                            checked.append(submission.id)
                        alertUsers = {}
                        for eachUser in userFollows.items():
                            for anime in eachUser[1][0].items():
                                key_words = any(string in op_title for string in anime[1])
                                updateType = True
                                if not anime[0].startswith('[All Threads] '):
                                    if '[Spoilers] ' not in submission.title:
                                        updateType = False
                                    title = anime[0][16:]
                                else:
                                    title = anime[0][14:]
                                if submission.id not in checked and key_words:
                                    if updateType:
                                        if eachUser:
                                            if eachUser[1][2] in alertUsers.keys():
                                                temp = alertUsers[eachUser[1][2]]
                                                temp.append(eachUser[0].strip())
                                                alertUsers[eachUser[1][2]] = temp
                                            else:
                                                alertUsers[eachUser[1][2]] = [eachUser[0].strip()]
                                            msg = '\n%s related thread: "%s"\n%s in %s' % (title, (submission.title[:50] + '..') if len(submission.title) > 50 else submission.title, submission.shortlink, errorCatch)
                                            notifssent += 1
                        allmentions = ''
                        checked.append(submission.id)
                        if alertUsers:
                            for i in alertUsers.keys():
                                if bot.get_channel(i):
                                    for j in alertUsers[i]:
                                        temp = await bot.get_user_info(j)
                                        allmentions += temp.mention + ' '
                                    await bot.send_message(discord.Object(id=i), allmentions + msg)
                                    allmentions = ''
                                else:
                                    await bot.send_message(discord.User(id=i), msg)
                            hits += 1
                            await bot.send_message(discord.Object(id='260971339903533056'), msg)
                    await asyncio.sleep(4)
                msg = ''
                if 'manga' in f:
                    errorCatch = '/r/manga'
                    subreddit = r.subreddit('manga')
                    for submission in subreddit.new(limit=8):
                        if submission.id in checked:
                            continue
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
                        alertUsers = {}
                        for eachUser in userFollows.items():
                            for manga in eachUser[1][1].items():
                                key_words = any(string in op_title for string in manga[1])
                                updateType = True
                                if not manga[0].startswith('[All Threads] '):
                                    if '[DISC]' not in submission.title:
                                        updateType = False
                                    title = manga[0][16:]
                                else:
                                   title = manga[0][14:]
                                if submission.id not in checked and key_words:
                                    if updateType:
                                        if eachUser:
                                            if eachUser[1][2] in alertUsers.keys():
                                                temp = alertUsers[eachUser[1][2]]
                                                temp.append(eachUser[0].strip())
                                                alertUsers[eachUser[1][2]] = temp
                                            else:
                                                alertUsers[eachUser[1][2]] = [eachUser[0].strip()]
                                            msg = '\n%s related thread: "%s"\n%s in %s' % (title, (submission.title[:50] + '..') if len(submission.title) > 50 else submission.title, submission.shortlink, errorCatch)
                                            notifssent += 1
                        allmentions = ''
                        checked.append(submission.id)
                        if alertUsers:
                            for i in alertUsers.keys():
                                if bot.get_channel(i):
                                    for j in alertUsers[i]:
                                        temp = await bot.get_user_info(j)
                                        allmentions += temp.mention + ' '
                                    await bot.send_message(discord.Object(id=i), allmentions + msg)
                                    allmentions = ''
                                else:
                                    await bot.send_message(discord.User(id=i), msg)
                            hits += 1
                            await bot.send_message(discord.Object(id='260971339903533056'), msg)
                    run = open('current_run' , 'w')
                    run.truncate()
                    run.write(str(allcheckcount) + '\n' + str(hits) + '\n' + str(notifssent) + '\n' + str(loopCount))
                    run.close()
                    await asyncio.sleep(4)
        except Exception as e:
            traceback.print_exc()
            failCount += 1
            pass

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----------')
    await checker()

try:
    bot.loop.create_task(on_ready())
except Exception as e:
    bot.loop.run_until_complete(on_ready())
    raise e

bot.run('MjYwNjUxNDYxMTgzMTQzOTM4.CzzG2g.EkOac6xCIJ0VT_MiYWHCazWdp-k')