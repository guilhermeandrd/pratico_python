from pgzero.actor import Actor

# Inimigos simples
class Enemy(Actor):
    def __init__(self, pos, idle_frames, walk_frames_left, walk_frames_right, platform_rect, speed = 1):
        super().__init__(idle_frames[0], pos)
        self.speed = speed
        self.direction = 1
        self.start_x = pos[0]
        self.platform_rect = platform_rect # rastreia a plataforma em q esta
        self.vy = 0 # gravidade
        
        #embora nao seja usada a animacao de estado parado ainda existe
        self.idle_frames = idle_frames
        self.walk_frames_left = walk_frames_left
        self.walk_frames_right = walk_frames_right
        self.current_frames = self.walk_frames_right
        self.frame_index = 0
        self.animation_timer = 0
        self.current_animation = 'walk'
        
    def update_animation(self):
        self.animation_timer += 1

        animation_speed_factor = 7 if self.current_animation == 'idle' else 5 

        if self.animation_timer >= animation_speed_factor:
            self.animation_timer = 0

            self.frame_index = (self.frame_index + 1) % len(self.current_frames)
            self.image = self.current_frames[self.frame_index]

    
    def update(self):
        
        self.vy += 0.5
        self.y += self.vy
        self.x += self.speed * self.direction

        p = self.platform_rect
        if self.colliderect(p) and self.vy > 0 and self.bottom > p.top:
            self.y = p.top
            self.vy = 0     

        if self.direction == 1 and self.right >= p.right:
            self.direction = -1
            self.right = p.right
            if self.current_frames != self.walk_frames_left:
                self.current_frames = self.walk_frames_left
                self.frame_index = 0
        
        elif self.direction == -1 and self.left <= p.left:
            self.direction = 1
            self.left = p.left
            
            if self.current_frames != self.walk_frames_right:
                self.current_frames = self.walk_frames_right
                self.frame_index = 0
            
        self.x += self.speed * self.direction
        
        self.update_animation()