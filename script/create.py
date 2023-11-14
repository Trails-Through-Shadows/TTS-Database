from app import *


# Drop the database
clearScriptPath = '../manage/drop.sql'
executeFileSQL(clearScriptPath)

# Create the database
createScriptPath = '../manage/create.sql'
executeFileSQL(createScriptPath)

# Close the connection
conn.close()
log("Successfully executed all the SQL files.", "INFO")
