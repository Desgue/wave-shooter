import pygame
from player import Player, PlayerSprite
from settings import *
class GameScene:
    def __init__(self):
        self.player = PlayerSprite(PLAYER_COLOR, PLAYER_WIDTH, PLAYER_HEIGHT)
    def handle_events(self, event):
        pass
    def render(self, screen):
        screen.fill(SCREEN_COLOR)
        pygame.draw.rect(screen,  "white", self.player)
    def update(self, delta_time):
        self.player.update(delta_time)