import pygame
import numpy as np

MAP_SIZE = 2000
PLAYER_SIZE = 20
PLAYER_VELOCITY = 6

PLAYER_COLOR = (255, 219, 172)
BACKGROUND_COLOR = (161, 222, 100)


class Player():
    def __init__(self, Id, x, y):
        
        self.id = Id
        self.x, self.y = x, y
        
    def draw(self, window, camera_offset):
        # body
        pygame.draw.circle(window, PLAYER_COLOR, (self.x - camera_offset[0], self.y - camera_offset[1]), PLAYER_SIZE)
        pygame.draw.circle(window, (0, 0, 0), (self.x - camera_offset[0], self.y - camera_offset[1]), PLAYER_SIZE, 1)
        
        # hands
        pygame.draw.circle(window, PLAYER_COLOR, (self.x + PLAYER_SIZE - 2 - camera_offset[0], self.y + PLAYER_SIZE - 2 - camera_offset[1]), PLAYER_SIZE // 2)
        pygame.draw.circle(window, PLAYER_COLOR, (self.x - PLAYER_SIZE + 2 - camera_offset[0], self.y + PLAYER_SIZE - 2 - camera_offset[1]), PLAYER_SIZE // 2)
        pygame.draw.circle(window, (0, 0, 0), (self.x + PLAYER_SIZE - 2 - camera_offset[0], self.y + PLAYER_SIZE - 2 - camera_offset[1]), PLAYER_SIZE // 2, 1)
        pygame.draw.circle(window, (0, 0, 0), (self.x - PLAYER_SIZE + 2 - camera_offset[0], self.y + PLAYER_SIZE - 2 - camera_offset[1]), PLAYER_SIZE // 2, 1)
            
    def move(self, players, walls):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            temp = self.x - PLAYER_VELOCITY
            if not ((detect_wall_collision(temp, self.y, walls)) or (detect_players_collision(temp, self.y, self.id, players))):
                self.x = temp
            
        if keys[pygame.K_RIGHT]:
            temp = self.x + PLAYER_VELOCITY
            if not ((detect_wall_collision(temp, self.y, walls)) or (detect_players_collision(temp, self.y, self.id, players))):
                self.x = temp
            
        if keys[pygame.K_UP]:
            temp = self.y - PLAYER_VELOCITY
            if not ((detect_wall_collision(self.x, temp, walls)) or (detect_players_collision(self.x, temp, self.id, players))):
                self.y = temp
            
        if keys[pygame.K_DOWN]:
            temp = self.y + PLAYER_VELOCITY
            if not ((detect_wall_collision(self.x, temp, walls)) or (detect_players_collision(self.x, temp, self.id, players))):
                self.y = temp
        

class Battle_field():
    
    def __init__(self):
        self.walls = []
        
        # map borders
        self.walls.append(((0, 0), (0, MAP_SIZE)))
        self.walls.append(((0, 0), (MAP_SIZE, 0)))
        
        self.walls.append(((MAP_SIZE, MAP_SIZE), (MAP_SIZE, 0)))
        self.walls.append(((MAP_SIZE, MAP_SIZE), (0, MAP_SIZE)))
        
    def draw(self, window, camera_offset):
        window.fill(BACKGROUND_COLOR)
        
        for wall in self.walls:
            pygame.draw.line(window, (0, 0, 0), (wall[0][0] - camera_offset[0], wall[0][1] - camera_offset[1]), 
                             (wall[1][0] - camera_offset[0], wall[1][1] - camera_offset[1]), 5)
        

def object_collistion(p1, p2, tollerance):
    en = np.array([p1[0], p1[1]])
    ms = np.array([p2[0], p2[1]])

    distance = np.linalg.norm(en - ms)
    if(distance < tollerance):
        return True
    return False  


# p1 and p2 create a line
def line_collision(p1, p2, p3, tollerance):
    distance = np.linalg.norm(np.cross(np.asarray(p2) - np.asarray(p1), np.asarray(p1) - np.asarray(p3))) / np.linalg.norm(np.asarray(p2) - np.asarray(p1))

    if(distance < tollerance):
        return True
    
    return False


def detect_players_collision(x, y, my_id, players):
    for player in players.values():
        if player.id == my_id:
            continue
        elif(object_collistion((x, y), (player.x, player.y), PLAYER_SIZE * 2 - 1)):
            return True
        
    return False


def detect_wall_collision(x, y, walls):
    for wall in walls:
        if(line_collision(wall[0], wall[1], (x, y), PLAYER_SIZE - 1) is True):
            return True
        
    return False


def detect_bullet_hit(player, bullets, players):
    hits = 0
    for bullet in bullets:
        if(object_collistion((bullet.x, bullet.y), (player.x, player.y), PLAYER_SIZE - 1)):
            bullet.explode()
            hits += 1
        
    return hits
