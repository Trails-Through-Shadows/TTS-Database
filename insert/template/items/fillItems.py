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
dataFilePath = currentFolderPath + "/items.json"
with open(dataFilePath, encoding='utf8') as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/3-items.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

for entry in data:
    entryID = entry["id"]
    sqlFile.write("-- Item {}\n".format(entryID))

    sqlFile.write(
        "INSERT INTO Item (id, title, tag, type, description, idAction) "
        "VALUES ({}, '{}', '{}', '{}', '{}', {});\n"
        .format(entryID,
                entry["title"],
                entry["tag"],
                entry["type"],
                entry["description"],
                entry["idAction"]
        )
    )

    # Insert effects
    for effect in entry["effects"]:
        sqlFile.write(
            "INSERT INTO ItemEffect (idItem, idEffect) "
            "VALUES ({}, {});\n"
            .format(entryID, effect["key"]["idEffect"])
        )
