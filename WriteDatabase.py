from dataclasses import dataclass
import json

digest = "testingtest"

# Read database file
with open('Database.json') as file:
    database = file.read()

# Parse json file
databasedata = json.loads(database)
print("Database data: ", databasedata)

print("\nOpencore Version: ", end = '')


#fruit_json = {"apple" : "1", "orange" : "2"}

key = "0.7.5 MD5"

value = "OC 0.7.5 DEBUG"

databasedata[key] = value

print("new data: ", databasedata)