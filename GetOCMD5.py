#!/usr/bin/python
#
# Script to find OpenCore bootloader MD5 checksum from OpenCore.efi downloaded from GitHub releases
#
# by Stijn Rombouts <stijnrombouts@outlook.com>
#
# Copyright (c) 2021,2022 Stijn Rombouts <stijnrombouts@outlook.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import hashlib, json, tkinter.messagebox, tkinter, datetime, os, urllib, shutil, zipfile
from urllib.request import urlopen
from tkinter.messagebox import askyesno

Version = "V1.2" 
debug = 0
match = 0

root = tkinter.Tk()  # Creating instance of tkinter class
root.title("Get OC MD5")
root.resizable(False, False)  # Disable rootwindow resizing

fm1 = tkinter.Frame(root)
fm2 = tkinter.Frame(root)
fm3 = tkinter.Frame(root)
fm4 = tkinter.Frame(root) 
fm5 = tkinter.Frame(root) 
fm6 = tkinter.Frame(root) 

os.chdir(os.path.dirname(os.path.abspath(__file__)))
working_dir = os.getcwd()
DatabaseLocation = working_dir + '/Database.json'
if debug == 1:
    print("\nCurrent working directory: ", working_dir)
    print("Database Location: " + DatabaseLocation)

def showinfo():
     tkinter.messagebox.showinfo("About", "Script to find OpenCore bootloader MD5 checksum from OpenCore.efi downloaded from GitHub releases.\n\nVersion: %s\n " % (Version))

def exitwindow():
    print("\nThanks for using Get OC MD5 " + Version)
    print("Written By Core i99 - © Stijn Rombouts 2021\n")
    print("Check out my GitHub:\n")
    print("https://github.com/Core-i99/\n\n")
    hour = datetime.datetime.now().time().hour
    if hour > 3 and hour < 12:
        print("Have a nice morning!\n\n")
    elif hour >= 12 and hour < 17:
        print("Have a nice afternoon!\n\n")
    elif hour >= 17 and hour < 21:
        print("Have a nice evening!\n\n")
    else:
        print("Have a nice night! (And don't forget to sleep!)\n\n")  
    exit()       

def start():
    global match
    OCVersion = OCVersionVar.get()
    if debug == 1:
        print("Entered OC Version: " , OCVersion)
    if OCVersion == "":
        tkinter.messagebox.showerror("ERROR", "No OpenCore version entered!")
    elif OCVersion >= "0.0.1" and OCVersion <= "0.0.3":
        urlrelease = "https://github.com/acidanthera/OpenCorePkg/releases/download/" + OCVersion  + "/OpenCore-V"+ OCVersion + "-RELEASE.zip"
        urldebug = "https://github.com/acidanthera/OpenCorePkg/releases/download/" + OCVersion  + "/OpenCore-v"+ OCVersion + "-DEBUG.zip"
        match = 1
        if debug == 1:
            print ("\nOC release URL: " + urlrelease)  
            print ("\nOC debug URL: " + urldebug) 
    elif OCVersion >= "0.5.0" or OCVersion == "0.0.4":
        urlrelease = "https://github.com/acidanthera/OpenCorePkg/releases/download/" + OCVersion  + "/OpenCore-"+ OCVersion + "-RELEASE.zip" # from version 0.0.4 and up "v" is removed from the download url
        urldebug = "https://github.com/acidanthera/OpenCorePkg/releases/download/" + OCVersion  + "/OpenCore-"+ OCVersion + "-DEBUG.zip"   
        match = 1
    else:
        tkinter.messagebox.showerror("ERROR", "Can't get the entered OpenCore version from GitHub!")
        match = 0

    if match == 1 :
        if debug == 1:
            print ("\nOC release URL: " + urlrelease)  
            print ("\nOC debug URL: " + urldebug) 
        DocPath = os.path.expanduser('~/Documents')# Get Documents folder path

        # Create GetOCMD5 folder
        path = DocPath + "/GetOCMD5"
        if not os.path.exists(path):
            os.makedirs(path)
        if debug == 1:    
            print("DocPath: " + DocPath)

        # Create paths for OpenCore zips
        OCRELZip_path = path + "/OpenCore-" + OCVersion + "-RELEASE.zip" # path to write OpenCore.zip        
        OCDBGZip_path = path + "/OpenCore-" + OCVersion + "-DEBUG.zip" # path to write OpenCore.zip   
        if debug == 1:    
            print("OCRELZip path: " + OCRELZip_path)
            print("OCDBGZip path: " + OCDBGZip_path)

        # Check if internet connection works
        try:
            urllib.request.urlopen(urlrelease)
            if debug == 1:
                print("\nFound the url")
        except:
            tkinter.messagebox.showerror("ERROR", "Failed to download OpenCore from GitHub! Check your internet connection!") 

        # Download OpenCore from GitHub
        urllib.request.urlretrieve(urlrelease, OCRELZip_path)
        urllib.request.urlretrieve(urldebug, OCDBGZip_path)
        if debug == 1:
            print ("\nDownloaded the file")    
        
        # Create tmp directory
        RELtemppath = path + '/tmp' + " RELEASE"
        DBGtemppath = path + '/tmp' + " DEBUG"
        if os.path.exists(RELtemppath):
            shutil.rmtree(RELtemppath) # remove existing tmp folder
            if debug == 1:
                print("\nFound an existing RELEASE tmp directory.")
                print("\nRemoved existing  RELEASE tmp folder.")
        if os.path.exists(DBGtemppath):
            shutil.rmtree(DBGtemppath) # remove existing tmp folder
            if debug == 1:
                print("\nFound an existing DEBUG tmp directory.")
                print("\nRemoved existing DEBUG tmp folder.")   

        # Unzip downloaded OpenCore.zip
        with zipfile.ZipFile(OCRELZip_path, 'r') as zip_REL:
            zip_REL.extractall(RELtemppath)
        with zipfile.ZipFile(OCDBGZip_path, 'r') as zip_DBG:
            zip_DBG.extractall(DBGtemppath)    
        if debug == 1:
            print("\nUnzipped the OpenCore.zip for to tmp directory")    

        # Finally! Get the MD5 checksum
        if OCVersion >= "0.6.2": # Since OC 0.6.2 the X64 folder is used
            OpenCoreEFIFileREL = RELtemppath + "/X64/EFI/OC/OpenCore.efi"
            OpenCoreEFIFileDBG = DBGtemppath + "/X64/EFI/OC/OpenCore.efi" 
        elif OCVersion >= "0.0.4":
            OpenCoreEFIFileREL = RELtemppath + "/EFI/OC/OpenCore.efi"  
            OpenCoreEFIFileDBG = DBGtemppath + "/EFI/OC/OpenCore.efi" 
        elif OCVersion <= "0.0.3":
            OpenCoreEFIFileREL = RELtemppath + "/OC/OpenCore.efi"  
            OpenCoreEFIFileDBG = DBGtemppath + "/OC/OpenCore.efi"            
     
        if debug == 1:
            print("\nOpenCore.efi RELEASE file: " + OpenCoreEFIFileREL)
            print("\nOpenCore.efi DEBUG file: " + OpenCoreEFIFileDBG)    

        # OC Release MD5 checksum
        md5_hashREL = hashlib.md5()
        REL_file = open(OpenCoreEFIFileREL, "rb")
        content = REL_file.read()
        md5_hashREL.update(content)
        RELdigest = md5_hashREL.hexdigest()

        # OC Debug MD5 checksum
        md5_hashDBG = hashlib.md5()
        DBG_file = open(OpenCoreEFIFileDBG, "rb")
        content = DBG_file.read()
        md5_hashDBG.update(content)
        DBGdigest = md5_hashDBG.hexdigest()

        tkinter.messagebox.showinfo("MD5 checksums", "OpenCore Release %s MD5 checksum: %s\n\nOpenCore Debug %s MD5 checksum: %s" % (OCVersion, RELdigest, OCVersion, DBGdigest))

        SaveToDatabase = askyesno(title='Save to database?', message='Would you like to write the MD5 checksum to the database?')
        if SaveToDatabase == True:
            if debug == 1:
                print("\nWriting to database...")

            # Read database file
            with open(DatabaseLocation) as file:
                database = file.read()
            # Parse json file
            databasedata = json.loads(database) 

            valueREL = "OC %s RELEASE" % (OCVersion)
            valueDBG = "OC %s DEBUG" % (OCVersion)

            if debug == 1:
                print("\nOC RELEASE name for database: " + valueREL)
                print("\nOC DEBUG name for database: " + valueDBG)

            databasedata[RELdigest] = valueREL 
            databasedata[DBGdigest] = valueDBG

            with open('Database.json', 'w') as file: # Open the database in write mode as file
                json.dump(databasedata, file, indent=4) # write json data to file with 4 spaces in the beginning of a line  

def ChangeDebug():  
    global debug
    if debug == 0:
        debug = 1
        print("Enabled debug mode")  
        DebugButton['text'] = 'Disable debug mode'
    elif debug == 1:
        debug = 0
        DebugButton['text'] = 'Enable debug mode'

def centerwindow():
    app_height = 200
    app_width = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (app_width/2))
    y_cordinate = int((screen_height/2) - (app_height/2))
    root.geometry("{}x{}+{}+{}".format(app_width, app_height, x_cordinate, y_cordinate))

centerwindow() # center the gui window on the screen

# Buttons and labels
OCVersionVar = tkinter.StringVar()  
tkinter.Button(fm2, text="Start", command=start).pack(side='left', expand=1, padx=10)
tkinter.Button(fm3, text="About", command=showinfo).pack(side='left', expand=1, padx=10)
tkinter.Label(fm1, text = "Enter OC Version:").pack(side='left', expand=1, padx=5)
OCVersionEntry = tkinter.Entry(fm1, textvariable=OCVersionVar).pack()
DebugButton = tkinter.Button(fm3, text='Enable debug mode', command=ChangeDebug)
DebugButton.pack(side='left', expand=1, padx=10)  
tkinter.Button(fm4, text='Exit', command=exitwindow).pack(side='left', expand=1, padx=10)

# pack the frames
fm1.pack(pady=10)
fm2.pack(pady=10)
fm3.pack(pady=10)
fm4.pack(pady=10)
fm5.pack(pady=10)
fm6.pack(pady=10)

root.mainloop()
