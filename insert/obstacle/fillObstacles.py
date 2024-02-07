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
            "INSERT INTO Effect (id, type, duration, `target`, strength) "
            "VALUES ({}, '{}', {}, '{}', {}) "
            "ON DUPLICATE KEY UPDATE id=id;\n"
            .format("NULL", effect["type"], effect["duration"], effect["target"], effect["strength"])
        )

        sqlFile.write(
            "SET @idEffect = (SELECT id FROM Effect WHERE type = '{}' AND duration = {} AND `target` = '{}' AND strength = {});\n"
            .format(effect["type"], effect["duration"], effect["target"], effect["strength"])
        )

        sqlFile.write(
            "INSERT INTO {} VALUES ({}, @idEffect);\n"
            .format(type, id)
        )


# Get current file path even if it's executed from another file
currentFolderPath = os.path.dirname(os.path.realpath(__file__))

# Open the JSON file
dataFilePath = currentFolderPath + "/obstacles.json"
with open(dataFilePath, encoding='utf8') as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/0-obstacles.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

for obstacle in data:
    obstacleID = obstacle["id"]

    # Params
    obstacleTitle = obstacle["title"]
    obstacleTag = obstacle["tag"]
    obstacleDamage = obstacle["baseDamage"]
    obstacleCrossable = obstacle["crossable"]
    obstacleHealth = obstacle["baseHealth"]
    obstacleEffects = obstacle["effects"]

    sqlFile.write("-- Obstacle {}\n".format(obstacleTitle))
    sqlFile.write(
        "INSERT INTO Obstacle (id, title, tag, baseDamage, baseHealth, crossable) "
        "VALUES ({}, '{}', '{}', {}, {}, {});\n"
        .format(obstacleID, obstacleTitle, obstacleTag, obstacleDamage, obstacleHealth, obstacleCrossable)
    )

    insertEffects(obstacleID, obstacleEffects, "ObstacleEffect")