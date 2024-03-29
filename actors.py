import pygame
from settings import *
from spritesheet import Spritesheet
from random import randrange

class Player(pygame.sprite.Sprite):
    def __init__(self,pos, group, collision_sprites, enemies_sprites):
        pygame.sprite.Sprite.__init__(self, group)
        self.spritesheet = Spritesheet(ASSAULT_PLAYER_SPRITESHEET)
        
        self.load_sprites()
        self.current_sprite = 0
        self.image = self.idle_sprites[self.current_sprite]
        self.idle = True        
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.copy().inflate((-self.rect.width * SCALE * 0.15 , -self.rect.height * SCALE * 0.15))

        # Movement Attributes
        self.status = "right"
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.velocity = PLAYER_VELOCITY

        #Hitpoint
        self.hitpoints = 200

        #Collision
        self.collision_sprites = collision_sprites
        self.enemies_sprites = enemies_sprites

        # Shooting config
        self.shooting = False
        self.bullets = pygame.sprite.Group()

        
     
    def load_sprites(self):
        sprites_coords = self.spritesheet.parse_sheet(SPRITE_WIDTH, SPRITE_HEIGHT)

        self.idle_sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite1"][:2][i].x,
            sprites_coords["sprite1"][:2][i].y,
            PLAYER_WIDTH, PLAYER_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite1"][:2]))
            ]
        
        self.walk_sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite2"][:2][i].x,
            sprites_coords["sprite2"][:2][i].y,
            PLAYER_WIDTH, PLAYER_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite2"][:2]))
            ]
        self.crawl_sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite3"][:2][i].x,
            sprites_coords["sprite3"][:2][i].y,
            PLAYER_WIDTH, PLAYER_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite3"][:2]))
            ]
        self.fire_sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite4"][:2][i].x,
            sprites_coords["sprite4"][:2][i].y,
            PLAYER_WIDTH, PLAYER_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite4"][:2]))
            ]
        self.hit_sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite5"][:3][i].x,
            sprites_coords["sprite5"][:3][i].y,
            PLAYER_WIDTH, PLAYER_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite5"][:3]))
            ]
        
        self.death_sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite6"][i].x,
            sprites_coords["sprite6"][i].y,
            PLAYER_WIDTH, PLAYER_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite6"]))
            ]
        self.throw_sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite7"][:3][i].x,
            sprites_coords["sprite7"][:3][i].y,
            PLAYER_WIDTH, PLAYER_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite7"][:3]))
            ]

    def animate(self, dt):
        if self.idle:
            self.current_sprite += 3 * dt
            if self.current_sprite >= len(self.idle_sprites):
                self.current_sprite = 0
            self.image = self.idle_sprites[int(self.current_sprite)]
        else:
            self.image = self.walk_sprites[int(self.current_sprite)]
            self.current_sprite += 4 * dt
            if self.current_sprite >= len(self.walk_sprites):
                self.current_sprite = 0
            self.image = self.walk_sprites[int(self.current_sprite)]

    def animate_death(self, dt):
        if self.hitpoints <= 0:
            self.current_sprite  = 0
            self.image = self.death_sprites[self.current_sprite]
            self.current_sprite += 2 * dt
            print("Game Over")
            """ if self.current_sprite >= len(self.death_sprites): """
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

        # Shooting
        if pygame.mouse.get_pressed()[0]:
            if self.status == "left": Bullet((self.rect.centerx - BULLET_WIDTH * 2, self.rect.centery),[self.groups()[0], self.bullets],self.enemies_sprites, self.status)
            else: Bullet((self.rect.centerx + BULLET_WIDTH * 2, self.rect.centery),[self.groups()[0], self.bullets],self.enemies_sprites, self.status)
        
    def flip(self):
        if self.status == "left":
            self.image = pygame.transform.flip(self.image, True, False)
    
    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, "hitbox"):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == "horizontal":
                        if self.direction.x > 0: self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0: self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if direction == "vertical":
                        if self.direction.y > 0: self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0: self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
        if pygame.sprite.spritecollideany(self, self.enemies_sprites): 
            self.hitpoints -= 10


    def handle_movement(self, delta_time):

        self.pos.x += self.velocity * self.direction.x * delta_time
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")

        self.pos.y += self.velocity * self.direction.y * delta_time
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

    def shoot(self):
        pass

    def update(self, delta_time):
        self.animate(delta_time)
        self.flip()
        self.input()
        self.handle_movement(delta_time)


class Scarab(pygame.sprite.Sprite):
    def __init__(self,pos, group, collision_sprites):
        pygame.sprite.Sprite.__init__(self, group)

        # Sprite Config
        self.spritesheet = Spritesheet(SCARAB_SPRITESHEET_SRC)
        self.load_sprites()
        self.current_sprite = 0
        self.image = self.idle_sprites[self.current_sprite]
        self.idle = True        
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.copy().inflate((-self.rect.width* 0.25*SCALE, -self.rect.height* 0.25 * SCALE))

        # Collision
        self.collision_sprites = collision_sprites
        
    def load_sprites(self):
        sprites_coords = self.spritesheet.parse_sheet(SPRITE_WIDTH, SPRITE_HEIGHT)

        self.idle_sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite1"][:2][i].x,
            sprites_coords["sprite1"][:2][i].y,
            SPRITE_WIDTH, SPRITE_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite1"][:2]))
            ]

        self.walk_sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite2"][:4][i].x,
            sprites_coords["sprite2"][:4][i].y,
            SPRITE_WIDTH, SPRITE_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite2"][:4]))
            ]
        
        self.firing_sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite3"][:2][i].x,
            sprites_coords["sprite3"][:2][i].y,
            SPRITE_WIDTH, SPRITE_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite3"][:2]))
            ]
        
        self.melee_sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite4"][i].x,
            sprites_coords["sprite4"][i].y,
            SPRITE_WIDTH, SPRITE_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite4"]))
            ]
        
        self.destroyed_sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite5"][:1][i].x,
            sprites_coords["sprite5"][:1][i].y,
            SPRITE_WIDTH, SPRITE_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite5"][:1]))
            ]
    
    def animate(self, delta_time):
        if self.idle:
            self.current_sprite += 3 * delta_time
            if self.current_sprite >= len(self.idle_sprites):
                self.current_sprite = 0
            self.image = self.idle_sprites[int(self.current_sprite)]

    def handle_movement(self, delta_time):
        pass
    
    def update(self, delta_time):
        self.animate(delta_time)
        

class Spider(pygame.sprite.Sprite):
    def __init__(self, group, collision_sprites) -> None:
        super().__init__(group)
        self.display = pygame.display.get_surface()
        # Collision sprite group
        self.collision_sprites = collision_sprites
         # Sprite Config
        self.spritesheet = Spritesheet(SPIDER_SPRITESHEET_SRC)
        self.idle = True 
        self.current_sprite = 0       
        self.load_sprites()
        self.image = self.idle_sprites[self.current_sprite]
        self.randomize_pos()
        self.hitpoints = 100

    def randomize_pos(self):
        left, top  = float(randrange(0, SCREEN_WIDTH *SCALE, SPRITE_WIDTH * SCALE)), float(randrange(0, SCREEN_HEIGHT * SCALE, SPRITE_HEIGHT * SCALE))
        self.rect = self.image.get_rect(center = (left,top))
        self.hitbox = self.rect.copy().inflate(-SPRITE_WIDTH * SCALE * 0.2, -SPRITE_HEIGHT * SCALE * 0.2)
        if pygame.sprite.spritecollideany(self, self.collision_sprites):
            self.kill()
            
    def load_sprites(self):
        sprites_coords = self.spritesheet.parse_sheet(SPRITE_WIDTH, SPRITE_HEIGHT)

        self.idle_sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite1"][:2][i].x,
            sprites_coords["sprite1"][:2][i].y,
            SPRITE_WIDTH, SPRITE_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite1"][:2]))
            ]

        self.walk_sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite2"][:4][i].x,
            sprites_coords["sprite2"][:4][i].y,
            SPRITE_WIDTH, SPRITE_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite2"][:4]))
            ]
        
        self.firing_sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite3"][:2][i].x,
            sprites_coords["sprite3"][:2][i].y,
            SPRITE_WIDTH, SPRITE_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite3"][:2]))
            ]
        
        self.melee_sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite4"][i].x,
            sprites_coords["sprite4"][i].y,
            SPRITE_WIDTH, SPRITE_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite4"]))
            ]
        
        self.destroyed_sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite5"][:1][i].x,
            sprites_coords["sprite5"][:1][i].y,
            SPRITE_WIDTH, SPRITE_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite5"][:1]))
            ]
    
    def animate(self, dt):
        if self.idle:
            self.current_sprite += 3 * dt
            if self.current_sprite >= len(self.idle_sprites):
                self.current_sprite = 0
            self.image = self.idle_sprites[int(self.current_sprite)]
    def death(self):
        if self.hitpoints <= 0: self.kill()
    def update(self, dt):
        self.death()
        self.animate(dt)


class Wasp(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites) -> None:
        super().__init__(group)
         # Sprite Config
        self.spritesheet = Spritesheet(WASP_SPRITESHEET)
        self.load_sprites()
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.idle = True        
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.copy().inflate((-4*SCALE, -4*SCALE))

        # Collision
        self.collision_sprites = collision_sprites



    def load_sprites(self):
        sprites_coords = self.spritesheet.parse_sheet(SPRITE_WIDTH, SPRITE_HEIGHT)

        self.sprites = [
            self.spritesheet.get_sprite(
            sprites_coords["sprite1"][i].x,
            sprites_coords["sprite1"][i].y,
            SPRITE_WIDTH, SPRITE_HEIGHT
            ) 
            for i in range(len(sprites_coords["sprite1"]))
            ]
    
    def animate(self, dt):
        self.current_sprite += 2 * dt
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

    def update(self, dt):
        self.animate(dt)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, group, enemies_sprites, status) -> None:
        super().__init__(group)
        self.spritesheet = Spritesheet(BULLET_SPRITESHEET_SRC)
        self.load_sprites()
        self.rect = self.image.get_rect(center = pos)
        self.velocity = 800
        self.status = status
        self.enemies_sprites = enemies_sprites

    def load_sprites(self):
        sprites_coords = self.spritesheet.parse_sheet(BULLET_WIDTH, BULLET_HEIGHT)
        self.image = self.spritesheet.get_sprite(sprites_coords["sprite1"][0].x, sprites_coords["sprite1"][0].y, BULLET_WIDTH, BULLET_HEIGHT)

    

    def update(self, delta_time):
        if self.status == "left":
            direction = -1
        else: direction = 1
        self.rect.centerx += round(self.velocity  * delta_time * direction)
        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH * SCALE: self.kill()
            