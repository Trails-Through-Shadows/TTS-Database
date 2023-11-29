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

# Create a temp unique index
sqlFile.write("DROP INDEX IF EXISTS `tempUnique` ON Effect;\n")
sqlFile.write("ALTER TABLE Effect ADD UNIQUE INDEX `tempUnique` (type, duration, `range`, strength);\n")

for enemy in data:
    id = enemy["id"]
    name = enemy["name"]
    health = enemy["health"]
    defence = enemy["defence"]

    sqlFile.write("-- Enemy {}\n".format(name))
    sqlFile.write(
        "INSERT INTO Enemy (id, name, health, defence) "
        "VALUES ({}, '{}', {}, {});\n".format(id, name, health, defence)
    )

    # Actions
    for action in enemy["actions"]:
        lvlReq = action["lvlReq"]
        actionID = action["id"]

        sqlFile.write(
            "INSERT INTO EnemyAction (id, idEnemy, levelReq, idAction) "
            "VALUES ({}, {}, {}, {});\n".format("NULL", id, lvlReq, actionID)
        )

    # Effects
    if "effects" in enemy:
        for effect in enemy["effects"]:
            lvlReq = effect["lvlReq"]
            eff = effect["effect"]

            sqlFile.write(
                "INSERT INTO Effect (id, type, duration, `range`, strength) "
                "VALUES ({}, '{}', {}, '{}', {}) "
                "ON DUPLICATE KEY UPDATE id=id;\n"
                .format("NULL", eff["type"], eff["duration"], eff["range"], eff["strength"])
            )

            sqlFile.write(
                "SET @idEffect = (SELECT id FROM Effect WHERE type = '{}' AND duration = {} AND `range` = '{}' AND strength = {});\n"
                .format(eff["type"], eff["duration"], eff["range"], eff["strength"])
            )

            sqlFile.write(
                "INSERT INTO EnemyEffect (idEnemy, idEffect, levelReq) "
                "VALUES ({}, @idEffect, {});\n".format(id, lvlReq)
            )

# Drop the unique index
sqlFile.write("-- Drop the unique index\n")
sqlFile.write("ALTER TABLE Effect DROP INDEX `tempUnique`;\n")