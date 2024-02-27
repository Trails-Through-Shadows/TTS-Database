import json
import os

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

# Iterate through the JSON data and insert records into tables
for location in data:
    locationID = location["id"]

    # Params
    locationTitle = location["title"]
    locationTag = location["tag"]
    locationType = location["type"]
    locationDesc = location["description"]

    sqlFile.write("-- Location {}\n".format(locationTag))
    sqlFile.write(
        "INSERT INTO Location (id, title, tag, type, description) "
        "VALUES ({}, '{}', '{}', '{}', '{}');\n"
        .format(locationID, locationTitle, locationTag, locationType, locationDesc)
    )

    if location["type"] == "MARKET":
        if "items" in location:
            for itemID in location["items"]["ids"]:
                price = "NULL"
                amount = "NULL"

                if str(itemID) in location["items"]["prices"]:
                    price = location["items"]["prices"][str(itemID)]

                if str(itemID) in location["items"]["amounts"]:
                    amount = location["items"]["amounts"][str(itemID)]

                sqlFile.write(
                    "INSERT INTO Market (idLocation, idItem, defPrice, defAmount) "
                    "VALUES ({}, {}, {}, {});\n"
                    .format(location["id"], itemID, price, amount)
                )

    # Parts
    if "parts" in location:
        for part in location["parts"]:

            # Params
            partScheme = part["scheme"]
            partRotation = part["rotation"]
            partHexes = part["hexes"]

            #HexEnemy relationship
            # Hexes
            for hex in partHexes:

                # Params
                hexType = hex["type"]
                hexTypeID = hex["id"]
                hexCordR = hex["cords"]["r"]
                hexCordQ = hex["cords"]["q"]
                hexCordS = hex["cords"]["s"]

                # Get Hex ID
                sqlFile.write(
                    "SET @hexID = (SELECT id FROM Hex WHERE idPart = {} AND qCoord = {} AND rCoord = {} AND sCoord = {});\n"
                    .format(partScheme, hexCordQ, hexCordR, hexCordS)
                )

                if hexType == "ENEMY":
                    sqlFile.write(
                        "INSERT INTO HexEnemy (idEnemy, idLocation, idPart, idHex) "
                        "VALUES ({}, {}, {}, @hexID);\n"
                        .format(hexTypeID, locationID, partScheme)
                    )
                elif hexType == "OBSTACLE":
                    sqlFile.write(
                        "INSERT INTO HexObstacle (idObstacle, idLocation, idPart, idHex) "
                        "VALUES ({}, {}, {}, @hexID);\n"
                        .format(hexTypeID, locationID, partScheme)
                    )

            #Start
            if "start" in part:
                for start in part["start"]:

                    # Params
                    startCordR = start["r"]
                    startCordQ = start["q"]
                    startCordS = start["s"]

                    # First hex
                    sqlFile.write(
                        "SET @hexID = (SELECT id FROM Hex WHERE idPart = {} AND qCoord = {} AND rCoord = {} AND sCoord = {});\n"
                        .format(partScheme, startCordQ, startCordR, startCordS)
                    )

                    sqlFile.write(
                        "INSERT INTO LocationStart (idLocation, idPart, idHex) "
                        "VALUES ({}, {}, @hexID);\n"
                        .format(locationID, partScheme)
                    )

            # LocationPart Relationship
            sqlFile.write(
                "INSERT INTO LocationPart (idLocation, idPart, rotation) "
                "VALUES ({}, {}, {});\n"
                .format(locationID, partScheme, partRotation)
            )

    # Doors
    if "doors" in location:
        for door in location["doors"]:

            # Params
            doorFirstPart = door["firstPart"]
            doorSecondPart = door["secondPart"]
            doorCordR = door["cords"]["r"]
            doorCordQ = door["cords"]["q"]
            doorCordS = door["cords"]["s"]

            sqlFile.write(
                "INSERT INTO LocationDoor (idLocation, idPartFrom, idPartTo, qCoord, rCoord, sCoord) "
                "VALUES ({}, {}, {}, {}, {}, {});\n"
                .format(locationID, doorFirstPart, doorSecondPart, doorCordQ, doorCordR, doorCordS)
            )