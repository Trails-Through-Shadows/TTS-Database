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
dataFilePath = currentFolderPath + "/parts.json"
with open(dataFilePath, "r") as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/0-parts.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

# Iterate through the JSON data and insert records into tables
for entry in data:
    entryID = entry["id"]
    sqlFile.write("-- Part {}\n".format(entryID))

    # Insert Part
    sqlFile.write(
        "INSERT INTO Part (id, title, tag, usages) "
        "VALUES ({}, '{}', '{}', {});\n"
        .format(entryID,
                replaceQuotes(entry["title"]),
                entry["tag"],
                0
        )
    )

    # Insert Hexes
    for hex in entry["hexes"]:
        sqlFile.write(
            "INSERT INTO Hex (idPart, id, qCoord, rCoord, sCoord) "
            "VALUES ({}, {}, {}, {}, {});\n"
            .format(entryID,
                    hex["key"]["id"],
                    hex["q"],
                    hex["r"],
                    hex["s"]
            )
        )
