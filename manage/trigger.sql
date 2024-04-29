# Trigger on Part relation update

CREATE OR REPLACE TRIGGER trg_UpdatePartRelationsINSERT
    AFTER INSERT ON LocationPart
    FOR EACH ROW
BEGIN
    UPDATE Part
    SET usages = Part.usages + 1
    WHERE id = NEW.idPart;
END;

CREATE OR REPLACE TRIGGER trg_UpdatePartRelationsDELETE
    AFTER DELETE ON LocationPart
    FOR EACH ROW
BEGIN
    UPDATE Part
    SET usages = Part.usages - 1
    WHERE id = OLD.idPart;
END;

# Trigger on Enemy relation update

CREATE OR REPLACE TRIGGER trg_UpdateEnemyRelationsINSERT
    AFTER INSERT ON HexEnemy
    FOR EACH ROW
BEGIN
    UPDATE Enemy
    SET usages = Enemy.usages + 1
    WHERE id = NEW.idEnemy;
END;

CREATE OR REPLACE TRIGGER trg_UpdateEnemyRelationsDELETE
    AFTER DELETE ON HexEnemy
    FOR EACH ROW
BEGIN
    UPDATE Enemy
    SET usages = Enemy.usages - 1
    WHERE id = OLD.idEnemy;
END;


# Trigger on Obstacle relation update

CREATE OR REPLACE TRIGGER trg_UpdateObstacleRelationsINSERT
    AFTER INSERT ON HexObstacle
    FOR EACH ROW
BEGIN
    UPDATE Obstacle
    SET usages = Obstacle.usages + 1
    WHERE id = NEW.idObstacle;
END;

CREATE OR REPLACE TRIGGER trg_UpdateObstacleRelationsDELETE
    AFTER DELETE ON HexObstacle
    FOR EACH ROW
BEGIN
    UPDATE Obstacle
    SET usages = Obstacle.usages - 1
    WHERE id = OLD.idObstacle;
END;
