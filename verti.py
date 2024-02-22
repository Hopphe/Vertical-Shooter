import pygame
import os
import random
from enum import Enum 
from collections import namedtuple
import numpy as np

pygame.font.init()

WIDTH, HEIGHT = 400,400
##pygame.display.set_mode((WIDTH,HEIGHT))
##pygame.display.set_caption("SPACE JAM")

#LOAD IMAGE
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

class Ship:
    COOLDOWN = 30

    def __init__(self, x , y , health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y,50,50))


class VerticalShooterAI(Ship) :
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 5
    
    #ship = Ship(300,650)

    #player = Player(300, 630)

    clock = pygame.time.Clock()

    #lost = False
    #lost_count = 0
    
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))
    
    def __init__(self,  w=WIDTH, h=HEIGHT , win=WIN, RUN = run, x = 300, y = 650, health=100):
        super().__init__(x ,y ,health)
        self.w = w
        self.h = h
        #self.x = x
        #self.y = y
        #self.health = health
        self.win = win
        pygame.display.set_caption("SPACE JAM")
        
        
        
        
        while self.run:
            
            self.clock.tick(self.FPS)
            # self.draw_char(self.win)
            self.redraw_window(self.win)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            
        pygame.quit()
       
        #pass
        
    def draw_char(self, window):
        super().draw(window)    
    
    def redraw_window(self,window):
        self.win.blit(BG, (0,0))
        self.draw_char(window)
        lives_label = self.main_font.render(f"Lives: {self.lives}", 1, (255,255,255))
        level_label = self.main_font.render(f"Level: {self.level}", 1, (255,255,255))

        self.WIN.blit(lives_label, (10, 10))
        self.WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        
        #self.draw(self.WIN)
        
        pygame.display.update()
        
    
        
if __name__ ==  '__main__':
    game = VerticalShooterAI()
    
    
   
