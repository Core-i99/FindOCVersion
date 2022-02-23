#!/usr/bin/python
#
# Script to find OpenCore bootloader version from OpenCore.efi based on md5 checksum
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

import hashlib, json, tkinter.messagebox, tkinter, datetime, os
from tkinter import filedialog

Script_Version = "V1.2" 
debug = 0

root = tkinter.Tk()  # Creating instance of tkinter class
root.title("Find OC Version")
root.resizable(False, False)  # Disable rootdow resizing

fm1 = tkinter.Frame(root)
fm2 = tkinter.Frame(root)
fm3 = tkinter.Frame(root)
fm4 = tkinter.Frame(root)

def openFileClicked():
    OcVersionLabel['text'] = ''
    filetypes = [
        ('EFI files', '*.efi')
    ]
    inputfile = filedialog.askopenfilename(filetypes=filetypes)
    if inputfile != '': # if inputfile isn't an empty string
        if debug == 1:
            print("Selected OpenCore.efi: " + inputfile)
            print("Database location: " + DatabaseLocation)

        md5_hash = hashlib.md5()
        a_file = open(inputfile, "rb")
        content = a_file.read()
        md5_hash.update(content)
        digest = md5_hash.hexdigest()

        if debug == 1:
            print("OpenCore.efi MD5 checksum: " + digest)

        # Read database file
        with open(DatabaseLocation) as file:
            database = file.read()

        # Parse json file
        databasedata = json.loads(database)

        if digest not in databasedata:
            tkinter.messagebox.showwarning( "OC version not found in database", "OC Version not found in database!\n\nPlease update the database using GetOCMD5 for the latest OpenCore versions.\n\nNote that only Opencore Releases from GitHub are supported.")
        
        OcVersionLabel['text'] = 'OC Version ' + databasedata[digest]

    elif debug == 1:
            print("Nothing Selected")    

def showinfo():
     tkinter.messagebox.showinfo("About", "Script to find the OpenCore version from an OpenCore EFI folder.\n\nScript version: %s\n " % (Script_Version))

def exitwindow():
    print("\nThanks for using Find OC Version " + Script_Version)
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

centerwindow() #center the gui window on the screen

# working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
working_dir = os.getcwd()
DatabaseLocation = working_dir + '\Database.json'
if debug == 1:
    print("\nCurrent working directory: ", working_dir)
    print("Database Location: "+ DatabaseLocation)

# Buttons and labels
tkinter.Button(fm1, text='Select OpenCore.efi', command=openFileClicked).pack(side='left', expand=1, padx=10)
tkinter.Button(fm3, text="About", command=showinfo).pack(side='left', expand=1, padx=10)

DebugButton = tkinter.Button(fm3, text='Enable debug mode', command=ChangeDebug)
DebugButton.pack(side='left', expand=1, padx=10)  

OcVersionLabel = tkinter.Label(fm2, text='')
OcVersionLabel.pack(side='left', expand=1, padx=10)

tkinter.Button(fm4, text='Exit', command=exitwindow).pack(side='left', expand=1, padx=10)

# pack the frames
fm1.pack(pady=10)
fm2.pack(pady=10)
fm3.pack(pady=10)
fm4.pack(pady=10)

root.mainloop()