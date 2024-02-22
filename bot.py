import pygame
import os
import time
import random
import numpy as np
from verticalshooter import Game 
import pickle
import matplotlib.pyplot as plt

def convert(arr1, arr2):
    arr1_grid, arr2_grid = np.meshgrid(arr1, arr2)
    new_arr = np.stack((arr1_grid, arr2_grid), axis=-1)
    return new_arr

def con(arr1, arr2):
    new_arr = np.stack((arr1, arr2), axis=-1)
    return new_arr
    
    

def run(episodes, is_training=True , render=False):
#def run(episodes, is_training=True):
    game = Game()
    
    low = game.player.x
    high = game.WIDTH - game.player.x

    # Divide player , enemies and bullets position into segments
    
    player_space = np.linspace(low, high, 20)    
    
    enemy_pos_space = np.linspace(low, high, 20)
    enemy_num_space = np.linspace(1, 20, 20)
    
    # Convert into grid and then 2D array 
    enemy_space = convert(enemy_num_space,enemy_pos_space)
      
    bullet_pos_space = np.linspace(low, high, 20)
    bullet_num_space = np.linspace(1, 20, 20)
    
    # Convert into grid and then 2D array
    bullet_space = convert(bullet_num_space,bullet_pos_space)
    
     
     
    
    if(is_training):
        # Initialize Q-table
        q_table = np.zeros((len(player_space), len(enemy_space), len(bullet_space),game.action_space)) # init a 20x{20x20}x{20x20}x4 array
    # else:
    #     f = open('vertical_shooter.pkl', 'rb')
    #     q = pickle.load(f)
    #     f.close()
    
    # Q-learning parameters
    LEARNING_RATE = 0.1
    DISCOUNT = 0.99
    EPISODES = 10000
    # SHOW_EVERY = 1000
    
    # Exploration-exploitation parameters    
    epsilon = 0.5
    START_EPSILON_DECAYING = 1
    END_EPSILON_DECAYING = EPISODES // 2
    epsilon_decay_value = epsilon / (END_EPSILON_DECAYING - START_EPSILON_DECAYING) 
    
    rewards_per_episode = np.zeros(episodes)
    
    
    
    for i in range(episodes):
        # Starting state
        player_state = 300
        enemy_num_state = np.zeros(20) 
        enemy_pos_state = np.zeros(20)
        bullet_num_state = np.zeros(20) 
        bullet_pos_state = np.zeros(20)
        
        #convert into 2D array
        enemy_state = con(enemy_num_state,enemy_pos_state)
        bullet_state = con(bullet_num_state,bullet_pos_state)
        
        #take the value of state and push it to the appropriate place in space
        state_p = np.digitize(player_state, player_space)
        state_e = np.digitize(enemy_state, enemy_space)
        state_b = np.digitize(bullet_state, bullet_space)
        
        
        terminated = False          # True when game is over

        rewards=0

        while(not terminated and rewards>-1000):
            if is_training and np.random.random() < epsilon :
                # Explore: choose a random action
                action = np.random.choice(game.action_space)
                
                
            else:
                # Choose the best action based on the Q-table
                action = np.argmax(q_table[state_p,state_e,state_b :])
                
            
            new_player_state, new_enemy_num_state, new_enemy_pos_state, new_bullet_num_state, new_bullet_pos_state, reward, terminated = game.play_step(action)
            
            new_enemy_state = con(new_enemy_num_state, new_enemy_pos_state)
            new_bullet_state = con(new_bullet_num_state, new_bullet_pos_state)
            
            new_state_p = np.digitize(new_player_state, player_space)
            new_state_e = np.digitize(new_enemy_state, enemy_space)
            new_state_b = np.digitize(new_bullet_state, bullet_space)
            
            if is_training:
                q[state_p, state_e, state_b, action] = q[state_p, state_e, state_b, action] + LEARNING_RATE * (
                    reward + DISCOUNT*np.max(q[new_state_p, new_state_e, new_state_b:]) - q[state_p, state_e, state_b, action]
                )    
            
            
            state_p = new_state_p
            state_e = new_state_e
            state_b = new_state_b

            rewards+=reward
        
        if END_EPSILON_DECAYING >= i >= START_EPSILON_DECAYING:
            epsilon -= epsilon_decay_value
            
            
        rewards_per_episode[i] = rewards
        
    if render:
        game.redraw_window()    
    
    # Save Q table to file
    if is_training:
        f = open('vertical_shooter.pkl','wb')
        pickle.dump(q, f)
        f.close()

  
if __name__ == '__main__':
    #run(1, is_training= True, render= True)
    #run(5000, is_training=True, render=False)

    #run(10, is_training=False, render=True)
    run(5, is_training=True, render=True)





# # Action space: 0 = move left, 1 = move right, 2 = do nothing, 3 = shoot
# ACTION_SPACE = 4  # Update action space based on your environment

# # State space size 
# STATE_SPACE = len(Game().get_state())

# def main():
#     print(STATE_SPACE)
    
# if __name__ == "__main__":
#     main()                   


# def get_discrete_state(state):
#     # Convert continuous state to a discrete state representation (if needed)
#     return tuple(state)

# for episode in range(EPISODES):
#     action_state = 4
#     state = game.get_state()
#     #state = 
#     print(state)
#     print(q_table)
#     # print(state)
#     # discrete_state = get_discrete_state(state)
#     # print(discrete_state)
    
#     if episode % SHOW_EVERY == 0:
#         render = True
#         print(f"Episode: {episode}")
#     else:
#         render = False

#     done = False
#     while not done:
#         if np.random.random() > epsilon:
#             # Choose the best action based on the Q-table
#             action = np.argmax(q_table[state, :])
#         else:
#             # Explore: choose a random action
#             action = np.random.choice(game.action_space)

#         # Execute the action in the environment
#         new_state, reward, done = game.play_step(action)
        
#         q_table[state, action] = q_table[state, action] + LEARNING_RATE * (
#                     reward + DISCOUNT*np.max(q_table[new_state,:]) - q_table[state, action]
#                 )

#         # Update Q-value based on the Bellman equation
#         #flat_new_state = np.ravel(np.array(new_state), q_table.shape[:-1])
        
#         # max_future_q = np.max(q_table[])
#         # print(max_future_q)
#         # flat_state = np.ravel(np.array(state), q_table.shape[:-1])
#         # current_q = q_table[flat_state + (action,)]

#         # new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
#         # q_table[flat_state + (action,)] = new_q

#         if render:
#             game.redraw_window()

#     # Decay epsilon to shift from exploration to exploitation
#     if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
#         epsilon -= epsilon_decay_value
