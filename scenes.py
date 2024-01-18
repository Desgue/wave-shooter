from os import scandir
import pygame
from actors import *
from settings import *
from sprites import Generic
from pytmx.util_pygame import load_pygame


class GameScene:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.floor_img = pygame.image.load(FLOOR).convert_alpha()
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()
        self.max_enemies = 100
        self.setup()
    
    def setup(self):
        
        tmx_data = load_pygame("./assets/Tiled/level0.tmx")

        Generic(pos = (0,0),
                surface = pygame.transform.scale(self.floor_img, 
                                                 (self.floor_img.get_width() * SCALE, self.floor_img.get_height() * SCALE) ),
                group= self.all_sprites)
        
        # Collision Group
        for x,y,surface in tmx_data.get_layer_by_name("Collision").tiles():
            Generic((x*TILE_SIZE, y * TILE_SIZE ), pygame.surface.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

        #Spawn Player
        for obj in tmx_data.get_layer_by_name("Player"):
            if obj.name == "Start":
                self.player = Player( (obj.x* SCALE, obj.y* SCALE), self.all_sprites, self.collision_sprites, self.enemies_sprites)

        # Enemies
        for i in range(self.max_enemies):
            Spider( [self.all_sprites, self.enemies_sprites], self.collision_sprites)
        
        
        
    def handle_events(self, event):
        pass
    
    def collision(self):
        def spider_callback(bullet, spider):
            if pygame.sprite.collide_rect(bullet, spider):
                spider.hitpoints -= 5
                print(spider.hitpoints)
                return True
            else: return False

        for sprite in self.player.bullets.sprites():
                if pygame.sprite.spritecollideany(sprite, self.enemies_sprites, spider_callback):
                    sprite.kill()
                if pygame.sprite.spritecollideany(sprite, self.collision_sprites):
                    sprite.kill()

    def render(self, screen):
        self.display_surface.fill(SCREEN_COLOR)
        self.all_sprites.custom_draw(self.player)
    def update(self, delta_time):
        self.collision()
        self.all_sprites.update(delta_time)



class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
        for sprite in self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)
