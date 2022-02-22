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

#TODO
# - Get MD5 checksums from a database file

import hashlib, os, datetime, platform, json

Script_Version = "V1.0" 
debug = 0

def clearConsole(): #clear console
    command = 'clear'
    if platform.system() == ("Windows"):  # If system is running Windows
        command = 'cls'
    if platform.system() == ("Darwin"): #If system is running macOS
        command = 'clear'    
    os.system(command)

# heading
terminalwith = os.get_terminal_size().columns
print("\033[1;31m") # change text color to red
clearConsole()
print(("# Welcome to Find OC Version - Script to find the OpenCore version of an OpenCore EFI folder #\n").center(terminalwith))

# debug mode
setdebug = input('Would you like to enable debug mode? (default = no) '+ "Options: Y or N \n" )
if setdebug in ['yes', 'Yes', 'Y', 'y']:
  debug = 1
  print("\n" + "Enabled debug mode")
else:
  debug = 0

inputfile = input("\nDrag & drop OpenCore.efi: ").strip()

if debug == 1:
    print("\nDetected platform: " + platform.system()) # Print the current platform

if platform.system() == ('Windows'):  # If system is running Windows
    fixedinputfile = inputfile.replace('"', ' ').strip() # Remove quotation marks from the inputfile string. Otherwise checkinputfile will return false.
    if debug == 1:
        print("\nDetected Windows system")

elif platform.system() == ("Darwin"): #If system is running macOS
    fixedinputfile = inputfile.replace("\\",  '')  # Remove the backslashes from the inputfile string. Otherwise checkinputfile will return false.
    if debug == 1:
        print("\nDetected macOS system")
else:
    print("\nCould not detect Windows or macOS Operating System. This script currently only supports Windows and macOS")
    exit()

if debug == 1:
    print("\nfixed input file: " + fixedinputfile)

checkinputfile = os.path.isfile (fixedinputfile)

if debug == 1:
    if checkinputfile == 1:
        print("Found the input file")

if checkinputfile == 0:
  print("Couldn't find the file")
  print("Script will now exit")
  exit()  

md5_hash = hashlib.md5()
a_file = open(fixedinputfile, "rb")
content = a_file.read()
md5_hash.update(content)
digest = md5_hash.hexdigest()

if debug == 1:
    print("\nmd5 checksum: " + digest)

# Read database file
with open('Database.json') as file:
    database = file.read()

# Parse json file
databasedata = json.loads(database)
if debug == 1:
    print("Database data: ", databasedata)

print("\nOpencore Version: ", end = '')

if digest not in databasedata:
    print("OC Version not in database. Please update the database using GetOCMD5 for the latest OpenCore version. Note that only Opencore Releases from GitHub are supported!")
    exit()

print(databasedata[digest])

#end of script
print("\n\n\n\n\nThanks for using Find OC Version " + Script_Version)
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