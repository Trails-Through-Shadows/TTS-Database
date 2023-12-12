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
dataFilePath = currentFolderPath + "/races.json"
with open(dataFilePath, encoding='utf8') as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/2-races.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

for race in data:
    raceID = race["id"]

    # Params
    raceName = race["name"]
    raceEffects = race["effects"]
    raceActions = race["actions"]

    sqlFile.write("-- Race {}\n".format(raceName))
    sqlFile.write(
        "INSERT INTO Race (id, name) "
        "VALUES ({}, '{}');\n"
        .format(raceID, raceName)
    )

    # Actions
    for action in raceActions:
        actionID = action["id"]

        # Params
        actionLevelReq = action["levelReq"]

        sqlFile.write(
            "INSERT INTO RaceAction (id, idRace, levelReq, idAction) "
            "VALUES ({}, {}, {}, {});\n"
            .format("NULL", raceID, actionLevelReq, actionID)
        )

    # Effects
    for effect in raceEffects:
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
            "INSERT INTO RaceEffect (idRace, idEffect, levelReq) "
            "VALUES ({}, @idEffect, {});\n".format(raceID, lvlReq)
        )