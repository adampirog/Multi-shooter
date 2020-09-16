import sys
import pygame
import numpy as np
from Network import Network
from Weapons import Battle_field, WINDOW_WIDTH, WINDOW_HEIGHT
from Player import detect_bullet_collision

#variables
players = {}
battle_field = Battle_field()
camera_offset = [0, 0]


def redrawWindow(window, my_id):
    battle_field.draw(window, camera_offset)
    
    for player in players.values():
        player.draw(window, camera_offset)
        
    players[my_id].display_hud(window)
    pygame.display.update()
    

def main():
    global players, battle_field, camera_offset
    
    run = True
    
    network = Network()
    data = network.connect()
    
    if(not data):
        print("Server connection failed.\nExiting")
        sys.exit(0)
    
    my_id = data[0]
    players = data[1]
    
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Client")
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    
    mouse_pos = pygame.mouse.get_pos()
    delta_x = mouse_pos[0] - (WINDOW_WIDTH // 2)
    delta_y = (WINDOW_HEIGHT // 2) - mouse_pos[1]
    players[my_id].angle = np.arctan2(delta_x, delta_y)

    while run:
        clock.tick(30)
        players = network.send((my_id, players[my_id]))
            
        camera_offset[0] += (players[my_id].x - camera_offset[0] - (WINDOW_WIDTH // 2))  # // 15
        camera_offset[1] += (players[my_id].y - camera_offset[1] - (WINDOW_HEIGHT // 2))  # // 15
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                delta_x = mouse_pos[0] - (WINDOW_WIDTH // 2)
                delta_y = (WINDOW_HEIGHT // 2) - mouse_pos[1]
                players[my_id].angle = np.arctan2(delta_x, delta_y)
                
        players[my_id].move(players, battle_field.walls, window, camera_offset)
        detect_bullet_collision(players, battle_field.walls)
        redrawWindow(window, my_id)


if __name__ == "__main__":
    main()
