import os,subprocess,logging
log = logging.getLogger(__name__)
while True:
    systray = subprocess.Popen(["pip","install","infi.systray"])
    systray.wait()
    stdout,stderr = systray.communicate()
    if stderr:
        cont += 1
        if cont >= 5:
            log.critical("Failed to install infi.systray in 5 attempts.")
            exit()
    else:
        break
while True:
    systray = subprocess.Popen(["pip","install","youtube_dl"])
    systray.wait()
    stdout,stderr = systray.communicate()
    if stderr:
        cont += 1
        if cont >= 5:
            log.critical("Failed to install youtube_dl in 5 attempts.")
            exit()
    else:
        break
while True:
    systray = subprocess.Popen(["pip","install","newgroundsdl"])
    systray.wait()
    stdout,stderr = systray.communicate()
    if stderr:
        cont += 1
        if cont >= 5:
            log.critical("Failed to install newgroundsdl in 5 attempts.")
            exit()
    else:
        break
while True:
    systray = subprocess.Popen(["pip","install","requests"])
    systray.wait()
    stdout,stderr = systray.communicate()
    if stderr:
        cont += 1
        if cont >= 5:
            log.critical("Failed to install requests in 5 attempts.")
            exit()
    else:
        break

print("\n")
print("Successfully installed all dependencies.")
