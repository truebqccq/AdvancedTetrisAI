def heuristical_reward(self):
    # Adds additional reward based on heuristical measures to allow agent to better place the pieces
    bump = 0
    holes = 0
    height = 0
    for col in range(10):
        found_top = False
        for row in range(23):
            if found_top:
                if self.field[row][col] == 0:
                    holes += 1
            else:
                if self.field[row][col] != 0:
                    found_top = True
                    if col != 0:
                        bump += abs(height - row)
                    height = row

    return (0.5 if holes < 5 else -0.2*(holes - 5)) + (0.5 if bump < 5 else -0.2*(bump - 5))



def move_x(self, x): 
    reward = 0.01*(2 - self.turns_without_drop)
    # Punish doing moves that undoes the previous move
    if self.previous_move == (3-x)//2:
        reward -= 0.05
    self.turns_without_drop += 1
    self.previous_move = (3+x)//2 # 1 = left, 2 = right
    x_position = self.dropping_mino.current_pos[0] + x
    y_position = self.dropping_mino.current_pos[1]
    if self.check_collision(self.dropping_mino.current_rot, [x_position, y_position]) == False: # won't collide
        self.dropping_mino.current_pos[0] += x
        self.last_move_is_rotate = False
    return reward