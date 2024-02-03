# Trigger on Part relation update

CREATE OR REPLACE TRIGGER trg_UpdatePartRelationsINSERT
    AFTER INSERT ON LocationPart
    FOR EACH ROW
BEGIN
    UPDATE Part
    SET usages = COALESCE((SELECT COUNT(idLocation) FROM LocationPart WHERE idPart = NEW.idPart GROUP BY idPart), 0)
    WHERE id = NEW.idPart;
END;

CREATE OR REPLACE TRIGGER trg_UpdatePartRelationsDELETE
    AFTER DELETE ON LocationPart
    FOR EACH ROW
BEGIN
    UPDATE Part
    SET usages = COALESCE((SELECT COUNT(idLocation) FROM LocationPart WHERE id = OLD.idPart GROUP BY idPart), 0)
    WHERE id = OLD.idPart;
END;

# Trigger on Enemy relation update

CREATE OR REPLACE TRIGGER trg_UpdateEnemyRelationsINSERT
    AFTER INSERT ON HexEnemy
    FOR EACH ROW
BEGIN
    UPDATE Enemy
    SET usages = COALESCE((SELECT COUNT(idLocation) FROM HexEnemy WHERE idEnemy = NEW.idEnemy GROUP BY idEnemy), 0)
    WHERE id = NEW.idEnemy;
END;

CREATE OR REPLACE TRIGGER trg_UpdateEnemyRelationsDELETE
    AFTER DELETE ON HexEnemy
    FOR EACH ROW
BEGIN
    UPDATE Enemy
    SET usages = COALESCE((SELECT COUNT(idLocation) FROM HexEnemy WHERE id = OLD.idEnemy GROUP BY idEnemy), 0)
    WHERE id = OLD.idEnemy;
END;

# Trigger on Obstacle relation update

CREATE OR REPLACE TRIGGER trg_UpdateObstacleRelationsINSERT
    AFTER INSERT ON HexObstacle
    FOR EACH ROW
BEGIN
    UPDATE Obstacle
    SET usages = COALESCE((SELECT COUNT(idLocation) FROM HexObstacle WHERE idObstacle = NEW.idObstacle GROUP BY idObstacle), 0)
    WHERE id = NEW.idObstacle;
END;

CREATE OR REPLACE TRIGGER trg_UpdateObstacleRelationsDELETE
    AFTER DELETE ON HexObstacle
    FOR EACH ROW
BEGIN
    UPDATE Obstacle
    SET usages = COALESCE((SELECT COUNT(idLocation) FROM HexObstacle WHERE id = OLD.idObstacle GROUP BY idObstacle), 0)
    WHERE id = OLD.idObstacle;
END;
