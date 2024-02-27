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
dataFilePath = currentFolderPath + "/summons.json"
with open(dataFilePath, encoding='utf8') as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/2-summons.sql"
lateSqlFilePath = currentFolderPath + "/3-summons-late.sql"
sqlFile = open(sqlFilePath, "w")
lateSqlFile = open(lateSqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
lateSqlFile.truncate(0)
sqlFile.flush()
lateSqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

for entry in data:
    entryID = entry["id"]
    sqlFile.write("-- Summon {}\n".format(entryID))

    sqlFile.write(
        "INSERT INTO Summon (id, title, tag, duration, health, idAction) "
        "VALUES ({}, '{}', '{}', {}, {}, {}); \n"
        .format(entryID,
                replaceQuotes(entry["title"]),
                entry["tag"],
                entry["duration"],
                entry["health"],
                'NULL'
        )
    )

    # Insert effects
    for effect in entry["effects"]:
        sqlFile.write(
            "INSERT INTO SummonEffect (idSummon, idEffect) "
            "VALUES ({}, {});\n"
            .format(entryID, effect["key"]["idEffect"])
        )

    lateSqlFile.write(
        "UPDATE Summon SET idAction = {} WHERE id = {};\n"
        .format(entry["action"], entryID)
    )

