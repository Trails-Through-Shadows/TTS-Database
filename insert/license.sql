/*
 Randomly generate rows for the License table.
  - UUID = String formatted: xxxx-xxxx-xxxx-xxxx
  - Password = 16 characters
  - Activated = 50% chance of being NULL, otherwise a random date between now and 30 days from now.
 */

SET @numRows = 50;

CREATE OR REPLACE PROCEDURE InsertRandomData()
BEGIN
    DECLARE i INT DEFAULT 0;

    WHILE i < @numRows DO
        SET @randUUID = MD5(UUID());
        SET @randKey = CONCAT(
                LEFT(@randUUID, 4), '-',
                MID(@randUUID, 5, 4), '-',
                MID(@randUUID, 9, 4), '-',
                MID(@randUUID, 13, 4));
        SET @randPassword = SUBSTRING(MD5(RAND()), 1, 16);
        SET @randActivated = IF(RAND() > 0.5, NULL, DATE_ADD(NOW(), INTERVAL FLOOR(RAND() * 30) DAY));

        INSERT INTO License (`key`, password, activated)
        VALUES (@randKey, @randPassword, @randActivated);

        SET i = i + 1;
    END WHILE;
END;

CALL InsertRandomData();