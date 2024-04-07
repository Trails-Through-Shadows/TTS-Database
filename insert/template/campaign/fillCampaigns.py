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
dataFilePath = currentFolderPath + "/campaigns.json"
with open(dataFilePath, encoding='utf8') as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/5-campaigns.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

for entry in data:
    entryID = entry["id"]
    sqlFile.write("-- Campaign {}\n".format(entryID))

    campaignStart = entry["startLocation"]
    campaignFinish = entry["finishLocation"]

    sqlFile.write(
        "INSERT INTO Campaign (id, title, description) "
        "VALUES ('{}', '{}', '{}');\n"
        .format(entryID,
                replaceQuotes(entry["title"]),
                replaceQuotes(entry["description"])
        )
    )

    # Locations
    for location in entry["locations"]:
        if location["winCondition"] != 'NULL':
            l_type = location["winCondition"]["type"]
            l_value = location["winCondition"]["value"]
            winCondition = "{" + '"type": "{}", "value": {}'.format(l_type, l_value) + "}"
        else:
            winCondition = 'NULL'

        starting = location["id"] == campaignStart
        finishing = location["id"] in campaignFinish

        sqlFile.write(
            "INSERT INTO CampaignLocation (idCampaign, idLocation, winCondition, `start`, `finish`) "
            "VALUES ('{}', '{}', '{}', {}, {});\n"
            .format(entryID,
                    location["id"],
                    winCondition,
                    starting,
                    finishing
            )
        )

    # Achievements
    for achievement in entry["achievements"]:
        sqlFile.write(
            "INSERT INTO CampaignAchievements (idCampaign, idAchievement) "
            "VALUES ({}, {});\n"
            .format(entryID, achievement)
        )

    # Paths
    for path in entry["paths"]:
        sqlFile.write(
            "INSERT INTO LocationPath (idCampaign, idStart, idEnd) "
            "VALUES ({}, {}, {});\n"
            .format(entryID, path["from"], path["to"])
        )
