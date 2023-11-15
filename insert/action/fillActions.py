import json
import os

# Get current file path even if it's executed from another file
currentFolderPath = os.path.dirname(os.path.realpath(__file__))

# Open the JSON file
dataFilePath = currentFolderPath + "/actions.json"
with open(dataFilePath, "r") as dataFile:
    data = json.load(dataFile)

# Write the SQL file
sqlFilePath = currentFolderPath + "/actions.sql"
sqlFile = open(sqlFilePath, "w")

# Clear the SQL file
sqlFile.truncate(0)
sqlFile.flush()

for action in data:
    id = action["id"]
    title = action["title"]
    description = action["description"]
    summonID = "NULL"
    attackID = "NULL"
    skillID = "NULL"
    movementID = "NULL"
    restoreCardID = "NULL"
    discard = action["discard"]

    # Summon
    if action["summon"]:
        summon = action["summon"]
        summonID = summon["id"]

        sqlFile.write(
            "INSERT INTO SummonAction (id, idSummon, idAction) "
            "VALUES ({}, {}, {});\n"
            .format(summon["id"], summon["idSummon"], summon["idAction"])
        )

        # SummonEffect
        if "summonEffects" in summon:
            for effect in summon["summonEffects"]:
                sqlFile.write(
                    "INSERT INTO SummonEffect (idSummon, idEffect) "
                    "VALUES ({}, {});\n"
                    .format(summon["id"], effect)
                )

    # Attack
    if action["attack"]:
        attack = action["attack"]
        attackID = attack["id"]

        sqlFile.write(
            "INSERT INTO AttackAction (id, `range`, damage, area, target, numAttacks) "
            "VALUES ({}, {}, {}, {}, '{}', {});\n"
            .format(attack["id"], attack["range"], attack["damage"], attack["area"], attack["target"], attack["numAttacks"])
        )

        # AttackEffect
        if "attackEffects" in attack:
            for effect in attack["attackEffects"]:
                sqlFile.write(
                    "INSERT INTO AttackEffect (idAttack, idEffect) "
                    "VALUES ({}, {});\n"
                    .format(attack["id"], effect)
                )

    # Skill
    if action["skill"]:
        skill = action["skill"]
        skillID = skill["id"]

        sqlFile.write(
            "INSERT INTO SkillAction (id, `range`, duration, heal, area, target) "
            "VALUES ({}, {}, {}, {}, {}, {});\n"
            .format(skill["id"], skill["range"], skill["duration"], skill["heal"], skill["area"], skill["target"])
        )

        # SkillEffect
        if "skillEffects" in skill:
            for effect in skill["skillEffects"]:
                sqlFile.write(
                    "INSERT INTO SkillEffect (idSkill, idEffect) "
                    "VALUES ({}, {});\n"
                    .format(skill["id"], effect)
                )

    # Movement
    if action["movement"]:
        movement = action["movement"]
        movementID = movement["id"]

        sqlFile.write(
            "INSERT INTO MovementAction (id, `range`, type) "
            "VALUES ({}, {}, {});\n"
            .format(movement["id"], movement["range"], movement["type"])
        )

        # MovementEffect
        if "movementEffects" in movement:
            for effect in movement["movementEffects"]:
                sqlFile.write(
                    "INSERT INTO MovementEffect (idMovement, idEffect) "
                    "VALUES ({}, {});\n"
                    .format(movement["id"], effect)
                )

    # RestoreCards
    if action["restoreCards"]:
        restoreCards = action["restoreCards"]
        restoreCardID = restoreCards["id"]

        sqlFile.write(
            "INSERT INTO RestoreCardsAction (id, cards, target, random) "
            "VALUES ({}, {}, {}, {});\n"
            .format(restoreCards["id"], restoreCards["cards"], restoreCards["target"], restoreCards["random"])
        )

    # Insert Action
    sqlFile.write(
        "INSERT INTO Action (id, title, description, summon, attack, skill, movement, restoreCards, discard) "
        "VALUES ({}, '{}', '{}', {}, {}, {}, {}, {}, '{}');\n"
        .format(id, title, description, summonID, attackID, skillID, movementID, restoreCardID, discard)
    )