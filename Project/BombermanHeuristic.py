import math

import BombermanSource as bs
import testBoards as boards

EMPTY = 0
MAX_BOMB_NUM = 1
A_BOMBS = [43,42,41]
B_BOMBS = [53,52,51]

def makeMove(curr_state):
    move_choice = decide_best(curr_state, curr_state, 1, 6)
    #print("orig: " + str(curr_state.board) + " val: " + str(static_eval(curr_state)))
    #print("move: " + str(move_choice[1].board) + " val: " + str(static_eval(move_choice[1])))
    return move_choice[2]

def decide_best(state, first, level, plyLeft):
    if plyLeft == 0: return [static_eval(state), state, first, level]
    if state.player == bs.PLAYER_A:
        provisional = [-100000, state, first, level]
    else:
        provisional = [100000, state, first, level]
    for s in bs.look_for_successors(state):
        s2 = bs.Bman_state(s.board, s.turn_count, state.player, s.bomb_count)
        if find_location(state) != find_location(s2):
            if level == 1:
                first = s
            new = decide_best(s, first, level+1, plyLeft-1)
            if (state.player == bs.PLAYER_A and new[0] > provisional[0]) or\
               (state.player == bs.PLAYER_B and new[0] < provisional[0]):
                provisional = new
    return provisional

# good things are not bombs (minus if gunna die),
# if you are close to an enemy bomb then thats bad,
# if your bomb is close to an enemy player thats good,
# less walls (minus points per wall),
# better in the center (higher value for center pieces),
# win if opponent is dead,
# if you are dead then lose

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
   # print("location of player " + str(state.player) + " is " + str(location))
    #print("location of player " + str(other_player) + " is " + str(other_location))
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
     #   print("location val of player " + str(state.player) + " is " + str(get_location_value(location, state.player)))
      #  print("location val of player " + str(other_player) + " is " + str(get_location_value(other_location, other_player)))

    state_value += get_euc_dist(state, location, other_location)
    state_value += get_euc_dist(other_state, other_location, location)
    
    state_value += check_bomb_proximity(state, state.player, location)
    state_value += check_bomb_proximity(other_state, other_player, other_location)
   # print("bomb proximity val of player " + str(state.player) + " is " + str(check_bomb_proximity(state, state.player, location)))
    #print("bomb proximity val of player " + str(other_player) + " is " + str(check_bomb_proximity(other_state, other_player, other_location)))
    state_value += bomb_nums(state)
    state_value += bomb_nums(other_state)
    #print("bomb nums val of player " + str(state.player) + " is " + str(bomb_nums(state)))
    #print("bomb nums val of player " + str(other_player) + " is " + str(bomb_nums(other_state)))
    return state_value

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
        '''
        if state.player == player:
            other_state = bs.Bman_state(state.board, state.turn_count, bs.PLAYER_B, state.bomb_count)
            if check_bomb_proximity(state, bs.PLAYER_B, find_location(other_state)) >= 0:
                value += 1
                '''
        return value
    else: # bs.PLAYER_B
        if state.player == player:
            '''
            other_state = bs.Bman_state(state.board, state.turn_count, bs.PLAYER_A, state.bomb_count)
            if check_bomb_proximity(state, bs.PLAYER_A, find_location(other_state)) <= 0:
                value -= 1
                '''
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
    
def find_location(state):
    for row in range(bs.BOARD_SIZE):
        for col in range(bs.BOARD_SIZE):
            #print("board value is: " + str(state.board[row][col]) + " state player is: " + str(state.player))
            if state.board[row][col] == (state.player* 10 + bs.PLAYER_CODE_OFFSET):
                return (row, col)
    return (0, 0)

#print(bs.Bman_state(bs.create_initial_board()))
print(static_eval(bs.Bman_state(bs.create_initial_board())))
initial = bs.Bman_state(bs.create_initial_board())
for s in bs.look_for_successors(initial):
    s2 = bs.Bman_state(s.board, s.turn_count, initial.player, s.bomb_count)
    if find_location(initial) != find_location(s2):
        print(s)
        print(static_eval(s))


















