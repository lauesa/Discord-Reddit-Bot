import time
import math
from appudiscordbot import start_time

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