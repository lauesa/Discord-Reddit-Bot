import os, math, time, asyncio
import discord
import json
import pytz
import praw
import traceback
from discord.ext import commands
import spice_api as spice

with open('config.json', 'r') as f:
    config = json.load(f)
path = config["path"]
description = '''Subreddit keyword notifier by appu1232'''

bot = commands.Bot(command_prefix='ap:', description=description)

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
                        await bot.send_message(ctx.message.channel, 'Could not find the user\'s list. They might not be subscribed.')
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
                await bot.send_message(ctx.message.channel, 'Subscribed and imported %s\'s list. Do ``ap:list`` to view list.' % name)
                await bot.send_message(discord.Object(id=config["log_location"]), 'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))
            except Exception as e:
                traceback.print_exc()
                if e == IndexError:
                    await bot.send_message(ctx.message.channel, 'Not a valid argument. Example use: ``ap:follow`` or ``ap:follow appu1232#2569`` (You don\'t need to tag them)' % toFollow)
                else:
                    await bot.send_message(ctx.message.channel, 'Could not find the user\'s list. They might not be subscribed.')
        else:
            keywords = open('%susers/user%s.txt' % (path, ctx.message.author.id), 'w+')
            keywords.write(ctx.message.author.id + '\nNotif location: ' + ctx.message.author.id + '\n----Blacklist----\ngore, nsfl\n\n----Anime----\n\n----Manga----\n\n----re_zero----\n\n----gamedeals----\n\n----End----')
            keywords.close()
            await bot.send_message(ctx.message.channel, '**You are now subscribed to the reddit notifier feed.** Your following list is empty.\nDo ``ap:addsubreddit <subreddit>`` to add a subreddit you want to follow. Ex: ``ap:addsubreddit discordapp``\nDo ``ap:add <subreddit> <title> = <keywords1>, <keywords2>, etc.`` to add the keywords you want to follow from that subreddit. Ex: ``ap:add gamedeals GTA V = grand theft auto 5, gta v, gta 5``\nDo ``ap:list`` to see your current list.\nDo``ap:commands`` for more commands.')
            await bot.send_message(discord.Object(id=config["log_location"]), 'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))
    else:
        await bot.send_message(ctx.message.channel, 'You are **already subscribed** to the notifier. Do ``ap:list`` to see your current list. Do ``ap:commands`` to see other commands.')
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
        await bot.send_message(ctx.message.channel, 'You have unsubscribed from the reddit notifier feed. Use ``ap:follow`` to resubscribe if you\'d like. **Note: your list has been deleted** so if you subscribe again, you must remake your list.')
        await bot.send_message(discord.Object(id=config["log_location"]), 'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))
    else:
        await bot.send_message(ctx.message.channel, 'You are already unsubscribed from the notifier.')
    f.close()

@bot.command(pass_context=True)
async def location(ctx):
    if not isFollowing(ctx.message.author.id):
        await bot.send_message(ctx.message.channel, 'Use ``ap:follow`` first to subscribe to the bot. Do ``ap:commands`` for more help')
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
                    await bot.send_message(ctx.message.channel, 'Invalid location. Ex: ``ap:location dm`` Possible locations:\n``ap:location dm`` - Direct message you\n``ap:location here`` - This channel\n``ap:location #channel`` - Other channel on this server')
                    return
            f.seek(0)
            f.truncate()
            for i in content:
                f.write(i)
            f.close()
            await bot.send_message(ctx.message.channel, 'Successfully set location. Sent a test message to specified location.')
            await bot.send_message(discord.Object(id=config["log_location"]),
                                   'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))
            if bot.get_channel(content[1][16:].strip()):
                await bot.send_message(discord.Object(id=content[1][16:].strip()), 'This is where you will recieve notifications.')
            else:
                await bot.send_message(discord.User(id=content[1][16:].strip()), 'This is where you will recieve notifications.')
        except:
            traceback.print_exc()
            await bot.send_message(ctx.message.channel, 'Please specify a location. Ex: ``ap:location dm`` Possible locations:\n``ap:location dm`` - Direct message you\n``ap:location here`` - This channel\n``ap:location #channel`` - Other channel on this server')


@bot.command(pass_context=True)
async def on(ctx):
    if not isFollowing(ctx.message.author.id):
        await bot.send_message(ctx.message.channel, 'Use ``ap:follow`` first to subscribe to the bot. Do ``ap:commands`` for more help')
    else:
        f = open('%susers/user%s.txt' % (path, ctx.message.author.id), 'r+')
        content = f.read()
        if content.startswith('--disable--'):
            content = content[11:]
            f.seek(0)
            f.truncate()
            f.write(content)
        f.close()
        await bot.send_message(ctx.message.channel, 'Notifications have been enabled for you. Use ``ap:off`` to disable notifications.')
        await bot.send_message(discord.Object(id=config["log_location"]),
                               'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))

@bot.command(pass_context=True)
async def off(ctx):
    if not isFollowing(ctx.message.author.id):
        await bot.send_message(ctx.message.channel, 'Use ``ap:follow`` first to subscribe to the bot. Do ``ap:commands`` for more help')
    else:
        f = open('%susers/user%s.txt' % (path, ctx.message.author.id), 'r+')
        content = f.read()
        f.seek(0)
        if content.startswith('--disable--'):
            f.write(content)
        else:
            f.write('--disable--' + content)
        f.close()
        await bot.send_message(ctx.message.channel, 'Notifications have been disabled for you. Use ``ap:on`` to enable notifications.')
        await bot.send_message(discord.Object(id=config["log_location"]),
                               'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))


@bot.group(pass_context=True)
async def ping(ctx):
    if ctx.invoked_subcommand is None:
        await bot.send_message(ctx.message.channel, 'Command use: ``ap:ping off`` to disable pinging you on notifications. ``ap:ping on`` to enable. Make sure your location is not set to DM if you choose to disable pings.')
        return

@ping.command(pass_context=True)
async def on(ctx):
    if not isFollowing(ctx.message.author.id):
        await bot.send_message(ctx.message.channel, 'Use ``ap:follow`` first to subscribe to the bot. Do ``ap:commands`` for more help')
    else:
        f = open('%susers/user%s.txt' % (path, ctx.message.author.id), 'r+')
        content = f.read()
        f.seek(0)
        if content.startswith('--disable--off'):
            f.write('--disable--' + content[14:])
        elif content.startswith('off'):
            f.write(content[3:])
        else:
            f.write(content)
        f.close()
        await bot.send_message(ctx.message.channel, 'The bot will ping you on every message. Do ``ap:ping off`` to reverse this.')
        await bot.send_message(discord.Object(id=config["log_location"]),
                               'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))

@ping.command(pass_context=True)
async def off(ctx):
    if not isFollowing(ctx.message.author.id):
        await bot.send_message(ctx.message.channel, 'Use ``ap:follow`` first to subscribe to the bot. Do ``ap:commands`` for more help')
    else:
        f = open('%susers/user%s.txt' % (path, ctx.message.author.id), 'r+')
        content = f.read()
        f.seek(0)
        if content.startswith('--disable--off'):
            f.write(content)
        elif content.startswith('off'):
            f.write(content)
        elif content.startswith('--disable--'):
            f.write('--disable--off' + content[11:])
        else:
            f.write('off' + content)
        f.close()
        await bot.send_message(ctx.message.channel, 'The bot will no longer ping you on every message. Do ``ap:ping on`` to reverse this.')
        await bot.send_message(discord.Object(id=config["log_location"]),
                               'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))


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
                await bot.send_message(ctx.message.channel, '**%s\'s list:**' % str(toFollow))
                toFollow = toFollow.id
            except IndexError:
                server = ctx.message.server
                try:
                    toFollow = discord.Server.get_member_named(server, sub).id
                    temp = await bot.get_user_info(toFollow)
                except:
                    await bot.send_message(ctx.message.channel, 'Could not find the user\'s list. They might not be subscribed.')
                    return
                await bot.send_message(ctx.message.channel, '**%s\'s list:**' % temp)
        except Exception as e:
            traceback.print_exc()
            if e == IndexError:
                await bot.send_message(ctx.message.channel, 'Not a valid argument. Example use: ``ap:follow`` or ``ap:follow appu1232#2569`` (You don\'t need to tag them)' % toFollow)
            else:
                await bot.send_message(ctx.message.channel, 'Could not find the user\'s list. They might not be subscribed.')
                return
        list = listKeyWords(str(toFollow))
        await bot.send_message(discord.Object(id=config["log_location"]), 'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))
        if len(list) > 2:
            await bot.send_message(ctx.message.channel, 'List is very large. Sending via DM so chat doesn\'t get cluttered.')
            for i in list:
                await bot.send_message(discord.User(id=ctx.message.author.id), '```%s```' % i)
        else:
            for i in list:
                await bot.send_message(ctx.message.channel, '```%s```' % i)

    else:
        if ctx.message.author.id not in users:
            await bot.send_message(ctx.message.channel, 'You are not subscribed to the notifier. Do ``ap:follow`` to subscribe and start adding subreddits to follow.')
        else:
            list = listKeyWords(ctx.message.author.id)
            await bot.send_message(discord.Object(id=config["log_location"]), 'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))
            if len(list) > 2:
                await bot.send_message(ctx.message.channel, 'List is very large. Sending via DM so chat doesn\'t get cluttered.')
                for i in list:
                    await bot.send_message(discord.User(id=ctx.message.author.id), '```%s```' % i)
            else:
                for i in list:
                    await bot.send_message(ctx.message.channel, '```%s```' % i)

@bot.command(pass_context=True)
async def add(ctx):
    if not isFollowing(ctx.message.author.id):
        await bot.send_message(ctx.message.channel, 'Use ``ap:follow`` first to subscribe to the bot. Do ``ap:commands`` for more help')
    else:
        msg = '**Error** Something went wrong. Are you using the command right? Example uses: ``ap:add manga One Piece`` or ``ap:add manga Kaguya Wants to Be Confessed to = Kaguya wants, kaguya-sama wants`` or ``ap:add -u anime One Punch Man S2 = opm s2, opm season 2, one punch man season 2``'
        try:
            toFollow = ctx.message.content.split('ap:add')[1].strip()
            status = addKeyWords(toFollow, ctx.message.author.id)
            if status == True:
                await bot.send_message(ctx.message.channel, 'Successfully added ``%s`` to ``%s``. View your list with ``ap:list``.' % (toFollow.split(' ', 1)[1].strip(), toFollow.split(' ', 1)[0].strip()))
                await bot.send_message(discord.Object(id=config["log_location"]),
                                       'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))
            elif status != '--blacklistempty--' and status != False:
                await bot.send_message(ctx.message.channel,
                                       'Successfully set blacklist to ``%s``. View your list with ``ap:list``.' % status)
                await bot.send_message(discord.Object(id=config["log_location"]),
                                       'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))
            elif status == '--blacklistempty--':
                await bot.send_message(ctx.message.channel,
                                       'Successfully removed all words from blacklist. View your list with ``ap:list``.')
                await bot.send_message(discord.Object(id=config["log_location"]),
                                       'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))
            else:
                await bot.send_message(ctx.message.channel, msg)
        except Exception as e:
            traceback.print_exc()
            await bot.send_message(ctx.message.channel, msg)

@bot.command(pass_context=True)
async def remove(ctx):
    msg = '**Error** Something went wrong. Are you using the command right? Example use: ``ap:remove anime One Punch Man S2``'
    try:
        toUnfollow = ctx.message.content.split('ap:remove')[1].strip()
        status = removeKeyWords(toUnfollow, ctx.message.author.id)
        if status == True:
            await bot.send_message(ctx.message.channel, 'Successfully removed ``%s`` from ``%s``. View your list with ``ap:list``.' % (toUnfollow.split(' ', 1)[1].strip(), toUnfollow.split(' ', 1)[0].strip()))
            await bot.send_message(discord.Object(id=config["log_location"]),
                                   'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))
        elif status == 'blacklist':
            await bot.send_message(ctx.message.channel,
                                   'Successfully removed all words from blacklist. View your list with ``ap:list``.')
            await bot.send_message(discord.Object(id=config["log_location"]),
                                   'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))
        else:
            await bot.send_message(ctx.message.channel, msg)
    except Exception as e:
        traceback.print_exc()
        await bot.send_message(ctx.message.channel, msg)

@bot.command(pass_context=True)
async def edit(ctx):
    msg = '**Error** Something went wrong. Are you using the command right? Example use: ``ap:edit anime One Punch Man S2 = opm s2, one punch man s2`` to replace entire entry. Add a ``+`` or ``-`` after ``edit`` to just add or remove some keywords from entry.'
    sub = ctx.message.content.split('edit', 1)[1].strip()
    if sub:
        try:
            entry = editEntry(sub, ctx.message.author.id)
            if '=' in entry:
                await bot.send_message(ctx.message.channel, 'Successfully edited entry. Entry is now: %s. View your list with ``ap:list``.' % entry)
                await bot.send_message(discord.Object(id=config["log_location"]),
                                       'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))
            else:
                await bot.send_message(ctx.message.channel, '**Could not find the specified entry.**')
                await bot.send_message(discord.Object(id=config["log_location"]),
                                       'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))
        except:
            await bot.send_message(ctx.message.channel, '**Error** Something went wrong. Are you using the command right? Example uses: ``ap:edit + manga Boku no Hero`` For changing notifications to all threads (``-`` for episode/chapters only) or ``ap:edit manga Boku no Hero = my hero academia, boku no hero academia`` to change the entry values.')
            traceback.print_exc()

    else:
        await bot.send_message(ctx.message.channel, msg)

@bot.command(pass_context=True)
async def addsubreddit(ctx):
    msg = '**Error** Something went wrong. Are you using the command right? Example use: ``ap:addsubreddit gamedeals``.'
    sub = ctx.message.content.split('addsubreddit', 1)[1].strip()
    if sub:
        if sub.startswith('-all'):
            sub = sub.split('-all')[1].strip()
            allposts = True
        else:
            allposts = False
        if subredditExists(sub, ctx.message.author.id):
            await bot.send_message(ctx.message.channel, '**You already have this subreddit in your list** Go ahead and add stuff to this subreddit by doing ``ap:add %s name = keyword1, keyword2`` Do ``ap:commands`` for more info.' % sub)
        else:
            try:
                r = praw.Reddit(client_id=config["reddit_client_id"],
                                client_secret=config["reddit_client_secret"],
                                password=config["reddit_password"],
                                user_agent="Discord bot for Reddit related submissions by appu1232",
                                username=config["reddit_username"])
                subreddit = r.subreddit(sub.lower())
                for submission in subreddit.new(limit=2):
                    pass
                userData = open('%susers/user%s.txt' % (path, ctx.message.author.id), 'r+')
                data = userData.readlines()
                totalSubs = 0
                for i in data:
                    if '----' in i:
                        totalSubs += 1
                if totalSubs > 22:
                    await bot.send_message(ctx.message.channel, 'Sorry, you have reached your subreddit limit of 20! D: The notifier will slow down considerably without a hard cap on number of subreddits so please delete a subreddit and try again.')
                    return
                userData.seek(0)
                userData.truncate()
                if allposts == True:
                    data[len(data) - 2] = '\n----%s----' % sub.lower() + '\n' + '[ALL POSTS FROM THIS SUB]' + '\n' + data[len(data) - 2]
                else:
                    data[len(data)-2] = '\n----%s----' % sub.lower() + '\n' + data[len(data)-2]
                userData.writelines(data)
                userData.close()
                await bot.send_message(ctx.message.channel, 'Successfully added subreddit ``%s`` to your list. Now start adding keywords to it. View your list with ``ap:list`` and view all the commands with detailed info with ``ap:commands``' % sub)
                await bot.send_message(discord.Object(id=config["log_location"]),
                                       'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))
            except:
                await bot.send_message(ctx.message.channel, '**Invalid subreddit.** reddit.com/r/%s doesn\'t seem to exist or is a private sub.' % sub)
    else:
        await bot.send_message(ctx.message.channel, msg)

@bot.command(pass_context=True)
async def removesubreddit(ctx):
    msg = '**Error** Something went wrong. Are you using the command right? Example use: ``ap:removesubreddit gamedeals``.'
    sub = ctx.message.content.split('removesubreddit', 1)[1].strip()
    if sub:
        if subredditExists(sub, ctx.message.author.id):
            userData = open('%susers/user%s.txt' % (path, ctx.message.author.id), 'r+')
            data = userData.readlines()
            for i, d in enumerate(data):
                if '----%s----' % sub.lower() in d.lower() and '----Blacklist----' not in d and '----End----' not in d:
                    c = 0
                    data[i] = ''
                    while data[i+c] != '\n':
                        data[i + c] = ''
                        c += 1
                    data[i+c] = ''
            userData.seek(0)
            userData.truncate()
            userData.writelines(data)
            userData.close()
            await bot.send_message(ctx.message.channel, 'Successfully removed subreddit ``%s`` from your list.' % sub)
            await bot.send_message(discord.Object(id=config["log_location"]),
                                   'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))
        else:
            await bot.send_message(ctx.message.channel, '**Could not find the subreddit ``%s`` in your list** View your list with ``ap:list`` to see what subreddits are there.' % sub)

    else:
        await bot.send_message(ctx.message.channel, msg)

@bot.command(pass_context=True)
async def addmal(ctx):
    sub = ctx.message.content.split('addmal', 1)[1].strip().lower()
    try:
        if sub:
            if isFollowing(ctx.message.author.id):
                if sub.startswith('anime'):
                    if subredditExists('anime', ctx.message.author.id):
                        maluser = sub.split('anime')[1].strip()
                        await bot.send_message(ctx.message.channel, 'Fetching your MAL currently watching entries... This may take a minute or two, I\'ll ping you when I\'m done. :)')
                        await malImport('anime', ctx.message.author.id, maluser)
                        await bot.send_message(ctx.message.channel, '%s Successfully imported your watching anime from your MAL. View your list with ``ap:list``' % ctx.message.author.mention)
                        await bot.send_message(discord.Object(id=config["log_location"]),
                                               'User: ' + str(ctx.message.author) + '\nCmd: ' + str(
                                                   ctx.message.content))
                    else:
                        await bot.send_message(ctx.message.channel, '**Error, you don\'t seem to have the anime subreddit in your list. Add it with ``ap:addsubreddit anime`` and try again.')
                    pass
                elif sub.startswith('manga'):
                    if subredditExists('manga', ctx.message.author.id):
                        maluser = sub.split('manga')[1].strip()
                        await bot.send_message(ctx.message.channel, 'Fetching your MAL currently reading entries... This may take a minute or two, I\'ll ping you when I\'m done. :)')
                        await malImport('manga', ctx.message.author.id, maluser)
                        await bot.send_message(ctx.message.channel, '%s Successfully imported your watching manga from your MAL. View your list with ``ap:list``' % ctx.message.author.mention)
                        await bot.send_message(discord.Object(id=config["log_location"]),
                                               'User: ' + str(ctx.message.author) + '\nCmd: ' + str(
                                                   ctx.message.content))
                    else:
                        await bot.send_message(ctx.message.channel, '**Error, you don\'t seem to have the manga subreddit in your list. Add it with ``ap:addsubreddit manga`` and try again.')
                else:
                    await bot.send_message(ctx.message.channel, '**Error, invalid syntax. Example use: ``ap:addmal manga appu1232``.')
            else:
                await bot.send_message(ctx.message.channel, 'Use ``ap:follow`` first to subscribe to the bot. Do ``ap:commands`` for more help')
        else:
            await bot.send_message(ctx.message.channel, '**Error, invalid syntax. Example use: ``ap:addmal manga appu1232``.')


    except:
        traceback.print_exc()
        await bot.send_message(ctx.message.channel, '**Error** Something went wrong. Are you using the command right? Example use: ``ap:addmal appu1232`` for both anime and manga or ``ap:addmal anime appu1232`` or ``ap:addmal manga appu1232`` for anime or manga only respectively.')

@bot.command(pass_context=True)
async def commands(ctx):
    await bot.send_message(ctx.message.channel, 'I\'ve sent you the list of commands via direct message.')
    await bot.send_message(discord.User(id=ctx.message.author.id), '\n**Bot commands:**\n\n**__START HERE:__ CREATE A LIST**\n\n``ap:follow`` or ``ap:follow <user>`` - Subscribe to the bot. This means you can start adding and removing subreddits and keywords for those subreddits. Optionally, put a person username (doesn\'t have to be a mention) to import their list.\n\n``ap:unfollow`` - Unsubscribe from the bot. Warning: this deletes your list.\n\n\n**GET YOUR CURRENT LIST** (will be empty if you just did ap:follow)\n\n``ap:list`` or ``ap:list <user>`` - Get your current keywords list or seomeone else\'s.\n\n\n**ADD OR REMOVE SUBREDDITS FROM YOUR LIST**\n\n``ap:addsubreddit <subreddit>`` - Add a subreddit to your list. Ex: ``ap:addsubreddit worldnews`` **IF you want to get notified on every new post made, do ``ap:addsubreddit -all <subreddit>``**\n\n``ap:removesubreddit <subreddit>`` - Remove a subreddit from your list.\n\n**ADD SPECIFIC KEYWORDS TO FOLLOW FROM A SUBREDDIT**\n\n**For all subreddits:**\n``ap:add <subreddit> <title>`` or ``ap:add <subreddit> <title> = <keywords1>, <keywords2>, ...`` - Add a topic to follow. <title> can be anything (if no keywords given then the title will be used as keywords). Add keywords to specify more in case you think it could be posted under different titles (like GTA V vs. Grand Theft Auto V or Boku no Hero Academia vs. My Hero Academia).\n\n**For the anime and manga subreddits specifically:**\nUsing the ``-u`` flag gives allows you to **only get notifications for your topic’s new episode/new manga chapter.** Leave it out to receive all related threads like normal. Ex: ``ap:add -u anime Little Witch Academia``.\n\n**IMPORT YOUR MAL CURRENTLY WATCHING/READING TITLES TO FOLLOW**')
    await bot.send_message(discord.User(id=ctx.message.author.id), '``ap:addmal <anime/manga> <malusername>`` - This will import the airing/publishing anime/manga from your currently watching or currently reading list (based on if you put anime or manga). The entries keywords should be compatible with the episode/chapter threads of Reddit but **if the entry has multiple names you should add it to the entries keywords using ap:edit.** Example use: ``ap:addmal manga appu1232`` **Note that all imported anime and manga are set to [Chapters Only].** If needed, you can change an entry to [All Threads] using the ap:edit command (see below). \n\n\n**REMOVING STUFF YOU FOLLOW**\n\n``ap:remove <subreddit> <title>`` - Remove the specified title in the subreddit. Ex: ``ap:remove anime Hunter x Hunter``\n\n``ap:edit <subreddit> <title> = <keyword1>, <keyword2>, ...`` to edit an entry or ``ap:edit +/- <anime/manga> <title>`` to set/unset anime/manga title to notify for all threads. Example uses: ``ap:edit + manga Boku no Hero`` or ``ap:edit manga Boku no Hero = my hero academia, boku no hero academia``\n\n\n** BLACKLIST WORDS YOU DON\'T WANT** (i.e. if you have added "fanart" to your list but you don\'t want fanart of a certain character, you would blacklist that character\'s name)\n\n``ap:add blacklist = <word1>, <word2>, ...`` - Add words to your blacklist. Example: ``ap:add blacklist = rem, yuno``\n\n``ap:remove blacklist`` - Remove all words from blacklist.\n\n\n**SET WHERE YOU WANT TO RECIEVE NOTIFICATIONS**\n\n``ap:location <dm/channel>`` - Where to get notifications. ``dm`` for direct message, ``here`` for current channel or ``#channel_name`` for another channel. Default after you follow is ``dm``\n\n\n**TURN NOTIFIER ON AND OFF**\n\n``ap:off`` - Turn off all notifications for you. Useful if you want to stop notifications temporarily but don\'t want to delete your list.\n\n``ap:on`` - Turn on notifications if off.\n\n\n**OTHER**\n\n``ap:info`` - Get bot info and current settings.')
    await bot.send_message(discord.Object(id=config["log_location"]), 'User: ' + str(ctx.message.author) + '\nCmd: ' + str(ctx.message.content))

@bot.command(pass_context=True)
async def info(ctx):
    run = run = open('current_run.txt', 'r')
    info = run.readlines()
    await bot.send_message(ctx.message.channel, currentRun(info[0], info[1], info[2], info[3]))

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
    currRun = '```Bot has been running for: %s days, %s hours, %s minutes, and %s seconds\n\nLinks checked: %s\nHits: %s\nNotifications sent: %s\nItterations without fail: %s```' % (int(days), int(hours), int(minutes), int(seconds), allcheck, hits, notifssent, loops)
    return currRun

def subredditExists(word, user):
    userData = open('%susers/user%s.txt' % (path, user), 'r')
    data = userData.readlines()
    userData.close()
    word = '----' + word.lower()
    for i in data:
        if word in i.lower():
            return True
    return False

async def malImport(word, user, malUser):
    creds = spice.init_auth(config["mal_username"], config["mal_password"])
    try:
        anime_list = spice.get_list(spice.get_medium(word), malUser, creds)
        allList = anime_list.get_status(1)
        allwatch = []
        for i in allList:
            result = spice.search_id(i, spice.get_medium(word), creds)
            await asyncio.sleep(2)
            if result.status == 'Publishing' or result.status == 'Currently Airing':
                if result.title != '' and result.english != '' and result.title != result.english:
                    allwatch.append(result.title + ' = ' + result.title + ', ' + result.english)
                else:
                    allwatch.append(result.title)
        for title in allwatch:
            addKeyWords('-u ' + word + ' ' + title, user)
        return True
    except:
        pass

def editEntry(word, user):
    title = ''
    keys = ''
    if word.startswith('+'):
            mode = 0
            aorm = word.split(' ', 2)[1].strip()
            title = word.split(' ', 2)[2].strip()
    elif word.startswith('-'):
            mode = 1
            aorm = word.split(' ', 2)[1].strip()
            title = word.split(' ', 2)[2].strip()
    else:
        mode = 2
        aorm = word.split(' ', 1)[0].strip()
        title = word.split(' ', 1)[1].strip()
    if '=' not in title:
        title2 = title.strip()
        keys = title.lower().strip()
    else:
        title2 = title.split('=', 1)[0].strip()
        keys = title.split('=', 1)[1].lower().strip()
    if keys.endswith(','):
        keys = keys[:-1]
    userData = open('%susers/user%s.txt' % (path, user), 'rU')
    data = userData.readlines()
    userData.close()
    entry = '##noentryfound##'
    for i, d in enumerate(data):
        if '----' in d:
            if aorm.lower() in d.lower():
                c = 0
                while title2.lower().strip() + ' = ' not in data[i + c].lower():
                    c += 1
                if aorm.lower() == 'anime' or aorm.lower() == 'manga':
                    if mode == 0:
                        if data[i + c].startswith('[Episodes Only]') or data[i + c].startswith('[Chapters Only]'):
                            data[i + c] = '[All Threads] ' + data[i + c][16:]
                        entry = '``%s``' % data[i + c].strip()
                    if mode == 1:
                        if data[i + c].startswith('[All Threads]'):
                            if aorm.lower() == 'anime':
                                data[i + c] = '[Episodes Only] ' + data[i + c][14:]
                                entry = '``%s``' % data[i + c].strip()
                            else:
                                data[i + c] = '[Chapters Only] ' + data[i + c][14:]
                                entry = '``%s``' % data[i + c].strip()
                        else:
                            entry = '``%s``' % data[i + c].strip()
                else:
                    mode = 2
                if mode == 2:
                    data[i + c] = data[i + c].split(' = ')[0] + ' = ' + keys + '\n'
                    entry = '``%s``' % data[i + c].strip()
            userData = open('%susers/user%s.txt' % (path, user), 'w')
            userData.writelines(data)
            userData.close()
    return entry


def listKeyWords(msg):
    userData = open('%susers/user%s.txt' % (path, msg), 'rU')
    msg = ''
    userData.readline()
    userData.readline()
    userList = userData.read()
    part = int(math.ceil(len(userList) / 1900))
    splitList = [userList[i:i+1900] for i in range(0, len(userList), 1900)]
    allWords = []
    for i,blocks in enumerate(splitList):
        msg += 'List of keywords: %s of %s\n' % (i+1, part)
        for b in blocks.split('\n'):
            msg += b + '\n'
        allWords.append(msg)
        msg = ''
    userData.close()
    return allWords

def addKeyWords(word, user):
    title = ''
    keys = ''
    if word.lower().startswith('blacklist'):
        if '=' in word:
            blacklist = word.split(' = ')[1].lower().strip().rstrip(',')
            status = blacklist
        else:
            blacklist = ''
            status = '--blacklistempty--'
        userlist = open('%susers/user%s.txt' % (path, user), 'r+')
        data = userlist.readlines()
        data[3] = blacklist + '\n'
        userlist.seek(0)
        userlist.truncate()
        userlist.writelines(data)
        userlist.close()
        return status
    else:
        if word.split(' ', 1)[0].strip() == '-u':
            aorm = word.split(' ', 2)[1].strip()
            title = word.split(' ', 2)[2].strip()
            allthreads = False
        elif not subredditExists(word.split(' ', 1)[0].strip(), user):
            return False
        else:
            aorm = word.split(' ', 1)[0].strip()
            title = word.split(' ', 1)[1].strip()
            allthreads = True
        if '=' not in title:
            title2 = title.strip()
            keys = title.lower().strip()
        else:
            title2 = title.split('=', 1)[0].strip()
            keys = title.split('=', 1)[1].lower().strip()
        keys = keys.rstrip(',')
        userData = open('%susers/user%s.txt' % (path, user), 'rU')
        data = userData.readlines()
        userData.close()
        if title2 == '' or keys == '':
            return False
        for i,d in enumerate(data):
            if '----' in d:
                if aorm.lower() in d.lower():
                    c = 0
                    while data[i+c] != '\n':
                        c += 1
                    if aorm.lower() == 'anime' or aorm.lower() == 'manga':
                        if allthreads:
                            title2 = '[All Threads] ' + title2
                        else:
                            if aorm.lower() == 'anime':
                                title2 = '[Episodes Only] ' + title2
                            else:
                                title2 = '[Chapters Only] ' + title2
                    data[i+c] = title2 + ' = ' + keys + '\n' + data[i+c]
                    userData = open('%susers/user%s.txt' % (path, user), 'w')
                    userData.writelines(data)
                    userData.close()
                    return True
    return False

def removeKeyWords(word, user):
    if word.startswith('blacklist'):
        userlist = open('%susers/user%s.txt' % (path, user), 'r+')
        data = userlist.readlines()
        data[3] = '\n'
        userlist.seek(0)
        userlist.truncate()
        userlist.writelines(data)
        userlist.close()
        return 'blacklist'
    userData = open('%susers/user%s.txt' % (path, user), 'r')
    aorm = word.split(' ', 1)[0].strip()
    title = word.split(' ', 1)[1].strip()
    data = userData.readlines()
    userData.close()
    for i,d in enumerate(data):
        if '----' in d:
            if aorm.lower() in d.lower():
                c = 0
                line = '----End----'
                while title.lower().strip() != line:
                    c += 1
                    if aorm.lower() == 'anime' or aorm.lower() == 'manga':
                        if data[i+c].startswith('[All Threads]'):
                            line = data[i+c][14:].lower().split(' = ', 1)[0].strip()
                        elif data[i+c].startswith('[Episodes Only]') or data[i+c].startswith('[Chapters Only]'):
                            line = data[i+c][16:].lower().split(' = ', 1)[0].strip()
                    else:
                        line = data[i + c].lower().split(' = ', 1)[0].strip()
                data[i+c] = ''
                userData = open('%susers/user%s.txt' % (path, user), 'w')
                userData.truncate()
                userData.writelines(data)
                userData.close()
                return True
    userData.close()
    return False

async def checker():
    loopCount = 0
    allcheckcount = 0
    hits = 0
    notifssent = 0
    failCount = 0
    userFollows = {}

    while True:
        try:
            with(open('config.json', 'r')) as f:
                config = json.load(f)
            if failCount > 5:
                await asyncio.sleep(30)
            #traceback.print_exc()
            r = praw.Reddit(client_id=config["reddit_client_id"],
                                 client_secret=config["reddit_client_secret"],
                                 password=config["reddit_password"],
                                 user_agent="Discord bot for Reddit related submissions by appu1232",
                                 username=config["reddit_username"])
            while True:
                checked = []
                loopCount += 1
                userFollows.clear()
                try:
                    checkList = open('checked.txt', 'r')
                    info = checkList.read()
                    for i in info.split(','):
                        checked.append(i)
                    checkList.close()
                    checked.remove(checked[len(checked) - 1])
                except:
                    pass
                for users in os.listdir('users'):
                    blacklist = []
                    allSubreddits = {}
                    subreddit = {}
                    if users == 'allusers.txt':
                        continue
                    with open('%susers/%s' % (path, users), 'r') as stuff:
                        str1 = stuff.readline()
                        if '--disable--' in str1:
                            continue
                        if str1.startswith('off'):
                            ping = False
                            str1 = str1[3:]
                        else:
                            ping = True
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
                            if '----' in str1 and '----Blacklist---' not in str1 and '----End----' not in str1:
                                sub = str1.strip().lower()[4:][:-4]
                                keyWords = {}
                                while str1 != '':
                                    str1 = stuff.readline()
                                    if '[ALL POSTS FROM THIS SUB]' in str1:
                                        keyWords['New'] = ['####allposts####']
                                        break
                                    str2 = str1.strip().split(' = ', 1)
                                    if str2[0] == '':
                                        break
                                    temp = []
                                    if ',' in str2[1]:
                                        lstr2 = str2[1].lstrip().split(',')
                                        for word in lstr2:
                                            temp.append(word.strip())
                                        keyWords[str2[0]] = temp
                                    else:
                                        temp.append(str2[1].lstrip())
                                        keyWords[str2[0]] = temp
                                subreddit[sub] = keyWords
                                allSubreddits[sub] = subreddit
                                subreddit = {}
                    userFollows[currUser] = [allSubreddits, notif, blacklist, ping]
                msg = ''
                checkSubs = []
                for eachUser in userFollows.items():
                    for allTemp in eachUser[1][0].items():
                        checkSubs.append(allTemp[0])
                if len(checked) >= 8000 * ((len(checkSubs) // 2) + 1):
                    checked = checked[4000 * ((len(checkSubs) // 2) + 1):]
                for count, eachSub in enumerate(checkSubs):
                    links = r.subreddit(eachSub)
                    for submission in links.new(limit=8):
                        if submission.id in checked:
                            continue
                        op_title = submission.title.lower()
                        wordInTitle = op_title.split(' ')
                        wordInTitle = [x for x in wordInTitle if x != '']
                        allcheckcount += 1
                        alertUsers = {}
                        for eachUser in userFollows.items():
                            if eachUser[1][2] != ['']:
                                blacklist_words = any(string in wordInTitle for string in eachUser[1][2])
                            else:
                                blacklist_words = False
                            if eachSub not in eachUser[1][0]:
                                continue
                            for sub in eachUser[1][0][eachSub][eachSub].items():
                                if '####allposts####' in sub[1]:
                                    allPosts = True
                                else:
                                    allPosts = False
                                for i in sub[1]:
                                    if ' ' in i.strip():
                                        key_words = any(string in op_title for string in sub[1])
                                        if key_words == True:
                                            break
                                    else:
                                        key_words = any(string in wordInTitle for string in sub[1])
                                        if key_words == True:
                                            break
                                updateType = True
                                if eachSub == 'anime':
                                    aorm = 0
                                elif eachSub == 'manga':
                                    aorm = 1
                                else:
                                    aorm = 2
                                title = sub[0]
                                if aorm != 2:
                                    if not sub[0].startswith('[All Threads] '):
                                        if aorm == 0:
                                            if '[Spoilers] ' not in submission.title and 'discussion' not in op_title:
                                                updateType = False
                                            title = sub[0][16:]
                                        elif aorm == 1:
                                            if '[DISC]' not in submission.title:
                                                updateType = False
                                            title = sub[0][16:]
                                    else:
                                        title = sub[0][14:]
                                if submission.id not in checked and (key_words or allPosts) and not blacklist_words:
                                    if updateType:
                                        if eachUser:
                                            if eachUser[1][1] in alertUsers.keys():
                                                temp = alertUsers[eachUser[1][1]]
                                                temp.append(eachUser[0].strip())
                                                alertUsers[eachUser[1][1]] = temp
                                            else:
                                                alertUsers[eachUser[1][1]] = [eachUser[0].strip()]
                                            if allPosts == False:
                                                msg = '\n%s related thread: "%s"\n%s in %s' % (title, (submission.title[:400] + '..') if len(submission.title) > 400 else submission.title, submission.shortlink, '/r/' + eachSub)
                                            else:
                                                msg = '\n%s thread: "%s"\n%s in %s' % (title, (
                                                submission.title[:400] + '..') if len(
                                                    submission.title) > 400 else submission.title, submission.shortlink,
                                                                                               '/r/' + eachSub)
                                            allPosts = False
                                            notifssent += 1
                        allmentions = ''
                        checked.append(submission.id)
                        if alertUsers:
                            totalmentions = ''
                            for i in alertUsers.keys():
                                if bot.get_channel(i):
                                    for j in alertUsers[i]:
                                        temp = await bot.get_user_info(j)
                                        totalmentions += str(temp) + ' '
                                        if userFollows[j][3]:
                                            allmentions += temp.mention + ' '
                                    try:
                                        await bot.send_message(discord.Object(id=i), allmentions + msg)
                                    except:
                                        pass
                                    allmentions = ''
                                else:
                                    try:
                                        await bot.send_message(discord.User(id=i), msg)
                                    except:
                                        pass
                            hits += 1
                            try:
                                await bot.send_message(discord.Object(id=config["log_location"]), 'Users: %s \n%s' % (totalmentions, msg))
                            except:
                                pass
                    if count % 2 == 0:
                        await asyncio.sleep(1)
                run = open('current_run.txt', 'w')
                run.truncate()
                run.write(str(allcheckcount) + '\n' + str(hits) + '\n' + str(notifssent) + '\n' + str(loopCount))
                run.close()
                checkList = open('checked.txt', 'w')
                checkList.truncate()
                for i in checked:
                    checkList.write(i + ',')
                checkList.close()
                await asyncio.sleep(20)
            failCount = 0
        except Exception as e:
            traceback.print_exc()
            loopCount = 0
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
    task = bot.loop.create_task(on_ready())
except Exception as e:
    task.cancel()
    raise e

bot.run(config["bot_token"])
