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
dataFilePath = currentFolderPath + "/adventures.json"
with open(dataFilePath, encoding='utf8') as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/5-adventures.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

for adventure in data:
    adventureID = adventure["id"]

    # Params
    idCampaign = adventure["idCampaign"]
    idLicense = adventure["idLicense"]
    reputation = adventure["reputation"]
    partyXp = adventure["partyXp"]

    sqlFile.write("-- Adventure {}\n".format(adventureID))
    sqlFile.write(
        "INSERT INTO Adventure (id, idCampaign, idLicense, reputation, partyXp) "
        "VALUES ({}, {}, {}, {}, {});\n"
        .format(adventureID, idCampaign, idLicense, reputation, partyXp)
    )
