-- Disable foreign key checks to avoid errors during table drop
SET FOREIGN_KEY_CHECKS = 0;

-- Store the table names in the @tables variable
SELECT GROUP_CONCAT('`', table_name, '`') INTO @tables
FROM information_schema.tables
WHERE table_schema = (SELECT DATABASE());

-- Declare variables for loop control
SET @table_count = 0;
SET @table_name = '';

-- Start a loop to delete data from each table
WHILE @table_count < LENGTH(@tables) DO
    -- Get the table name for the current iteration
    SET @table_name = SUBSTRING_INDEX(SUBSTRING_INDEX(@tables, ',', @table_count + 1), ',', -1);

    -- Construct and execute the DELETE statement
    SET @delete_statement = CONCAT('DROP TABLE IF EXISTS ', @table_name);
    PREPARE stmt FROM @delete_statement;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    -- Increment the table count for the next iteration
    SET @table_count = @table_count + 1;
END WHILE;

-- Re-enable foreign key checks to ensure data integrity
SET FOREIGN_KEY_CHECKS = 1;