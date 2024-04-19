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

def replaceQuotes(data):
    return data.replace('"', '\\"').replace("'", "\\'")


# Get current file path even if it's executed from another file
currentFolderPath = os.path.dirname(os.path.realpath(__file__))

# Open the JSON file
dataFilePath = currentFolderPath + "/races.json"
with open(dataFilePath, encoding='utf8') as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/3-races.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

for entry in data:
    entryID = entry["id"]
    sqlFile.write("-- Race {}\n".format(entryID))

    # Insert class
    sqlFile.write(
        "INSERT INTO Race (id, title, tag, description, baseInitiative)"
        "VALUES ({}, '{}', '{}', '{}', {});\n"
        .format(entryID,
                replaceQuotes(entry["title"]),
                replaceQuotes(entry["tag"]),
                replaceQuotes(entry["description"]),
                entry["baseInitiative"]
        )
    )

    # Insert effects
    for effect in entry["effects"]:
        sqlFile.write(
            "INSERT INTO RaceEffect (idRace, idEffect, levelReq) "
            "VALUES ({}, {}, {});\n"
            .format(entryID, effect["key"]["idEffect"], effect["levelReq"])
        )

    # Insert actions
    for action in entry["actions"]:
        sqlFile.write(
            "INSERT INTO RaceAction (idRace, idAction) "
            "VALUES ({}, {});\n"
            .format(entryID, action["key"]["idAction"])
        )