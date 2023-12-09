import sys

from app import *

# Drop the database
clearScriptPath = 'manage/drop.sql'
executeFileSQL(clearScriptPath)

# Create the database
createScriptPath = 'manage/create.sql'
executeFileSQL(createScriptPath)

# If -s, then skip auto-inserting
if not (len(sys.argv) > 1 and sys.argv[1] == '-s'):
    # Clear the database
    clearScriptPath = 'script/insert.py'
    executeFilePython(clearScriptPath, ['-s'])

# Close the connection
conn.close()
log("Successfully executed all the SQL files.", "INFO")
