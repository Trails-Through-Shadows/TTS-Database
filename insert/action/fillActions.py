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


def insertEffects(id, effects: [], type: str) -> int:
    for effect in effects:
        sqlFile.write(
            "INSERT INTO Effect (id, type, duration, `target`, strength) "
            "VALUES ({}, '{}', {}, '{}', {}) "
            "ON DUPLICATE KEY UPDATE id=id;\n"
            .format("NULL", effect["type"], effect["duration"], effect["target"], effect["strength"])
        )

        sqlFile.write(
            "SET @idEffect = (SELECT id FROM Effect WHERE type = '{}' AND duration = {} AND `target` = '{}' AND strength = {});\n"
            .format(effect["type"], effect["duration"], effect["target"], effect["strength"])
        )

        sqlFile.write(
            "INSERT INTO {} VALUES ({}, @idEffect);\n"
            .format(type, id)
        )


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

for action in data:
    actionID = action["id"]

    # Skip templated actions
    if actionID == -1:
        continue

    # Params
    actionTitle = action["title"]
    actionDesc = action["description"]
    actionDiscard = action["discard"]

    sqlFile.write("-- Action {}\n".format(actionTitle))

    # Movement
    movementID = "NULL"
    if action.get('movement') is not None:
        movement = action["movement"]
        movementID = movement["id"]

        # Params
        moveRange = movement["range"]
        moveType = movement["type"]
        moveEffects = movement["effects"]

        sqlFile.write(
            "INSERT INTO Movement (id, `range`, type) "
            "VALUES ({}, {}, '{}');\n"
            .format(movementID, moveRange, moveType)
        )

        insertEffects(movementID, moveEffects, "MovementEffect")

    # Skill
    skillID = "NULL"
    if action.get('skill') is not None:
        skill = action["skill"]
        skillID = skill["id"]

        # Params
        skillRange = skill["range"]
        skillArea = skill["area"]
        skillTarget = skill["target"]
        skillEffects = skill["effects"]

        sqlFile.write(
            "INSERT INTO Skill (id, `range`, area, target) "
            "VALUES ({}, {}, {}, '{}');\n"
            .format(skillID, skillRange, skillArea, skillTarget)
        )

        insertEffects(skillID, skillEffects, "SkillEffect")

    # Attack
    attackID = "NULL"
    if action.get('attack') is not None:
        attack = action["attack"]
        attackID = attack["id"]

        # Params
        attackRange = attack["range"]
        attackDamage = attack["damage"]
        attackArea = attack["area"]
        attackTarget = attack["target"]
        attackNumAttacks = attack["numAttacks"]
        attackEffects = attack["effects"]

        sqlFile.write(
            "INSERT INTO Attack (id, `range`, damage, area, target, numAttacks) "
            "VALUES ({}, {}, {}, {}, '{}', {});\n"
            .format(attackID, attackRange, attackDamage, attackArea, attackTarget, attackNumAttacks)
        )

        insertEffects(attackID, attackEffects, "AttackEffect")

    # RestoreCards
    restoreCardID = "NULL"
    if action.get('restoreCards') is not None:
        restoreCards = action["restoreCards"]
        restoreCardID = restoreCards["id"]

        # Params
        restoreCardsNumber = restoreCards["numCards"]
        restoreCardTarget = restoreCards["target"]
        restoreCardRandom = restoreCards["random"]

        sqlFile.write(
            "INSERT INTO RestoreCards (id, numCards, target, random) "
            "VALUES ({}, {}, '{}', {});\n"
            .format(restoreCardID, restoreCardsNumber, restoreCardTarget, restoreCardRandom)
        )

    # Insert Action
    sqlFile.write(
        "INSERT INTO Action (id, title, description, attack, skill, movement, restoreCards, discard) "
        "VALUES ({}, '{}', '{}', {}, {}, {}, {}, '{}');\n"
        .format(actionID, actionTitle, actionDesc, attackID, skillID, movementID, restoreCardID, actionDiscard)
    )

    # Summon
    if action.get('summon') is not None:
        summons = action["summon"]
        for summon in summons:
            summonID = summon["id"]

            # Params
            summonRange = summon["range"]

            sqlFile.write(
                "INSERT INTO SummonAction (idSummon, idAction, `range`) "
                "VALUES ({}, {}, {});\n"
                .format(summonID, actionID, summonRange)
            )
