import pygame
from Network import Network

# global variables
players = []
WIDTH = 500
HEIGHT = 500


def redrawWindow(window):
    
    window.fill((255, 255, 255))
    for player in players:
        player.draw(window)
    pygame.display.update()
    

def main():
    global players
    run = True
    
    network = Network()
    data = network.get_object()
    
    my_id = data[0]
    players = data[1]
    
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Client")
     
    while run:
        clock.tick(60)
        players = network.send([my_id, players[my_id]])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        players[my_id].move()
        redrawWindow(window)


if __name__ == "__main__":
    main()
