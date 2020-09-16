
import time
import pygame
import numpy as np

MAP_SIZE = 1000 
BACKGROUND_COLOR = (161, 222, 100)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


class Bullet():
    
    def __init__(self, x, y, speed, angle, damage, range):
        
        self.x, self.y = x, y
        self.start_x, self.start_y = x, y 
        
        self.speed = speed
        self.angle = angle
        
        self.damage = damage
        self.range = range
        
        self.traveled = 0
        
    def draw(self, window, camera_offset):
        self.move()
        
        pygame.draw.circle(window, (0, 0, 0), (int(self.x - camera_offset[0]), int(self.y - camera_offset[1])), 3)
        
    def move(self):
        dx = np.sin(self.angle) * self.speed
        dy = np.cos(self.angle) * self.speed
        
        self.x += dx
        self.y -= dy
        
        self.traveled += np.linalg.norm(np.array([dx, dy]))
        
        
class Gun():
    FIRE_RATE = 0
    
    BULLET_SPEED = 0
    BULLET_DAMAGE = 0
    BULLET_RANGE = 0
    
    def __init__(self):
        self.timer = 0
        self.ammo = 30
    
    def fire(self, x, y, angle):

        if((time.time() - self.timer) >= self.FIRE_RATE) or self.timer == 0:
            self.timer = time.time()
            self.ammo -= 1
            return Bullet(x, y, self.BULLET_SPEED, angle, self.BULLET_DAMAGE, self.BULLET_RANGE)
        else:
            return None
        
        
class Pistol(Gun):
    FIRE_RATE = 0.45
    
    BULLET_SPEED = 15
    BULLET_DAMAGE = 7
    BULLET_RANGE = 300
    
    def __init__(self):
        super().__init__()
        
        
class MachineGun(Gun):
    FIRE_RATE = 0.2
    
    BULLET_SPEED = 20
    BULLET_DAMAGE = 5
    BULLET_RANGE = 400
    
    def __init__(self):
        super().__init__()
        

class ShotGun(Gun):
    FIRE_RATE = 0.75
    
    BULLET_SPEED = 20
    BULLET_DAMAGE = 5
    BULLET_RANGE = 200
    
    def __init__(self):
        super().__init__()
        
    def fire(self, x, y, angle):

        if((time.time() - self.timer) >= self.FIRE_RATE) or self.timer == 0:
            self.timer = time.time()
            
            bullets = []
            bullets.append(Bullet(x, y, self.BULLET_SPEED, angle, self.BULLET_DAMAGE, self.BULLET_RANGE))
            bullets.append(Bullet(x, y, self.BULLET_SPEED, angle + 0.1, self.BULLET_DAMAGE, self.BULLET_RANGE))
            bullets.append(Bullet(x, y, self.BULLET_SPEED, angle - 0.1, self.BULLET_DAMAGE, self.BULLET_RANGE))
            #bullets.append(Bullet(x, y, self.BULLET_SPEED, angle + 0.15, self.BULLET_DAMAGE, self.BULLET_RANGE))
            #bullets.append(Bullet(x, y, self.BULLET_SPEED, angle - 0.15, self.BULLET_DAMAGE, self.BULLET_RANGE))
            
            self.ammo -= len(bullets)
            return bullets
        else:
            return None
        
        
class Battle_field():
    
    def __init__(self):
        self.walls = []
        
        # map borders
        self.walls.append(((0, 0), (0, MAP_SIZE)))
        self.walls.append(((0, 0), (MAP_SIZE, 0)))
        
        self.walls.append(((MAP_SIZE, MAP_SIZE), (MAP_SIZE, 0)))
        self.walls.append(((MAP_SIZE, MAP_SIZE), (0, MAP_SIZE)))
        
        # house1
        self.walls.append(((200, 200), (400, 200)))
        self.walls.append(((400, 200), (400, 350)))
        
        self.walls.append(((400, 400), (200, 400)))
        self.walls.append(((200, 400), (200, 250)))
        
        # house1
        self.walls.append(((650, 600), (800, 600)))
        self.walls.append(((800, 600), (800, 800)))
        
        self.walls.append(((750, 800), (600, 800)))
        self.walls.append(((600, 800), (600, 600)))
        
        # corners
        self.walls.append(((700, 100), (900, 300)))
        self.walls.append(((100, 700), (300, 900)))
        
    def draw(self, window, camera_offset):
        window.fill(BACKGROUND_COLOR)
        
        for wall in self.walls:
            pygame.draw.line(window, (0, 0, 0), (wall[0][0] - camera_offset[0], wall[0][1] - camera_offset[1]), 
                             (wall[1][0] - camera_offset[0], wall[1][1] - camera_offset[1]), 5)
        
