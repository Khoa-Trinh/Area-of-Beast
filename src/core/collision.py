def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def handle_collisions(player1, player2):
    if check_collision(player1.hitbox, player2.hurtbox) and player1.is_attacking == True:
        player2.take_damage(player1.attack_power)
    if check_collision(player2.hitbox, player1.hurtbox) and player2.is_attacking == True:
        player1.take_damage(player2.attack_power)

def update_hitboxes(character):
    character.hitbox = character.rect.inflate(character.attack_range, character.attack_range)
    character.hurtbox = character.rect.inflate(-character.hurt_range, -character.hurt_range)