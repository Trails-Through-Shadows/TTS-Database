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
        sqlFile.write(
            "INSERT INTO Market (id, idLocation) "
            "VALUES ('{}', '{}');\n"
            .format(location["id"], location["id"])
        )

        if "items" in location:
            for itemID in location["items"]["ids"]:
                req = "NULL"

                if str(itemID) in location["items"]["requirements"]:
                    req = location["items"]["requirements"][str(itemID)]

                sqlFile.write(
                    "INSERT INTO MarketItem (idMarket, idItem, requirements) "
                    "VALUES ({}, {}, '{}');\n"
                    .format(location["id"], itemID, req)
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
                    "SET @hexID = (SELECT id FROM Hex WHERE idPart = {} AND qCord = {} AND rCord = {} AND sCord = {});\n"
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
                        .format( hexTypeID, locationID, partScheme)
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

            # First Hex
            sqlFile.write(
                "SET @doorHex = (SELECT id FROM Hex WHERE idPart = {} AND qCord = {} AND rCord = {} AND sCord = {});\n"
                .format(doorFirstPart, doorCordQ, doorCordR, doorCordS)
            )

            sqlFile.write(
                "INSERT INTO PartDoor (location, fromPart, toPart, hex) "
                "VALUES ({}, {}, {}, @doorHex);\n"
                .format(locationID, doorFirstPart, doorSecondPart)
            )

    # Paths
    if "paths" in location:
        for path in location["paths"]:
            sqlFile.write(
                "INSERT INTO Path (idStart, idEnd) "
                "VALUES ({}, {});\n"
                .format(path, location["id"])
            )
