import pygame
import random

PLAYER_SIZE = 20
PLAYER_VELOCITY = 3


class Player():
    def __init__(self, Id, x, y):
        
        self.id = Id
        self.x, self.y = x, y
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
    def draw(self, window, camera_offset):
        pygame.draw.circle(window, self.color, (self.x - camera_offset[0], self.y - camera_offset[1]), PLAYER_SIZE)
        
    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.x -= PLAYER_VELOCITY
            
        if keys[pygame.K_RIGHT]:
            self.x += PLAYER_VELOCITY
            
        if keys[pygame.K_UP]:
            self.y -= PLAYER_VELOCITY
            
        if keys[pygame.K_DOWN]:
            self.y += PLAYER_VELOCITY
        

class Battle_field():
    
    def draw(self, window, camera_offset):
        window.fill((255, 255, 255))
        pygame.draw.line(window, (0, 0, 0), (100 - camera_offset[0], 100 - camera_offset[1]), (100 - camera_offset[0], 300 - camera_offset[1]), 3)
        pygame.draw.line(window, (0, 0, 0), (100 - camera_offset[0], 100 - camera_offset[1]), (300 - camera_offset[0], 100 - camera_offset[1]), 3)
        
        pygame.draw.line(window, (0, 0, 0), (600 - camera_offset[0], 600 - camera_offset[1]), (600 - camera_offset[0], 800 - camera_offset[1]), 3)
        pygame.draw.line(window, (0, 0, 0), (600 - camera_offset[0], 600 - camera_offset[1]), (800 - camera_offset[0], 600 - camera_offset[1]), 3)
       
       
# return array index for player with a given id 
def index_for_player(id, players_array):
    
    for index, player in enumerate(players_array):
        if(player.id == id):
            return index
    
    return -1 
        

