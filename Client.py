import sys
import time
import pygame
from Network import Network
from Classes import WIDTH, HEIGHT, Player, Battle_field


def redrawWindow(window, players, battle_field):
    battle_field.draw(window)
    for player in players:
        player.draw(window)
    pygame.display.update()
    
    
def analyze_package(players, package_list):
    if (len(package_list) != len(players)):
        players.clear()
        for package in package_list:
            player = Player()
            player.import_package(package)
            players.append(player)
    else:
        for player, package in zip(players, package_list):
            player.import_package(package)
            
    return players


def main():
    players = []
    battle_field = Battle_field()
    run = True
    
    network = Network()
    data = network.get_object()
    
    if(not data):
        print("Server capacity reached. \nExiting.")
        time.sleep(5)
        sys.exit(0)
        
    my_id = data[0]
    players = analyze_package(players, data[1])
    
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Client")
     
    while run:
        clock.tick(60)
        players = analyze_package(players, network.send([my_id, players[my_id].export_package()]))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        players[my_id].move()
        redrawWindow(window, players, battle_field)


if __name__ == "__main__":
    main()
