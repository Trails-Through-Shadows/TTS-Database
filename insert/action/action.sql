INSERT INTO Action (id, title, description, attack, skill, movement, restore_cards, discard)
VALUES
    (1, 'Basic Attack', 'A standard melee attack.', 1, null, 1, null, 'PERMANENT'),
    (2, 'Fireball', 'Casts a fiery spell at a target.', null, 1, 1, null, 'LONG_REST'),
    (3, 'Healing Touch', 'A gentle touch that heals the target.', null, 2, 1, null, 'SHORT_REST'),
    (4, 'Swift Movement', 'Quickly move to a nearby location.', null, null, 4, null, 'PERMANENT'),
    (5, 'Draw Cards', 'Replenish your hand with new cards.', null, null, 1, 10, 'LONG_REST');
