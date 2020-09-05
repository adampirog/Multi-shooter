import pygame
import random


class Player():
    def __init__(self, Id, position):
        
        self.id = Id
        self.x, self.y = position
        self.width = 50
        self.height = 50
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        self.vel = 3
        self.rect = (self.x, self.y, self.width, self.height)
        
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        
    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
            
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
            
        if keys[pygame.K_UP]:
            self.y -= self.vel
            
        if keys[pygame.K_DOWN]:
            self.y += self.vel
        
        self.update()
        
    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


