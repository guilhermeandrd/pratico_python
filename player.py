from pgzero.actor import Actor
from pgzero.loaders import sounds

class Player(Actor):

    is_muted = False

    def __init__(self, pos, idle_frames, walk_frames):
        super().__init__(idle_frames[0], pos)
        self.vy = 0 
        self.on_ground = False
        
        self.idle_frames = idle_frames
        self.walk_frames = walk_frames
        self.current_frames = idle_frames
        self.frame_index = 0
        self.animation_timer = 0
        self.current_animation = 'idle'
        
    def update_animation(self):
        self.animation_timer += 1
        animation_speed_factor = 7 if self.current_animation == 'idle' else 5 
        if self.animation_timer >= animation_speed_factor:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.current_frames)
            self.image = self.current_frames[self.frame_index]

    def jump(self, is_muted_state): 
        if self.on_ground:
            if not is_muted_state:
                sounds.jump.play()
            self.vy = -12
            self.on_ground = False
            self.current_frames = self.walk_frames
            self.image = self.current_frames[1]
        
    def update(self, platforms, keys):
        vx = 0
        
        if keys.a:
            vx = -3
        elif keys.d:
            vx = 3
            
        self.x += vx

        if not self.on_ground:
            self.image = self.walk_frames[1]
        
        if vx != 0 and self.current_animation != 'walk':
            self.current_animation = 'walk'
            self.current_frames = self.walk_frames
            self.frame_index = 0
        elif vx == 0 and self.current_animation != 'idle':
            self.current_animation = 'idle'
            self.current_frames = self.idle_frames
            self.frame_index = 0
            
        self.update_animation()

        self.vy += 0.5
        self.y += self.vy
        
        if keys.space and self.on_ground:
            self.jump()          
          
        self.on_ground = False
        for p in platforms:
            if self.colliderect(p.rect) and self.vy > 0 and self.bottom > p.rect.top:
                self.y = p.rect.top
                self.vy = 0
                self.on_ground = True