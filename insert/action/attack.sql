INSERT INTO Attack (id, `range`, damage, area, target, numAttacks)
VALUES
    (1, 1, 1, null, 'ONE', 1),
    (2, 1, 5, null, 'ONE', 1),
    (3, 2, 3, null, 'ALL', 1),
    (4, 2, 2, 2, 'ALL', 1),
    (5, 3, 8, null, 'ONE', 2),
    (6, 3, 1, 3, 'ALL', 1),
    (7, 1, 7, null, 'SELF', 1),
    (8, 4, 10, null, 'ONE', 1),
    (9, 5, 0, null, 'SELF', 2),
    (10, 4, 6, null, 'ALL', 1);
