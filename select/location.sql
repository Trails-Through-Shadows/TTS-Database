-- Show all parts of current location
SELECT LocPart.idPart AS Part FROM Location Loc
JOIN LocationPart LocPart on Loc.id = LocPart.idLocation
WHERE Loc.id = 1;

-- Show all hexes of current location, with obstacles and enemies
SELECT Hex.idPart AS Part, Hex.id AS Hex, HexObst.idObstacle AS Obstacle, HexEnemy.idEnemy AS Enemy FROM Location Loc
JOIN LocationPart LocPart on Loc.id = LocPart.idLocation
JOIN Hex on LocPart.idPart = Hex.idPart
LEFT JOIN HexObstacle HexObst on Hex.id = HexObst.idHex
LEFT JOIN HexEnemy on Hex.id = HexEnemy.idHex
WHERE Loc.id = 1;