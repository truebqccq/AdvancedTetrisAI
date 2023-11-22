from gym.envs.registration import register

register(
    id='tetris_rl',
    entry_point='gym_tetris.envs:TetrisEnv',
)