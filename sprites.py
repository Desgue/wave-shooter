import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, group):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height *0.4)