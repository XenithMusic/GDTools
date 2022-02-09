import tkinter,time,shutil,os,logging,subprocess
from tkinter import messagebox,filedialog
from zipfile import ZipFile
from win32com.client import Dispatch as disp
from modules.backups import * # Module for backup operations
from modules.songs import *   # Module for song operations

try:
    daeconf = open("./daemon.cfg","r")
    exec(daeconf.read())
    daeconf.close()
except IOError as e:
    daeconf = open("./daemon.cfg","w")
    daeconf.write("dcfg_wait = 0\ndcfg_allow = True\ndcfg_backupTime = 604800\ndcfg_refreshTime = 10\ndcfg_failRefresh = 100")
    daeconf.close()
    dcfg_wait = 0
    dcfg_allow = True
    dcfg_backupTime = 604800
    dcfg_refreshTime = 10
    dcfg_failRefresh = 100
try:
    analytics = open("./analytics.cfg","r")
    exec(analytics.read())
    analytics.close()
except FileNotFoundError as e:
    analytics = open("./analytics.cfg","w")
    analytics.write("lastbackuptime = None\nappdatapath = None")
    lastbackuptime = None
    appdatapath = None
    analytics.close()

# Thing for creating startup shortcut.

if dcfg_allow == True:
    userfolder  = os.path.expanduser("~")
    startupapps = userfolder + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
    path        = startupapps + "GDToolsd.lnk"
    target      = os.path.abspath("./GDToolsd.pyw")
    wDir        = os.path.abspath("./")
    icon        = os.path.abspath("./assets/icon/16.png")

    shell       = disp("WScript.Shell")
    shortcut    = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation = icon
    shortcut.save()
    del startupapps,path,target,wDir,icon,shell



log = logging.getLogger(__name__)

def saveback():
    btn_newback.grid_forget()
    lab_backing.grid(column=0,row=0,padx=20,pady=20)
    cmd_newback()
    lab_backing.grid_forget()
    btn_newback.grid(column=0,row=0,padx=20,pady=20)

def loadback():
    btn_loadback.grid_forget()
    lab_loading.grid(column=0,row=1)
    cmd_loadback(appdatapath)
    lab_loading.grid_forget()
    btn_loadback.grid(column=0,row=1)

def replsong():
    btn_repsong.grid_forget()
    lab_repsong.grid(column=1,row=0,padx=20,pady=20)
    cmd_replacesong()
    lab_repsong.grid_forget()
    btn_repsong.grid(column=1,row=0,padx=20,pady=20)

def revrsong():
    btn_revsong.grid_forget()
    lab_revsong.grid(column=1,row=1)
    cmd_revertsong()
    lab_revsong.grid_forget()
    btn_revsong.grid(column=1,row=1)

win = tkinter.Tk()
win.title("GDTools")
win.iconphoto(True,tkinter.PhotoImage(file='./assets/icon/16.png'))
win.columnconfigure(2, minsize=200, weight=1)
win.rowconfigure(2, minsize=350, weight=1)
lab_backing = tkinter.Label(text="Creating backup...",font=("Hevletica","9"))
lab_loading = tkinter.Label(text="Loading backup...",font=("Hevletica","9"))
lab_repsong = tkinter.Label(text="Replacing song...",font=("Hevletica","9"))
lab_revsong = tkinter.Label(text="Reinstating song...",font=("Hevletica","9"))
btn_newback = tkinter.Button(text="                Create backup                ",command=saveback)
btn_loadback = tkinter.Button(text="                Load backup                ",command=loadback)
btn_repsong = tkinter.Button(text="                Replace song                ",command=replsong)
btn_revsong = tkinter.Button(text="                Reinstate song                ",command=revrsong)
btn_newback.grid(column=0,row=0,padx=20,pady=20)
btn_loadback.grid(column=0,row=1)
btn_repsong.grid(column=2,row=0,padx=20,pady=20)
btn_revsong.grid(column=2,row=1)
win.mainloop()
