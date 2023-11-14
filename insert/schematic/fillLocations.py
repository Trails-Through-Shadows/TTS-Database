import json
import os

# Get current file path even if it's executed from another file
currentFolderPath = os.path.dirname(os.path.realpath(__file__))

# Open the JSON file
dataFilePath = currentFolderPath + "/locations.json"
with open(dataFilePath, "r") as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/locations.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Iterate through the JSON data and insert records into tables
for location in data:
    sqlFile.write(
        "INSERT INTO Location (id, title, type, description) "
        "VALUES ('{}', '{}', '{}', '{}');\n"
        .format(location["id"], location["title"], location["type"], location["description"])
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
                    "VALUES ('{}', '{}', '{}');\n"
                    .format(location["id"], str(itemID), req)
                )

    # Get json
    if "parts" in location:
        for part in location["parts"]:
            sqlFile.write(
                "INSERT INTO Part (id) "
                "VALUES ('{}');\n"
                .format(str(part["id"]))
            )

            # LocationPart Relationship
            sqlFile.write(
                "INSERT INTO LocationPart (idLocation, idPart) "
                "VALUES ('{}', '{}');\n"
                .format(location["id"], str(part["id"]))
            )

            # Hexes
            for i in range(1, int(part["hexCount"])):
                sqlFile.write(
                    "INSERT INTO Hex (idPart, id) "
                    "VALUES ('{}', '{}');\n"
                    .format(str(part["id"]), i)
                )

                # HexEnemy or HexObstacle
                if str(i) in part["hexes"]:
                    hex = part["hexes"][str(i)]
                    hexType = hex["type"]

                    if hexType == "ENEMY":
                        sqlFile.write(
                            "INSERT INTO HexEnemy (idEnemy, idLocation, idPart, idHex) "
                            "VALUES ('{}', '{}', '{}', '{}');\n"
                            .format(hex["id"], location["id"], str(part["id"]), i)
                        )
                    elif hexType == "OBSTACLE":
                        sqlFile.write(
                            "INSERT INTO HexObstacle (idObstacle, idLocation, idPart, idHex) "
                            "VALUES ('{}', '{}', '{}', '{}');\n"
                            .format(hex["id"], location["id"], str(part["id"]), i)
                        )

    # Doors
    if "doors" in location:
        for door in location["doors"]:
            sqlFile.write(
                "INSERT INTO HexDoor (idLocation, firstPart, secondPart, firstHex, secondHex, firstEdge, secondEdge) "
                "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');\n"
                .format(location["id"],
                        str(door["first"]["partId"]), str(door["second"]["partId"]),
                        str(door["first"]["hexId"]), str(door["second"]["hexId"]),
                        door["first"]["edge"], door["second"]["edge"])
            )

    # Paths
    if "paths" in location:
        for path in location["paths"]:
            sqlFile.write(
                "INSERT INTO Path (idStart, idEnd) "
                "VALUES ('{}', '{}');\n"
                .format(path, str(location["id"]))
            )
