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

#TODO
# - get both release and debug versions
# - store the md5 checksums in a database file

import datetime,  platform, os, urllib, shutil, zipfile, hashlib, getpass
from pydoc import Doc
from urllib.request import urlopen

Script_Version = "V0.1"
debug = 0
def clearConsole(): #clear console
    command = 'clear'
    if platform.system() == ("Windows"):  # If system is running Windows
        command = 'cls'
    if platform.system() == ("Darwin"): #If system is running macOS
        command = 'clear'    
    os.system(command)

clearConsole()
print('\nWelcome to Get OC MD5! A tool to get OpenCore.efi MD5 checksum\n')

# debug mode
setdebug = input('Would you like to enable debug mode? (default = no) '+ "Options: Y or N \n" )
if setdebug in ['yes', 'Yes', 'Y', 'y']:
  debug = 1
  print("\n" + "Enabled debug mode\n")
else:
  debug = 0

OCversion = input("Which OpenCore version do you want to download? ")

if debug == 1:
    print("\nChosen version: " + OCversion)

if OCversion >= "0.0.1" and OCversion <= "0.0.3":
    urlrelease = "https://github.com/acidanthera/OpenCorePkg/releases/download/" + OCversion  + "/OpenCore-V"+ OCversion + "-RELEASE.zip"
    urldebug = "https://github.com/acidanthera/OpenCorePkg/releases/download/" + OCversion  + "/OpenCore-v"+ OCversion + "-DEBUG.zip"

elif OCversion >= "0.5.0" and OCversion <= "0.7.8" or OCversion == "0.0.4":
    urlrelease = "https://github.com/acidanthera/OpenCorePkg/releases/download/" + OCversion  + "/OpenCore-"+ OCversion + "-RELEASE.zip" # from version 0.0.4 and up "v" is removed from the download url
    urldebug = "https://github.com/acidanthera/OpenCorePkg/releases/download/" + OCversion  + "/OpenCore-"+ OCversion + "-DEBUG.zip"   

else:
    print("Can't get this version from GitHub!")  
    exit()  

if debug == 1:
    print ("\nOC release URL: " + urlrelease)  
    print ("\nOC debug URL: " + urldebug) 

custompath = input('\nWould you like to use a custom path for the OpenCore downloads? By default the script will store the OpenCore downloads in the documents folder. (default = no) '+ "Options: Y or N \n" )
if custompath in ['yes', 'Yes', 'Y', 'y']:
  if debug == 1:
        print("\nYou chose to use a custom path")  
  path = input("\nDrag & drop the path where you want to store OpenCore downloads: ")

else:
    DocPath = os.path.expanduser('~/Documents')
    path = DocPath + "/GetOCMD5"
    if not os.path.exists(path):
        os.makedirs(path)
    if debug == 1:    
        print("DocPath: " + DocPath)

print("Path: " + path)

if platform.system() == ('Windows'):  # If system is running Windows
    fixedinputpath = path.replace('"', ' ').strip() # Remove quotation marks from the inputfile string. Otherwise checkinputfile will return false.
    fixedinputpath2 = fixedinputpath
    if debug == 1:
        print("\nDetected Windows system")

elif platform.system() == ("Darwin"): #If system is running macOS
    fixedinputpath = path.replace("\\",  '') # Remove the backslashes from the inputfile string. Otherwise checkinputfile will return false.
    fixedinputpath2 = fixedinputpath.replace(" ",  "") # Remove the spaces from the inputfile string. Otherwise checkinputfile will return false.
    if debug == 1:
        print("\nDetected macOS system")
else:
    print("\nCouldn't detect Windows or macOS Operating System. This script currently only supports Windows and macOS! Script will now exit.")
    exit()

if debug == 1:
    print("\nfixed input path: " + fixedinputpath2)

checkpath = os.path.isdir (fixedinputpath2)

if debug == 1:
    if checkpath == 1:
        print("\nFound the path")

if checkpath == 0:
  print("\nCouldn't find the specified path where OpenCore.zip needs to be saved! Script will now exit.")
   
if platform.system() == ("Windows"):  # If system is running Windows
        OCZip_path = fixedinputpath2 + "\OpenCore-" + OCversion + "-RELEASE.zip" # path to write OpenCore.zip
if platform.system() == ("Darwin"): #If system is running macOS
        OCZip_path = fixedinputpath2 + "/OpenCore-" + OCversion + "-RELEASE.zip" # path to write OpenCore.zip        

if debug == 1:
    print("\nPath: " + fixedinputpath2)
    print("\nFixed path: " + OCZip_path)
    
try:
    site = urllib.request.urlopen(urlrelease)
    if debug == 1:
        print("\nFound the url")
except:
    print("\nFailed to download file")
    
download = urllib.request.urlretrieve(urlrelease, OCZip_path)
if debug == 1:
    print ("\nDownloaded the file")

# Create tmp directory
temppath = fixedinputpath2 + '/tmp'

if os.path.exists(temppath):
    shutil.rmtree(temppath)
    if debug == 1:
      print("\nFound an existing tmp directory.")
      print("\nRemoved existing tmp folder.")

os.makedirs(temppath)
if debug == 1:
    print("\nCreated tmp directory")

# Unzip downloaded OpenCore.zip
with zipfile.ZipFile(OCZip_path, 'r') as zip_ref:
    zip_ref.extractall(temppath)
if debug == 1:
    print("\nUnzipped the OpenCore.zip for to tmp directory")    

# Finally! Get the MD5 checksum
if OCversion >= "0.6.2": # Since OC 0.6.2 the X64 folder is used
    if platform.system() == ("Windows"): # If system is running Windows
        OpenCoreEFIFile = temppath + "\X64\EFI\OC\OpenCore.efi"    
    if platform.system() == ("Darwin"): # If system is running macOS
        OpenCoreEFIFile = temppath + "/X64/EFI/OC/OpenCore.efi" 
else:
    if platform.system() == ("Windows"): # If system is running Windows
        OpenCoreEFIFile = temppath + "\EFI\OC\OpenCore.efi"     
    if platform.system() == ("Darwin"): # If system is running macOS
        OpenCoreEFIFile = temppath + "/EFI/OC/OpenCore.efi"  
     
if debug == 1:
    print("\nOpenCore.efi file: " + OpenCoreEFIFile)

md5_hash = hashlib.md5()
a_file = open(OpenCoreEFIFile, "rb")
content = a_file.read()
md5_hash.update(content)
digest = md5_hash.hexdigest()

print("\n\nmd5 checksum of OpenCore.efi: " + digest)

# End of script
print("\n\n\n\n\nThanks for using Get OC MD5 " + Script_Version)
print("\nWritten By Core i99 - © Stijn Rombouts 2021\n")
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