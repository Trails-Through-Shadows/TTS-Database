CREATE TABLE `License` (
                           `id` INT NOT NULL AUTO_INCREMENT,
                           `key` VARCHAR(20) NOT NULL,
                           `password` TEXT NOT NULL,
                           `activated` DATETIME,
                           PRIMARY KEY (`id`)
);

CREATE TABLE `Campaign` (
                            `id` INT NOT NULL AUTO_INCREMENT,
                            `title` VARCHAR(50) NOT NULL,
                            `description` TEXT,
                            PRIMARY KEY (`id`)
);

CREATE TABLE `CampaignLocation` (
                                    `idCampaign` INT NOT NULL,
                                    `idLocation` INT NOT NULL,
                                    PRIMARY KEY (`idCampaign`, `idLocation`)
);

CREATE TABLE `Adventure` (
                             `id` INT NOT NULL,
                             `idCampaign` INT NOT NULL,
                             `idLicense` INT NOT NULL,
                             `reputation` INT NOT NULL,
                             `partyXp` INT NOT NULL,
                             PRIMARY KEY (`id`)
);

CREATE TABLE `AdventureAchievements` (
                                         `idAdventure` INT NOT NULL,
                                         `idAchievement` INT NOT NULL,
                                         `progress` INT NOT NULL,
                                         PRIMARY KEY (`idAdventure`, `idAchievement`)
);

CREATE TABLE `Location` (
                            `id` INT NOT NULL AUTO_INCREMENT,
                            `title` VARCHAR(100) NOT NULL,
                            `tag` VARCHAR(30),
                            `type` ENUM ('CITY', 'DUNGEON', 'MARKET', 'QUEST') NOT NULL,
                            `description` TEXT,
                            PRIMARY KEY (`id`)
);

CREATE TABLE `Path` (
                        `idStart` INT NOT NULL,
                        `idEnd` INT NOT NULL
);

CREATE TABLE `LocationPart` (
                                `idLocation` INT NOT NULL,
                                `idPart` INT NOT NULL,
                                `rotation` INT NOT NULL DEFAULT 0,
                                PRIMARY KEY (`idLocation`, `idPart`)
);

CREATE TABLE `Part` (
                        `id` INT NOT NULL AUTO_INCREMENT,
                        `tag` VARCHAR(30),
                        `usages` INT DEFAULT 0,
                        PRIMARY KEY (`id`)
);

CREATE TABLE `Hex` (
                       `idPart` INT NOT NULL,
                       `id` INT NOT NULL AUTO_INCREMENT,
                       `qCord` INT NOT NULL DEFAULT 0,
                       `rCord` INT NOT NULL DEFAULT 0,
                       `sCord` INT NOT NULL DEFAULT 0,
                       PRIMARY KEY (`id`, `idPart`)
);

CREATE TABLE `PartDoor` (
                            `location` INT NOT NULL,
                            `fromPart` INT NOT NULL,
                            `toPart` INT NOT NULL,
                            `hex` INT NOT NULL,
                            PRIMARY KEY (`location`, `fromPart`, `hex`)
);

CREATE TABLE `Class` (
                         `id` INT NOT NULL AUTO_INCREMENT,
                         `name` VARCHAR(50) NOT NULL,
                         `baseHealth` INT NOT NULL,
                         PRIMARY KEY (`id`)
);

CREATE TABLE `Character` (
                             `id` INT NOT NULL AUTO_INCREMENT,
                             `idAdventure` INT NOT NULL,
                             `idClass` INT NOT NULL,
                             `idRace` INT NOT NULL,
                             `level` INT NOT NULL,
                             `name` VARCHAR(50) NOT NULL,
                             `playerName` VARCHAR(50),
                             PRIMARY KEY (`id`)
);

CREATE TABLE `Inventory` (
                             `idCharacter` INT NOT NULL,
                             `idItem` INT NOT NULL,
                             `amount` INT DEFAULT 1,
                             PRIMARY KEY (`idCharacter`, `idItem`)
);

CREATE TABLE `ClassAction` (
                               `id` INT NOT NULL AUTO_INCREMENT,
                               `idClass` INT NOT NULL,
                               `levelReq` INT,
                               `itemReq` INT,
                               `idAction` INT NOT NULL,
                               PRIMARY KEY (`id`)
);

CREATE TABLE `Enemy` (
                         `id` INT NOT NULL AUTO_INCREMENT,
                         `name` VARCHAR(45) NOT NULL,
                         `health` INT NOT NULL,
                         `defence` INT NOT NULL,
                         `combatStyle` ENUM ('MELEE', 'RANGED') NOT NULL,
                         PRIMARY KEY (`id`)
);

CREATE TABLE `HexEnemy` (
                            `idEnemy` INT NOT NULL,
                            `idLocation` INT NOT NULL,
                            `idPart` INT NOT NULL,
                            `idHex` INT NOT NULL,
                            PRIMARY KEY (`idLocation`, `idPart`, `idHex`)
);

CREATE TABLE `EnemyAction` (
                               `id` INT NOT NULL AUTO_INCREMENT,
                               `idEnemy` INT NOT NULL,
                               `levelReq` INT NOT NULL,
                               `idAction` INT NOT NULL,
                               PRIMARY KEY (`id`)
);

CREATE TABLE `Action` (
                          `id` INT NOT NULL AUTO_INCREMENT,
                          `title` VARCHAR(50) NOT NULL,
                          `description` TEXT,
                          `movement` INT,
                          `skill` INT,
                          `attack` INT,
                          `restoreCards` INT,
                          `discard` ENUM ('PERMANENT', 'SHORT_REST', 'LONG_REST', 'NEVER') DEFAULT "NEVER",
                          PRIMARY KEY (`id`)
);

CREATE TABLE `Summon` (
                          `id` INT NOT NULL AUTO_INCREMENT,
                          `name` VARCHAR(50) NOT NULL,
                          `duration` INT,
                          `health` INT,
                          `combatStyle` ENUM ('MELEE', 'RANGED') NOT NULL,
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
                            `type` ENUM ('WALK', 'JUMP') NOT NULL DEFAULT "WALK",
                            PRIMARY KEY (`id`)
);

CREATE TABLE `RestoreCards` (
                                `id` INT NOT NULL AUTO_INCREMENT,
                                `numCards` INT,
                                `target` ENUM ('SELF', 'ONE', 'ALL', 'ALL_ENEMIES', 'ALL_ALLIES') NOT NULL,
                                `random` BOOL,
                                PRIMARY KEY (`id`)
);

CREATE TABLE `Effect` (
                          `id` INT NOT NULL AUTO_INCREMENT,
                          `type` ENUM ('PUSH', 'PULL', 'FORCED_MOVEMENT_RESISTANCE', 'POISON', 'POISON_RESISTANCE', 'FIRE', 'FIRE_RESISTANCE', 'BLEED', 'BLEED_RESISTANCE', 'DISARM', 'DISARM_RESISTANCE', 'STUN', 'STUN_RESISTANCE', 'CONFUSION', 'CONFUSION_RESISTANCE', 'CHARM', 'CHARM_RESISTANCE', 'FEAR', 'FEAR_RESISTANCE', 'INVISIBILITY', 'SHIELD', 'HEAL', 'REGENERATION', 'BONUS_HEALTH', 'BONUS_DAMAGE', 'BONUS_MOVEMENT') NOT NULL,
                          `duration` INT NOT NULL,
                          `target` ENUM ('SELF', 'ONE', 'ALL', 'ALL_ENEMIES', 'ALL_ALLIES') NOT NULL,
                          `strength` INT,
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
                               `levelReq` INT,
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
                               PRIMARY KEY (`idLocation`, `idPart`, `idHex`)
);

CREATE TABLE `Obstacle` (
                            `id` INT NOT NULL AUTO_INCREMENT,
                            `name` VARCHAR(50) NOT NULL,
                            `damage` INT,
                            `health` INT,
                            `crossable` BOOL NOT NULL,
                            PRIMARY KEY (`id`)
);

CREATE TABLE `Race` (
                        `id` INT NOT NULL AUTO_INCREMENT,
                        `name` VARCHAR(50) NOT NULL,
                        PRIMARY KEY (`id`)
);

CREATE TABLE `RaceAction` (
                              `id` INT NOT NULL AUTO_INCREMENT,
                              `idRace` INT NOT NULL,
                              `levelReq` INT,
                              `idAction` INT NOT NULL,
                              PRIMARY KEY (`id`)
);

CREATE TABLE `Achievement` (
                               `id` INT NOT NULL AUTO_INCREMENT,
                               `title` VARCHAR(50) NOT NULL,
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
                        `id` INT NOT NULL,
                        `title` VARCHAR(50) NOT NULL,
                        `type` ENUM ('WEAPON', 'POTION', 'HELMET', 'CHESTPLATE', 'LEGGINGS', 'BOOTS', 'ACCESSORY', 'SHIELD', 'SCROLL', 'WAND', 'STAFF', 'BOOK', 'CONSUMABLE', 'TOOL', 'MISC') NOT NULL,
                        `description` TEXT,
                        PRIMARY KEY (`id`)
);

CREATE TABLE `Market` (
                          `id` INT NOT NULL,
                          `idLocation` INT NOT NULL,
                          PRIMARY KEY (`id`)
);

CREATE TABLE `MarketItem` (
                              `idMarket` INT NOT NULL,
                              `idItem` INT NOT NULL,
                              `price` INT,
                              `requirements` TEXT,
                              PRIMARY KEY (`idMarket`, `idItem`)
);

CREATE INDEX `uk_Adventure_idCampaign` ON `Adventure` (`idCampaign`);

CREATE INDEX `uk_Adventure_idLicense` ON `Adventure` (`idLicense`);

CREATE INDEX `uk_Path_idStart` ON `Path` (`idStart`);

CREATE INDEX `uk_Path_idEnd` ON `Path` (`idEnd`);

CREATE INDEX `uk_Character_idAdventure` ON `Character` (`idAdventure`);

CREATE INDEX `uk_Character_idClass` ON `Character` (`idClass`);

CREATE INDEX `uk_Character-idRace` ON `Character` (`idRace`);

CREATE INDEX `uk_ClassAction_idItem` ON `ClassAction` (`itemReq`);

CREATE INDEX `uk_ClassAction_idClass` ON `ClassAction` (`idClass`);

CREATE INDEX `uk_ClassAction_idAction` ON `ClassAction` (`idAction`);

CREATE INDEX `uk_HexEnemy_idEnemy` ON `HexEnemy` (`idEnemy`);

CREATE INDEX `uk_EnemyAction_idEnemy` ON `EnemyAction` (`idEnemy`);

CREATE INDEX `uk_EnemyAction_idAction` ON `EnemyAction` (`idAction`);

CREATE INDEX `pk_Action_attack` ON `Action` (`attack`);

CREATE INDEX `pk_Action_skill` ON `Action` (`skill`);

CREATE INDEX `pk_Action_movement` ON `Action` (`movement`);

CREATE INDEX `pk_Action_restore_card` ON `Action` (`restoreCards`);

CREATE INDEX `uk_SummonAction_idSummon` ON `SummonAction` (`idSummon`);

CREATE INDEX `uk_SummonAction_idAction` ON `SummonAction` (`idAction`);

CREATE UNIQUE INDEX `uk_SummonEffect` ON `Effect` (`type`, `duration`, `target`, `strength`);

CREATE INDEX `uk_HexObstacle_idLocation` ON `HexObstacle` (`idLocation`);

CREATE INDEX `uk_RaceAction_idRace` ON `RaceAction` (`idRace`);

CREATE INDEX `uk_RaceAction_idAction` ON `RaceAction` (`idAction`);

CREATE UNIQUE INDEX `uk_Market_Location` ON `Market` (`idLocation`);

ALTER TABLE `CampaignLocation` ADD CONSTRAINT `fk_CampaignLocation_Campaign` FOREIGN KEY (`idCampaign`) REFERENCES `Campaign` (`id`);

ALTER TABLE `CampaignLocation` ADD CONSTRAINT `fk_CampaignLocation_Location` FOREIGN KEY (`idLocation`) REFERENCES `Location` (`id`);

ALTER TABLE `Adventure` ADD CONSTRAINT `fk_Adventure_Campaign` FOREIGN KEY (`idCampaign`) REFERENCES `Campaign` (`id`);

ALTER TABLE `Adventure` ADD CONSTRAINT `fk_Adventure_License` FOREIGN KEY (`idLicense`) REFERENCES `License` (`id`);

ALTER TABLE `AdventureAchievements` ADD CONSTRAINT `fk_AdventureAchievements_Adventure` FOREIGN KEY (`idAdventure`) REFERENCES `Adventure` (`id`);

ALTER TABLE `AdventureAchievements` ADD CONSTRAINT `fk_AdventureAchievements_Achievement` FOREIGN KEY (`idAchievement`) REFERENCES `Achievement` (`id`);

ALTER TABLE `Path` ADD CONSTRAINT `fk_Path_idStart` FOREIGN KEY (`idStart`) REFERENCES `Location` (`id`);

ALTER TABLE `Path` ADD CONSTRAINT `fk_Path_idEnd` FOREIGN KEY (`idEnd`) REFERENCES `Location` (`id`);

ALTER TABLE `LocationPart` ADD CONSTRAINT `fk_LocationPart_Location` FOREIGN KEY (`idLocation`) REFERENCES `Location` (`id`) ON DELETE CASCADE;

ALTER TABLE `LocationPart` ADD CONSTRAINT `fk_LocationPart_Part` FOREIGN KEY (`idPart`) REFERENCES `Part` (`id`) ON DELETE CASCADE;

ALTER TABLE `Hex` ADD CONSTRAINT `fk_Hex_Part` FOREIGN KEY (`idPart`) REFERENCES `Part` (`id`) ON DELETE CASCADE;

ALTER TABLE `PartDoor` ADD CONSTRAINT `fk_PartDoor_Location` FOREIGN KEY (`location`) REFERENCES `Location` (`id`) ON DELETE CASCADE;

ALTER TABLE `PartDoor` ADD CONSTRAINT `fk_PartDoor_fromPart` FOREIGN KEY (`fromPart`) REFERENCES `Part` (`id`) ON DELETE CASCADE;

ALTER TABLE `PartDoor` ADD CONSTRAINT `fk_PartDoor_toPart` FOREIGN KEY (`toPart`) REFERENCES `Part` (`id`) ON DELETE CASCADE;

ALTER TABLE `PartDoor` ADD CONSTRAINT `fk_PartDoor_hex` FOREIGN KEY (`hex`) REFERENCES `Hex` (`id`) ON DELETE CASCADE;

ALTER TABLE `Character` ADD CONSTRAINT `fk_Character_Adventure` FOREIGN KEY (`idAdventure`) REFERENCES `Adventure` (`id`);

ALTER TABLE `Character` ADD CONSTRAINT `fk_Character_Class` FOREIGN KEY (`idClass`) REFERENCES `Class` (`id`);

ALTER TABLE `Inventory` ADD CONSTRAINT `fk_Inventory_Character` FOREIGN KEY (`idCharacter`) REFERENCES `Character` (`id`);

ALTER TABLE `Inventory` ADD CONSTRAINT `fk_Inventory_Item` FOREIGN KEY (`idItem`) REFERENCES `Item` (`id`);

ALTER TABLE `ClassAction` ADD CONSTRAINT `fk_Action_Item` FOREIGN KEY (`itemReq`) REFERENCES `Item` (`id`);

ALTER TABLE `ClassAction` ADD CONSTRAINT `fk_Action_Class` FOREIGN KEY (`idClass`) REFERENCES `Class` (`id`);

ALTER TABLE `ClassAction` ADD CONSTRAINT `fk_ClassAction_Action` FOREIGN KEY (`idAction`) REFERENCES `Action` (`id`);

ALTER TABLE `HexEnemy` ADD CONSTRAINT `fk_HexEnemy_Enemy` FOREIGN KEY (`idEnemy`) REFERENCES `Enemy` (`id`) ON DELETE CASCADE;

ALTER TABLE `HexEnemy` ADD CONSTRAINT `fk_HexEnemy_Hex` FOREIGN KEY (`idHex`) REFERENCES `Hex` (`id`) ON DELETE CASCADE;

ALTER TABLE `HexEnemy` ADD CONSTRAINT `fk_HexEnemy_Part` FOREIGN KEY (`idPart`) REFERENCES `Part` (`id`) ON DELETE CASCADE;

ALTER TABLE `HexEnemy` ADD CONSTRAINT `fk_HexEnemy_Location` FOREIGN KEY (`idLocation`) REFERENCES `Location` (`id`) ON DELETE CASCADE;

ALTER TABLE `EnemyAction` ADD CONSTRAINT `fk_EnemyAction_Enemy` FOREIGN KEY (`idEnemy`) REFERENCES `Enemy` (`id`);

ALTER TABLE `EnemyAction` ADD CONSTRAINT `fk_EnemyAction_Action` FOREIGN KEY (`idAction`) REFERENCES `Action` (`id`);

ALTER TABLE `SummonAction` ADD CONSTRAINT `fk_SummonAction_Summon` FOREIGN KEY (`idSummon`) REFERENCES `Summon` (`id`);

ALTER TABLE `SummonAction` ADD CONSTRAINT `fk_SummonAction_Action` FOREIGN KEY (`idAction`) REFERENCES `Action` (`id`);

ALTER TABLE `Summon` ADD CONSTRAINT `fk_Summon_Action` FOREIGN KEY (`idAction`) REFERENCES `Action` (`id`);

ALTER TABLE `Action` ADD CONSTRAINT `fk_Action_Attack` FOREIGN KEY (`attack`) REFERENCES `Attack` (`id`);

ALTER TABLE `Action` ADD CONSTRAINT `fk_Action_Skill` FOREIGN KEY (`skill`) REFERENCES `Skill` (`id`);

ALTER TABLE `Action` ADD CONSTRAINT `fk_Action_Movement` FOREIGN KEY (`movement`) REFERENCES `Movement` (`id`);

ALTER TABLE `Action` ADD CONSTRAINT `fk_Action_RestoreCards` FOREIGN KEY (`restoreCards`) REFERENCES `RestoreCards` (`id`);

ALTER TABLE `SummonEffect` ADD CONSTRAINT `fk_SummonEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`);

ALTER TABLE `SummonEffect` ADD CONSTRAINT `fk_SummonEffect_Summon` FOREIGN KEY (`idSummon`) REFERENCES `Summon` (`id`);

ALTER TABLE `AttackEffect` ADD CONSTRAINT `fk_AttackEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`);

ALTER TABLE `AttackEffect` ADD CONSTRAINT `fk_AttackEffect_Attack` FOREIGN KEY (`idAttack`) REFERENCES `Attack` (`id`);

ALTER TABLE `SkillEffect` ADD CONSTRAINT `fk_SkillEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`);

ALTER TABLE `SkillEffect` ADD CONSTRAINT `fk_SkillEffect_Skill` FOREIGN KEY (`idSkill`) REFERENCES `Skill` (`id`);

ALTER TABLE `MovementEffect` ADD CONSTRAINT `fk_MovementEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`);

ALTER TABLE `MovementEffect` ADD CONSTRAINT `fk_MovementEffect_Movement` FOREIGN KEY (`idMovement`) REFERENCES `Movement` (`id`);

ALTER TABLE `ClassEffect` ADD CONSTRAINT `fk_ClassEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`);

ALTER TABLE `ClassEffect` ADD CONSTRAINT `fk_ClassEffect_Class` FOREIGN KEY (`idClass`) REFERENCES `Class` (`id`);

ALTER TABLE `RaceEffect` ADD CONSTRAINT `fk_RaceEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`);

ALTER TABLE `RaceEffect` ADD CONSTRAINT `fk_RaceEffect_Race` FOREIGN KEY (`idRace`) REFERENCES `Race` (`id`);

ALTER TABLE `ItemEffect` ADD CONSTRAINT `fk_ItemEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`);

ALTER TABLE `ItemEffect` ADD CONSTRAINT `fk_ItemEffect_Item` FOREIGN KEY (`idItem`) REFERENCES `Item` (`id`);

ALTER TABLE `EnemyEffect` ADD CONSTRAINT `fk_EnemyEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`);

ALTER TABLE `EnemyEffect` ADD CONSTRAINT `fk_EnemyEffect_Enemy` FOREIGN KEY (`idEnemy`) REFERENCES `Enemy` (`id`);

ALTER TABLE `ObstacleEffect` ADD CONSTRAINT `fk_ObstacleEffect_Effect` FOREIGN KEY (`idEffect`) REFERENCES `Effect` (`id`);

ALTER TABLE `ObstacleEffect` ADD CONSTRAINT `fk_ObstacleEffect_Obstacle` FOREIGN KEY (`idObstacle`) REFERENCES `Obstacle` (`id`);

ALTER TABLE `HexObstacle` ADD CONSTRAINT `fk_HexObstacle_Hex` FOREIGN KEY (`idHex`) REFERENCES `Hex` (`id`) ON DELETE CASCADE;

ALTER TABLE `HexObstacle` ADD CONSTRAINT `fk_HexObstacle_Location` FOREIGN KEY (`idLocation`) REFERENCES `Location` (`id`) ON DELETE CASCADE;

ALTER TABLE `HexObstacle` ADD CONSTRAINT `fk_HexObstacle_Part` FOREIGN KEY (`idPart`) REFERENCES `Part` (`id`) ON DELETE CASCADE;

ALTER TABLE `HexObstacle` ADD CONSTRAINT `fk_HexObstacle_Obstacle` FOREIGN KEY (`idObstacle`) REFERENCES `Obstacle` (`id`) ON DELETE CASCADE;

ALTER TABLE `Character` ADD CONSTRAINT `fk_Character_Race` FOREIGN KEY (`idRace`) REFERENCES `Race` (`id`);

ALTER TABLE `RaceAction` ADD CONSTRAINT `fk_Action_Race` FOREIGN KEY (`idRace`) REFERENCES `Race` (`id`);

ALTER TABLE `RaceAction` ADD CONSTRAINT `fk_RaceAction_Action` FOREIGN KEY (`idAction`) REFERENCES `Action` (`id`);

ALTER TABLE `CampaignAchievements` ADD CONSTRAINT `fk_CampaignAchievements_Campaign` FOREIGN KEY (`idCampaign`) REFERENCES `Campaign` (`id`);

ALTER TABLE `CampaignAchievements` ADD CONSTRAINT `fk_CampaignAchievements_Achievement` FOREIGN KEY (`idAchievement`) REFERENCES `Achievement` (`id`);

ALTER TABLE `Market` ADD CONSTRAINT `fk_Market_Location` FOREIGN KEY (`idLocation`) REFERENCES `Location` (`id`);

ALTER TABLE `MarketItem` ADD CONSTRAINT `fk_MarketItem_Item` FOREIGN KEY (`idItem`) REFERENCES `Item` (`id`);

ALTER TABLE `MarketItem` ADD CONSTRAINT `fk_MarketItem_Market` FOREIGN KEY (`idMarket`) REFERENCES `Market` (`id`);
