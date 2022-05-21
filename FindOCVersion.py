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
import sys
from tkinter.messagebox import showerror, showinfo
from tkinter import Frame, Tk, Label, Button
from tkinter.filedialog import askopenfilename


class MainWindow():
    def __init__(self):
        self.Script_Version = "V2.0"
        self.debug = False
        self.root = Tk()  # Creating instance of tkinter class
        self.root.title("Find OC Version")
        self.root.resizable(False, False)  # Disable rootwindow resizing

        fm1 = Frame(self.root)
        fm2 = Frame(self.root)
        fm3 = Frame(self.root)
        fm4 = Frame(self.root)

        # Buttons and labels
        Button(fm1, text='Select OpenCore.efi', command=self.openFileClicked).pack(side='left', expand=1, padx=10)
        Button(fm3, text="About", command=self.about).pack(side='left', expand=1, padx=10)

        self.DebugButton = Button(fm3, text='Enable debug mode', command=self.ChangeDebug)
        self.DebugButton.pack(side='left', expand=1, padx=10)

        self.OcVersionLabel = Label(fm2, text='')
        self.OcVersionLabel.pack(side='left', expand=1, padx=10)

        Button(fm4, text='Exit', command=self.exitwindow).pack(side='left', expand=1, padx=10)

        # pack the frames
        fm1.pack(pady=10)
        fm2.pack(pady=10)
        fm3.pack(pady=10)
        fm4.pack(pady=10)

        

        # working directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        working_dir = os.getcwd()
        self.DatabaseLocation = f"{working_dir}//Database.json"
        self.debugPrint(f"Current working directory: {working_dir}")
        self.debugPrint(f"Database Location: {self.DatabaseLocation}")

        self.centerwindow()
        self.root.mainloop()

    def debugPrint(self, message):
        if self.debug:
            print(f"Debug: {message}")


    def openFileClicked(self):
        FoundOC = False
        self.OcVersionLabel['text'] = ''
        filetypes = [
            ('EFI files', '*.efi')
        ]
        inputfile = askopenfilename(filetypes=filetypes)
        if inputfile != '': # if inputfile isn't an empty string
            self.debugPrint(f"Selected OpenCore.efi: {inputfile}")
            self.debugPrint(f"Database location: {self.DatabaseLocation}")

            # read input file (OpenCore.efi)
            with open(inputfile, 'rb') as f:
                hexdata = str(f.read().hex()).upper()

            # Read database file
            with open(self.DatabaseLocation , encoding="utf8") as file:
                database = file.read()

            # Parse json file
            databasedata = json.loads(database)

            for line in databasedata:
                self.debugPrint(f"Line from database: {line}")
                line_no_space = str(line).replace(" ", "")
                if line_no_space in hexdata:
                    FoundOC = True
                    self.debugPrint(f"OpenCore Version: {databasedata[line]}")
                    self.OcVersionLabel['text'] = f"OC Version {databasedata[line]}"

            if FoundOC is False:
                showerror("Error", "Couldn't find the version of this OpenCore.efi")

        else: self.debugPrint("Nothing selected")

    def about(self):
        showinfo("About", f"Script to find the OpenCore version from an OpenCore EFI folder.\n\nScript version: {self.Script_Version}\n ")


    def exitwindow(self):
        print(f"\nThanks for using Find OC Version {self.Script_Version}")
        print("Written By Core i99 - © Stijn Rombouts 2021\n")
        print("Check out my GitHub:\n")
        print("https://github.com/Core-i99/\n\n")

        hour = datetime.datetime.now().time().hour
        if 3 < hour < 12:
            print("Have a nice morning!\n\n")
        elif 12 <= hour < 17:
            print("Have a nice afternoon!\n\n")
        elif 17 <= hour < 21:
            print("Have a nice evening!\n\n")
        else:
            print("Have a nice night! (And don't forget to sleep!)\n\n")
        sys.exit()


    def ChangeDebug(self):
        if debug is False:
            debug = True
            print("Enabled debug mode")
            self.DebugButton['text'] = 'Disable debug mode'
        elif debug:
            debug = False
            self.DebugButton['text'] = 'Enable debug mode'

    def centerwindow(self):
        app_height = 200
        app_width = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (app_width/2))
        y_cordinate = int((screen_height/2) - (app_height/2))
        self.root.geometry(f"{app_width}x{app_height}+{x_cordinate}+{y_cordinate}")

MainWindow()