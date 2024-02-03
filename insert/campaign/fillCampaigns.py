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
dataFilePath = currentFolderPath + "/campaigns.json"
with open(dataFilePath, encoding='utf8') as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/4-campaigns.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

for campaign in data:
    campaignID = campaign["id"]

    # Params
    campaignTitle = campaign["title"]
    campaignDesc = campaign["description"]
    campaignStart = campaign["startLocation"]
    campaignFinish = campaign["finishLocation"]

    # Escape double quotes
    campaignTitle = campaignTitle.replace('"', '\\"')
    campaignDesc = campaignDesc.replace('"', '\\"')

    # Escape single quotes
    campaignTitle = campaignTitle.replace("'", "\\'")
    campaignDesc = campaignDesc.replace("'", "\\'")

    sqlFile.write("-- Campaign {}\n".format(campaignTitle))
    sqlFile.write(
        "INSERT INTO Campaign (id, title, description) "
        "VALUES ('{}', '{}', '{}');\n"
        .format(campaignID, campaignTitle, campaignDesc)
    )

    # Locations
    for location in campaign["locations"]:
        sqlFile.write(
            "INSERT INTO CampaignLocation (idCampaign, idLocation, winCondition, `start`, `finish`) "
            "VALUES ('{}', '{}', '{}', {}, {});\n"
            .format(campaignID, location["id"], str(location["winCondition"])
                    .replace("'", "\""), campaignStart == location["id"], location["id"] in campaignFinish)
        )

    # Achievements
    for achievement in campaign["achievements"]:
        sqlFile.write(
            "INSERT INTO CampaignAchievements (idCampaign, idAchievement) "
            "VALUES ('{}', '{}');\n"
            .format(campaignID, achievement)
        )

    for path in campaign["paths"]:
        sqlFile.write(
            "INSERT INTO LocationPath (idCampaign, idStart, idEnd) "
            "VALUES ('{}', '{}', '{}');\n"
            .format(campaignID, path["from"], path["to"])
        )
