from app import *


# Drop the database
clearScriptPath = 'manage/drop.sql'
executeFileSQL(clearScriptPath)

# Close the connection
conn.close()
log("Successfully executed all the SQL files.", "INFO")
