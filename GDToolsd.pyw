import time,os
from infi.systray import SysTrayIcon
from modules.backups import *
def trayConfiguration(tray):
    os.system("notepad " + os.path.abspath("./daemon.cfg"))

def trayAnalytics(tray):
    os.system("notepad " + os.path.abspath("./analytics.cfg"))

def trayQuit(tray):
    global quit
    print("Quit callback requested.")
    quit = True


trayItems = (("Configuration",None,trayConfiguration),("View Analytics",None,trayAnalytics))
systray = SysTrayIcon("./assets/icon/16.ico","GDTools Daemon",trayItems,on_quit=trayQuit)
systray.start()
quit = False

try:
    time.sleep(1)
    config = open("./daemon.cfg","r")
    exec(config.read())
    config.close()
    backupinfo = open("./analytics.cfg","r")
    exec(backupinfo.read())
    backupinfo.close()
    print(dcfg_wait)
    print(dcfg_allow)
    print(dcfg_backupTime)
    time.sleep(dcfg_wait)
    if dcfg_allow == False:
        print("Daemon blocked by config setting dcfg_allow")
        exit()
    print("Daemon allowed.")
    print("To disable the daemon, change .daeconf setting dcfg_allow")
    while not quit:
        config = open("./daemon.cfg","r")
        exec(config.read())
        config.close()
        backupinfo = open("./analytics.cfg","r")
        exec(backupinfo.read())
        backupinfo.close()
        for i in range(dcfg_refreshTime*10):
            time.sleep(0.1)
            if quit:
                break
        try:
            if (time.time()-dcfg_backupTime)-lastbackuptime > 0:
                print("Attempting GD Backup...")
                cmd_newback(appdatapath,silent=True)
            else:
                print("Time until backup:",(time.time()-dcfg_backupTime)-lastbackuptime)
        except:
            print("No backup has ever been done!")
            print("Failed to do backup.")
            for i in range(dcfg_failRefresh*10):
                time.sleep(0.1)
                if quit or not dcfg_allow:
                    break
except Exception as e:
    systray.shutdown()
    raise e

systray.shutdown()
print("Daemon stopped.")
