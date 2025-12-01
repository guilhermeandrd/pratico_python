from pgzero.actor import Actor
from pgzero.rect import Rect
import math

class Hazard(Actor):
    
    def __init__(self, x, y, width, height, image_name):
        super().__init__(image_name, center=(x + width/2, y + height/2))
        
        self.rect = Rect(x, y, width, height)
        
       
        self.tile_actor = Actor(image_name, (0, 0)) 
        self.tile_width = self.tile_actor.width 
        self.tile_height = self.tile_actor.height

    def draw(self):
        
        num_tiles_x = math.ceil(self.rect.width / self.tile_width) 
        num_tiles_y = math.ceil(self.rect.height / self.tile_height)
        
        for i in range(num_tiles_x):
            for j in range(num_tiles_y):
                tile_x_center = self.rect.left + (i * self.tile_width) + (self.tile_width / 2)
                tile_y_center = self.rect.top + (j * self.tile_height) + (self.tile_height / 2)
                
                self.tile_actor.pos = (tile_x_center, tile_y_center)
                self.tile_actor.draw()