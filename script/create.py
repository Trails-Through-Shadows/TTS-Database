import sys

from app import *

# Drop the database
clearScriptPath = 'manage/drop.sql'
executeFileSQL(clearScriptPath)

# Create the database
createScriptPath = 'manage/create.sql'
executeFileSQL(createScriptPath)

# Create the triggers
createScriptPath = 'manage/trigger.sql'
executeFileSQL(createScriptPath)

# If -s, then skip auto-inserting
if not (len(sys.argv) > 1 and sys.argv[1] == '-s'):
    # Clear the database
    clearScriptPath = 'script/insert.py'
    executeFilePython(clearScriptPath, ['-s'], True)
else:
    log("Successfully executed all the SQL files.", "INFO")

# Close the connection
conn.close()
