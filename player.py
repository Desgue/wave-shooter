import pygame
from settings import *
from spritesheet import Spritesheet

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self,pos, group):
        pygame.sprite.Sprite.__init__(self, group)
        self.spritesheet = Spritesheet(ASSAULT_PLAYER_SPRITESHEET)

        
        self.load_sprites()
        self.current_sprite = 0
        self.image = self.idle_sprites[self.current_sprite]
        self.idle = True        
        self.rect = self.image.get_rect(center = pos)

        # Movement Attributes
        self.status = "right"
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.velocity = PLAYER_VELOCITY

    
    def load_sprites(self):
        self.sprites_coords = self.spritesheet.parse_sheet(SPRITES_WIDTH, SPRITE_HEIGHT)

        self.idle_sprites = [
            self.spritesheet.get_sprite(
            self.sprites_coords["sprite1"][:2][i].x,
            self.sprites_coords["sprite1"][:2][i].y,
            PLAYER_WIDTH, PLAYER_HEIGHT
            ) 
            for i in range(len(self.sprites_coords["sprite1"][:2]))
            ]
        
        self.walk_sprites = [
            self.spritesheet.get_sprite(
            self.sprites_coords["sprite2"][:2][i].x,
            self.sprites_coords["sprite2"][:2][i].y,
            PLAYER_WIDTH, PLAYER_HEIGHT
            ) 
            for i in range(len(self.sprites_coords["sprite2"][:2]))
            ]
        self.crawl_sprites = [
            self.spritesheet.get_sprite(
            self.sprites_coords["sprite3"][:2][i].x,
            self.sprites_coords["sprite3"][:2][i].y,
            PLAYER_WIDTH, PLAYER_HEIGHT
            ) 
            for i in range(len(self.sprites_coords["sprite3"][:2]))
            ]
        self.fire_sprites = [
            self.spritesheet.get_sprite(
            self.sprites_coords["sprite4"][:2][i].x,
            self.sprites_coords["sprite4"][:2][i].y,
            PLAYER_WIDTH, PLAYER_HEIGHT
            ) 
            for i in range(len(self.sprites_coords["sprite4"][:2]))
            ]
        self.hit_sprites = [
            self.spritesheet.get_sprite(
            self.sprites_coords["sprite5"][:3][i].x,
            self.sprites_coords["sprite5"][:3][i].y,
            PLAYER_WIDTH, PLAYER_HEIGHT
            ) 
            for i in range(len(self.sprites_coords["sprite5"][:3]))
            ]
        
        self.death_sprites = [
            self.spritesheet.get_sprite(
            self.sprites_coords["sprite6"][i].x,
            self.sprites_coords["sprite6"][i].y,
            PLAYER_WIDTH, PLAYER_HEIGHT
            ) 
            for i in range(len(self.sprites_coords["sprite6"]))
            ]
        self.throw_sprites = [
            self.spritesheet.get_sprite(
            self.sprites_coords["sprite7"][:3][i].x,
            self.sprites_coords["sprite7"][:3][i].y,
            PLAYER_WIDTH, PLAYER_HEIGHT
            ) 
            for i in range(len(self.sprites_coords["sprite7"][:3]))
            ]
    


    def animate(self, dt):
        if self.idle:
            self.current_sprite += 4 * dt
            if self.current_sprite >= len(self.idle_sprites):
                self.current_sprite = 0
            self.image = self.idle_sprites[int(self.current_sprite)]
        else:
            self.image = self.walk_sprites[int(self.current_sprite)]
            self.current_sprite += 4 * dt
            if self.current_sprite >= len(self.walk_sprites):
                self.current_sprite = 0
            self.image = self.walk_sprites[int(self.current_sprite)]
           
    def update(self, delta_time):
        self.animate(delta_time)
        self.flip()
        self.input()
        self.handle_movement(delta_time)

    def flip(self):
        if self.status == "left":
            self.image = pygame.transform.flip(self.image, True, False)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.idle = False
            self.direction.y = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.idle = False
            self.direction.y = 1
        else: 
            self.idle = True
            self.direction.y = 0

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) :
            self.status = "left"
            self.idle = False
            self.direction.x = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.status = "right"
            self.idle = False
            self.direction.x = 1
        else: 
            self.idle = True
            self.direction.x = 0


    def handle_movement(self, delta_time):
        self.pos += self.velocity * self.direction * delta_time
        self.rect.center = self.pos

    

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
                self.rect.y -= self.velocity *delta_time
                print(self.rect.y)
            case Direction.DOWN:
                self.rect.y += self.velocity *delta_time
            case Direction.LEFT:
                self.rect.x -= self.velocity *delta_time
            case Direction.RIGHT:
                self.rect.x += self.velocity *delta_time
    