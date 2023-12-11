import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

from gym_tetris.envs.tetris_ctl import controller
from gym_tetris.envs.env_test import *

class TetrisEnv(gym.Env):
    metadata = {
            "render_modes": ["human", "rgb_array", "none"],
            "render_fps": 30,
    }
    
    def __init__(self, render_mode = "human"):
        print('Built Tetris v3.0')
        self.action_space = spaces.Discrete(7)
        self.observation_space = spaces.Box(low=0, high=2, shape=(1, 29, 10), dtype=np.float32)
        self.controller = controller()
        self.render_mode = render_mode

        pg.init()
        if render_mode == 'none':
            return
        self.display = TetrisDisplay()
        self.screen = pg.Surface((self.display.screen_width, self.display.screen_length))
        self.display.screen_init(self.screen)
        if render_mode == "human":
            pg.display.init()
            pg.display.set_caption("tetris display")
            self.window = pg.display.set_mode((self.display.screen_width, self.display.screen_length))
            pg.display.update()
        

    """
    action space
        0: move right
        1: move left
        2: rotate clockwise
        3: rotate counterclockwise
        4: soft drop
        5: hard drop
        6: hold
    """
    def step(self, action):
        reward = 0
        landed = False
        fire = 0
        pos = [0, 0]
        if action == 0:
            reward += self.controller.move_x(1)
        elif action == 1:
            reward += self.controller.move_x(-1)
        elif action == 2:
            reward += self.controller.rotate(1)
        elif action == 3:
            reward += self.controller.rotate(-1)
        elif action == 4 or action == 5:
            if action == 4:
                landed, reward, column_list, landing_bonus, pos = self.controller.soft_drop()
            elif action == 5:
                landed, reward, column_list, landing_bonus, pos = self.controller.hard_drop()
            fire = reward
            if reward > 0:
                reward += 2
            if landed:
                reward += landing_bonus                
                height = self.controller.highest()
                reward -= height * 0.01
        elif action == 6:
            reward += self.controller.hold()
        
        obs = np.array(self.controller.get_state(), dtype=np.float32)

        is_done = self.controller.gameover

        return obs, reward, is_done, {'landed':landed, 'fire':fire, 'pos':pos}
            

    def reset(self):
        self.controller.reset()
        obs = np.array(self.controller.get_state(), dtype=np.float32)
        return obs

    def render(self):
        if self.render_mode == 'none':
            return
        if self.render_mode is None:
            gym.logger.warn(
                "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. gym("{self.spec.id}", render_mode="rgb_array")'
            )
            return
        self.display.screen_update(self.screen, self)
        if self.render_mode == "human":
            self.window.blit(self.screen, self.screen.get_rect())
            pg.display.update()
        elif self.render_mode == "rgb_array":
            return np.transpose(
                np.array(pg.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )
        


    def close(self):
        if self.screen is not None:
            import pygame

            pygame.display.quit()
            pygame.quit()

    def add_fire(self, fire):
        self.controller.add_fire(fire)