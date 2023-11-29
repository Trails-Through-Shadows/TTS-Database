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


# Get current file path even if it's executed from another file
currentFolderPath = os.path.dirname(os.path.realpath(__file__))

# Open the JSON file
dataFilePath = currentFolderPath + "/actions.json"
with open(dataFilePath, encoding='utf8') as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/1-actions.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

# Replace None with NULL
data = replaceNoneWithNull(data)

# Create a temp unique index
sqlFile.write("DROP INDEX IF EXISTS `tempUnique` ON Effect;\n")
sqlFile.write("ALTER TABLE Effect ADD UNIQUE INDEX `tempUnique` (type, duration, `range`, strength);\n")

for action in data:
    id = action["id"]
    title = action["title"]
    description = action["description"]
    discard = action["discard"]

    if id == -1: continue
    sqlFile.write("-- Action {}\n".format(title))

    # Summon
    summonID = "NULL"
    if action["summon"] != 'NULL':
        summon = action["summon"]
        summonID = summon["id"]
        actionIDs = summon["idAction"]

        for actionID in actionIDs:
            sqlFile.write(
                "INSERT INTO SummonAction (idSummon, idAction) "
                "VALUES ({}, {});\n"
                .format(summonID, actionID)
            )

            # SummonEffect
            if "summonEffects" in summon:
                for effect in summon["summonEffects"]:
                    sqlFile.write(
                        "INSERT INTO Effect (id, type, duration, `range`, strength) "
                        "VALUES ({}, '{}', {}, '{}', {}) "
                        "ON DUPLICATE KEY UPDATE id=id;\n"
                        .format("NULL", effect["type"], effect["duration"], effect["range"], effect["strength"])
                    )

                    sqlFile.write(
                        "SET @idEffect = (SELECT id FROM Effect WHERE type = '{}' AND duration = {} AND `range` = '{}' AND strength = {});\n"
                        .format(effect["type"], effect["duration"], effect["range"], effect["strength"])
                    )

                    sqlFile.write(
                        "INSERT INTO SummonEffect (idSummon, idEffect) "
                        "VALUES ({}, @idEffect);\n"
                        .format(summonID)
                    )

    # Attack
    attackID = "NULL"
    if action["attack"] != 'NULL':
        attack = action["attack"]
        attackID = attack["id"]

        sqlFile.write(
            "INSERT INTO AttackAction (id, `range`, damage, area, target, numAttacks) "
            "VALUES ({}, {}, {}, {}, '{}', {});\n"
            .format(attackID, attack["range"], attack["damage"], attack["area"], attack["target"], attack["numAttacks"])
        )

        # AttackEffect
        if "attackEffects" in attack:
            for effect in attack["attackEffects"]:
                sqlFile.write(
                    "INSERT INTO Effect (id, type, duration, `range`, strength) "
                    "VALUES ({}, '{}', {}, '{}', {}) "
                    "ON DUPLICATE KEY UPDATE id=id;\n"
                    .format("NULL", effect["type"], effect["duration"], effect["range"], effect["strength"])
                )

                sqlFile.write(
                    "SET @idEffect = (SELECT id FROM Effect WHERE type = '{}' AND duration = {} AND `range` = '{}' AND strength = {});\n"
                    .format(effect["type"], effect["duration"], effect["range"], effect["strength"])
                )

                sqlFile.write(
                    "INSERT INTO AttackEffect (idAttack, idEffect) "
                    "VALUES ({}, @idEffect);\n"
                    .format(attackID)
                )

    # Skill
    skillID = "NULL"
    if action["skill"] != 'NULL':
        skill = action["skill"]
        skillID = skill["id"]

        sqlFile.write(
            "INSERT INTO SkillAction (id, `range`, duration, heal, area, target) "
            "VALUES ({}, {}, {}, {}, {}, '{}');\n"
            .format(skillID, skill["range"], skill["duration"], skill["heal"], skill["area"], skill["target"])
        )

        # SkillEffect
        if "skillEffects" in skill:
            for effect in skill["skillEffects"]:
                sqlFile.write(
                    "INSERT INTO Effect (id, type, duration, `range`, strength) "
                    "VALUES ({}, '{}', {}, '{}', {}) "
                    "ON DUPLICATE KEY UPDATE id=id;\n"
                    .format("NULL", effect["type"], effect["duration"], effect["range"], effect["strength"])
                )

                sqlFile.write(
                    "SET @idEffect = (SELECT id FROM Effect WHERE type = '{}' AND duration = {} AND `range` = '{}' AND strength = {});\n"
                    .format(effect["type"], effect["duration"], effect["range"], effect["strength"])
                )

                sqlFile.write(
                    "INSERT INTO SkillEffect (idSkill, idEffect) "
                    "VALUES ({}, @idEffect);\n"
                    .format(skillID)
                )

    # Movement
    movementID = "NULL"
    if action["movement"] != 'NULL':
        movement = action["movement"]
        movementID = movement["id"]

        sqlFile.write(
            "INSERT INTO MovementAction (id, `range`, type) "
            "VALUES ({}, {}, '{}');\n"
            .format(movementID, movement["range"], movement["type"])
        )

        # MovementEffect
        if "movementEffects" in movement:
            for effect in movement["movementEffects"]:
                sqlFile.write(
                    "INSERT INTO Effect (id, type, duration, `range`, strength) "
                    "VALUES ({}, '{}', {}, '{}', {}) "
                    "ON DUPLICATE KEY UPDATE id=id;\n"
                    .format("NULL", effect["type"], effect["duration"], effect["range"], effect["strength"])
                )

                sqlFile.write(
                    "SET @idEffect = (SELECT id FROM Effect WHERE type = '{}' AND duration = {} AND `range` = '{}' AND strength = {});\n"
                    .format(effect["type"], effect["duration"], effect["range"], effect["strength"])
                )

                sqlFile.write(
                    "INSERT INTO MovementEffect (idMovement, idEffect) "
                    "VALUES ({}, @idEffect);\n"
                    .format(movementID)
                )

    # RestoreCards
    restoreCardID = "NULL"
    if action["restoreCards"] != 'NULL':
        restoreCards = action["restoreCards"]
        restoreCardID = restoreCards["id"]

        sqlFile.write(
            "INSERT INTO RestoreCardsAction (id, cards, target, random) "
            "VALUES ({}, {}, {}, {});\n"
            .format(restoreCardID, restoreCards["cards"], restoreCards["target"], restoreCards["random"])
        )

    # Insert Action
    sqlFile.write(
        "INSERT INTO Action (id, title, description, summon, attack, skill, movement, restoreCards, discard) "
        "VALUES ({}, '{}', '{}', {}, {}, {}, {}, {}, '{}');\n"
        .format(id, title, description, summonID, attackID, skillID, movementID, restoreCardID, discard)
    )

# Drop the unique index
sqlFile.write("-- Drop the unique index\n")
sqlFile.write("ALTER TABLE Effect DROP INDEX `tempUnique`;\n")
