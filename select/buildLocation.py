from script.app import *

# Query location from the database
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM Location")

# Get the results
locations = cursor.fetchall()
print(locations)
