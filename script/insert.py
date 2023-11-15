import subprocess
from app import *


# Clear the database
clearScriptPath = '../manage/clear.sql'
executeFileSQL(clearScriptPath)

# Directory where the .sql files are located
insertFolder = '../insert'

sqlFiles = []
pyFiles = []

for dirPath, dirNames, fileNames in os.walk(insertFolder):
    for fileName in fileNames:
        filePath = os.path.join(dirPath, fileName)

        # Python files
        if fileName.lower().endswith('.py'):
            pyFiles.append((fileName, filePath))

        # SQL files
        if fileName.lower().endswith('.sql'):
            sqlFiles.append((fileName, filePath))

log("Found {} SQL files and {} Python files.".format(len(sqlFiles), len(pyFiles)), "INFO", True)

# Sort sql files by name
sqlFiles.sort(key=lambda x: x[0])

# Execute all python files
for fileName, filePath in pyFiles:
    log("Executing {}...".format(filePath), "INFO")
    try:
        subprocess.call(['python', filePath])
        log("Executing {}... Done".format(filePath), "INFO", True)
    except Exception as e:
        log("Executing {}... Error: {}".format(filePath, e), "ERROR", True)
        log(e, "ERROR", True)

# Execute all sql files
for fileName, filePath in sqlFiles:
    executeFileSQL(filePath)

# Close the connection
conn.close()
log("Successfully executed all the SQL files.", "INFO")
