import json
import os


# Replace None with NULL recursively
def replaceNoneWithNull(data):
    if isinstance(data, dict):
        for key in data:
            if data[key] is None:
                data[key] = "NULL"
            else:
                data[key] = replaceNoneWithNull(data[key])
    elif isinstance(data, list):
        for i in range(len(data)):
            if data[i] is None:
                data[i] = "NULL"
            else:
                data[i] = replaceNoneWithNull(data[i])
    else:
        if data is None:
            data = "NULL"

    return data


# Get current file path even if it's executed from another file
currentFolderPath = os.path.dirname(os.path.realpath(__file__))

# Open the JSON file
dataFilePath = currentFolderPath + "/characters.json"
with open(dataFilePath, encoding='utf8') as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/5-characters.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

for character in data:
    characterID = character["id"]

    # Params
    idAdventure = character["idAdventure"]
    idClass = character["idClass"]
    idRace = character["idRace"]
    level = character["level"]
    title = character["title"]
    playerName = character["playerName"]

    sqlFile.write("-- Character {}\n".format(characterID))
    sqlFile.write(
        "INSERT INTO `Character` (id, idAdventure, idClass, idRace, `level`, `title`, playerName) "
        "VALUES ({}, {}, {}, {}, {}, '{}', '{}');\n"
        .format(characterID, idAdventure, idClass, idRace, level, title, playerName)
    )
