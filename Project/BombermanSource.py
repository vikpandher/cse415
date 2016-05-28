
import testBoards as test

PLAYER_A = 0
PLAYER_B = 1
#PLAYER_C = 0
#PLAYER_D = 1

PLAYER_COUNT = 2
PLAYER_CODE_OFFSET = 40
BOARD_SIZE = 11 # sizes are width and height
BOMB_BLAST_RADIUS = 3 # 0 means just at bomb location, 1 is one out from there
BOMB_COUNT_START = 3
DEFAULT_BOMB_COUNT = 1 # players can only drop one bomb at a time

# renamed these just because
'''
Str Cod Name
--  0   Blank Space
XX  10  Solid Wall
##  20  Breakable Wall
!!  30  Explosion
AA  40  Player A
A*  4*  Player A's Bomb (* = countdown from 3-1)
BB  50  Player B
B*  5*  Player B's Bomb (* = countdown from 3-1)
'''
STRING_TO_CODE = {'--':0, 'XX':10, '##':20, '!!':30, 'AA':40, 'BB':50,
                  'A1':41, 'A2':42, 'A3':43, 'B1':51, 'B2':52, 'B3':53}
CODE_TO_STRING = {0:'--', 10:'XX', 20:'##', 30:'!!', 40:'AA', 50:'BB',
                  41:'A1', 42:'A2', 43:'A3', 51:'B1', 52:'B2', 53:'B3'}

INITIAL = ('''
XX XX XX XX XX XX XX XX XX XX XX
XX AA -- -- -- ## -- -- -- -- XX
XX -- XX -- XX -- XX -- XX -- XX
XX -- -- ## -- ## -- ## -- -- XX
XX -- XX -- XX -- XX -- XX -- XX
XX ## -- ## -- ## -- ## -- ## XX
XX -- XX -- XX -- XX -- XX -- XX
XX -- -- ## -- ## -- ## -- -- XX
XX -- XX -- XX -- XX -- XX -- XX
XX -- -- -- -- ## -- -- -- BB XX
XX XX XX XX XX XX XX XX XX XX XX
''')



def parse(board_string):
  '''Translate a board string into the list of lists representation.'''
  board_list = [[0 for c in range(BOARD_SIZE)] for r in range(BOARD_SIZE)]
  row_list = board_string.split("\n")
  row_list = row_list[1:] # first new line causes an empty row
  for row in range(BOARD_SIZE):
    col_list = row_list[row].split(' ')
    for col in range(BOARD_SIZE):
      board_list[row][col] = STRING_TO_CODE[col_list[col]]
  return board_list
  
def copy_board(old_board):
  '''Make a copy of the game board (which is a list of lists).'''
  new_board = [[0 for c in range(BOARD_SIZE)] for r in range(BOARD_SIZE)]
  for row in range(BOARD_SIZE):
    for col in range(BOARD_SIZE):
      new_board[row][col] = old_board[row][col]
  return new_board

class Bman_state:
  '''Object that tracks Bomberman's board state.'''
  def __init__(self, old_board=INITIAL, turn_count=0, player=PLAYER_A, bomb_count=DEFAULT_BOMB_COUNT):
    new_board = [r[:] for r in old_board]
    self.board = new_board
    self.player = player
    self.turn_count = turn_count
    self.bomb_count = bomb_count

  def __repr__(self):
    output = ''
    for row in range(BOARD_SIZE):
      for col in range(BOARD_SIZE):
        output += CODE_TO_STRING[self.board[row][col]] + " "
      output += "\n"
    output += "Turn " + str(self.turn_count) + ", Player "
    if self.player == PLAYER_A:
      output += "A"
    if self.player == PLAYER_B:
      output += "B"
    #if self.player == PLAYER_C:
    #  output += "C"
    #if self.player == PLAYER_D:
    #  output += "D"
    output += "'s move, " + str(self.bomb_count) + " bombs\n"
    return output

def look_for_successors(state):
  '''Generate all possible successor states from the current state'''
  successors = []
  bomb_locations = []
  player_location = None
  
  # Find the location of all the current player's pieces
  for row in range(BOARD_SIZE): # look through rows
    for col in range(BOARD_SIZE): # look through columns
      current_piece = state.board[row][col]
      
      # Old Explosion
      if (current_piece == 30):
        state.board[row][col] = 0
      
      # Player
      elif (current_piece == PLAYER_CODE_OFFSET + state.player * 10):
        player_location = (row, col)
      
      # Player's Bomb
      elif (current_piece > PLAYER_CODE_OFFSET + state.player * 10 and current_piece < PLAYER_CODE_OFFSET + 10 + state.player * 10):
        bomb_locations.append((row, col))
      
        
  if (bomb_locations != []):
    post_bomb_state = analyze_bombs(state, bomb_locations)
  else:
    post_bomb_state = state
  if (player_location != None):
    successors.extend(analyze_player(post_bomb_state, player_location))
  else:
    end_state = Bman_state(post_bomb_state.board, post_bomb_state.turn_count + 1, (post_bomb_state.player + 1) % PLAYER_COUNT, post_bomb_state.bomb_count)
    print(end_state)
  return successors
  
def states_to_string(states):
  '''Takes a list of states and turns them into a string.'''
  output = ''
  for state in states:
    output += str(state) + "\n"
  return output

def analyze_piece(piece, player):
  '''Finds what type of piece the current piece is.'''
  # Player
  if (piece == PLAYER_CODE_OFFSET + player * 10):
    return "player"
  
  # Player's Bomb
  if (piece > PLAYER_CODE_OFFSET + player * 10 and piece < PLAYER_CODE_OFFSET + 10 + player * 10):
    return "bomb"
  
  return '''ERROR: I don't got no type
  Bad bitches is the only thing that I like
  You ain't got no life
  Cups with the ice and we do this every night'''
  
def analyze_bombs(state, bomb_locations):
  post_bomb_board = copy_board(state.board)
  explo_val = 0 # used to return bomb to player if it exploded
  
  # update all given bombs  
  for spot in bomb_locations:
    row, col = spot
    bomb_timer = int(CODE_TO_STRING[post_bomb_board[row][col]][-1])
    # bombs tick down
    if(bomb_timer > 1):
      post_bomb_board[row][col] -= 1
    # bombs explode
    elif(bomb_timer == 1):
      explo_val += 1
      post_bomb_board[row][col] = 30
      
      # explode towards the highest column
      k = 1
      while (col + k < BOARD_SIZE):
        if(k > BOMB_BLAST_RADIUS): # out of blast range
          break
        if (post_bomb_board[row][col + k] == 10): # hit a solid wall
          break
        elif (post_bomb_board[row][col + k] == 0): # blank space
          post_bomb_board[row][col + k] = 30 # add an explosion
        else: # hit something else
          post_bomb_board[row][col + k] = 30 # add an explosion
          break
        k += 1
      
      # explode towards the 0th column
      k = 1
      while (col - k > -1):
        if(k > BOMB_BLAST_RADIUS): # out of blast range
          break
        if (post_bomb_board[row][col - k] == 10): # hit a solid wall
          break
        elif (post_bomb_board[row][col - k] == 0): # blank space
          post_bomb_board[row][col - k] = 30 # add an explosion
        else: # hit something else
          post_bomb_board[row][col - k] = 30 # add an explosion
          break
        k += 1
        
      # explode towards the highest row
      k = 1
      while (row + k < BOARD_SIZE):
        if(k > BOMB_BLAST_RADIUS): # out of blast range
          break
        if (post_bomb_board[row + k][col] == 10): # hit a solid wall
          break
        elif (post_bomb_board[row + k][col] == 0): # blank space
          post_bomb_board[row + k][col] = 30 # add an explosion
        else: # hit something else
          post_bomb_board[row + k][col] = 30 # add an explosion
          break
        k += 1
      
      # explode towards the 0th row
      k = 1
      while (row - k > -1):
        if(k > BOMB_BLAST_RADIUS): # out of blast range
          break
        if (post_bomb_board[row - k][col] == 10): # hit a solid wall
          break
        elif (post_bomb_board[row - k][col] == 0): # blank space
          post_bomb_board[row - k][col] = 30 # add an explosion
        else: # hit something else
          post_bomb_board[row - k][col] = 30 # add an explosion
          break
        k += 1
      
  new_state = Bman_state(post_bomb_board, state.turn_count, state.player, state.bomb_count + explo_val)
  return new_state
  
def analyze_player(state, player_location):
  new_states = []
  piece = PLAYER_CODE_OFFSET + state.player * 10
  row, col = player_location
  
  # checking horizontal movement toward the highest column
  # NOTE: Allowed to walk into empty space or an explosion, but piece dies if explosion
  if (col < BOARD_SIZE - 1 and (state.board[row][col + 1] == 0 or state.board[row][col + 1] == 30)):
    # add regular move state
    new_board = copy_board(state.board)
    if (state.board[row][col + 1] == 0):
      new_board[row][col + 1] = piece
    new_board[row][col] = 0
    new_state = Bman_state(new_board, state.turn_count + 1, (state.player + 1) % PLAYER_COUNT, state.bomb_count)
    new_states.append(new_state)
    
    # add bomb drop state
    if(state.bomb_count > 0):
      new_board = copy_board(state.board)
      if (state.board[row][col + 1] == 0):
        new_board[row][col + 1] = piece
      new_board[row][col] = PLAYER_CODE_OFFSET + state.player * 10 + BOMB_COUNT_START
      new_state = Bman_state(new_board, state.turn_count + 1, (state.player + 1) % PLAYER_COUNT, state.bomb_count - 1)
      new_states.append(new_state)
  
  # checking horizontal movement toward the 0th column
  if (col > 0 and (state.board[row][col - 1] == 0 or state.board[row][col - 1] == 30)):
    # add regular move state
    new_board = copy_board(state.board)
    if (state.board[row][col - 1] == 0):
      new_board[row][col - 1] = piece
    new_board[row][col] = 0
    new_state = Bman_state(new_board, state.turn_count + 1, (state.player + 1) % PLAYER_COUNT, state.bomb_count)
    new_states.append(new_state)
    
    # add bomb drop state
    if(state.bomb_count > 0):
      new_board = copy_board(state.board)
      if (state.board[row][col - 1] == 0):
        new_board[row][col - 1] = piece
      new_board[row][col] = PLAYER_CODE_OFFSET + state.player * 10 + BOMB_COUNT_START
      new_state = Bman_state(new_board, state.turn_count + 1, (state.player + 1) % PLAYER_COUNT, state.bomb_count - 1)
      new_states.append(new_state)
  
  # checking vertical movement toward the highest row
  if (row < BOARD_SIZE - 1 and (state.board[row + 1][col] == 0 or state.board[row + 1][col] == 30)):
    # add regular move state
    new_board = copy_board(state.board)
    if (state.board[row + 1][col] == 0):
      new_board[row + 1][col] = piece
    new_board[row][col] = 0
    new_state = Bman_state(new_board, state.turn_count + 1, (state.player + 1) % PLAYER_COUNT, state.bomb_count)
    new_states.append(new_state)
    
    # add bomb drop state
    if(state.bomb_count > 0):
      new_board = copy_board(state.board)
      if (state.board[row + 1][col] == 0):
        new_board[row + 1][col] = piece
      new_board[row][col] = PLAYER_CODE_OFFSET + state.player * 10 + BOMB_COUNT_START
      new_state = Bman_state(new_board, state.turn_count + 1, (state.player + 1) % PLAYER_COUNT, state.bomb_count - 1)
      new_states.append(new_state)
  
  # checking vertical movement toward the 0th row
  if (row > 0 and (state.board[row - 1][col] == 0 or state.board[row - 1][col] == 30)):
    # add regular move state
    new_board = copy_board(state.board)
    if (state.board[row - 1][col] == 0):
      new_board[row - 1][col] = piece
    new_board[row][col] = 0
    new_state = Bman_state(new_board, state.turn_count + 1, (state.player + 1) % PLAYER_COUNT, state.bomb_count)
    new_states.append(new_state)
    
    # add bomb drop state
    if(state.bomb_count > 0):
      new_board = copy_board(state.board)
      if (state.board[row - 1][col] == 0):
        new_board[row - 1][col] = piece
      new_board[row][col] = PLAYER_CODE_OFFSET + state.player * 10 + BOMB_COUNT_START
      new_state = Bman_state(new_board, state.turn_count + 1, (state.player + 1) % PLAYER_COUNT, state.bomb_count - 1)
      new_states.append(new_state)
  
  return new_states



init_state = Bman_state(parse(test.BOMB_TEST_1), 0, PLAYER_A)
print(init_state)
print(states_to_string(look_for_successors(init_state)))