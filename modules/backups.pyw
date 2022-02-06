import time,shutil,os,logging,zipfile,psutil
from tkinter import messagebox,filedialog
from zipfile import ZipFile

log = logging.getLogger(__name__)

def onImport():
    print("Backups module imported!")

def cmd_loadback(location,*,silent=False):
    print("Loading backup...")
    messagebox.showinfo("Backup","Select the backup archive you want to load.")
    archive = filedialog.askopenfilename(title="Backup",initialdir=os.path.abspath("./backups/"))
    if archive == "":
        messagebox.showerror("Loading failed.","Cannot load backup; Cancel was pressed.")
    elif not os.path.exists(archive):
        messagebox.showerror("Loading failed.","Missing file.")
    elif not archive.endswith(".zip"):
        messagebox.showerror("Loading failed.","Invalid file.")
    else:
        print("Copying archive to ./temp/...")
        rdyArchive = "./temp/extract/archive.zip"
        try:
            os.mkdir("./temp/extract")
        except:
            log.warning("Last directory cleanup never completed, skipping dir creation.")
        try:
            with open(rdyArchive,"x"):
                print("Created archive.zip and copying data over...")
        except:
            log.warning("Last file cleanup never completed, skipping file creation.")
        shutil.copy(archive,rdyArchive)
        zip = ZipFile("./temp/extract/archive.zip")
        zip.extractall("./temp/extract/extracted")
        zip.close()
        safe = True
        for proc in psutil.process_iter():
            try:
                if "geometrydash" in proc.name().lower():
                    safe = False
                else:
                    pass
            except:
                pass
        if safe == True:
            levels1tar = location + "/CCLocalLevels.dat"
            levels2tar = location + "/CCLocalLevels2.dat"
            gameman1tar = location + "/CCGameManager.dat"
            gameman2tar = location + "/CCGameManager2.dat"
            print("Removing old files")
            try:
                os.remove(levels1tar)
            except:
                log.warning("CCLocalLevels not found.")
            try:
                os.remove(levels2tar)
            except:
                log.warning("CCLocalLevels2 not found.")
            try:
                os.remove(gameman1tar)
            except:
                log.warning("CCGameManager not found.")
            try:
                os.remove(gameman2tar)
            except:
                log.warning("CCGameManager2 not found.")
            print("Moving backup files")
            shutil.move("./temp/extract/extracted/temp/appdata/CCLocalLevels.dat",levels1tar)
            shutil.move("./temp/extract/extracted/temp/appdata/CCLocalLevels2.dat",levels2tar)
            shutil.move("./temp/extract/extracted/temp/appdata/CCGameManager.dat",gameman1tar)
            shutil.move("./temp/extract/extracted/temp/appdata/CCGameManager2.dat",gameman2tar)
            print("Cleaning up...")
            shutil.rmtree("./temp/extract")
            print("Done!")
            messagebox.showinfo("Backup","Successfully loaded backup!")
        else:
            messagebox.showerror("Backup failed to load.","Geometry Dash is open.\nPlease close Geometry Dash before loading a backup.")




def cmd_newback(location=None,*,silent=False):
    print("Creating backup...")
    if location == None:
        messagebox.showinfo("Backup","Select your AppData Geometry Dash Folder")
        appdata = filedialog.askdirectory(mustexist=True,title="Backup",initialdir="C:/")
    else:
        appdata = location
    if appdata == "":
        if silent == False: messagebox.showerror("Backup failed!","Backup failed while asking for AppData folder.")
    else:
        try:
            print("Copying important files...")
            try:
                os.mkdir("./temp/appdata")
            except:
                log.warning("Last directory cleanup never completed, skipping dir creation.")
            print("Directory for temporary files created.")
            try:
                levels1tar  = "./temp/appdata/CCLocalLevels.dat"
                levels2tar  = "./temp/appdata/CCLocalLevels2.dat"
                gameman1tar = "./temp/appdata/CCGameManager.dat"
                gameman2tar = "./temp/appdata/CCGameManager2.dat"
                with open(levels1tar,"x"):
                    print("Created CCLocalLevels")
                with open(levels2tar,"x"):
                    print("Created CCLocalLevels2")
                with open(gameman1tar,"x"):
                    print("Created CCGameManager")
                with open(gameman2tar,"x"):
                    print("Created CCGameManager2")
            except:
                log.warning("Last file cleanup never completed, skipping file creation.")
            shutil.copy(appdata + "/CCLocalLevels.dat",levels1tar)
            shutil.copy(appdata + "/CCLocalLevels2.dat",levels2tar)
            shutil.copy(appdata + "/CCGameManager.dat",gameman1tar)
            shutil.copy(appdata + "/CCGameManager2.dat",gameman2tar)
            try:
                print("Compressing appdata and steamapps into .zip")
                with ZipFile("./backups/" + str(round(time.time())) + ".zip","w",compression=zipfile.ZIP_BZIP2) as zipObj:
                    for f in os.listdir("./temp/appdata"):
                        print("Writing",f,"to zip.")
                        zipObj.write("./temp/appdata/" + f)
                try:
                    zipObj.close()
                except:
                    pass
                print("Updating analytics.cfg...")
                analytics = open("./analytics.cfg","w")
                analytics.write(  "# Note: These analytics are not sent to anyone, and are completely private.")
                analytics.write("\n#       Looking through the code can verify this.")
                analytics.write("\n")
                analytics.write("\nlastbackuptime = " + str(time.time()))
                analytics.write("\nappdatapath = \"" + str(appdata) + "\"")
                print("Cleaning up...")
                try:
                    shutil.rmtree("./temp/appdata")
                    print("Backup complete!")
                    if silent == False: messagebox.showinfo("Backup successful!","Backup has been completed successfully!")
                except Exception as e:
                    if silent == False: messagebox.showwarning("Backup cleanup failed!","Cleanup failed;\n" + str(e))
            except Exception as e:
                if silent == False: messagebox.showerror("Backup failed!","Backup failed with exit code -2 (Compression);\n" + str(e))
        except Exception as e:
            if silent == False: messagebox.showerror("Backup failed!","Backup failed with exit code -1 (General);\n" + str(e))
