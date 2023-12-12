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
dataFilePath = currentFolderPath + "/enemies.json"
with open(dataFilePath, encoding='utf8') as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/2-enemies.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

for enemy in data:
    enemyID = enemy["id"]

    # Params
    enemyName = enemy["name"]
    enemyHealth = enemy["health"]
    enemyDefence = enemy["defence"]
    enemyActions = enemy["actions"]
    enemyEffects = enemy["effects"]

    sqlFile.write("-- Enemy {}\n".format(enemyName))
    sqlFile.write(
        "INSERT INTO Enemy (id, name, health, defence) "
        "VALUES ({}, '{}', {}, {});\n".format(enemyID, enemyName, enemyHealth, enemyDefence)
    )

    # Actions
    for action in enemyActions:
        actionID = action["id"]

        # Params
        actionLvlReq = action["lvlReq"]

        sqlFile.write(
            "INSERT INTO EnemyAction (id, idEnemy, levelReq, idAction) "
            "VALUES ({}, {}, {}, {});\n".format("NULL", enemyID, actionLvlReq, actionID)
        )

    # Effects
    for effect in enemyEffects:
        lvlReq = effect["lvlReq"]
        eff = effect["effect"]

        sqlFile.write(
            "INSERT INTO Effect (id, type, duration, `target`, strength) "
            "VALUES ({}, '{}', {}, '{}', {}) "
            "ON DUPLICATE KEY UPDATE id=id;\n"
            .format("NULL", eff["type"], eff["duration"], eff["target"], eff["strength"])
        )

        sqlFile.write(
            "SET @idEffect = (SELECT id FROM Effect WHERE type = '{}' AND duration = {} AND `target` = '{}' AND strength = {});\n"
            .format(eff["type"], eff["duration"], eff["target"], eff["strength"])
        )

        sqlFile.write(
            "INSERT INTO EnemyEffect (idEnemy, idEffect, levelReq) "
            "VALUES ({}, @idEffect, {});\n".format(enemyID, lvlReq)
        )