import time,youtube_dl,os,logging,shutil,newgroundsdl,urllib
from tkinter import messagebox,filedialog,simpledialog

log = logging.getLogger(__name__)
try:
    analytics = open("./analytics.cfg")
    data = analytics.read()
    print(data)
    exec(data)
    analytics.close()
except Exception as e:
    messagebox.showerror("Song Replacer","Internal error. Exit code -102 (internal_replace-configstupidcheck);\n" + str(e))

def cmd_revertsong():
    attempt = 1
    retryable = True
    success = False
    try:
        os.mkdir("./temp/songrevr/")
    except:
        log.warning("Last cleanup never completed. Cleaning up now.")
        shutil.rmtree("./temp/songrevr/")
        os.mkdir("./temp/songrevr/")
    while attempt <= 3 and retryable == True and success == False:
        print("Waiting to prevent ratelimiting.")
        time.sleep(5)
        try:
            try:
                print("Setting up downloader...")
                id = 310673
                fileuri = "https://www.newgrounds.com/audio/listen/" + str(id)
                audio = newgroundsdl.getSongFileURI(fileuri)
                print("Beginning stream...")
                print("[newgroundsdl-inspired] Downloading...")
                try:
                    dlreq = urllib.request.Request(fileuri, data=None, headers=newgroundsdl.headers)
                    with urllib.request.urlopen(dlreq) as dlfile, open("./temp/songrevr/" + str(id) + ".mp3","wb") as dlout:
                        shutil.copyfileobj(dlfile, dlout, length=1024*1024)
                except MemoryError as e:
                    messagebox.showerror("Reinstating song","Out of memory during stream!")
                    del stream,audio,id
                except Exception as e:
                    messagebox.showerror("Reinstating song","Unexpected error during stream!\nError: " + str(e))
                print("Successfully gotten song file.")
                print("Replacing internally...")
                try:
                    internal_replace(id,mode="revert")
                except Exception as e:
                    messagebox.showerror("Reinstating song","Internal error.\nError:" + str(e))
                success = True
            except urllib.error.URLError as e:
                messagebox.showerror("Reinstating song","Unknown error",str(e))
                retryable = True
                attempt += 1
        except Exception as e:
            messagebox.showerror("Reinstating song","Internal error\n" + str(e))
        
        try:
            shutil.rmtree("./temp/songrevr")
            messagebox.showinfo("Reinstated song","Successfully reinstated song without problems.")
        except Exception as e:
            messagebox.showwarning("Reinstating song","Successfully reinstated song, but cleanup failed.\nError: " + str(e))
def cmd_replacesong():
    url = simpledialog.askstring("Song Replacer","Please type the URL of the song.")
    if url.startswith("https://youtube.com/watch?v=") or url.startswith("https://www.youtube.com/watch?v="):
        print("Video URL is valid.")
        try:
            rep = simpledialog.askinteger("Song Replacer","Please type the ID you want to replace.")
            video_info = youtube_dl.YoutubeDL().extract_info(
                url = url,download=False
            )
            title = f"{video_info['title']}"
            try:
                os.mkdir("./temp/songrepl/")
            except:
                log.warning("Last cleanup never completed. Cleaning up now.")
                shutil.rmtree("./temp/songrepl/")
                os.mkdir("./temp/songrepl/")
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': './temp/songrepl/' + str(rep) + '.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                internal_replace(rep,mode="replace")
                print("Cleaning up...")
                try:
                    shutil.rmtree("./temp/songrepl/")
                except:
                    messagebox.showwarning("Song Replacer","Song replace successfully, but cleanup failed.")
            except Exception as e:
                messagebox.showerror("Song Replacer","Failed with exit code -2 (Download);\n" + str(e))
            return ["./queue/" + url + ".mp3",title]
        except Exception as e:
            messagebox.showerror("Song Replacer","Failed with exit code -1 (General);\n" + str(e))
    else:
        messagebox.showerror("Song Replacer","Invalid URL.")
def internal_replace(rep,*,mode):
    try:
        if appdatapath == None:
            appdata = filedialog.askdirectory(mustexist=True,title="Backup",initialdir="C:/")
            if appdata == "":
                messagebox.showerror("Song Replacer","Failed with exit code -100 (internal_replace)\nMost likely, you cancelled the prompt to\nselect your GD folder.")
            else:
                print("Valid path given.")
        else:
            print("Valid path found.")
        try:
            print("Removing original...")
            os.remove(appdatapath + "/" + str(rep) + ".mp3")
        except:
            print("Song never existed, skipping removal.")
        print("Copying in new song...")
        if mode == "replace":
            shutil.move("./temp/songrepl/" + str(rep) + ".mp3", appdatapath + "/" + str(rep) + ".mp3")
        elif mode == "revert":
            shutil.move("./temp/songrevr/" + str(rep) + ".mp3", appdatapath + "/" + str(rep) + ".mp3")

        return 0
    except Exception as e:
        messagebox.showerror("Song Replacer","Internal error. Exit code -101 (internal_replace-general);\n" + str(e))
        return -101
