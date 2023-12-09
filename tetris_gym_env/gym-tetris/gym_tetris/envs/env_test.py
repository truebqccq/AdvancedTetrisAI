import gym
import numpy as np
import pygame as pg
import sys
from gym_tetris.envs.tetris_ctl import minos

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

COLOR_BG = (43, 43, 43)
COLOR_I = (38, 203, 226)
COLOR_J = (0, 0, 200)
COLOR_L = (221, 109, 23)
COLOR_O = (243, 250, 0)
COLOR_S = (114, 238, 0)
COLOR_T = (140, 3, 140)
COLOR_Z = (250, 0, 0)
# color for fires
COLOR_F = (65, 85, 86)
COLORS = [COLOR_BG, COLOR_I, COLOR_J, COLOR_L, COLOR_O, COLOR_S, COLOR_T, COLOR_Z, COLOR_F]

class TetrisDisplay:
# data for single play
    def __init__(self):
        self.num_rows = 23
        self.num_columns = 10

        self.block_size = 30
        self.screen_width = self.block_size * 40 
        self.screen_length = self.block_size * 22

        self.field_width = self.block_size * 10
        self.field_length = self.block_size * 20
        self.field_x = self.block_size * 7
        self.field_y = self.block_size * 1

        self.hold_ratio = 0.8
        self.hold_block_size = self.block_size * self.hold_ratio
        self.hold_width = self.hold_block_size * 5
        self.hold_length = self.hold_block_size * 5
        self.hold_x = self.block_size * 1
        self.hold_y = self.block_size * 8
        self.hold_text_x = self.block_size * 1
        self.hold_text_y = self.block_size * 7

        self.score_width = self.block_size * 5
        self.score_length = self.block_size * 1
        self.score_x = self.block_size * 1
        self.score_y = self.block_size * 17
        self.score_text_x = self.block_size * 1
        self.score_text_y = self.block_size * 16


        self.nexts_ratio = 0.7
        self.nexts_block_size = self.block_size * self.nexts_ratio
        self.nexts_width = self.nexts_block_size * 5
        self.nexts_length = self.nexts_block_size * 5
        self.nexts_text_x = self.field_x + self.field_width + self.block_size * 2
        self.nexts_text_y = self.block_size * 1
        self.nexts_x = [self.field_x + self.field_width + self.block_size * 2] * 5
        self.nexts_y = [self.nexts_text_y + self.block_size + i * (self.nexts_length + 10) for i in range(5)]

   # View functions here
    def draw_hold(self, screen):
        # show the square blank for held mino
        pg.draw.rect(screen, COLOR_BG, [self.hold_x, self.hold_y, self.hold_width, self.hold_length])

    # show field based on its contents
    # draw dropping tetriminos as well
    def draw_field(self, screen):
        pg.draw.rect(screen, BLACK, [self.field_x, self.field_y, self.field_width, self.field_length], 5)
        pg.draw.rect(screen, COLOR_BG, [self.field_x, self.field_y, self.field_width, self.field_length])

    def draw_nexts(self, screen):
        # show string "NEXT"
        for i in range(5):
            pg.draw.rect(screen, COLOR_BG, [self.nexts_x[i], self.nexts_y[i], self.nexts_width, self.nexts_length])

    def screen_init(self, screen):
        screen.fill(BLACK)
        self.draw_hold(screen)
        self.draw_field(screen)
        self.draw_nexts(screen)

    # Note that this doesn't update screen if there is nothing in hold
    def update_hold(self, screen, hold_mino_id):
        self.draw_hold(screen)
        if hold_mino_id != None:
            # delete current drawing first
            self.draw_mino(screen, hold_mino_id, self.hold_x, self.hold_y, self.hold_block_size, 0)


    def update_score(self, screen, score, score_text):
        # reset
        pg.draw.rect(screen, COLOR_BG, [self.score_x, self.score_y, self.score_width, self.score_length])
        # reset text
        pg.draw.rect(screen, BLACK, [self.score_x, self.score_y + self.block_size, self.field_x - self.score_x, self.score_length])

        # draw new value
        font = pg.font.Font(None, self.block_size)
        txt = font.render(str(score), True, WHITE)
        screen.blit(txt, [self.score_x, self.score_y])
        # show string "SCORE"
        font = pg.font.Font(None, self.block_size)
        txt = font.render(score_text, True, WHITE)
        screen.blit(txt, [self.score_x, self.score_y + self.block_size])

    def update_field(self, screen, field):
        self.draw_field(screen)
        for y in range(20):
            for x in range(10):
                if field[y + 3][x] > 0: # if there is a block
                    color = COLORS[field[y + 3][x]]
                    start_x = self.block_size * x + self.field_x
                    start_y = self.block_size * y + self.field_y
                    pg.draw.rect(screen, color, [start_x, start_y, self.block_size, self.block_size])
                    # enclose it with bg color line
                    pg.draw.rect(screen, COLOR_BG, [start_x, start_y, self.block_size, self.block_size], 1)

    def draw_mino(self, screen, mino_id, draw_x, draw_y, b_size, rot):
        mino_layout = minos[mino_id].block_data[rot] # 4 x 2
        for xy in mino_layout:
            d_x = draw_x + xy[0] * b_size
            d_y = draw_y + xy[1] * b_size
            pg.draw.rect(screen, COLORS[mino_id], [d_x, d_y, b_size, b_size])
            pg.draw.rect(screen, COLOR_BG, [d_x, d_y, b_size, b_size], 1)

    def update_nexts(self, screen, next_minos):
        for i in range(5):
            draw_x = self.nexts_x[i]
            draw_y = self.nexts_y[i]
            pg.draw.rect(screen, COLOR_BG, [draw_x, draw_y, self.nexts_width, self.nexts_length])
            self.draw_mino(screen, next_minos[i], draw_x, draw_y, self.nexts_block_size, 0)

    def update_drop(self, screen, dropping_mino):
        if dropping_mino != None:
            d_x = dropping_mino.current_pos[0] * self.block_size + self.field_x
            d_y = dropping_mino.current_pos[1] * self.block_size + self.field_y - (23-20) * self.block_size
            self.draw_mino(screen, dropping_mino.mino_id, d_x, d_y, self.block_size, dropping_mino.current_rot)
            pg.draw.rect(screen, BLACK, [self.field_x, 0, self.field_width, self.block_size])
            

    def screen_update(self, screen, env):
        ctl = env.controller
        self.update_hold(screen, ctl.hold_mino_id)
        self.update_field(screen, ctl.field)
        self.update_nexts(screen, ctl.next_minos)
        self.update_drop(screen, ctl.dropping_mino)

if __name__ == '__main__':
    env = gym.make("gym_tetris:tetris_rl")
    env.reset()
    # env.render()
    disp = TetrisDisplay()
    screen = pg.Surface((disp.screen_width, disp.screen_length))
    disp.screen_init(screen)
    # screen = pg.display.set_mode((disp.screen_width, disp.screen_length))

    pg.init()
    if env.render_mode == "human":
        pg.display.init()
        pg.display.set_caption("tetris env test")
        window = pg.display.set_mode((disp.screen_width, disp.screen_length))
        pg.display.update()

    while True:
        obs = None
        reward = 0
        is_done = False
        event = pg.event.wait()
        info = {}
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                obs, reward, is_done, info = env.step(1)
            elif event.key == pg.K_RIGHT:
                obs, reward, is_done, info = env.step(0)
            elif event.key == pg.K_DOWN:
                obs, reward, is_done, info = env.step(4)
            elif event.key == pg.K_SPACE:
                obs, reward, is_done, info = env.step(5)
            elif event.key == pg.K_z:
                obs, reward, is_done, info = env.step(2)
            elif event.key == pg.K_x:
                obs, reward, is_done, info = env.step(3)
            elif event.key == pg.K_c:
                obs, reward, is_done, info = env.step(6)
            elif event.key == pg.K_p:
                pg.quit()
                sys.exit()
        print(env.controller.heuristical_reward())
        #print(np.array(obs))
        print("reward is " + str(reward))
        #print("pos : " + str(info['pos']))
        if is_done:
            env.reset()
        disp.screen_update(screen, env)
        if env.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            window.blit(screen, screen.get_rect())
            pg.display.update()
        # env.render()

        pg.event.clear()
