import json

# Read database file
with open('Database.json') as file:
    database = file.read()

# Parse json file
databasedata = json.loads(database) 

key = "0.7.5 MD5"

value = "OC 0.7.5 DEBUG"

databasedata[key] = value 

with open('Database.json', 'w') as file: # Open the database in write mode as file
    json.dump(databasedata, file, indent=4) # write json data to file with 4 spaces in the beginning of a line  