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

import hashlib, os, datetime, platform

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

print("\nOpencore Version: ", end = '')
if digest == "25b357c3b0d7842e1bb99c18d1367fc0":   # 0.7.8 REL
    print("0.7.8 RELEASE")
elif digest == "7de24a3b50a581765a211fa45055214b": # 0.7.8 DEB
    print("0.7.8 DEBUG")
elif digest == "236d5622b556c56888dae3410dbcf2de": # 0.7.7 REL
    print("0.7.7 RELEASE") 
elif digest == "7c09a5bd5c1554881b0acd1594b971be": # 0.7.7 DEB
    print("0.7.7 DEBUG")     
elif digest == "e8a18dd8bc56ade19eee855d3caad928": # 0.7.6 REL
    print("0.7.6 RELEASE")     
elif digest == "a0f63021d1605fe580eea882f3760823": # 0.7.6 DEB
    print("0.7.6 DEBUG")    
elif digest == "f4ee8bbaf27fcb34367d6192b5db1eec": # 0.7.5 REL
    print("0.7.5 RELEASE")     
elif digest == "5be2c6ee90d95f786e8d511ce2124055": # 0.7.5 DEB
    print("0.7.5 DEBUG")   
elif digest == "81a2ac329da9548da0ab0cb140eb9661": # 0.7.4 REL
    print("0.7.4 RELEASE")     
elif digest == "95497990f2dde60661ec66c57f55a28b": # 0.7.4 DEB
    print("0.7.4 DEBUG")   
elif digest == "95a3f5b7df5e3aee7f44588d56fe1cd3": # 0.7.3 REL
    print("0.7.3 RELEASE")     
elif digest == "bda0fed36bdb3301c1b788f8259c74fe": # 0.7.3 DEB
    print("0.7.3 DEBUG")  
elif digest == "1314c4f3220539d997637fa0b57026b5": # 0.7.2 REL
    print("0.7.2 RELEASE")     
elif digest == "9848c07e173aa448ea701b3ed0e210b5": # 0.7.2 DEB
    print("0.7.2 DEBUG")  
elif digest == "1160d5af5f29ef17c2c870862f2a4728": # 0.7.1 REL
    print("0.7.1 RELEASE")     
elif digest == "9001a6107a0db056e896cf68c26471c8": # 0.7.1 DEB
    print("0.7.1 DEBUG")  
elif digest == "67406c9656c353aa8919c8930c897c3c": # 0.7.0 REL
    print("0.7.0 RELEASE")     
elif digest == "26f6d78711ec93afededcee86abe7c8d": # 0.7.0 DEB
    print("0.7.0 DEBUG")    
elif digest == "33dc9e8185b66f4ab466890590011351": # 0.6.9 REL
    print("0.6.9 RELEASE")     
elif digest == "5b8545e031bd9341f7bc20fe313cc390": # 0.6.9 DEB
    print("0.6.9 DEBUG")    

else: 
    print("Could not find OpenCore version. Please update the script, or edit it for the newest OpenCore versions.")  
    exit()  

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