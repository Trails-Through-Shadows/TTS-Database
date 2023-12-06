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


def insertEffects(id, effects: [], type: str) -> int:
    for effect in effects:
        sqlFile.write(
            "INSERT INTO Effect (id, type, duration, `range`, strength) "
            "VALUES ({}, '{}', {}, '{}', {}) "
            "ON DUPLICATE KEY UPDATE id=id;\n"
            .format("NULL", effect["type"], effect["duration"], effect["range"], effect["strength"])
        )

        sqlFile.write(
            "SET @idEffect = (SELECT id FROM Effect WHERE type = '{}' AND duration = {} AND `range` = '{}' AND strength = {});\n"
            .format(effect["type"], effect["duration"], effect["range"], effect["strength"])
        )

        sqlFile.write(
            "INSERT INTO {} VALUES ({}, @idEffect);\n"
            .format(type, id)
        )


# Get current file path even if it's executed from another file
currentFolderPath = os.path.dirname(os.path.realpath(__file__))

# Open the JSON file
dataFilePath = currentFolderPath + "/items.json"
with open(dataFilePath, encoding='utf8') as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/0-items.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

for item in data:
    itemID = item["id"]

    # Params
    itemTitle = item["title"]
    itemType = item["type"]
    itemDesc = item["description"]
    itemEffects = item["effects"]

    sqlFile.write("-- Item {}\n".format(itemTitle))
    sqlFile.write(
        "INSERT INTO Item (id, title, type, description) "
        "VALUES ({}, '{}', '{}', '{}');\n".format(itemID, itemTitle, itemType, itemDesc)
    )

    insertEffects(itemID, itemEffects, "ItemEffect")
