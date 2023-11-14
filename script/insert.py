import subprocess
from app import *


# Clear the database
clearScriptPath = '../manage/clear.sql'
executeFileSQL(clearScriptPath)

# Directory where the .sql files are located
insertFolder = '../insert'

# Iterate over all the .sql files in the 'insert' directory
for dirPath, dirNames, fileNames in os.walk(insertFolder):
    for fileName in fileNames:
        if fileName.lower().endswith('.py'):
            filePath = os.path.join(dirPath, fileName)
            subprocess.call(['python', filePath])

        if fileName.lower().endswith('.sql'):
            filePath = os.path.join(dirPath, fileName)
            executeFileSQL(filePath)

# Close the connection
conn.close()
log("Successfully executed all the SQL files.", "INFO")
