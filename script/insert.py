import sys

from app import *

# If -s, then skip clear.sql
if not (len(sys.argv) > 1 and sys.argv[1] == '-s'):
    # Clear the database
    clearScriptPath = 'manage/clear.sql'
    executeFileSQL(clearScriptPath)

# Directory where the .sql files are located
insertFolder = 'insert'

log("", "INFO", True)
log("Removing all the .sql files in the directory...", "INFO", True)

# Remove all .sql files in directory
for dirPath, _, fileNames in os.walk(insertFolder):
    for fileName in fileNames:
        filePath = os.path.join(dirPath, fileName)

        # SQL files
        if fileName.lower().endswith('.sql') and fileName.lower() != '0-license.sql':
            log(" - Removing " + filePath + "...", "INFO", True)
            os.remove(filePath)
            
log("Successfully removed all the .sql files in the directory.", "INFO", True)
log("", "INFO", True)
log("Executing all the Python files...", "INFO", True)

# Execute all the Python files
for dirPath, _, fileNames in os.walk(insertFolder):
    for fileName in fileNames:
        filePath = os.path.join(dirPath, fileName)

        # Python files
        if fileName.lower().endswith('.py'):
            executeFilePython(filePath)

log("Successfully executed all the Python files.", "INFO", True)
log("", "INFO", True)
log("Executing all the SQL files...", "INFO", True)

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
log("", "INFO", True)
