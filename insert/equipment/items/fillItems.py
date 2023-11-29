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

# Create a temp unique index
sqlFile.write("DROP INDEX IF EXISTS `tempUnique` ON Effect;\n")
sqlFile.write("ALTER TABLE Effect ADD UNIQUE INDEX `tempUnique` (type, duration, `range`, strength);\n")

for item in data:
    id = item["id"]
    title = item["title"]
    type = item["type"]
    description = item["description"]

    sqlFile.write("-- Item {}\n".format(title))
    sqlFile.write(
        "INSERT INTO Item (id, title, itemType, description) "
        "VALUES ({}, '{}', '{}', '{}');\n".format(id, title, type, description)
    )

    # Effects
    for effect in item["effects"]:
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
            "INSERT INTO ItemEffect (idItem, idEffect) "
            "VALUES ({}, @idEffect);\n".format(id)
        )

# Drop the unique index
sqlFile.write("-- Drop the unique index\n")
sqlFile.write("ALTER TABLE Effect DROP INDEX `tempUnique`;\n")