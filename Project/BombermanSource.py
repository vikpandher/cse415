
import testBoards as test

PLAYER_A = 0
PLAYER_B = 1

PLAYER_COUNT = 2
PLAYER_CODE_OFFSET = 40
BOARD_SIZE = 11 # sizes are width and height, must be odd
BOMB_BLAST_RADIUS = 3 # 0 means just at bomb location, 1 is one out from there
BOMB_COUNT_START = 3
DEFAULT_BOMB_COUNT = [1 for x in range(PLAYER_COUNT)] # players can only drop one bomb at a time

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
MOVES = ['Stay', 'East', 'B.East', 'West', 'B.West', 'South', 'B.South', 'North', 'B.North']

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

INTRO_MESSAGE = ('''
This is bomberman.
This is how you play.
These are your controls.
When asked for input input:
e = move east
E = move east and drop a bomb
w = move west
W = move west and drop a bomb
s = move south
S = move south and drop a bomb
n = move north
N = move north and dorp a bomb
anything else your stay where you were

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
  def __init__(self, old_board=parse(INITIAL), turn_count=0, player=PLAYER_A, bomb_count=DEFAULT_BOMB_COUNT):
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
    output += "'s move, " + str(self.bomb_count[self.player]) + " bomb(s)\n"
    #output += "'s move, " + str(self.bomb_count) + " bomb(s)\n"
    return output

AVAILABLE_MOVES = [] # Tracks which moves are in successors returned by look_for_successors
def make_move(state, move):
  '''Take a state and apply a move to it.'''
  successors = look_for_successors(state)
  index = 0
  while move != AVAILABLE_MOVES[index] and len(AVAILABLE_MOVES) != 0:
    index += 1
    if index == len(AVAILABLE_MOVES):
      print("ERROR: That's not a move.")
      return successors[0]
  return successors[index]

def look_for_successors(state):
  '''Generate all possible successor states from the current state'''
  successors = []
  bomb_locations = []
  player_location = None
  
  # Find the location of all the bombs and snuff out old explosions
  for row in range(BOARD_SIZE): # look through rows
    for col in range(BOARD_SIZE): # look through columns
      current_piece = state.board[row][col]      
      
      # Old Explosion die out
      if (current_piece == 30):
        state.board[row][col] = 0

      # Find all bombs belonging to the current player
      if (current_piece > PLAYER_CODE_OFFSET + 10 * state.player and current_piece < PLAYER_CODE_OFFSET + 10 * state.player + 10):
        bomb_owner = (state.board[row][col] - PLAYER_CODE_OFFSET) // 10
        bomb_locations.append((bomb_owner, row, col))

  if (bomb_locations != []):
    post_bomb_state = analyze_bombs(state, bomb_locations)
  else:
    post_bomb_state = state
  
  for row in range(BOARD_SIZE): # look through rows
    for col in range(BOARD_SIZE): # look through columns
      current_piece = post_bomb_state.board[row][col]
      
      # Player
      if (current_piece == PLAYER_CODE_OFFSET + state.player * 10):
        player_location = (row, col)
        
  if (player_location != None):
    successors.extend(analyze_player(post_bomb_state, player_location))
  else:
    end_state = Bman_state(post_bomb_state.board, post_bomb_state.turn_count + 1, (post_bomb_state.player + 1) % PLAYER_COUNT, post_bomb_state.bomb_count)
    successors.append(end_state)
    
  return successors

def states_to_string(states):
  '''Takes a list of states and turns them into a string.'''
  output = ''
  for state in states:
    output += str(state) + "\n"
  return output

def analyze_bombs(state, bomb_locations):
  '''This takes a states and returns one with all the bombs updated.'''
  post_bomb_board = copy_board(state.board)
  new_bomb_count = state.bomb_count[:]
  
  # update bombs until none left to update
  while (bomb_locations != []):
    bomb_owner, row, col = bomb_locations.pop()
    
    bomb_timer = post_bomb_board[row][col] % 10
    
    # bomb ticks down, only increment bombs that belong to the current player
    if (bomb_timer > 1 and bomb_owner == state.player):
      post_bomb_board[row][col] -= 1
    # bomb is set to blow
    elif (bomb_timer == 1):
      # recheck the owner since, oponent's bombs may have been added (bombs chain)
      this_owner = (post_bomb_board[row][col] - PLAYER_CODE_OFFSET) // 10
      
      new_bomb_count[this_owner] += 1
      post_bomb_board[row][col] = 30
      
      # explode towards the highest column
      k = 1
      while (col + k < BOARD_SIZE):
        # out of blast range
        if(k > BOMB_BLAST_RADIUS):
          break
        # blank space or explosion space
        elif (post_bomb_board[row][col + k] == 0 or post_bomb_board[row][col + k] == 30):
          post_bomb_board[row][col + k] = 30 # explosion
        # hit a solid wall
        elif (post_bomb_board[row][col + k] == 10):
          break
        # hit a bomb
        elif (post_bomb_board[row][col + k] > PLAYER_CODE_OFFSET and\
              post_bomb_board[row][col + k] < PLAYER_CODE_OFFSET + PLAYER_COUNT * 10 and\
              post_bomb_board[row][col + k] % 10 != 0):
          bomb_owner = (post_bomb_board[row][col + k] - PLAYER_CODE_OFFSET) // 10
          post_bomb_board[row][col + k] = post_bomb_board[row][col + k] // 10 * 10 + 1
          bomb_locations.append((bomb_owner, row, col + k))
        # hit something else
        else:
          post_bomb_board[row][col + k] = 30 # add an explosion
          break
        k += 1
      
      # explode towards the 0th column
      k = 1
      while (col - k > -1):
        # out of blast range
        if(k > BOMB_BLAST_RADIUS):
          break
        # blank space or explosion space
        elif (post_bomb_board[row][col - k] == 0 or post_bomb_board[row][col - k] == 30):
          post_bomb_board[row][col - k] = 30 # explosion
        # hit a solid wall
        elif (post_bomb_board[row][col - k] == 10):
          break
        # hit a bomb
        elif (post_bomb_board[row][col - k] > PLAYER_CODE_OFFSET and\
              post_bomb_board[row][col - k] < PLAYER_CODE_OFFSET + PLAYER_COUNT * 10 and\
              post_bomb_board[row][col - k] % 10 != 0):
          bomb_owner = (post_bomb_board[row][col - k] - PLAYER_CODE_OFFSET) // 10
          post_bomb_board[row][col - k] = post_bomb_board[row][col - k] // 10 * 10 + 1
          bomb_locations.append((bomb_owner, row, col - k))
        # hit something else
        else:
          post_bomb_board[row][col - k] = 30 # add an explosion
          break
        k += 1
      
      # explode towards the highest row
      k = 1
      while (row + k < BOARD_SIZE):
        # out of blast range
        if(k > BOMB_BLAST_RADIUS):
          break
        # blank space or explosion space
        elif (post_bomb_board[row + k][col] == 0 or post_bomb_board[row + k][col] == 30):
          post_bomb_board[row + k][col] = 30 # explosion
        # hit a solid wall
        elif (post_bomb_board[row + k][col] == 10):
          break
        # hit a bomb
        elif (post_bomb_board[row + k][col] > PLAYER_CODE_OFFSET and\
              post_bomb_board[row + k][col] < PLAYER_CODE_OFFSET + PLAYER_COUNT * 10 and\
              post_bomb_board[row + k][col] % 10 != 0):
          bomb_owner = (post_bomb_board[row + k][col] - PLAYER_CODE_OFFSET) // 10
          post_bomb_board[row + k][col] = post_bomb_board[row + k][col] // 10 * 10 + 1
          bomb_locations.append((bomb_owner, row + k, col))
        # hit something else
        else:
          post_bomb_board[row + k][col] = 30 # add an explosion
          break
        k += 1
      
      # explode towards the 0th row
      k = 1
      while (row - k > -1):
        # out of blast range
        if(k > BOMB_BLAST_RADIUS):
          break
        # blank space or explosion space
        elif (post_bomb_board[row - k][col] == 0 or post_bomb_board[row - k][col] == 30):
          post_bomb_board[row - k][col] = 30 # explosion
        # hit a solid wall
        elif (post_bomb_board[row - k][col] == 10):
          break
        # hit a bomb
        elif (post_bomb_board[row - k][col] > PLAYER_CODE_OFFSET and\
              post_bomb_board[row - k][col] < PLAYER_CODE_OFFSET + PLAYER_COUNT * 10 and\
              post_bomb_board[row - k][col] % 10 != 0):
          bomb_owner = (post_bomb_board[row - k][col] - PLAYER_CODE_OFFSET) // 10
          post_bomb_board[row - k][col] = post_bomb_board[row - k][col] // 10 * 10 + 1
          bomb_locations.append((bomb_owner, row - k, col))
        # hit something else
        else:
          post_bomb_board[row - k][col] = 30 # add an explosion
          break
        k += 1
    
  new_state = Bman_state(post_bomb_board, state.turn_count, state.player, new_bomb_count)
  return new_state

def analyze_player(state, player_location):
  '''This takes a state and returns a list of states for each of the the
     players potential moves.'''
  AVAILABLE_MOVES.clear()
  new_states = []
  piece = PLAYER_CODE_OFFSET + state.player * 10
  row, col = player_location
  
  # adding the option no move move
  new_board = copy_board(state.board)
  new_state = Bman_state(new_board, state.turn_count + 1, (state.player + 1) % PLAYER_COUNT, state.bomb_count)
  new_states.append(new_state)
  AVAILABLE_MOVES.append('Stay')
  
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
    AVAILABLE_MOVES.append('East')
    
    # add bomb drop state
    if(state.bomb_count[state.player] > 0):
      new_board = copy_board(state.board)
      if (state.board[row][col + 1] == 0):
        new_board[row][col + 1] = piece
      new_board[row][col] = PLAYER_CODE_OFFSET + state.player * 10 + BOMB_COUNT_START
      new_bomb_count = state.bomb_count[:]
      new_bomb_count[state.player] -= 1
      new_state = Bman_state(new_board, state.turn_count + 1, (state.player + 1) % PLAYER_COUNT, new_bomb_count)
      new_states.append(new_state)
      AVAILABLE_MOVES.append('B.East')
  
  # checking horizontal movement toward the 0th column
  if (col > 0 and (state.board[row][col - 1] == 0 or state.board[row][col - 1] == 30)):
    # add regular move state
    new_board = copy_board(state.board)
    if (state.board[row][col - 1] == 0):
      new_board[row][col - 1] = piece
    new_board[row][col] = 0
    new_state = Bman_state(new_board, state.turn_count + 1, (state.player + 1) % PLAYER_COUNT, state.bomb_count)
    new_states.append(new_state)
    AVAILABLE_MOVES.append('West')
    
    # add bomb drop state
    if(state.bomb_count[state.player] > 0):
      new_board = copy_board(state.board)
      if (state.board[row][col - 1] == 0):
        new_board[row][col - 1] = piece
      new_board[row][col] = PLAYER_CODE_OFFSET + state.player * 10 + BOMB_COUNT_START
      new_bomb_count = state.bomb_count[:]
      new_bomb_count[state.player] -= 1
      new_state = Bman_state(new_board, state.turn_count + 1, (state.player + 1) % PLAYER_COUNT, new_bomb_count)
      new_states.append(new_state)
      AVAILABLE_MOVES.append('B.West')
  
  # checking vertical movement toward the highest row
  if (row < BOARD_SIZE - 1 and (state.board[row + 1][col] == 0 or state.board[row + 1][col] == 30)):
    # add regular move state
    new_board = copy_board(state.board)
    if (state.board[row + 1][col] == 0):
      new_board[row + 1][col] = piece
    new_board[row][col] = 0
    new_state = Bman_state(new_board, state.turn_count + 1, (state.player + 1) % PLAYER_COUNT, state.bomb_count)
    new_states.append(new_state)
    AVAILABLE_MOVES.append('South')
    
    # add bomb drop state
    if(state.bomb_count[state.player] > 0):
      new_board = copy_board(state.board)
      if (state.board[row + 1][col] == 0):
        new_board[row + 1][col] = piece
      new_board[row][col] = PLAYER_CODE_OFFSET + state.player * 10 + BOMB_COUNT_START
      new_bomb_count = state.bomb_count[:]
      new_bomb_count[state.player] -= 1
      new_state = Bman_state(new_board, state.turn_count + 1, (state.player + 1) % PLAYER_COUNT, new_bomb_count)
      new_states.append(new_state)
      AVAILABLE_MOVES.append('B.South')
  
  # checking vertical movement toward the 0th row
  if (row > 0 and (state.board[row - 1][col] == 0 or state.board[row - 1][col] == 30)):
    # add regular move state
    new_board = copy_board(state.board)
    if (state.board[row - 1][col] == 0):
      new_board[row - 1][col] = piece
    new_board[row][col] = 0
    new_state = Bman_state(new_board, state.turn_count + 1, (state.player + 1) % PLAYER_COUNT, state.bomb_count)
    new_states.append(new_state)
    AVAILABLE_MOVES.append('North')
    
    # add bomb drop state
    if(state.bomb_count[state.player] > 0):
      new_board = copy_board(state.board)
      if (state.board[row - 1][col] == 0):
        new_board[row - 1][col] = piece
      new_board[row][col] = PLAYER_CODE_OFFSET + state.player * 10 + BOMB_COUNT_START
      new_bomb_count = state.bomb_count[:]
      new_bomb_count[state.player] -= 1
      new_state = Bman_state(new_board, state.turn_count + 1, (state.player + 1) % PLAYER_COUNT, new_bomb_count)
      new_states.append(new_state)
      AVAILABLE_MOVES.append('B.North')
  
  return new_states

def win_check(state):
  PLAYER_A_DEAD = True
  PLAYER_B_DEAD = True
  for row in range(BOARD_SIZE): # look through rows
    for col in range(BOARD_SIZE): # look through columns
      current_piece = state.board[row][col]      
      
      # Player A found on the board
      if (current_piece == PLAYER_A * 10 + PLAYER_CODE_OFFSET):
        PLAYER_A_DEAD = False
      
      # Player B found on the board
      if (current_piece == PLAYER_B * 10 + PLAYER_CODE_OFFSET):
        PLAYER_B_DEAD = False
  
  if (PLAYER_A_DEAD and PLAYER_B_DEAD):
    return "draw"
  elif (PLAYER_B_DEAD):
    return PLAYER_A
  elif (PLAYER_A_DEAD):
    return PLAYER_B
  else:
    return -1
  
def win_message(code):
  message = "GAME OVER "
  if(code == "draw"):
    message += "draw"
  elif(code == PLAYER_B):
    message += "PLAYER_B wins"
  elif(code == PLAYER_A):
    message += "PLAYER_A wins"
  return message

#init_state = Bman_state(parse(test.MOVE_TEST_0), 0, PLAYER_A)
#print("INITIAL STATE:")
#print(init_state)
#print("SUCCESSORS:")
#print(states_to_string(look_for_successors(init_state)))