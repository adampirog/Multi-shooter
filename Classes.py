import pygame

# global variables
PLAYER_HEIGHT = 100
PLAYER_WIDTH = 50
PLAYER_IMG = pygame.transform.scale(pygame.image.load("graphics/player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
WIDTH = 1000
HEIGHT = 800
GROUND_LVL = 25


class Package():
    def __init__(self, Id, x, y):
        
        self.id = Id
        self.x = x
        self.y = y


class Player():
    def __init__(self, Id=-1, x=-100, y=-100):
        
        self.id = Id
        self.x = x
        self.y = y
        
        self.vel = 3
        
    def draw(self, window):
        window.blit(PLAYER_IMG, (self.x, self.y))
        
    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
            
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
            
        if keys[pygame.K_UP]:
            #self.y -= self.vel
            pass
        
        if keys[pygame.K_DOWN]:
            #self.y += self.vel
            pass
        
    def export_package(self):
        return Package(self.id, self.x, self.y)
    
    def import_package(self, package):
        self.x = package.x
        self.y = package.y


class Battle_field():
        
    def draw(self, window):
        window.fill((255, 255, 255))
        pygame.draw.rect(window, (0, 0, 0), (-1, HEIGHT - GROUND_LVL, WIDTH + 1, GROUND_LVL))
        
        
def main():
    import sys
    import pickle
    player = Player()
    package = player.export_package()
    
    print(sys.getsizeof(pickle.dumps(player, protocol=pickle.HIGHEST_PROTOCOL)))
    print(sys.getsizeof(pickle.dumps(package, protocol=pickle.HIGHEST_PROTOCOL)))


if __name__ == "__main__":
    main()
            


        


