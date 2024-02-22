import pygame
import os
import time
import random
from enum import Enum
import numpy as np

pygame.font.init()

class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    STAY = 2
    SHOOT = 3

class Game:
    
    # Load images
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
        
    def __init__(self, width=750, height=750):
        self.WIDTH = width
        self.HEIGHT = height
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Space Shooter Tutorial")

        

        # Background
        self.BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (self.WIDTH, self.HEIGHT))

        self.run_game()

    def run_game(self, action):
        run = True
        FPS = 60
        level = 0
        lives = 5
        main_font = pygame.font.SysFont("comicsans", 50)
        lost_font = pygame.font.SysFont("comicsans", 60)
        scores = 0

        enemies = []
        wave_length = 5
        enemy_vel = 1

        player_vel = 5
        laser_vel = 5

        player = Player(300, 630)

        clock = pygame.time.Clock()

        lost = False
        lost_count = 0

        def redraw_window():
            self.WIN.blit(self.BG, (0,0))
            # draw text
            lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
            level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
            scores_label = main_font.render(f"Scores: {scores}", 1, (255,255,255))

            self.WIN.blit(lives_label, (10, 10))
            self.WIN.blit(level_label, (self.WIDTH - level_label.get_width() - 10, 10))
            self.WIN.blit(scores_label, (self.WIDTH - scores_label.get_width() - 10, level_label.get_height() + 5))

            for enemy in enemies:
                enemy.draw(self.WIN)

            player.draw(self.WIN)
            
           
            if lost:
                lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
                self.WIN.blit(lost_label, (self.WIDTH/2 - lost_label.get_width()/2, 350))

            pygame.display.update()
        
        while run:
            #update display
            redraw_window()
            clock.tick(FPS)
        
                
            def play_step(action):
            
                #1. collect user input
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                
                #2. move
                #move_player(action)
            
                #3.update enemy and score
                if len(enemies) == 0:
                    self.level += 1
                    wave_length += 5
                    for i in range(wave_length):
                        enemy = Enemy(random.randrange(50, self.WIDTH - 100), random.randrange(-1500, -100),
                                    random.choice(["red", "blue", "green"]))
                        enemies.append(enemy)
                
                for enemy in enemies[:]:
                    enemy.move(enemy_vel)
                    enemy.move_lasers(laser_vel, player, self.HEIGHT)

                    if random.randrange(0, 2*60) == 1:
                        enemy.shoot()

                    #enemy_bullet_positions = enemy.get_bullet_positions()

                    if collide(enemy, player):
                        player.health -= 10
                        enemies.remove(enemy)
                        if player.health <= 0:
                            lives = -1
                    
                              
                
                # 4 Check if game over and return reward, score
                reward = 0
                game_over = False
                if lives <= 0 and player.health <= 0:
                    lost = True
                    lost_count += 1
                
                if lost:
                    if lost_count > FPS * 3:
                        run = False
                        game_over = True
                        reward = -10
                        scores = player.score
                        return game_over , reward , scores 
                

                        
                 
                
                #4 update game:
                
                redraw_window()
                clock.tick(FPS)
                
                #return game_over and scores
                return reward, game_over, scores 
                    
        # def move_player(action):
        #     #[left, stay , right , shoot]
        #     if np.array_equal(action, [1,0,0,0]) and player.x - player_vel > 0:
        #         player.x -= player_vel #move left
        #     elif np.array_equal(action, [0,1,0,0]) and player.x + player_vel + player.get_width() < self.WIDTH:
        #         player.x += player_vel #move right
        #     elif np.array_equal(action,[0,0,0,1]):
        #         player.shoot()
        #         player.move_lasers(-laser_vel, enemies, self.HEIGHT)
                
                        
                                
        #     else: #[0,0,1,0]
        #         player.x = player.x

                

    
        # while run:
        #     clock.tick(FPS)
        #     redraw_window()

            # if lives <= 0 or player.health <= 0:
            #     lost = True
            #     lost_count += 1

            # if lost:
            #     if lost_count > FPS * 3:
            #         run = False
            #     else:
            #         continue

            # if len(enemies) == 0:
            #     level += 1
            #     wave_length += 5
            #     for i in range(wave_length):
            #         enemy = Enemy(random.randrange(50, self.WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
            #         enemies.append(enemy)

            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         run = False

            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_a] and player.x - player_vel > 0: # left
            #     player.x -= player_vel
            # if keys[pygame.K_d] and player.x + player_vel + player.get_width() < self.WIDTH: # right
            #     player.x += player_vel
            # if keys[pygame.K_w] and player.y - player_vel > 0: # up
            #     player.y -= player_vel
            # if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < self.HEIGHT: # down
            #     player.y += player_vel
            # if keys[pygame.K_SPACE]:
            #     player.shoot()

            # for enemy in enemies[:]:
            #     enemy.move(enemy_vel)
            #     enemy.move_lasers(laser_vel, player, self.HEIGHT)

            #     if random.randrange(0, 2*60) == 1:
            #         enemy.shoot()
                
            #     if enemies:
            #         enemy_bullet_positions = enemies[0].get_bullet_positions()    

            #     if collide(enemy, player):
            #         player.health -= 10
            #         enemies.remove(enemy)
            #     elif enemy.y + enemy.get_height() > self.HEIGHT:
            #         lives -= 1
            #         enemies.remove(enemy)

            # player.move_lasers(-laser_vel, enemies, self.HEIGHT)

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj, height):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = Game.YELLOW_SPACE_SHIP
        self.laser_img = Game.YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.score = 0

    def move_lasers(self, vel, objs, height):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.score = +1
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):
    COLOR_MAP = {
                "red": (Game.RED_SPACE_SHIP, Game.RED_LASER),
                "green": (Game.GREEN_SPACE_SHIP, Game.GREEN_LASER),
                "blue": (Game.BLUE_SPACE_SHIP, Game.BLUE_LASER)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    # def get_bullet_positions(self):
    #     def get_bullet_positions(self):
    #         return [laser.x for laser in self.lasers]        

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

if __name__ == "__main__":
    game = Game()
