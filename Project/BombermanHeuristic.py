import math
import random

import BombermanSource as bs
import testBoards as boards

EMPTY = 0 # if a board space is not occupied
MAX_BOMB_NUM = 1 # max number of bombs a player can place at once, can be changed
A_BOMBS = [44,43,42,41] # bombs corresponding to player A
B_BOMBS = [54,53,52,51] # bombs corresponding to player B

# This method takes the current state and returns the next state that is the
# result of making the best possible move 
def makeMove(curr_state):
    move_choice = decide_best(curr_state, curr_state, 1, 6, -1000000, 1000000)
    return move_choice[2]

# This method recursively uses minimax with alpha beta pruning to determine the best
# possible action choice for the player.  Ply initially set to 6, can be adjusted.
def decide_best(state, first, level, plyLeft, alpha, beta):
    if plyLeft == 0: return [static_eval(state), state, first, level]
    if state.player == bs.PLAYER_A:
        provisional = [-100000, state, first, level]
    else: # bs.PLAYER_B
        provisional = [100000, state, first, level]
    for s in bs.look_for_successors(state):
        s2 = bs.Bman_state(s.board, s.turn_count, state.player, s.bomb_count)
        if find_location(state) != find_location(s2):
            if level == 1:
                # stores the first move in the chain of moves that the
                # player will optimally make
                first = s
            # recursively calls decide_best until ply run out
            new = decide_best(s, first, level+1, plyLeft-1, alpha, beta)
            if (state.player == bs.PLAYER_A and new[0] > provisional[0]) or\
               (state.player == bs.PLAYER_B and new[0] < provisional[0]):
                provisional = new
            # alpha-beta pruning using fail-soft variation
            if state.player == bs.PLAYER_A:
                if provisional[0] > alpha:
                    alpha = provisional[0]
                if beta < alpha:
                    break # beta cut off
            else: # state.player == bs.PLAYER_B:
                if provisional[0] < beta:
                    beta = provisional[0]
                if beta < alpha:
                    break # alpha cut off
            # small amount of randomness among choices w/ same value
            if (state.player == bs.PLAYER_A and new[0] == provisional[0]) or\
               (state.player == bs.PLAYER_B and new[0] == provisional[0]):
                rint = random.randint(0,1)
                if rint == 0:
                    provisional = new
    return provisional

# This function makes a static evaluation of the current state.  If the current player
# is dead that is maximally worst score and if other player is dead that gives the
# maximally best score.  A is given a high score as the maximizing player and B is
# given a low score as a minimizing player.  The score is better if closer to the center
# of the board as opposed to the outside and planting a bomb is better than not. The
# euclidean distance is used to try to minimize the distance between the current players
# bombs and the enemy piece thus incentivizing blowing up the enemy (the end goal). There
# is a penalty that is proportionate to the danger of being next to an enemy bomb.
def static_eval(state):
    state_value = 0
    other_state = state
    other_player = bs.PLAYER_B
    if state.player == bs.PLAYER_A:
        other_player = bs.PLAYER_B
        other_state = bs.Bman_state(state.board, state.turn_count, other_player, state.bomb_count)
    else: # bs.PLAYER_B
        other_player = bs.PLAYER_A
        other_state = bs.Bman_state(state.board, state.turn_count, other_player, state.bomb_count)
    location = find_location(state)
    other_location = find_location(other_state)
    if location == (0,0): # player is dead
        if state.player == bs.PLAYER_A:
            state_value += -100000
        else: # bs.PLAYER_B
            state_value += 100000
    if other_location == (0,0):# other player is dead
        if other_player == bs.PLAYER_A:
            state_value += -100000
        else: # bs.PLAYER_B
            state_value += 100000
    else: # player is still alive
        state_value += get_location_value(location, state.player)
        state_value += get_location_value(other_location, other_player)
        state_value += get_euc_dist(state, location, other_location)
    state_value += get_euc_dist(other_state, other_location, location)
    state_value += check_bomb_proximity(state, state.player, location)
    state_value += check_bomb_proximity(other_state, other_player, other_location)
    state_value += bomb_nums(state)
    state_value += bomb_nums(other_state)
    return state_value

# Determines the sum of the euclidean distance between all of current player's bombs and
# the enemy player.
def get_euc_dist(state, friend, enemy):
    value = 0
    row, col = enemy
    row_f, col_f = friend
    max_dist = math.sqrt(abs(row-row_f)*abs(row-row_f) + abs(col-col_f)*abs(col-col_f))
    for r in range(bs.BOARD_SIZE):
        for c in range(bs.BOARD_SIZE):
            if state.player == bs.PLAYER_A and state.board[r][c] in A_BOMBS:
                curr_dist = math.sqrt(abs(row-r)*abs(row-r) + abs(col-c)*abs(col-c))
                value += max_dist - curr_dist
            if state.player == bs.PLAYER_B and state.board[r][c] in B_BOMBS:
                curr_dist = math.sqrt(abs(row-r)*abs(row-r) + abs(col-c)*abs(col-c))
                value -= max_dist - curr_dist
    return value
                
# good to plant bombs
def bomb_nums(state):
    value = (MAX_BOMB_NUM - state.bomb_count[state.player]) * 10
    if state.player == bs.PLAYER_A:
        return value
    else: # bs.PLAYER_B
        return 0 - value

# checks if player is in impending doom
def check_bomb_proximity(state, player, location):
    value = 0
    row, col = location
    curr_row = row
    curr_col = col
    clear = True
    while clear:
        if curr_row + 1 < bs.BOARD_SIZE - 1:
            curr_row += 1
            curr_spot = state.board[curr_row][col]
            if curr_spot != EMPTY:
                count = curr_spot % 10
                if count != 0:
                    value -= 1/count * 30
                break
        else:
            break
    curr_row = row
    while clear:
        if curr_row - 1 < bs.BOARD_SIZE - 1:
            curr_row -= 1
            curr_spot = state.board[curr_row][col]
            if curr_spot != EMPTY:
                count = curr_spot % 10
                if count != 0:
                    value -= 1/count * 30
                break
        else:
            break
    curr_row = row
    while clear:
        if curr_col + 1 < bs.BOARD_SIZE - 1:
            curr_col += 1
            curr_spot = state.board[row][curr_col]
            if curr_spot != EMPTY:
                count = curr_spot % 10
                if count != 0:
                    value -= 1/count * 30
                break
        else:
            break
    curr_col = col
    while clear:
        if curr_col - 1 < bs.BOARD_SIZE - 1:
            curr_col -= 1
            curr_spot = state.board[row][curr_col]
            if curr_spot != EMPTY:
                count = curr_spot % 10
                if count != 0:
                    value -= 1/count * 30
                break
        else:
            break
    if state.player == bs.PLAYER_A:
        return value
    else: # bs.PLAYER_B
        return 0 - value

# returns a greater absolute value if closer to the center of the board
def get_location_value(location, player):
    row, col = location
    min_dist = min(row, col)
    if min_dist > bs.BOARD_SIZE / 2:
        min_dist = bs.BOARD_SIZE - 1 - min_dist
    value = min_dist
    if player == bs.PLAYER_A:
        return value
    else: # bs.PLAYER_B
        return 0 - value

# returns the row,col of the current player as a tuple
def find_location(state):
    for row in range(bs.BOARD_SIZE):
        for col in range(bs.BOARD_SIZE):
            #print("board value is: " + str(state.board[row][col]) + " state player is: " + str(state.player))
            if state.board[row][col] == (state.player* 10 + bs.PLAYER_CODE_OFFSET):
                return (row, col)
    return (0, 0)






