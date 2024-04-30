CREATE TABLE `License` (
                           `id` INT NOT NULL AUTO_INCREMENT,
                           `key` VARCHAR(20) NOT NULL,
                           `password` TEXT NOT NULL,
                           `activated` DATETIME,
                           PRIMARY KEY (`id`)
);

CREATE TABLE `Campaign` (
                            `id` INT NOT NULL AUTO_INCREMENT,
                            `title` VARCHAR(128) NOT NULL,
                            `description` TEXT,
                            PRIMARY KEY (`id`)
);

CREATE TABLE `CampaignLocation` (
                                    `id` INT NOT NULL AUTO_INCREMENT,
                                    `idCampaign` INT NOT NULL,
                                    `idLocation` INT NOT NULL,
                                    `condition` TEXT NOT NULL,
                                    `start` bool NOT NULL,
                                    `finish` bool NOT NULL,
                                    PRIMARY KEY (`id`)
);

CREATE TABLE `Story` (
                         `id` INT NOT NULL AUTO_INCREMENT,
                         `idCampaignLocation` INT NOT NULL,
                         `trigger` ENUM ('NEW', 'ONGOING', 'COMPLETED', 'FAILED') NOT NULL,
                         `story` TEXT NOT NULL,
                         PRIMARY KEY (`id`)
);

CREATE TABLE `AdventureLocation` (
                                     `idAdventure` INT NOT NULL,
                                     `idLocation` INT NOT NULL,
                                     `unlocked` BOOL NOT NULL DEFAULT 0,
                                     `state` ENUM ('NOT_VISITED', 'VISITED', 'FAILED', 'COMPLETED') NOT NULL DEFAULT 'NOT_VISITED',
                                     PRIMARY KEY (`idAdventure`, `idLocation`)
);

CREATE TABLE `Adventure` (
                             `id` INT NOT NULL AUTO_INCREMENT,
                             `idCampaign` INT NOT NULL,
                             `idLicense` INT NOT NULL,
                             `title` VARCHAR(128) NOT NULL,
                             `description` TEXT,
                             `reputation` INT NOT NULL,
                             `experience` INT NOT NULL,
                             `gold` INT NOT NULL,
                             `level` INT NOT NULL,
                             PRIMARY KEY (`id`)
);

CREATE TABLE `AdventureAchievement` (
                                        `idAdventure` INT NOT NULL,
                                        `idAchievement` INT NOT NULL,
                                        `progress` INT NOT NULL,
                                        PRIMARY KEY (`idAdventure`, `idAchievement`)
);

CREATE TABLE `Location` (
                            `id` INT NOT NULL AUTO_INCREMENT,
                            `title` VARCHAR(128) NOT NULL,
                            `tag` VARCHAR(32),
                            `type` ENUM ('CITY', 'DUNGEON', 'MARKET', 'QUEST') NOT NULL,
                            `description` TEXT,
                            PRIMARY KEY (`id`)
);

CREATE TABLE `LocationPath` (
                                `idCampaign` INT NOT NULL,
                                `idStart` INT NOT NULL,
                                `idEnd` INT NOT NULL,
                                PRIMARY KEY (`idCampaign`, `idStart`, `idEnd`)
);

CREATE TABLE `LocationPart` (
                                `idLocation` INT NOT NULL,
                                `idPart` INT NOT NULL,
                                `rotation` INT NOT NULL DEFAULT 0,
                                PRIMARY KEY (`idLocation`, `idPart`)
);

CREATE TABLE `Part` (
                        `id` INT NOT NULL AUTO_INCREMENT,
                        `title` VARCHAR(128) NOT NULL,
                        `tag` VARCHAR(32),
                        `usages` INT DEFAULT 0,
                        PRIMARY KEY (`id`)
);

CREATE TABLE `Hex` (
                       `idPart` INT NOT NULL,
                       `id` INT NOT NULL AUTO_INCREMENT,
                       `qCoord` INT NOT NULL DEFAULT 0,
                       `rCoord` INT NOT NULL DEFAULT 0,
                       `sCoord` INT NOT NULL DEFAULT 0,
                       PRIMARY KEY (`id`, `idPart`)
);

CREATE TABLE `LocationDoor` (
                                `idLocation` INT NOT NULL,
                                `idPartFrom` INT NOT NULL,
                                `idPartTo` INT NOT NULL,
                                `qCoord` INT NOT NULL DEFAULT 0,
                                `rCoord` INT NOT NULL DEFAULT 0,
                                `sCoord` INT NOT NULL DEFAULT 0,
                                PRIMARY KEY (`idLocation`, `idPartFrom`, `idPartTo`)
);

CREATE TABLE `LocationStart` (
                                 `idLocation` INT NOT NULL,
                                 `idPart` INT NOT NULL,
                                 `idHex` INT NOT NULL,
                                 PRIMARY KEY (`idLocation`, `idPart`, `idHex`)
);

CREATE TABLE `Class` (
                         `id` INT NOT NULL AUTO_INCREMENT,
                         `title` VARCHAR(128) NOT NULL,
                         `tag` VARCHAR(32),
                         `description` TEXT,
                         `baseHealth` INT NOT NULL,
                         `baseDefence` INT NOT NULL,
                         `baseInitiative` INT NOT NULL,
                         PRIMARY KEY (`id`)
);

CREATE TABLE `Character` (
                             `id` INT NOT NULL AUTO_INCREMENT,
                             `idClass` INT NOT NULL,
                             `idRace` INT NOT NULL,
                             `idAdventure` INT NOT NULL,
                             `title` VARCHAR(128) NOT NULL,
                             `playerName` VARCHAR(128),
                             PRIMARY KEY (`id`)
);

CREATE TABLE `Inventory` (
                             `idItem` INT NOT NULL,
                             `idCharacter` INT NOT NULL,
                             `amount` INT DEFAULT 1,
                             PRIMARY KEY (`idCharacter`, `idItem`)
);

CREATE TABLE `ClassAction` (
                               `idClass` INT NOT NULL,
                               `idAction` INT NOT NULL,
                               PRIMARY KEY (`idClass`, `idAction`)
);

CREATE TABLE `Enemy` (
                         `id` INT NOT NULL AUTO_INCREMENT,
                         `title` VARCHAR(128) NOT NULL,
                         `tag` VARCHAR(32),
                         `description` TEXT,
                         `baseHealth` INT NOT NULL,
                         `baseDefence` INT NOT NULL,
                         `baseInitiative` INT NOT NULL,
                         `usages` INT DEFAULT 0,
                         PRIMARY KEY (`id`)
);

CREATE TABLE `HexEnemy` (
                            `idEnemy` INT NOT NULL,
                            `idLocation` INT NOT NULL,
                            `idPart` INT NOT NULL,
                            `idHex` INT NOT NULL,
                            PRIMARY KEY (`idLocation`, `idPart`, `idHex`, `idEnemy`)
);

CREATE TABLE `EnemyAction` (
                               `idEnemy` INT NOT NULL,
                               `idAction` INT NOT NULL,
                               PRIMARY KEY (`idEnemy`, `idAction`)
);

CREATE TABLE `Action` (
                          `id` INT NOT NULL AUTO_INCREMENT,
                          `title` VARCHAR(128) NOT NULL,
                          `description` TEXT,
                          `movement` INT,
                          `skill` INT,
                          `attack` INT,
                          `restoreCards` INT,
                          `discard` ENUM ('PERMANENT', 'SHORT_REST', 'LONG_REST', 'NEVER') DEFAULT 'NEVER',
                          `levelReq` INT,
                          PRIMARY KEY (`id`)
);

CREATE TABLE `Summon` (
                          `id` INT NOT NULL AUTO_INCREMENT,
                          `title` VARCHAR(128) NOT NULL,
                          `tag` VARCHAR(32),
                          `duration` INT NOT NULL,
                          `health` INT NOT NULL,
                          `idAction` INT,
                          PRIMARY KEY (`id`)
);

CREATE TABLE `SummonAction` (
                                `idSummon` INT NOT NULL,
                                `idAction` INT NOT NULL,
                                `range` INT,
                                PRIMARY KEY (`idSummon`, `idAction`)
);

CREATE TABLE `Attack` (
                          `id` INT NOT NULL AUTO_INCREMENT,
                          `range` INT NOT NULL,
                          `damage` INT NOT NULL,
                          `area` INT,
                          `target` ENUM ('SELF', 'ONE', 'ALL', 'ALL_ENEMIES', 'ALL_ALLIES') NOT NULL,
                          `numAttacks` INT NOT NULL,
                          PRIMARY KEY (`id`)
);

CREATE TABLE `Skill` (
                         `id` INT NOT NULL AUTO_INCREMENT,
                         `range` INT NOT NULL,
                         `area` INT,
                         `target` ENUM ('SELF', 'ONE', 'ALL', 'ALL_ENEMIES', 'ALL_ALLIES') NOT NULL,
                         PRIMARY KEY (`id`)
);

CREATE TABLE `Movement` (
                            `id` INT NOT NULL AUTO_INCREMENT,
                            `range` INT NOT NULL,
                            `type` ENUM ('WALK', 'JUMP', 'TELEPORT') NOT NULL DEFAULT 'WALK',
                            PRIMARY KEY (`id`)
);

CREATE TABLE `RestoreCards` (
                                `id` INT NOT NULL AUTO_INCREMENT,
                                `numCards` INT NOT NULL,
                                `target` ENUM ('SELF', 'ONE', 'ALL', 'ALL_ENEMIES', 'ALL_ALLIES') NOT NULL,
                                `random` BOOL NOT NULL,
                                PRIMARY KEY (`id`)
);

CREATE TABLE `Effect` (
                          `id` INT NOT NULL AUTO_INCREMENT,
                          `type` ENUM ('PUSH', 'PULL', 'FORCED_MOVEMENT_RESISTANCE', 'POISON', 'POISON_RESISTANCE', 'FIRE', 'FIRE_RESISTANCE', 'BLEED', 'BLEED_RESISTANCE', 'STUN', 'STUN_RESISTANCE', 'PROTECTION', 'WEAKNESS', 'WEAKNESS_RESISTANCE', 'HEAL', 'REGENERATION', 'EMPOWER', 'ENFEEBLE', 'ENFEEBLE_RESISTANCE') NOT NULL,
                          `description` TEXT,
                          `duration` INT,
                          `strength` INT,
                          `target` ENUM ('SELF', 'ONE', 'ALL', 'ALL_ENEMIES', 'ALL_ALLIES') NOT NULL,
                          PRIMARY KEY (`id`)
);

CREATE TABLE `SummonEffect` (
                                `idSummon` INT NOT NULL,
                                `idEffect` INT NOT NULL,
                                PRIMARY KEY (`idSummon`, `idEffect`)
);

CREATE TABLE `AttackEffect` (
                                `idAttack` INT NOT NULL,
                                `idEffect` INT NOT NULL,
                                PRIMARY KEY (`idAttack`, `idEffect`)
);

CREATE TABLE `SkillEffect` (
                               `idSkill` INT NOT NULL,
                               `idEffect` INT NOT NULL,
                               PRIMARY KEY (`idSkill`, `idEffect`)
);

CREATE TABLE `MovementEffect` (
                                  `idMovement` INT NOT NULL,
                                  `idEffect` INT NOT NULL,
                                  PRIMARY KEY (`idMovement`, `idEffect`)
);

CREATE TABLE `ClassEffect` (
                               `idClass` INT NOT NULL,
                               `idEffect` INT NOT NULL,
                               `levelReq` INT,
                               PRIMARY KEY (`idClass`, `idEffect`)
);

CREATE TABLE `RaceEffect` (
                              `idRace` INT NOT NULL,
                              `idEffect` INT NOT NULL,
                              `levelReq` INT,
                              PRIMARY KEY (`idRace`, `idEffect`)
);

CREATE TABLE `ItemEffect` (
                              `idItem` INT NOT NULL,
                              `idEffect` INT NOT NULL,
                              PRIMARY KEY (`idItem`, `idEffect`)
);

CREATE TABLE `EnemyEffect` (
                               `idEnemy` INT NOT NULL,
                               `idEffect` INT NOT NULL,
                               PRIMARY KEY (`idEnemy`, `idEffect`)
);

CREATE TABLE `ObstacleEffect` (
                                  `idObstacle` INT NOT NULL,
                                  `idEffect` INT NOT NULL,
                                  PRIMARY KEY (`idEffect`, `idObstacle`)
);

CREATE TABLE `HexObstacle` (
                               `idLocation` INT NOT NULL,
                               `idPart` INT NOT NULL,
                               `idHex` INT NOT NULL,
                               `idObstacle` INT NOT NULL,
                               PRIMARY KEY (`idLocation`, `idPart`, `idHex`, `idObstacle`)
);

CREATE TABLE `Obstacle` (
                            `id` INT NOT NULL AUTO_INCREMENT,
                            `title` VARCHAR(128) NOT NULL,
                            `tag` VARCHAR(32),
                            `description` TEXT,
                            `baseDamage` INT,
                            `baseHealth` INT,
                            `crossable` BOOL NOT NULL,
                            `usages` INT DEFAULT 0,
                            PRIMARY KEY (`id`)
);

CREATE TABLE `Race` (
                        `id` INT NOT NULL AUTO_INCREMENT,
                        `title` VARCHAR(128) NOT NULL,
                        `tag` VARCHAR(32),
                        `description` TEXT,
                        `baseInitiative` INT NOT NULL,
                        PRIMARY KEY (`id`)
);

CREATE TABLE `RaceAction` (
                              `idRace` INT NOT NULL,
                              `idAction` INT NOT NULL,
                              PRIMARY KEY (`idRace`, `idAction`)
);

CREATE TABLE `Achievement` (
                               `id` INT NOT NULL AUTO_INCREMENT,
                               `title` VARCHAR(128) NOT NULL,
                               `description` TEXT NOT NULL,
                               `xpReward` INT NOT NULL,
                               PRIMARY KEY (`id`)
);

CREATE TABLE `CampaignAchievements` (
                                        `idCampaign` INT NOT NULL,
                                        `idAchievement` INT NOT NULL,
                                        PRIMARY KEY (`idCampaign`, `idAchievement`)
);

CREATE TABLE `Item` (
                        `id` INT NOT NULL AUTO_INCREMENT,
                        `idAction` INT,
                        `title` VARCHAR(128) NOT NULL,
                        `tag` VARCHAR(32),
                        `type` ENUM ('WEAPON', 'HELMET', 'CHESTPLATE', 'LEGGINGS', 'BOOTS', 'ACCESSORY', 'CONSUMABLE') NOT NULL,
                        `description` TEXT,
                        `requirements` TEXT,
                        PRIMARY KEY (`id`)
);

CREATE TABLE `Market` (
                          `idLocation` INT NOT NULL,
                          `idItem` INT NOT NULL,
                          `defAmount` INT DEFAULT 1,
                          `defPrice` INT DEFAULT 0,
                          PRIMARY KEY (`idLocation`, `idItem`)
);

CREATE TABLE `AdventureMarket` (
                                   `idLocation` INT NOT NULL,
                                   `idItem` INT NOT NULL,
                                   `idAdventure` INT NOT NULL,
                                   `amount` INT DEFAULT 1,
                                   `price` INT DEFAULT 0,
                                   PRIMARY KEY (`idLocation`, `idItem`, `idAdventure`)
);

CREATE TABLE `ImageLink` (
                             `tag` VARCHAR(32) PRIMARY KEY,
                             `variation` INT DEFAULT 0,
                             `url` TEXT
);

CREATE INDEX `CampaignLocation_fk` ON `CampaignLocation` (`idCampaign`);

CREATE INDEX `LocationCampaign_fk` ON `CampaignLocation` (`idLocation`);

CREATE INDEX `uk_Adventure_idCampaign` ON `Adventure` (`idCampaign`);

CREATE INDEX `uk_Adventure_idLicense` ON `Adventure` (`idLicense`);

CREATE INDEX `uk_Character_idAdventure` ON `Character` (`idAdventure`);

CREATE INDEX `uk_Character_idClass` ON `Character` (`idClass`);

CREATE INDEX `uk_Character_idRace` ON `Character` (`idRace`);

CREATE INDEX `uk_ClassAction_idClass` ON `ClassAction` (`idClass`);

CREATE INDEX `uk_ClassAction_idAction` ON `ClassAction` (`idAction`);

CREATE INDEX `pk_Action_attack` ON `Action` (`attack`);

CREATE INDEX `pk_Action_skill` ON `Action` (`skill`);

CREATE INDEX `pk_Action_movement` ON `Action` (`movement`);

CREATE INDEX `pk_Action_restore_card` ON `Action` (`restoreCards`);

CREATE INDEX `uk_SummonAction_idSummon` ON `SummonAction` (`idSummon`);

CREATE INDEX `uk_SummonAction_idAction` ON `SummonAction` (`idAction`);

CREATE UNIQUE INDEX `uk_SummonEffect` ON `Effect` (`type`, `duration`, `target`, `strength`);

CREATE INDEX `uk_RaceAction_idRace` ON `RaceAction` (`idRace`);

CREATE INDEX `uk_RaceAction_idAction` ON `RaceAction` (`idAction`);

ALTER TABLE `CampaignLocation` ADD CONSTRAINT `fk_CampaignLocation_Campaign` FOREIGN KEY (`idCampaign`) REFERENCES `Campaign` (`id`) ON DELETE CASCADE;

ALTER TABLE `CampaignLocation` ADD CONSTRAINT `fk_CampaignLocation_Location` FOREIGN KEY (`idLocation`) REFERENCES `Location` (`id`) ON DELETE CASCADE;

ALTER TABLE `Story` ADD CONSTRAINT `fk_CampaignLocationStory_Campaign` FOREIGN KEY (`idCampaignLocation`) REFERENCES `CampaignLocation` (`id`) ON DELETE CASCADE;

ALTER TABLE `AdventureLocation` ADD CONSTRAINT `fk_AdventureLocation_Adventure` FOREIGN KEY (`idAdventure`) REFERENCES `Adventure` (`id`) ON DELETE CASCADE;

ALTER TABLE `AdventureLocation` ADD CONSTRAINT `fk_AdventureLocation_Location` FOREIGN KEY (`idLocation`) REFERENCES `Location` (`id`) ON DELETE CASCADE;

ALTER TABLE `Adventure` ADD CONSTRAINT `fk_Adventure_Campaign` FOREIGN KEY (`idCampaign`) REFERENCES `Campaign` (`id`) ON DELETE RESTRICT;

ALTER TABLE `Adventure` ADD CONSTRAINT `fk_Adventure_License` FOREIGN KEY (`idLicense`) REFERENCES `License` (`id`) ON DELETE RESTRICT;

ALTER TABLE `AdventureAchievement` ADD CONSTRAINT `fk_AdventureAchievement_Adventure` FOREIGN KEY (`idAdventure`) REFERENCES `Adventure` (`id`) ON DELETE CASCADE;

ALTER TABLE `AdventureAchievement` ADD CONSTRAINT `fk_AdventureAchievement_Achievement` FOREIGN KEY (`idAchievement`) REFERENCES `Achievement` (`id`) ON DELETE CASCADE;

ALTER TABLE `LocationPath` ADD CONSTRAINT `fk_LocationPath_idStart` FOREIGN KEY (`idStart`) REFERENCES `Location` (`id`) ON DELETE CASCADE;

ALTER TABLE `LocationPath` ADD CONSTRAINT `fk_LocationPath_idEnd` FOREIGN KEY (`idEnd`) REFERENCES `Location` (`id`) ON DELETE CASCADE;

ALTER TABLE `LocationPath` ADD CONSTRAINT `fk_LocationPath_idCampaign` FOREIGN KEY (`idCampaign`) REFERENCES `Campaign` (`id`) ON DELETE CASCADE;

ALTER TABLE `LocationPart` ADD CONSTRAINT `fk_LocationPart_Location` FOREIGN KEY (`idLocation`) REFERENCES `Location` (`id`) ON DELETE CASCADE;

ALTER TABLE `LocationPart` ADD CONSTRAINT `fk_LocationPart_Part` FOREIGN KEY (`idPart`) REFERENCES `Part` (`id`) ON DELETE CASCADE;

ALTER TABLE `Hex` ADD CONSTRAINT `fk_Hex_Part` FOREIGN KEY (`idPart`) REFERENCES `Part` (`id`) ON DELETE CASCADE;

ALTER TABLE `LocationDoor` ADD CONSTRAINT `fk_LocationDoor_Location` FOREIGN KEY (`idLocation`) REFERENCES `Location` (`id`) ON DELETE CASCADE;

ALTER TABLE `LocationDoor` ADD CONSTRAINT `fk_LocationDoor_idPartFrom` FOREIGN KEY (`idPartFrom`) REFERENCES `Part` (`id`) ON DELETE CASCADE;

ALTER TABLE `LocationDoor` ADD CONSTRAINT `fk_LocationDoor_idPartTo` FOREIGN KEY (`idPartTo`) REFERENCES `Part` (`id`) ON DELETE CASCADE;

ALTER TABLE `LocationStart` ADD CONSTRAINT `fk_LocationStart_location` FOREIGN KEY (`idLocation`) REFERENCES `Location` (`id`) ON DELETE CASCADE;

ALTER TABLE `LocationStart` ADD CONSTRAINT `fk_LocationStart_part` FOREIGN KEY (`idPart`) REFERENCES `Part` (`id`) ON DELETE CASCADE;

ALTER TABLE `LocationStart` ADD CONSTRAINT `fk_LocationStart_hex` FOREIGN KEY (`idHex`) REFERENCES `Hex` (`id`) ON DELETE CASCADE;

ALTER TABLE `Character` ADD CONSTRAINT `fk_Character_Adventure` FOREIGN KEY (`idAdventure`) REFERENCES `Adventure` (`id`) ON DELETE CASCADE;

ALTER TABLE `Character` ADD CONSTRAINT `fk_Character_Class` FOREIGN KEY (`idClass`) REFERENCES `Class` (`id`) ON DELETE RESTRICT;

ALTER TABLE `Character` ADD CONSTRAINT `fk_Character_Race` FOREIGN KEY (`idRace`) REFERENCES `Race` (`id`) ON DELETE RESTRICT;

ALTER TABLE `Inventory` ADD CONSTRAINT `fk_Inventory_Character` FOREIGN KEY (`idCharacter`) REFERENCES `Character` (`id`) ON DELETE CASCADE;

ALTER TABLE `Inventory` ADD CONSTRAINT `fk_Inventory_Item` FOREIGN KEY (`idItem`) REFERENCES `Item` (`id`) ON DELETE CASCADE;

ALTER TABLE `ClassAction` ADD CONSTRAINT `fk_Action_Class` FOREIGN KEY (`idClass`) REFERENCES `Class` (`id`) ON DELETE CASCADE;

ALTER TABLE `ClassAction` ADD CONSTRAINT `fk_ClassAction_Action` FOREIGN KEY (`idAction`) REFERENCES `Action` (`id`) ON DELETE CASCADE;

ALTER TABLE `HexEnemy` ADD CONSTRAINT `fk_HexEnemy_Enemy` FOREIGN KEY (`idEnemy`) REFERENCES `Enemy` (`id`) ON DELETE CASCADE;

ALTER TABLE `HexEnemy` ADD CONSTRAINT `fk_HexEnemy_Hex` FOREIGN KEY (`idHex`) REFERENCES `Hex` (`id`) ON DELETE CASCADE;

ALTER TABLE `HexEnemy` ADD CONSTRAINT `fk_HexEnemy_Part` FOREIGN KEY (`idPart`) REFERENCES `Part` (`id`) ON DELETE CASCADE;

ALTER TABLE `HexEnemy` ADD CONSTRAINT `fk_HexEnemy_Location` FOREIGN KEY (`idLocation`) REFERENCES `Location` (`id`) ON DELETE CASCADE;

ALTER TABLE `EnemyAction` ADD CONSTRAINT `fk_EnemyAction_Enemy` FOREIGN KEY (`idEnemy`) REFERENCES `Enemy` (`id`) ON DELETE CASCADE;

ALTER TABLE `EnemyAction` ADD CONSTRAINT `fk_EnemyAction_Action` FOREIGN KEY (`idAction`) REFERENCES `Action` (`id`) ON DELETE CASCADE;

ALTER TABLE `SummonAction` ADD CONSTRAINT `fk_SummonAction_Summon` FOREIGN KEY (`idSummon`) REFERENCES `Summon` (`id`) ON DELETE CASCADE;

ALTER TABLE `SummonAction` ADD CONSTRAINT `fk_SummonAction_Action` FOREIGN KEY (`idAction`) REFERENCES `Action` (`id`) ON DELETE CASCADE;

ALTER TABLE `Summon` ADD CONSTRAINT `fk_Summon_Action` FOREIGN KEY (`idAction`) REFERENCES `Action` (`id`) ON DELETE SET NULL;

ALTER TABLE `Action` ADD CONSTRAINT `fk_Action_Attack` FOREIGN KEY (`attack`) REFERENCES `Attack` (`id`) ON DELETE SET NULL;

ALTER TABLE `Action` ADD CONSTRAINT `fk_Action_Skill` FOREIGN KEY (`skill`) REFERENCES `Skill` (`id`) ON DELETE SET NULL;

ALTER TABLE `Action` ADD CONSTRAINT `fk_Action_Movement` FOREIGN KEY (`movement`) REFERENCES `Movement` (`id`) ON DELETE SET NULL;

ALTER TABLE `Action` ADD CONSTRAINT `fk_Action_RestoreCards` FOREIGN KEY (`restoreCards`) REFERENCES `RestoreCards` (`id`) ON DELETE SET NULL;

ALTER TABLE `SummonEffect` ADD CONSTRAINT `fk_SummonEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`) ON DELETE CASCADE;

ALTER TABLE `SummonEffect` ADD CONSTRAINT `fk_SummonEffect_Summon` FOREIGN KEY (`idSummon`) REFERENCES `Summon` (`id`) ON DELETE CASCADE;

ALTER TABLE `AttackEffect` ADD CONSTRAINT `fk_AttackEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`) ON DELETE CASCADE;

ALTER TABLE `AttackEffect` ADD CONSTRAINT `fk_AttackEffect_Attack` FOREIGN KEY (`idAttack`) REFERENCES `Attack` (`id`) ON DELETE CASCADE;

ALTER TABLE `SkillEffect` ADD CONSTRAINT `fk_SkillEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`) ON DELETE CASCADE;

ALTER TABLE `SkillEffect` ADD CONSTRAINT `fk_SkillEffect_Skill` FOREIGN KEY (`idSkill`) REFERENCES `Skill` (`id`) ON DELETE CASCADE;

ALTER TABLE `MovementEffect` ADD CONSTRAINT `fk_MovementEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`) ON DELETE CASCADE;

ALTER TABLE `MovementEffect` ADD CONSTRAINT `fk_MovementEffect_Movement` FOREIGN KEY (`idMovement`) REFERENCES `Movement` (`id`) ON DELETE CASCADE;

ALTER TABLE `ClassEffect` ADD CONSTRAINT `fk_ClassEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`) ON DELETE CASCADE;

ALTER TABLE `ClassEffect` ADD CONSTRAINT `fk_ClassEffect_Class` FOREIGN KEY (`idClass`) REFERENCES `Class` (`id`) ON DELETE CASCADE;

ALTER TABLE `RaceEffect` ADD CONSTRAINT `fk_RaceEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`) ON DELETE CASCADE;

ALTER TABLE `RaceEffect` ADD CONSTRAINT `fk_RaceEffect_Race` FOREIGN KEY (`idRace`) REFERENCES `Race` (`id`) ON DELETE CASCADE;

ALTER TABLE `ItemEffect` ADD CONSTRAINT `fk_ItemEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`) ON DELETE CASCADE;

ALTER TABLE `ItemEffect` ADD CONSTRAINT `fk_ItemEffect_Item` FOREIGN KEY (`idItem`) REFERENCES `Item` (`id`) ON DELETE CASCADE;

ALTER TABLE `EnemyEffect` ADD CONSTRAINT `fk_EnemyEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`) ON DELETE CASCADE;

ALTER TABLE `EnemyEffect` ADD CONSTRAINT `fk_EnemyEffect_Enemy` FOREIGN KEY (`idEnemy`) REFERENCES `Enemy` (`id`) ON DELETE CASCADE;

ALTER TABLE `ObstacleEffect` ADD CONSTRAINT `fk_ObstacleEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`) ON DELETE CASCADE;

ALTER TABLE `ObstacleEffect` ADD CONSTRAINT `fk_ObstacleEffect_Obstacle` FOREIGN KEY (`idObstacle`) REFERENCES `Obstacle` (`id`) ON DELETE CASCADE;

ALTER TABLE `HexObstacle` ADD CONSTRAINT `fk_HexObstacle_Hex` FOREIGN KEY (`idHex`) REFERENCES `Hex` (`id`) ON DELETE CASCADE;

ALTER TABLE `HexObstacle` ADD CONSTRAINT `fk_HexObstacle_Location` FOREIGN KEY (`idLocation`) REFERENCES `Location` (`id`) ON DELETE CASCADE;

ALTER TABLE `HexObstacle` ADD CONSTRAINT `fk_HexObstacle_Part` FOREIGN KEY (`idPart`) REFERENCES `Part` (`id`) ON DELETE CASCADE;

ALTER TABLE `HexObstacle` ADD CONSTRAINT `fk_HexObstacle_Obstacle` FOREIGN KEY (`idObstacle`) REFERENCES `Obstacle` (`id`) ON DELETE CASCADE;

ALTER TABLE `RaceAction` ADD CONSTRAINT `fk_Action_Race` FOREIGN KEY (`idRace`) REFERENCES `Race` (`id`) ON DELETE CASCADE;

ALTER TABLE `RaceAction` ADD CONSTRAINT `fk_RaceAction_Action` FOREIGN KEY (`idAction`) REFERENCES `Action` (`id`) ON DELETE CASCADE;

ALTER TABLE `CampaignAchievements` ADD CONSTRAINT `fk_CampaignAchievements_Campaign` FOREIGN KEY (`idCampaign`) REFERENCES `Campaign` (`id`) ON DELETE CASCADE;

ALTER TABLE `CampaignAchievements` ADD CONSTRAINT `fk_CampaignAchievements_Achievement` FOREIGN KEY (`idAchievement`) REFERENCES `Achievement` (`id`) ON DELETE CASCADE;

ALTER TABLE `Item` ADD CONSTRAINT `fk_Item_Action` FOREIGN KEY (`idAction`) REFERENCES `Action` (`id`) ON DELETE SET NULL;

ALTER TABLE `Market` ADD CONSTRAINT `fk_Market_Item` FOREIGN KEY (`idItem`) REFERENCES `Item` (`id`) ON DELETE CASCADE;

ALTER TABLE `Market` ADD CONSTRAINT `fk_Market_Location` FOREIGN KEY (`idLocation`) REFERENCES `Location` (`id`) ON DELETE CASCADE;

ALTER TABLE `AdventureMarket` ADD CONSTRAINT `fk_AdventureMarket_Item` FOREIGN KEY (`idItem`) REFERENCES `Item` (`id`) ON DELETE CASCADE;

ALTER TABLE `AdventureMarket` ADD CONSTRAINT `fk_AdventureMarket_Location` FOREIGN KEY (`idLocation`) REFERENCES `Location` (`id`) ON DELETE CASCADE;

ALTER TABLE `AdventureMarket` ADD CONSTRAINT `fk_AdventureMarket_Adventure` FOREIGN KEY (`idAdventure`) REFERENCES `Adventure` (`id`) ON DELETE CASCADE;
