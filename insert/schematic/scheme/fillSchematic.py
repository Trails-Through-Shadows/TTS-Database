import json
import os

# Get current file path even if it's executed from another file
currentFolderPath = os.path.dirname(os.path.realpath(__file__))

# Open the JSON file
dataFilePath = currentFolderPath + "/scheme.json"
with open(dataFilePath, "r") as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/0-schematic.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Iterate through the JSON data and insert records into tables
for schematic in data:
    schematicID = schematic["id"]

    # Params
    schematicTag = schematic["tag"]
    schematicRows = schematic["rows"]

    # Offset Coordinates of schematic center
    found = False
    xCoord = None
    yCoord = None

    sqlFile.write("-- Schematic {}\n".format(schematicTag))
    sqlFile.write(
        "INSERT INTO Part (id, tag) "
        "VALUES ({}, '{}');\n"
        .format(schematicID, schematicTag)
    )

    for y, row in enumerate(schematicRows):
        if found:
            break

        for x, cell in enumerate(row):
            if cell == "o":
                xCoord = x
                yCoord = y
                found = True
                break

    if xCoord is None or yCoord is None:
        exit("Center points not found")

    hexID = 1
    axialCoordinates = []
    for y, row in enumerate(schematicRows):
        for x, cell in enumerate(row):
            if cell == "x" or cell == "o":
                q = round((x - xCoord) - ((y - yCoord) - ((y - yCoord) & 1)) / 2)
                r = round(y - yCoord)
                s = round(-q - r)

                sqlFile.write(
                    "INSERT INTO Hex (idPart, id, qCord, rCord, sCord) "
                    "VALUES ({}, {}, {}, {}, {});\n"
                    .format(schematicID, hexID, q, r, s)
                )

            hexID += 1
