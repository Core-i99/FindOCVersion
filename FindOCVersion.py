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
# pylint: disable=protected-access

from tkinter.messagebox import showerror, showinfo
from tkinter import Frame, Tk, Label, Button
from tkinter.filedialog import askopenfilename
import Logging
import os
import sys
import platform

# Database: 
OC080REL = ["30 38 C6 05 AE 56 02 00 30 C7 05 A6 56 02 00 32 30 32 32 66 C7 05 A2 56 02 00 30 34", "OC 0.8.0 RELEASE"]
OC080DBG = ["30 38 C6 05 BF DE 04 00 30 C7 05 B7 DE 04 00 32 30 32 32 66 C7 05 B3 DE 04 00 30 34", "OC 0.8.0 DEBUG"]
OC079REL = ["30 37 66 89 05 01 4F 02 00 C6 05 FC 4E 02 00 39 C7 05 F4 4E 02 00 32 30 32 32 66 C7 05 F0 4E 02 00 30 33", "OC 0.7.9 RELEASE"]
OC079DBG = ["30 37 66 89 05 17 D4 04 00 C6 05 12 D4 04 00 39 C7 05 0A D4 04 00 32 30 32 32 66 C7 05 06 D4 04 00 30 33", "OC 0.7.9 DEBUG"]
OC078REL = ["30 37 66 89 05 D0 46 02 00 C6 05 CB 46 02 00 38 C7 05 C3 46 02 00 32 30 32 32 66 C7 05 BF 46 02 00 30 32", "OC 0.7.8 RELEASE"]
OC078DBG = ["30 37 66 89 05 8C C1 04 00 C6 05 87 C1 04 00 38 C7 05 7F C1 04 00 32 30 32 32 66 C7 05 7B C1 04 00 30 32", "OC 0.7.8 DEBUG"]
OC077REL = ["30 37 C6 05 4D 47 02 00 37 C7 05 45 47 02 00 32 30 32 32 66 C7 05 41 47 02 00 30 31", "OC 0.7.7 RELEASE"]
OC077DBG = ["30 37 C6 05 3D C3 04 00 37 C7 05 35 C3 04 00 32 30 32 32 66 C7 05 31 C3 04 00 30 31", "OC 0.7.7 DEBUG"]
OC076REL = ["30 37 C6 05 9D 47 02 00 36 C7 05 95 47 02 00 32 30 32 31 66 C7 05 91 47 02 00 31 32", "OC 0.7.6 RELEASE"]
OC076DBG = ["30 37 C6 05 D1 B6 04 00 36 C7 05 C9 B6 04 00 32 30 32 31 66 C7 05 C5 B6 04 00 31 32", "OC 0.7.6 DEBUG"]
OC075REL = ["30 37 C6 05 B9 48 02 00 35 C7 05 B1 48 02 00 32 30 32 31 66 C7 05 AD 48 02 00 31 31", "OC 0.7.5 RELEASE"]
OC075DBG = ["30 37 C6 05 5D BC 04 00 35 C7 05 55 BC 04 00 32 30 32 31 66 C7 05 51 BC 04 00 31 31", "OC 0.7.5 DEBUG"]
OC074REL = ["30 37 C6 05 69 3C 02 00 34 C7 05 61 3C 02 00 32 30 32 31 66 C7 05 5D 3C 02 00 31 30", "OC 0.7.4 RELEASE"]
OC074DBG = ["30 37 C6 05 55 B5 04 00 34 C7 05 4D B5 04 00 32 30 32 31 66 C7 05 49 B5 04 00 31 30", "OC 0.7.4 DEBUG"]
OC073REL = ["30 37 C6 05 A5 38 02 00 33 C7 05 9D 38 02 00 32 30 32 31 66 C7 05 99 38 02 00 30 39", "OC 0.7.3 RELEASE"]
OC073DBG = ["30 37 C6 05 61 B2 04 00 33 C7 05 59 B2 04 00 32 30 32 31 66 C7 05 55 B2 04 00 30 39", "OC 0.7.3 DEBUG"]
OC072REL = ["30 37 C6 05 B8 33 02 00 32 C7 05 B0 33 02 00 32 30 32 31 66 C7 05 AC 33 02 00 30 38", "OC 0.7.2 RELEASE"]
OC072DBG = ["30 37 C6 05 1E A4 04 00 32 C7 05 16 A4 04 00 32 30 32 31 66 C7 05 12 A4 04 00 30 38", "OC 0.7.2 DEBUG"]
OC071REL = \
["30 37 66 89 05 73 2F 02 00 C6 05 6E 2F 02 00 31 C7 05 66 2F 02 00 32 30 32 31 66 89 05 64 2F 02 00 66 C7 05 5E 2F 02 00 30 35", 
"OC 0.7.1 RELEASE"]
OC071DBG = \
["30 37 66 89 05 85 99 04 00 C6 05 80 99 04 00 31 C7 05 78 99 04 00 32 30 32 31 66 89 05 76 99 04 00 66 C7 05 70 99 04 00 30 35", 
"OC 0.7.1 DEBUG"]
OC070REL = ["30 37 66 89 05 DF 31 02 00 C6 05 DA 31 02 00 30 C7 05 D2 31 02 00 32 30 32 31 66 C7 05 CE 31 02 00 30 36", "OC 0.7.0 RELEASE"]
OC070DBG = ["30 37 66 89 05 74 88 04 00 C6 05 6F 88 04 00 30 C7 05 67 88 04 00 32 30 32 31 66 C7 05 63 88 04 00 30 36", "OC 0.7.0 DEBUG"]
OCVersions = \
[OC080REL, OC080DBG, OC079REL, OC079DBG, OC078REL, OC078DBG, OC077REL, OC077DBG, OC076REL, OC076DBG, OC075REL, OC075DBG, 
OC074REL, OC074DBG, OC073REL, OC073DBG, OC073REL, OC073DBG, OC072REL, OC072DBG, OC071REL, OC071DBG, OC070REL, OC070DBG]   

class MainWindow():
    def __init__(self):
        self.Script_Version = "V2.0"
        self.debug = False
        self.root = Tk()  # Creating instance of tkinter class
        self.root.title("Find OC Version")
        if not platform.system() == 'Darwin':
            self.root.iconbitmap(self.resource_path("Icon.ico"))
        self.root.resizable(False, False)  # Disable rootwindow resizing
        # Frames
        fm1 = Frame(self.root)
        fm2 = Frame(self.root)
        fm3 = Frame(self.root)

        # Buttons and labels
        Button(fm1, text='Select OpenCore.efi', command=self.openFileClicked).pack(side='left', expand=1, padx=10)
        Button(fm3, text="About", command=self.about).pack()
        self.OcVersionLabel = Label(fm2, text='OpenCore Version:')
        self.OcVersionLabel.pack(side='left', expand=1, padx=10)

        # pack the frames
        fm1.pack(pady=10)
        fm2.pack(pady=10)
        fm3.pack(pady=10)

        self.centerwindow()
        self.root.mainloop()

    def resource_path(self, relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
        
    def openFileClicked(self):
        FoundOC = False
        self.OcVersionLabel['text'] = 'OpenCore Version:'
        filetypes = [
            ('EFI files', '*.efi')
        ]
        inputfile = askopenfilename(filetypes=filetypes)
        if inputfile != '': # if inputfile isn't an empty string
            Logging.info(f"Selected OpenCore.efi: {inputfile}")

            # read input file (OpenCore.efi)
            with open(inputfile, 'rb') as f:
                hexdata = str(f.read().hex()).upper()

            for i in OCVersions:
                Logging.info(f"Line from database: {i[0]}")
                OCHexData = i[0].replace(" ", "") # Remove the spaces from the hex data to search for in OpenCore.efi

                if OCHexData in hexdata:
                    Logging.info(f"Found OpenCore version: {i[1]}")
                    self.OcVersionLabel['text'] = f"OpenCore Version: {i[1]}"
                    FoundOC = True
                    break

            if FoundOC is False:
                Logging.critical("Couldn't find the version of this OpenCore.efi")
                showerror("Error", "Couldn't find the version of this OpenCore.efi")

        else:
            Logging.warning("No file has been selected")

    def about(self):
        showinfo("About", f"Script to find the OpenCore version from an OpenCore EFI folder.\n\nScript version: {self.Script_Version}\n ")

    def centerwindow(self):
        app_height = 150
        app_width = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (app_width/2))
        y_cordinate = int((screen_height/2) - (app_height/2))
        self.root.geometry(f"{app_width}x{app_height}+{x_cordinate}+{y_cordinate}")


MainWindow()