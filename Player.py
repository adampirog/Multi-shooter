import pygame
import numpy as np

from Weapons import WINDOW_HEIGHT, Pistol, MachineGun, ShotGun

PI = 3.1416

PLAYER_SIZE = 20
PLAYER_VELOCITY = 5

PLAYER_COLOR = (255, 219, 172)

HAND_IMG = pygame.image.load("graphics/hands.png")
PISTOL_IMG = pygame.image.load("graphics/pistol.png")
MACHINEGUN_IMG = pygame.image.load("graphics/machinegun.png")
SHOTGUN_IMG = pygame.image.load("graphics/shotgun.png")

pygame.mixer.init()
PISTOL_SOUND = pygame.mixer.Sound("sound/pistol.wav")
MACHINEGUN_SOUND = pygame.mixer.Sound("sound/pistol.wav")
SHOTGUN_SOUND = pygame.mixer.Sound("sound/pistol.wav")


pygame.font.init()
HUD_COLOR = (255, 255, 255)
font = pygame.font.Font('freesansbold.ttf', 32)


class Player():
    def __init__(self, Id, x, y):
        
        self.id = Id
        self.x, self.y = x, y

        self.angle = 0
        
        self.hp = 100
        self.armour = 0
        
        self.bullets = []
        self.equipment = [Pistol(), MachineGun(), ShotGun()]
        self.equipped = None
        
    def draw(self, window, camera_offset):
        
        # choose weapon image
        if(type(self.equipped) is Pistol):
            img = PISTOL_IMG
        elif(type(self.equipped) is MachineGun):
            img = MACHINEGUN_IMG
        elif(type(self.equipped) is ShotGun):
            img = SHOTGUN_IMG
        else:
            img = HAND_IMG
        
        # draw bullets
        for index, bullet in enumerate(self.bullets):
            bullet.draw(window, camera_offset)
            if(bullet.traveled > bullet.range):
                self.bullets.remove(bullet)
         
        # rotate and draw player        
        degree = -((self.angle * 180) / PI)
        img = pygame.transform.rotate(img, degree)
        x = self.x - (img.get_width() / 2)
        y = self.y - (img.get_height() / 2)        
        window.blit(img, (int(x - camera_offset[0]), int(y - camera_offset[1])))
        
    def display_hud(self, window):
        hp = font.render('HP: ' + str(self.hp), True, HUD_COLOR) 
        armor = font.render('ARMOR: ' + str(self.armour), True, HUD_COLOR) 
        
        window.blit(armor, (10, WINDOW_HEIGHT - 75))
        window.blit(hp, (10, WINDOW_HEIGHT - 40))
            
    def move(self, players, walls, window, camera_offset):
        keys = pygame.key.get_pressed()
        mouse_keys = pygame.mouse.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            temp = self.x - PLAYER_VELOCITY
            if not ((detect_wall_collision(temp, self.y, walls)) or (detect_players_collision(temp, self.y, self.id, players))):
                self.x = temp
            
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            temp = self.x + PLAYER_VELOCITY
            if not ((detect_wall_collision(temp, self.y, walls)) or (detect_players_collision(temp, self.y, self.id, players))):
                self.x = temp
            
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            temp = self.y - PLAYER_VELOCITY
            if not ((detect_wall_collision(self.x, temp, walls)) or (detect_players_collision(self.x, temp, self.id, players))):
                self.y = temp
            
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            temp = self.y + PLAYER_VELOCITY
            if not ((detect_wall_collision(self.x, temp, walls)) or (detect_players_collision(self.x, temp, self.id, players))):
                self.y = temp
                          
        if keys[pygame.K_0]:
            self.equipped = None       
        elif keys[pygame.K_1]:
            try:
                self.equipped = self.equipment[0]
            except Exception:
                self.equipped = None
        elif keys[pygame.K_2]:
            try:
                self.equipped = self.equipment[1]
            except Exception:
                self.equipped = None
        elif keys[pygame.K_3]:
            try:
                self.equipped = self.equipment[2]
            except Exception:
                self.equipped = None
                
        # mouse section
        elif mouse_keys[0]:
            self.fire()  
            
    def hit(self, damage):
        self.hp -= damage
        
    def fire(self):
        if self.equipped is not None:
            bullet = self.equipped.fire(self.x, self.y, self.angle)
            if bullet:
                if(type(bullet) in (list, tuple)):
                    self.bullets += bullet
                else:
                    self.bullets.append(bullet)
                
                # sound effects
                sound = None
                if(type(self.equipped) is Pistol):
                    sound = PISTOL_SOUND
                elif(type(self.equipped) is MachineGun):
                    sound = MACHINEGUN_SOUND
                elif(type(self.equipped) is ShotGun):
                    sound = SHOTGUN_SOUND
                
                sound.play()
       
                    
def detect_players_collision(x, y, my_id, players):
    for player in players.values():
        if player.id == my_id:
            continue
        elif(object_collision((x, y), (player.x, player.y), PLAYER_SIZE * 2)):
            return True
        
    return False


def detect_wall_collision(x, y, walls):
    for wall in walls:
        if(line_collision(wall[0], wall[1], (x, y), PLAYER_SIZE - 1)):
            return True
        
    return False


def detect_bullet_collision(players, walls):
    for upper in players.values():
        for index, bullet in enumerate(upper.bullets):
            for player in players.values():
                if upper == player:
                    continue
                if (object_collision((player.x, player.y), (bullet.x, bullet.y), PLAYER_SIZE + 5)):
                    player.hit(bullet.damage)
                    upper.bullets.remove(bullet)
                    
            for wall in walls:
                if(line_collision(wall[0], wall[1], (bullet.x, bullet.y), PLAYER_SIZE)):
                    try:
                        upper.bullets.remove(bullet)
                    except Exception:
                        pass


def object_collision(p1, p2, tollerance):
    distance = np.linalg.norm(np.array(p1) - np.array(p2))
    
    if(distance < tollerance):
        return True
    return False  


# p1 and p2 create a line. Distance is calcullated to p3
def line_collision(p1, p2, p3, tollerance):
    np1 = np.array(p1)
    np2 = np.array(p2)
    distance = np.linalg.norm(np.cross(np2 - np1, np1 - np.array(p3))) / np.linalg.norm(np2 - np1)

    if(distance < tollerance):
        return True
    
    return False
