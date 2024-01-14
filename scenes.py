import pygame
from player import Player, PlayerSprite
from settings import *

class GameScene:
    def __init__(self):
        self.all_sprites = CameraGroup()
        self.display_surface = pygame.display.get_surface()
        self.player = PlayerSprite( PLAYER_CENTER, self.all_sprites)
    def handle_events(self, event):
        pass
    def render(self, screen):
        self.display_surface.fill(SCREEN_COLOR)
        self.all_sprites.custom_draw()
    def update(self, delta_time):
        self.all_sprites.update(delta_time)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
    def custom_draw(self):
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect)
