import sys
import pygame
from Network import Network
from Classes import Battle_field, index_for_player

# constants

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

#variables
players = []
battle_field = Battle_field()
camera_offset = [0, 0]


def redrawWindow(window):
    battle_field.draw(window, camera_offset)
    for player in players:
        player.draw(window, camera_offset)
    pygame.display.update()
    

def main():
    global players, battle_field, camera_offset
    
    run = True
    
    network = Network()
    data = network.connect()
    
    if(not data):
        print("Server capactiy reached.\nExiting")
        sys.exit(0)
    
    my_id = data[0]
    players = data[1]
    previous_no_players = len(players)
    
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Client")
     
    while run:
        clock.tick(60)
        players = network.send([my_id, players[my_id]])
        if(len(players) != previous_no_players):
            my_id = index_for_player(my_id, players)
            previous_no_players = len(players)
            
        camera_offset[0] += (players[my_id].x - camera_offset[0] - 500) // 15
        camera_offset[1] += (players[my_id].y - camera_offset[1] - 400) // 15
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        players[my_id].move()
        redrawWindow(window)


if __name__ == "__main__":
    main()
