import subprocess, traceback

while True:
    try:
        p = subprocess.call(['python', 'appudiscordbot.py'])
    except:
        traceback.print_exc()