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
dataFilePath = currentFolderPath + "/summons.json"
with open(dataFilePath, encoding='utf8') as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/0-summons.sql"
lateSqlFilePath = currentFolderPath + "/2-summons-late.sql"
sqlFile = open(sqlFilePath, "w")
lateSqlFile = open(lateSqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
lateSqlFile.truncate(0)
sqlFile.flush()
lateSqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

for summon in data:
    summonID = summon["id"]

    # Params
    summonName = summon["name"]
    summonDuration = summon["duration"]
    summonHealth = summon["health"]
    summonStyle = summon["combatStyle"]

    summonAction = summon["action"]
    summonEffects = []
    if summon.get('effects') is not None:
        summonEffects = summon["effects"]

    sqlFile.write("-- Summon {}\n".format(summonName))
    sqlFile.write(
        "INSERT INTO Summon (id, name, duration, health, combatStyle, idAction) "
        "VALUES ({}, '{}', {}, {}, '{}', {}); \n"
        .format(summonID, summonName, summonDuration, summonHealth, summonStyle, 'NULL')
    )

    lateSqlFile.write(
        "UPDATE Summon "
        "SET idAction = {} "
        "WHERE id = {};\n"
        .format(summonAction, summonID)
    )

    insertEffects(summonID, summonEffects, "SummonEffect")
