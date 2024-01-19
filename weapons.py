import pygame
from settings import *
from spritesheet import Spritesheet


class Weapon(object):
    def __init__(self, bullet_groups, enemy_group) -> None:
        self.bullet_groups = bullet_groups
        self.enemy_group = enemy_group
        self.max_ammo = 50
        self.ammo = self.max_ammo
        self.damage = 10
        self.fire_cooldown = 100
        self.reload_cooldown = 1500
        self.reloading = False
        self.last_reload_time = 0
        self.last_fired = 0


    def fire(self, pos, direction, angle):
        now = pygame.time.get_ticks()
        if now - self.last_fired > self.fire_cooldown and self.ammo > 0:
            Bullet( pos,self.bullet_groups ,self.enemy_group, direction, angle)
            self.last_fired = pygame.time.get_ticks()
            self.ammo -= 1

    def reload(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.last_reload_time = pygame.time.get_ticks()
            self.reloading = True
            self.ammo = self.max_ammo

    def done_reloading(self):
        now = pygame.time.get_ticks()
        if self.reloading and now - self.last_reload_time > self.reload_cooldown:
            self.reloading = False
            self.last_reload_time = 0
        return not self.reloading
    

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, group, enemies_sprites, direction, angle) -> None:
        super().__init__(group)
        # Sprites
        self.spritesheet = Spritesheet(BULLET_SPRITESHEET_SRC)
        self.load_sprites()
        self.enemies_sprites = enemies_sprites

        # Movement 
        self.pos = pos
        self.rect = self.image.get_rect(center = self.pos)
        self.dir = direction
        self.angle = angle
        self.speed = 800

    def load_sprites(self):
        sprites_coords = self.spritesheet.parse_sheet(BULLET_WIDTH, BULLET_HEIGHT)
        self.image = self.spritesheet.get_sprite(sprites_coords["sprite1"][0].x, sprites_coords["sprite1"][0].y, BULLET_WIDTH, BULLET_HEIGHT)

    

    def update(self, delta_time):
        pygame.transform.rotate(self.image, self.angle)
        self.pos = (self.pos[0] + self.dir.x * self.speed * delta_time, self.pos[1] + self.dir.y * self.speed *  delta_time)
        self.rect.center = self.pos
        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH * SCALE: self.kill()
            