import pgzrun
from random import randint
from enemy import Enemy
from player import Player
from platform_me import Platform
from hazard import Hazard

# carrega arquivos inicias do jogo
music.play('intro')
idle_frames = ['monster', 'monster_3', 'monster_2', 'monster_4', 'monster_5']
walk_frames = ['monster', 'monster_walking']
enemy_idle_frames = ['enemy', 'enemy_3']
enemy_walk_frames_left = ['enemy', 'enemy_2']
enemy_walk_frames_right = ['enemy_right', 'enemy_2_right']

# cria a tela principal
WIDTH = 800
HEIGHT = 600
TITLE = 'Sobreviva nas Plataformas'
DEATH_Y_START = 550

# elementos para o menu
title_game = "Sobreviva Nas Plataformas"
button_start = "Iniciar Jogo"
button_mute = "Desligar/Ligar Músicas e Sons"
buton_exit = "Sair"

# atributos iniciais do jogo
player = Player((100, 400), idle_frames, walk_frames)
state = 'menu'
game_over = False
game_time = 0
is_muted = False
# para mecanica de quanto mais tempo passar mais rapidos os inimigos ficarem
ENEMY_BASE_SPEED = 1.0  
SPEED_INCREMENT = 0.5  
SPEED_INTERVAL = 30.0

platforms = [
    Platform(100, 400, 300, 20, 'plataforma'),
    Platform(400, 300, 150, 20, 'plataforma'), 
    Platform(200, 200, 200, 20, 'plataforma'),
    Platform(500, 500, 250, 20, 'plataforma')
]

enemies = [
    Enemy((150, 400 - 15), enemy_idle_frames, enemy_walk_frames_left, enemy_walk_frames_right, platform_rect=platforms[0].rect),
    Enemy((450, 300 - 15), enemy_idle_frames, enemy_walk_frames_left, enemy_walk_frames_right, platform_rect=platforms[1].rect),
    Enemy((300, 200 - 15), enemy_idle_frames, enemy_walk_frames_left, enemy_walk_frames_right, platform_rect=platforms[2].rect),
    Enemy((550, 500 - 15), enemy_idle_frames, enemy_walk_frames_left, enemy_walk_frames_right, platform_rect = platforms[3].rect)
]

hazard_area = Hazard(
    x=0, 
    y=DEATH_Y_START, 
    width=WIDTH, 
    height=HEIGHT - DEATH_Y_START, 
    image_name='mar'
)

def draw():
    screen.fill("brown")
    
    if state == 'menu':
        screen.draw.text(title_game, center=(WIDTH/2, HEIGHT/4), color="brown", fontsize=60, background = "green")
        screen.draw.text(button_start, center=(WIDTH/2, HEIGHT/2), color="green", fontsize=40, background = "brown")
        screen.draw.text(button_mute, center= (WIDTH/2, HEIGHT/2 + 40), color="green", fontsize=40, background = "brown")
        screen.draw.text(buton_exit, center=(WIDTH/2, HEIGHT/2 + 80), color="black", fontsize=40, background = "brown")
        
    elif state == 'gaming':
        screen.blit('tile_0013.png', (0, 0))
        
        for p in platforms:
            p.draw()

        for enemy in enemies:
            enemy.draw()
        
        hazard_area.draw()

        player.draw()
        
        screen.draw.text(f"TEMPO: {int(game_time)}s", (10, 40), color="white", fontsize=24)
        
        if game_over:
            screen.draw.text("GAME OVER", center=(400, 250), fontsize=72, color="red")
            screen.draw.text(f"Tempo: {int(game_time)} segundos", center=(400, 350), fontsize=36)

def on_key_down(key):
    global state, is_muted

    if state == 'gaming':
        if key == keys.SPACE:
            player.jump(is_muted)


def on_mouse_down(pos):
    global state, is_muted
    
    radius_y = 30 
    radius_x = 150
    
    x_min = WIDTH/2 - radius_x
    x_max = WIDTH/2 + radius_x
    y_center_start = HEIGHT/2
    y_center_mute = HEIGHT/2 + 40
    y_center_exit = HEIGHT/2 + 80
    
    if state == 'menu':
        if x_min < pos[0] < x_max and y_center_start - radius_y < pos[1] < y_center_start + radius_y:
            if not is_muted:
                sounds.rollover1.play()
                music.play("fase1")

            state = 'gaming'
        elif x_min < pos[0] < x_max and y_center_mute - radius_y < pos[1] < y_center_mute + radius_y:
            sounds.rollover1.play()
            if is_muted:
                is_muted = False
                music.unpause()
                music.set_volume(1.0)
            else:
                is_muted = True
                music.pause()
        elif x_min < pos[0] < x_max and y_center_exit - radius_y < pos[1] < y_center_exit + radius_y:
            if not is_muted:
                sounds.rollover1.play()
            quit()

def update(dt):
    global game_time, game_over
    
    if state != 'gaming' or game_over:
        return
    
    game_time += dt

    if keyboard.space and player.on_ground:
        player.jump(is_muted)

    if player.colliderect(hazard_area.rect):
        game_over = True
        if not is_muted:
            music.play('game_over')
        return

    player.update(platforms, keyboard)

    acceleration_steps = int(game_time // SPEED_INTERVAL)
    
    current_speed = ENEMY_BASE_SPEED + (acceleration_steps * SPEED_INCREMENT)
    
    for enemy in enemies:

        if enemy.speed < current_speed:
            enemy.speed = current_speed
            
        enemy.update()
        
        # colisão
        if player.colliderect(enemy):
            if not is_muted:
                sounds.knifeslice.play()
                music.play('game_over')
            game_over = True
            return
    
    player.x = max(0, min(WIDTH, player.x))
    player.y = max(0, min(HEIGHT, player.y))

pgzrun.go()