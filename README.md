**Outdated. Need to rework.**

# Reddit Notifier Discord Bot

A discord bot that notifies users when a thread with certain keywords is posted in a subreddit they are following. Each user gets an empty list where they can add subreddits to follow and specify what keywords to look for in each subreddit.

## Features:

- Anime and Manga support: You can specify to follow only anime episode and manga chapter updates from /r/anime and /r/manga. Also can import currently watching/reading list from [MyAnimeList.](https://myanimelist.net/)
- Set multiple keywords for each topic in a subreddit. Ex: in subreddit /r/gamedeals, look for GTA V or Grand Theft Auto V and notify me when a thread is posted with these words.
- Blacklist words you don't want even if the thread has keywords. Ex: If you want all posts with the word "nintendo" in /r/games but don't want any with the words "mario" you would add nintendo as a keyword for /r/games and then blacklist the word "mario".
- Option to recieve notifications on all new posts on a subreddit.
- Set where to recieve notifications. Default to direct messages but can be set to a certain channel if you so choose.

## Running the bot:

Python 3.5.2 or higher is required to run this bot. I am fine with hosting the bot and just inviting my instance to other servers but if someone wants to, they can create their own instance of the bot. The config.json file (the values are empty for the one on here) can be configured. You will need a [reddit app](https://www.reddit.com/prefs/apps/) api token/secret and client id, a [discord bot](https://discordapp.com/developers/applications/me) token/secret and client id, and a myanimelist username and password (just to log in and search mal, you can give your MAL account for this). The `log_location` is the channel id where you want to see all the commands used on the bot. Set your discord to developer mode and right click on the channel > copy id to get the id.

* conf.json:

```json
{
	"path": "",
	"bot_token": "",
	"log_location": "",
	"reddit_client_id": "",
	"reddit_client_secret": "",
	"reddit_username": "",
	"reddit_password": "",
	"mal_username": "",
	"mal_password": ""
}
```

Run the bot with ``python loopappu.py``. Additionally, this lets the bot auto-restart if it ever crashes. ``python appudiscordbot.py`` will aso work but the bot will not auto-restart.

## First step:

* No one has a list by default. In order to make a list, a user must do `ap:follow` or `ap:follow <discorduser>` to import that discord user's list.
* `ap:unfollow` to stop recieving all notifications and delete your list.

## View list:

* `ap:list` - View your list of subreddits and keywords.
* `ap:list <discorduser>` - View someone else's list. You do not need to tag the person; you can just put their username (not nickname) if you don't want to bother them.

## Add/Remove subreddits:

* `ap:addsubreddit <subreddit>` - Adds the subreddit to the list (no keywords specified so this does nothing until you add keywords to the subreddit).
* `ap:addsubreddit -all <subreddit>` - Recieve notifications for all new posts in a subreddit instead of specifying keywords.
* `ap:removesubreddit <subreddit>` - Remove the subreddit from your list.

## Add/Remove keywords from a subreddit:

* `ap:add <subreddit> <title>` or `ap:add <subreddit> <title> = <keywords1>, <keywords2>, ...` - The keywords specified for `<title>` will compared against every new post in `<subreddit>` and upon a match, will send a notification to you on discord. If no keywords are given (like the first example), `<title>` is used as the keyword. Strongly recommended to have multiple sets of keywords instead like the second example. This is useful if a title has different names. For example, to cover GTA V in /r/gamedeals, you would want to do: `ap:add gamedeals GTA V = gta v, grand theft auto v`.
* `ap:edit <subreddit> <title> = <keywords1>, <keywords2>, ...` = Edit an entry in your list.
* `ap:remove <subreddit> <title>` - Remove the entry from the subreddit in your list.

## For Anime and Manga Subreddits Only:

* `ap:add -u <subreddit> <title> = <keywords1>, <keywords2>, ...` - gives you notifications only on new episode/chapter updates for the specified title + keywords in the anime or manga subreddit.
* `ap:addmal anime <myanimelist username>` or `ap:addmal manga <myanimelist username>` - import your currently watching anime list or currently reading manga list from your myanimelist account.
* `ap:edit + <subreddit> <title>` - Change the entry to support all thread notifications instead of just new episode/chapter updates.
* `ap:edit - <subreddit> <title>` - Change the entry to episode/chapter updates only.

## Set Words to Blacklist:

* `ap:add blacklist = <keywords1>, <keywords2>, ...` - Set words to the blacklist. If a post matches a keyword in your list but also matches a word in the blacklist, the notification will not be sent. Note: the blacklist is for all subreddits, you cannot specify different blacklists for each subreddit (may be added in the future).
* `ap:remove blacklist` - Removes all words from your blacklist.

## Set location of notifications:

* `ap:location dm` or `ap:location here` or `ap:location <#channel_name>` - Set the location where you want the bot to message you. When you first follow, it is defaulted to `dm` (direct messages). If you set it to a channel, it will mention you when it posts in that channel.

## Turn Notifier on/off:

* `ap:off` - Turn off notifications. Useful if you want to stop notifications and plan to turn it on again but don't want to delete your current list.
* `ap:on` - Turn on notifications if off.

## Command info:

* `ap:commands` - Get all commands and info for each command.


That's it! If you have any questions/suggestions or just need some help running/using the bot, you can message me on discord as appu1232#2569, on reddit as /u/appu1232, or on MyAnimeList as appu1232 (see a pattern?). I will try to get back to you as soon as I can. Thanks and hope you find this bot useful too! :)
