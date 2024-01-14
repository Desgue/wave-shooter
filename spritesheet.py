import pygame
from settings import SPRITES_WIDTH, SPRITE_HEIGHT

class Spritesheet(object):
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename)


    def get_sprite(self, x, y , w, h):
        sprite = pygame.Surface((w,h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.spritesheet,(0,0), (x,y, w, h))
        
        return pygame.transform.scale(sprite, (w*4, h*4))
    
    def parse_sheet(self, sprite_w: int, sprite_h: int):

        sheet_w = self.spritesheet.get_width()
        sheet_h = self.spritesheet.get_height()

        sprites_per_state = int(sheet_w / sprite_w)
        number_of_states = int(sheet_h / sprite_h)

        individual_sprite_pos = []
        all_sprite_pos = []

        sprites_coords = {}
        
        for i in range(1, number_of_states + 1):
            for j in range(1, sprites_per_state +1):

                coord = pygame.math.Vector2( (j-1) * sprite_w, (i-1) * sprite_h)
                individual_sprite_pos.append(coord)
            all_sprite_pos.append(individual_sprite_pos)

        for i in range(len(all_sprite_pos)):
            sprites_coords["sprite{}".format(i+1)] = all_sprite_pos[i] 
        
        return sprites_coords
    

""" class PlayerSprite(Spritesheet):
    def __init__(self, filename, w = SPRITES_WIDTH, h = SPRITE_HEIGHT):
        super().__init__(filename)

    def get_idle_sprites(self,w ,h):
        idle_sprites = self.parse_sheet(w,h)["sprite1"]
        return  idle_sprites[:2]
    def get_walking_sprites(self, w,h):
        return self.parse_sheet(w,h)["sprite2"] """
