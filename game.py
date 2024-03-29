import pygame
from settings import *
from scenes import GameScene
from manager import SceneManager
from spritesheet import Spritesheet


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.manager = SceneManager(GameScene())
        self.dt = 0
        

    def run(self):
        while self.running:
            self.handle_events()
            self.manager.scene.render(self.screen)  
            self.manager.scene.update(self.dt)  
            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()
    def handle_events(self):   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.manager.scene.handle_events(event)