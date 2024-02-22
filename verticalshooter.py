import pygame
import os
import time
import random
import numpy as np

pygame.font.init()




class Game:
    RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
    GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
    BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
    YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

    RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
    GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
    BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
    YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
    action_space = 4

    def __init__(self, width=750, height=750):
        self.WIDTH = width
        self.HEIGHT = height
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Space Shooter")

        self.BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")),
                                         (self.WIDTH, self.HEIGHT))

        self.clock = pygame.time.Clock()

        self.main_font = pygame.font.SysFont("comicsans", 50)
        self.lost_font = pygame.font.SysFont("comicsans", 60)

        self.player = None
        self.enemies = []
        self.wave_length = 5
        self.enemy_vel = 1
        self.player_vel = 5
        self.laser_vel = 5

        self.level = 0
        self.lives = 5
        self.scores = 0
        self.new_scores = 0
        self.lasers_position = []
        
        
        

        self.lost = False
        self.lost_count = 0
        
        

        self.reset()

    def reset(self):
        # Reset the game state for a new episode
        self.player = Player(300, 630)
        self.enemies = []
        self.wave_length = 5
        self.enemy_vel = 1
        self.player_vel = 5
        self.laser_vel = 5
        self.level = 0
        self.lives = 5
        self.scores = 0
        self.new_scores = 0
        self.lost = False
        self.lost_count = 0
        self.lasers_position = []
        
        

        # Generate initial enemies for the new episode
        for i in range(self.wave_length):
            enemy = Enemy(random.randrange(50, self.WIDTH - 100), random.randrange(-1500, -100),
                          random.choice(["red", "blue", "green"]))
            self.enemies.append(enemy)
        
        return     

    def play_step(self, action):
        reward = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Move player based on the action
        self.move_player(action)
         

        # Update enemy positions 
        for enemy in self.enemies:
            enemy.move(self.enemy_vel)
            enemy.move_lasers(self.laser_vel, self.player, self.HEIGHT)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()
        
        # Generate new enemies if all are destroyed
        if len(self.enemies) == 0:
            self.level += 1
            self.wave_length += 5
            for i in range(self.wave_length):
                enemy = Enemy(random.randrange(50, self.WIDTH - 100), random.randrange(-1500, -100),
                              random.choice(["red", "blue", "green"]))
                self.enemies.append(enemy)        

        # Check for collisions and update lives and health
        for enemy in self.enemies[:]:
            if collide(enemy, self.player):
                self.player.health -= 10
                self.enemies.remove(enemy)
                if self.player.health <= 0:
                    self.lives -= 1
                    if self.lives > 0:
                        self.player.health = 100
                        self.player.healthbar(self.WIN)
                        
                if self.lives <= 0 and self.player.health <= 0:
                    self.lost = True
                    self.lost_count += 1

            elif enemy.y + enemy.get_height() > self.HEIGHT:
                self.enemies.remove(enemy)
        
        # Get enemies bullet position
        for enemy in self.enemies:
            for laser in enemy.lasers:
                if laser.y < self.HEIGHT - self.player.y:
                    laser_position = enemy.get_bullet_positions()
                    self.lasers_position.append(laser_position)
                
        # Update scores and reward
        self.scores = self.player.score
        if self.scores > self.new_scores:
            reward =+10
            self.new_scores = self.scores         

        # Check if the episode is done
        game_over = False
        if self.lost:
            if self.lost_count > 3 * 60:
                reward = -10
                game_over = True 
                return self.get_state(),reward, game_over
            else:
                return self.get_state(),reward, game_over

        # Redraw the game
        self.redraw_window()

        print(self.get_state())
        return self.get_state() ,reward , game_over
    
    def redraw_window(self):
        self.WIN.blit(self.BG, (0, 0))
        # draw text
        lives_label = self.main_font.render(f"Lives: {self.lives}", 1, (255, 255, 255))
        level_label = self.main_font.render(f"Level: {self.level}", 1, (255, 255, 255))
        scores_label = self.main_font.render(f"Scores: {self.new_scores}", 1, (255,255,255))

        self.WIN.blit(lives_label, (10, 10))
        self.WIN.blit(level_label, (self.WIDTH - level_label.get_width() - 10, 10))
        self.WIN.blit(scores_label, (self.WIDTH - scores_label.get_width() - 10, level_label.get_height() + 5))

        for enemy in self.enemies:
            enemy.draw(self.WIN)

        self.player.draw(self.WIN)

        if self.lost:
            lost_label = self.lost_font.render("You Lost!!", 1, (255, 255, 255))
            self.WIN.blit(lost_label, (self.WIDTH / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    def move_player(self, action):
        #keys = pygame.key.get_pressed()
        #[left, right , stay , shoot]
        
        if action == 0 and self.player.x - self.player_vel > 0:  # left
            self.player.x -= self.player_vel
        elif action == 1  and self.player.x + self.player_vel + self.player.get_width() < self.WIDTH:  # right
            self.player.x += self.player_vel
        elif action == 3: # shoot
            self.player.shoot()
            self.player.move_lasers(-self.laser_vel, self.enemies, self.HEIGHT)
            # for enemy in self.enemies:
            #     if enemy.x == self.player.x:
            #         self.player.shoot()
            #         self.player.move_lasers(-self.laser_vel, self.enemies, self.HEIGHT)
                    
                    
            #self.player.move_lasers(-self.laser_vel, self.enemies, self.HEIGHT)
            #self.scores = self.player.score 

    def get_state(self):
        # Return the current state of the game 
        player_state = self.player.x
        bullet_pos = self.lasers_position
        enemy_pos = []
        bullet_num = []
        enemy_num = []
        
        k = 1
        
        for position in self.lasers_position:
            bullet_num.append(k)
            k += 1
            
        for enemy in self.enemies:
            enemy_pos.append(enemy.x)
            enemy_num.append(k)
            k += 1
        
        #print(enemies_state.flatten())
        # Flatten the arrays and concatenate them to form the overall state
        #state = np.concatenate([player_state.flatten(), enemies_state.flatten(),bullet_state.flatten()])
        #print(state)
        # t = type(state)
        # print(t)
        
        #state = np.concatenate([state.flatten(), action.flatten()])
       

        return player_state, enemy_num, enemy_pos, bullet_num, bullet_pos


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
        return not (self.y <= height and self.y >= 0)

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
        
        
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1    

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
                        self.score += 1
                        if laser in self.lasers:
                            self.lasers.remove(laser)
        
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                                              self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                                              self.ship_img.get_width() * (self.health / self.max_health), 10))


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
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    def get_bullet_positions(self):
        return [laser.x for laser in self.lasers]        


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


if __name__ == "__main__":
    pygame.init()
    game = Game()

    # Main game loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        #game.redraw_window()        

        action = random.randint(0, 3)  
        state_tuple = game.play_step(action)
        player_state, enemy_num_state, enemy_pos_state, bullet_num_state, bullet_pos_state = state_tuple + (None,) * (5 - len(state_tuple))

        #run = False
    
        #player_state, enemy_num_state, enemy_pos_state, bullet_num_state, bullet_pos_state, reward, done = game.play_step(action)

        

        # if done:
        #     print("Game Over!")
        #     game.reset()