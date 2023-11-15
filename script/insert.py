import subprocess
from app import *


# Clear the database
clearScriptPath = '../manage/clear.sql'
executeFileSQL(clearScriptPath)

# Directory where the .sql files are located
insertFolder = '../insert'

for dirPath, _, fileNames in os.walk(insertFolder):
    for fileName in fileNames:
        filePath = os.path.join(dirPath, fileName)

        # Python files
        if fileName.lower().endswith('.py'):
            log("Executing {}...".format(filePath), "INFO")

            try:
                subprocess.call(['python', filePath])
                log("Executing {}... Done".format(filePath), "INFO", True)
            except Exception as e:
                log("Executing {}... Error: {}".format(filePath, e), "ERROR", True)
                log(e, "ERROR", True)

sqlFiles = []

# Excecute all sql files sorted by name in the insert folder
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
    log("Executing {}...".format(filePath), "INFO")

    try:
        executeFileSQL(filePath)
        log("Executing {}... Done".format(filePath), "INFO", True)
    except Exception as e:
        log("Executing {}... Error: {}".format(filePath, e), "ERROR", True)

# Close the connection
conn.close()
log("Successfully executed all the SQL files.", "INFO")
