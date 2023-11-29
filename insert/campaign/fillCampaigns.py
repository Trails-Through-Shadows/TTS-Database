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
    id = campaign["id"]
    title = campaign["title"]
    description = campaign["description"]

    # Escape double quotes
    title = title.replace('"', '\\"')
    description = description.replace('"', '\\"')

    # Escape single quotes
    title = title.replace("'", "\\'")
    description = description.replace("'", "\\'")

    sqlFile.write(
        "INSERT INTO Campaign (id, title, description) "
        "VALUES ('{}', '{}', '{}');\n"
        .format(id, title, description)
    )

    # Locations
    for location in campaign["locations"]:
        sqlFile.write(
            "INSERT INTO CampaignLocation (idCampaign, idLocation) "
            "VALUES ('{}', '{}');\n"
            .format(id, location)
        )

    # Achievements
    for achievement in campaign["achievements"]:
        sqlFile.write(
            "INSERT INTO CampaignAchievements (idCampaign, idAchievement) "
            "VALUES ('{}', '{}');\n"
            .format(id, achievement)
        )
