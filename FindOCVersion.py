#!/usr/bin/python3
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

import json
import datetime
import os
from tkinter.messagebox import showerror, showinfo
from tkinter import Frame, Tk, Label, Button
from tkinter.filedialog import askopenfilename

Script_Version = "V2.0"
debug = False

root = Tk()  # Creating instance of tkinter class
root.title("Find OC Version")
root.resizable(False, False)  # Disable rootwindow resizing

fm1 = Frame(root)
fm2 = Frame(root)
fm3 = Frame(root)
fm4 = Frame(root)

def debugPrint(message):
    if debug == True:
        print(f"Debug: {message}")


def openFileClicked():
    FoundOC = False
    OcVersionLabel['text'] = ''
    filetypes = [
        ('EFI files', '*.efi')
    ]
    inputfile = askopenfilename(filetypes=filetypes)
    if inputfile != '': # if inputfile isn't an empty string
        debugPrint(f"Selected OpenCore.efi: {inputfile}")
        debugPrint(f"Database location: {DatabaseLocation}")

        # read input file (OpenCore.efi)
        with open(inputfile, 'rb') as f:
            hexdata = str(f.read().hex()).upper()

        # Read database file
        with open (DatabaseLocation) as file:
            database = file.read()

        # Parse json file
        databasedata = json.loads(database)

        for line in databasedata:
            debugPrint(f"Line from database: {line}")
            line_no_space = str(line).replace(" ", "")
            if (line_no_space in hexdata):
                FoundOC = True
                debugPrint(f"OpenCore Version: {databasedata[line]}")
                OcVersionLabel['text'] = f"OC Version {databasedata[line]}"

        if (FoundOC == False):
            showerror("Error", "Couldn't find the version of this OpenCore.efi")

    else: debugPrint("Nothing selected")

def about():
    showinfo("About", f"Script to find the OpenCore version from an OpenCore EFI folder.\n\nScript version: {Script_Version}\n ")

def exitwindow():
    print(f"\nThanks for using Find OC Version {Script_Version}")
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
    if debug == False:
        debug = True
        print("Enabled debug mode")
        DebugButton['text'] = 'Disable debug mode'
    elif debug == True:
        debug = False
        DebugButton['text'] = 'Enable debug mode'

def centerwindow():
    app_height = 200
    app_width = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (app_width/2))
    y_cordinate = int((screen_height/2) - (app_height/2))
    root.geometry(f"{app_width}x{app_height}+{x_cordinate}+{y_cordinate}")

centerwindow() #center the gui window on the screen

# working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
working_dir = os.getcwd()
DatabaseLocation = f"{working_dir}//Database.json"

debugPrint(f"Current working directory: {working_dir}")
debugPrint(f"Database Location: {DatabaseLocation}")

# Buttons and labels
Button(fm1, text='Select OpenCore.efi', command=openFileClicked).pack(side='left', expand=1, padx=10)
Button(fm3, text="About", command=about).pack(side='left', expand=1, padx=10)

DebugButton = Button(fm3, text='Enable debug mode', command=ChangeDebug)
DebugButton.pack(side='left', expand=1, padx=10)

OcVersionLabel = Label(fm2, text='')
OcVersionLabel.pack(side='left', expand=1, padx=10)

Button(fm4, text='Exit', command=exitwindow).pack(side='left', expand=1, padx=10)

# pack the frames
fm1.pack(pady=10)
fm2.pack(pady=10)
fm3.pack(pady=10)
fm4.pack(pady=10)

root.mainloop()
