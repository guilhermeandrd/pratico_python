import math
from pgzero.actor import Actor
from pgzero.rect import Rect

# recebeu o nome plataform_me porque o nome plataform já está reservado
class Platform:    
    def __init__(self, x, y, width, height, image_name):
        self.actor = Actor(image_name)
        
        self.rect = Rect(x, y, width, height)

        self.image_name = image_name
        
        self.tile_actor = Actor(image_name, (0, 0))
        self.tile_width = self.tile_actor.width 

    def draw(self):        
        num_tiles = math.ceil(self.rect.width / self.tile_width) 
        
        for i in range(num_tiles):
            tile_x_center = self.rect.left + (i * self.tile_width) + (self.tile_width / 2)
            
            self.tile_actor.pos = (tile_x_center, self.rect.centery)
            self.tile_actor.draw()