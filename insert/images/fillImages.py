import json
import os


# Get current file path even if it's executed from another file
currentFolderPath = os.path.dirname(os.path.realpath(__file__))

# Open the JSON file
dataFilePath = currentFolderPath + "/images.json"
with open(dataFilePath, encoding='utf8') as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/0-images.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

for image in data:
    imageTag = image["tag"]
    imageUrl = image["url"]

    sqlFile.write(
        "INSERT INTO ImageLink (tag, url) "
        "VALUES ('{}', '{}');\n"
        .format(imageTag, imageUrl)
    )
