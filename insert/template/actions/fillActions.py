import json
import os


# Replace None with NULL recursively
def replaceNoneWithNull(data):
    if isinstance(data, dict):
        for key in data:
            if data[key] is None:
                data[key] = "NULL"
            else:
                data[key] = replaceNoneWithNull(data[key])
    elif isinstance(data, list):
        for i in range(len(data)):
            if data[i] is None:
                data[i] = "NULL"
            else:
                data[i] = replaceNoneWithNull(data[i])
    else:
        if data is None:
            data = "NULL"

    return data

def replaceQuotes(data):
    return data.replace('"', '\\"').replace("'", "\\'")


# Get current file path even if it's executed from another file
currentFolderPath = os.path.dirname(os.path.realpath(__file__))

# Open the JSON file
dataFilePath = currentFolderPath + "/actions.json"
with open(dataFilePath, encoding='utf8') as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/2-actions.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

for entry in data:
    entryID = entry["id"]
    sqlFile.write("-- Action {}\n".format(entryID))

    # Movement
    movementID = "NULL"
    if entry.get('movement') != 'NULL':
        movement = entry.get("movement")
        movementID = entry["id"]

        # Insert movement
        sqlFile.write(
            "INSERT INTO Movement (id, `range`, type) "
            "VALUES ({}, {}, '{}');\n"
            .format(movementID,
                    movement["range"],
                    movement["type"]
            )
        )

        # Insert effects
        for effect in movement["effects"]:
            sqlFile.write(
                "INSERT INTO MovementEffect (idMovement, idEffect) "
                "VALUES ({}, {});\n"
                .format(movementID, effect["key"]["idEffect"])
            )

    # Skill
    skillID = "NULL"
    if entry.get('skill') != 'NULL':
        skill = entry.get("skill")
        skillID = entry["id"]

        # Insert skill
        sqlFile.write(
            "INSERT INTO Skill (id, `range`, area, target) "
            "VALUES ({}, {}, {}, '{}');\n"
            .format(skillID, skill["range"], skill["area"], skill["target"])
        )

        # Insert effects
        for effect in skill["effects"]:
            sqlFile.write(
                "INSERT INTO SkillEffect (idSkill, idEffect) "
                "VALUES ({}, {});\n"
                .format(skillID, effect["key"]["idEffect"])
            )

    # Attack
    attackID = "NULL"
    if entry.get('attack') != 'NULL':
        attack = entry.get("attack")
        attackID = attack["id"]

        # Insert attack
        sqlFile.write(
            "INSERT INTO Attack (id, `range`, damage, area, target, numAttacks) "
            "VALUES ({}, {}, {}, {}, '{}', {});\n"
            .format(attackID,
                    attack["range"],
                    attack["damage"],
                    attack["area"],
                    attack["target"],
                    attack["numAttacks"]
            )
        )

        # Insert effects
        for effect in attack["effects"]:
            sqlFile.write(
                "INSERT INTO AttackEffect (idAttack, idEffect) "
                "VALUES ({}, {});\n"
                .format(attackID, effect["key"]["idEffect"])
            )

    # RestoreCards
    restoreCardID = "NULL"
    if entry.get('restoreCards') != 'NULL':
        restoreCards = entry.get("restoreCards")
        restoreCardID = restoreCards["id"]

        sqlFile.write(
            "INSERT INTO RestoreCards (id, numCards, target, random) "
            "VALUES ({}, {}, '{}', {});\n"
            .format(restoreCardID,
                    restoreCards["numCards"],
                    restoreCards["target"],
                    restoreCards["random"]
            )
        )

    # Insert Action
    sqlFile.write(
        "INSERT INTO Action (id, title, description, attack, skill, movement, restoreCards, discard, levelReq) "
        'VALUES ({}, "{}", "{}", {}, {}, {}, {}, "{}", {});\n'
        .format(entryID,
                replaceQuotes(entry["title"]),
                replaceQuotes(entry["description"]),
                attackID,
                skillID,
                movementID,
                restoreCardID,
                entry["discard"],
                entry["levelReq"]
        )
    )

    # Summon
    if entry.get('summonActions') != 'NULL':
        summons = entry.get("summonActions")

        for summon in summons:
            sqlFile.write(
                "INSERT INTO SummonAction (idSummon, idAction, `range`) "
                "VALUES ({}, {}, {});\n"
                .format(
                    summon["key"]["idSummon"],
                    entryID,
                    summon["range"]
                )
            )
