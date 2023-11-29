from app import *

# Query location from the database
cursor = conn.cursor(dictionary=True)
cursor.execute(""
                "SELECT Location.title AS Title, P.id AS PartId, H.id AS HexId, xCord, yCord "
                "FROM Location "
                "JOIN LocationPart LP on Location.id = LP.idLocation "
                "JOIN Part P on LP.idPart = P.id "
                "JOIN Hex H on P.id = H.idPart "
                "WHERE Location.id = 1 "
               )

# Get the results
locations = cursor.fetchall()

cursor.execute(""
               "SELECT * "
               "FROM Location "
               "JOIN HexDoor HD on Location.id = HD.idLocation "
               "WHERE Location.id = 1"
               )
doors = cursor.fetchall()

parts = []

for part in locations:
    # New part
    if len(location["parts"]) == 0 or location["parts"][-1]["id"] != part["PartId"]:
        location["parts"].append({
            "id": part["PartId"],
            "scheme": [],
            "hexes": []
        })

    # Add the hex
    location["parts"][-1]["hexes"].append({
        "id": part["HexId"],
        "xCord": part["xCord"],
        "yCord": part["yCord"]
    })

print(location["doors"])

# Print the schema by parts
for part in location["parts"]:
    print("Part {}".format(part["id"]))
    print("Scheme:")

    lastY = -1
    for hex in part["hexes"]:
        if lastY != hex["yCord"]:
            if lastY != -1:  # To avoid an extra newline at the start
                print()  # Newline for new row
            lastY = hex["yCord"]

    print("\n\n")  # Newline after finishing each part's scheme
