import subprocess, traceback

while True:
    try:
        p = subprocess.call(['python3', 'appudiscordbot.py'])
    except (SyntaxError, FileNotFoundError):
        p = subprocess.call(['python', 'appudiscordbot.py'])
    except:
        traceback.print_exc()
