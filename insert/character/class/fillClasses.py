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
dataFilePath = currentFolderPath + "/classes.json"
with open(dataFilePath, encoding='utf8') as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/2-classes.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

for clazz in data:
    clazzID = clazz["id"]

    # Params
    clazzName = clazz["name"]
    clazzBaseHealth = clazz["baseHealth"]
    clazzActions = clazz["actions"]

    sqlFile.write("-- Class {}\n".format(clazzName))
    sqlFile.write(
        "INSERT INTO Class (id, name, baseHealth) "
        "VALUES ({}, '{}', {});\n"
        .format(clazzID, clazzName, clazzBaseHealth)
    )

    # Actions
    for action in clazzActions:
        actionID = action["id"]

        # Params
        actionLevelReq = action["levelReq"]
        actionItemReq = action["itemReq"]

        sqlFile.write(
            "INSERT INTO ClassAction (id, idClass, levelReq, itemReq, idAction) "
            "VALUES ({}, {}, {}, {}, {});\n"
            .format("NULL", clazzID, actionLevelReq, actionItemReq, actionID)
        )
