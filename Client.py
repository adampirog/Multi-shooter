import sys
import pygame
import numpy as np
from Network import Network
from Weapons import Battle_field, WINDOW_WIDTH, WINDOW_HEIGHT
from Player import PLAYER_SIZE, detect_bullet_collision, SCOREBOARD_FONT, HUD_COLOR, object_collision

#variables
my_id = -1
players = {}
item_spawn_zones = None

battle_field = Battle_field()
camera_offset = [0, 0]


def spawn_items(window):
    global item_spawn_zones
    for item in item_spawn_zones:
        for player in players.values():
            if(object_collision((item[1], item[2]), (player.x, player.y), (PLAYER_SIZE * 2) - 3)):
                if(item[0] == 3):
                    if(player.armor != 100):
                        player.armor += 15
                        player.armor %= 100
                elif(item[0] == 0):
                    player.equipment[0].ammo += 15
                elif(item[0] == 1):
                    player.equipment[1].ammo += 15
                elif(item[0] == 2):
                    player.equipment[2].ammo += 15
                    
                item[0] = None
            
        for item in item_spawn_zones:
            if(item[0] == 0):
                pygame.draw.circle(window, (255, 0, 0), (item[1] - camera_offset[0], item[2] - camera_offset[1]), PLAYER_SIZE)
            elif(item[0] == 1):
                pygame.draw.circle(window, (0, 255, 0), (item[1] - camera_offset[0], item[2] - camera_offset[1]), PLAYER_SIZE)
            elif(item[0] == 2):
                pygame.draw.circle(window, (0, 0, 255), (item[1] - camera_offset[0], item[2] - camera_offset[1]), PLAYER_SIZE)
            elif(item[0] == 3):
                pygame.draw.circle(window, (255, 255, 255), (item[1] - camera_offset[0], item[2] - camera_offset[1]), PLAYER_SIZE)
        

def redrawWindow(window, my_id, _display_scoreboard):
    battle_field.draw(window, camera_offset)
    
    screen_center = window.get_rect().center
    screen_center = (screen_center[0], screen_center[1] // 3)
    
    spawn_items(window)
    for index, player in enumerate(players.values()):
        player.draw(window, camera_offset)
        
        if(_display_scoreboard):
            
            #kills - in the middle
            kills_string = f"KILLS {player.kills}"
            kills_render = SCOREBOARD_FONT.render(kills_string, True, HUD_COLOR) 
            
            rect = kills_render.get_rect()
            rect.center = (screen_center[0], screen_center[1] + index * 2 * kills_render.get_height())
            window.blit(kills_render, rect)
            
            #nick
            string = player.nick
            score = SCOREBOARD_FONT.render(string, True, HUD_COLOR) 
            
            rect = score.get_rect()
            rect.center = (screen_center[0] - int(kills_render.get_width() * 1.5), screen_center[1] + index * 2 * score.get_height())
            window.blit(score, rect)
            
            #deaths
            string = f"DEATHS {player.deaths}"
            score = SCOREBOARD_FONT.render(string, True, HUD_COLOR) 
            
            rect = score.get_rect()
            rect.center = (screen_center[0] + int(kills_render.get_width() * 1.75), screen_center[1] + index * 2 * score.get_height())
            window.blit(score, rect)
        
    players[my_id].display_hud(window)
    pygame.display.update()


def get_nick(screen):
    name = ""
    font = pygame.font.Font(None, 50)
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.unicode.isalpha():
                    name += evt.unicode
                elif evt.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif evt.key == pygame.K_RETURN:
                    return name
            elif evt.type == pygame.QUIT:
                return
        screen.fill((0, 0, 0))
        
        block = font.render("Enter your nick:", True, (255, 255, 255))
        rect = block.get_rect()
        rect.center = (screen.get_rect().center[0], screen.get_rect().center[1] // 4)
        screen.blit(block, rect)
        
        block = font.render(name, True, (255, 255, 255))
        rect = block.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(block, rect)
        pygame.display.update()
        

def main():
    global players, my_id, battle_field, item_spawn_zones, camera_offset
    
    run = True
    _display_scoreboard = False
    
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Shooter")
    nick = get_nick(window)
    
    network = Network()
    data = network.connect()
    
    if(not data):
        print("Server connection failed.\nExiting")
        sys.exit(0)
    
    my_id = data[0]
    players = data[1]
    item_spawn_zones = data[2]
    players[my_id].nick = nick
    
    clock = pygame.time.Clock()
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    
    mouse_pos = pygame.mouse.get_pos()
    delta_x = mouse_pos[0] - (WINDOW_WIDTH // 2)
    delta_y = (WINDOW_HEIGHT // 2) - mouse_pos[1]
    players[my_id].angle = np.arctan2(delta_x, delta_y)

    while run:
        clock.tick(30)
        players, item_spawn_zones = network.send((my_id, players[my_id], item_spawn_zones))
            
        camera_offset[0] += (players[my_id].x - camera_offset[0] - (WINDOW_WIDTH // 2))  # // 15
        camera_offset[1] += (players[my_id].y - camera_offset[1] - (WINDOW_HEIGHT // 2))  # // 15
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                delta_x = mouse_pos[0] - (WINDOW_WIDTH // 2)
                delta_y = (WINDOW_HEIGHT // 2) - mouse_pos[1]
                players[my_id].angle = np.arctan2(delta_x, delta_y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    _display_scoreboard = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_TAB:
                    _display_scoreboard = False        
                
        players[my_id].move(players, battle_field.walls, camera_offset)
        detect_bullet_collision(players, battle_field.walls)
        redrawWindow(window, my_id, _display_scoreboard)


if __name__ == "__main__":
    main()
