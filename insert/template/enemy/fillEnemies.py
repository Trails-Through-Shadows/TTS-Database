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
dataFilePath = currentFolderPath + "/enemies.json"
with open(dataFilePath, encoding='utf8') as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/3-enemies.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

for entry in data:
    entryID = entry["id"]
    sqlFile.write("-- Enemy {}\n".format(entryID))

    # Insert enemy
    sqlFile.write(
        "INSERT INTO Enemy (id, title, tag, description, baseHealth, baseDefence, baseInitiative, usages) "
        "VALUES ({}, '{}', '{}', '{}', {}, {}, {}, {});\n"
        .format(entryID,
                replaceQuotes(entry["title"]),
                replaceQuotes(entry["tag"]),
                replaceQuotes(entry["description"]),
                entry["baseHealth"],
                entry["baseDefence"],
                entry["baseInitiative"],
                0
        )
    )

    # Insert effects
    for effect in entry["effects"]:
        sqlFile.write(
            "INSERT INTO EnemyEffect (idEnemy, idEffect) "
            "VALUES ({}, {});\n"
            .format(entryID, effect["key"]["idEffect"])
        )

    # Insert actions
    for effect in entry["actions"]:
        sqlFile.write(
            "INSERT INTO EnemyAction (idEnemy, idAction) "
            "VALUES ({}, {});\n"
            .format(entryID, effect["key"]["idAction"])
        )