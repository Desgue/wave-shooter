import pygame
from settings import *

class Player(pygame.Rect):
    def __init__(self, 
                 left: float = PlAYER_X_CENTER, 
                 top: float = PLAYER_Y_CENTER, 
                 width: float = PLAYER_WIDTH, 
                 height: float = PLAYER_HEIGHT):
        
        super().__init__(left, top, width, height)
        self.color = PLAYER_COLOR
        self.velocity = PLAYER_VELOCITY


    def handle_movement(self, delta_time):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(Direction.UP, delta_time)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(Direction.DOWN, delta_time)
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) :
            self.move(Direction.LEFT, delta_time)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move(Direction.RIGHT, delta_time)

    def move(self,  direction: str, delta_time: float,):
        match direction:
            case Direction.UP:
                self.y -= self.velocity *delta_time
                print(self.y)
            case Direction.DOWN:
                self.y += self.velocity *delta_time
            case Direction.LEFT:
                self.x -= self.velocity *delta_time
            case Direction.RIGHT:
                self.x += self.velocity *delta_time
    