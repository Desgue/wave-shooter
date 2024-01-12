import pygame
from player import Player
from settings import *
class GameScene:
    def __init__(self):
        self.player = Player()
    def handle_events(self, event):
        pass
    def render(self, screen):
        screen.fill(SCREEN_COLOR)
        pygame.draw.rect(screen, self.player.color,  self.player)
    def update(self, delta_time):
        self.player.handle_movement(delta_time)