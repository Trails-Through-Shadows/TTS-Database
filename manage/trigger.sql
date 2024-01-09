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