from app import *


# Clear the database
clearScriptPath = '../manage/clear.sql'
executeFileSQL(clearScriptPath)

# Directory where the .sql files are located
insertFolder = '../insert'

# Execute all the Python files
for dirPath, _, fileNames in os.walk(insertFolder):
    for fileName in fileNames:
        filePath = os.path.join(dirPath, fileName)

        # Python files
        if fileName.lower().endswith('.py'):
            executeFilePython(filePath)

# Get all the SQL files
sqlFiles = []
for dirPath, _, fileNames in os.walk(insertFolder):
    for fileName in fileNames:
        filePath = os.path.join(dirPath, fileName)

        # SQL files
        if fileName.lower().endswith('.sql'):
            sqlFiles.append(filePath)

# Sort the files by name
sqlFiles.sort(key=lambda x: os.path.basename(x))

# Execute all the SQL files
for filePath in sqlFiles:
    executeFileSQL(filePath)

# Close the connection
conn.close()
log("Successfully executed all the SQL files.", "INFO")
