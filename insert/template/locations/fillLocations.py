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
dataFilePath = currentFolderPath + "/locations.json"
with open(dataFilePath, "r") as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/3-locations.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

# Iterate through the JSON data and insert records into tables
for entry in data:
    entryID = entry["id"]
    sqlFile.write("-- Location {}\n".format(entryID))

    # Insert location
    sqlFile.write(
        "INSERT INTO Location (id, title, tag, type, description) "
        "VALUES ({}, '{}', '{}', '{}', '{}');\n"
        .format(entryID,
                replaceQuotes(entry["title"]),
                entry["tag"],
                entry["type"],
                replaceQuotes(entry["description"])
        )
    )

    if entry["type"] == "MARKET":
        if "items" in entry:
            for itemID in entry["items"]["ids"]:
                price = "NULL"
                amount = "NULL"

                if str(itemID) in entry["items"]["prices"]:
                    price = entry["items"]["prices"][str(itemID)]

                if str(itemID) in entry["items"]["amounts"]:
                    amount = entry["items"]["amounts"][str(itemID)]

                sqlFile.write(
                    "INSERT INTO Market (idLocation, idItem, defPrice, defAmount) "
                    "VALUES ({}, {}, {}, {});\n"
                    .format(entryID, itemID, price, amount)
                )

    # Parts
    if "parts" in entry:
        for part in entry["parts"]:

            # Insert Part
            sqlFile.write(
                "INSERT INTO LocationPart (idLocation, idPart, rotation) "
                "VALUES ({}, {}, {});\n"
                .format(entryID,
                        part["part"],
                        part["rotation"])
            )

    #Start
    if "startHexes" in entry:
        for startHex in entry["startHexes"]:

            # Insert Start Hexes
            sqlFile.write(
                "INSERT INTO LocationStart (idLocation, idPart, idHex) "
                "VALUES ({}, {}, {});\n"
                .format(entryID,
                        startHex["idPart"],
                        startHex["idHex"]
                )
            )

    # Doors
    if "doors" in entry:
        for door in entry["doors"]:

            # Insert Door
            sqlFile.write(
                "INSERT INTO LocationDoor (idLocation, idPartFrom, idPartTo, qCoord, rCoord, sCoord) "
                "VALUES ({}, {}, {}, {}, {}, {});\n"
                .format(entryID,
                        door["key"]["idPartFrom"],
                        door["key"]["idPartTo"],
                        door["q"],
                        door["r"],
                        door["s"]
                )
            )

    # Enemies
    if "enemies" in entry:
        for enemy in entry["enemies"]:

            # Insert Enemy
            sqlFile.write(
                "INSERT INTO HexEnemy (idEnemy, idLocation, idPart, idHex) "
                "VALUES ({}, {}, {}, {});\n"
                .format(enemy["enemy"],
                        entryID,
                        enemy['key']["idPart"],
                        enemy['key']["idHex"],
                )
            )

    # Obstacles
    if "obstacles" in entry:
        for obstacle in entry["obstacles"]:

            # Insert Obstacle
            sqlFile.write(
                "INSERT INTO HexObstacle (idObstacle, idLocation, idPart, idHex) "
                "VALUES ({}, {}, {}, {});\n"
                .format(obstacle["obstacle"],
                        entryID,
                        obstacle["key"]["idPart"],
                        obstacle["key"]["idHex"],
                )
            )
