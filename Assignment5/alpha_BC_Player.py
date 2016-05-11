'''
Vikramjit Pandher, Chloe Nash, CSE 415, Spring 2016, University of Washington
Instructor:  S. Tanimoto.
Assignment 5 Baroque Chess

Status of the implementation:
All required features working. Works with sample puzzles.

Implementation of an Agent ___ that plays Baroque Chess.

The initial board state is represented as:
c l i w k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P P
F L I W K I L C

Where the starting board is shown using ASCII text, and the
encoding is as follows: (lower case for black, upper case for WHITE):

    p: pincer
    l: leaper
    i: imitator
    w: withdrawer
    k: king
    c: coordinator
    f: freezer
    -: empty square on the board

'''

#import baroque_succ as bcs
import random

BLACK = 0
WHITE = 1

INIT_TO_CODE = {'p':2, 'P':3, 'c':4, 'C':5, 'l':6, 'L':7, 'i':8, 'I':9,
  'w':10, 'W':11, 'k':12, 'K':13, 'f':14, 'F':15, '-':0}

CODE_TO_INIT = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}

CODE_TO_NAME = {0:'blank space', 2:'Black Pincer', 3:'White Pincer',
  4:'Black Coordinator', 5:'White Coordinator', 6:'Black Leaper', 7:'White Leaper',
  8:'Black Imitator', 9:'White Imitator', 10:'Black Withdrawer', 11:'White Withdrawer',
  12:'Black King', 13:'White King', 14:'Black Freezer', 15:'White Freezer'}

COL_TO_LETTER = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
  
def who(piece): return piece % 2

def parse(bs): # bs is board string
  '''Translate a board string into the list of lists representation.'''
  b = [[0,0,0,0,0,0,0,0] for r in range(8)]
  rs9 = bs.split("\n")
  rs8 = rs9[1:] # eliminate the empty first item.
  for iy in range(8):
    rss = rs8[iy].split(' ');
    for jx in range(8):
      b[iy][jx] = INIT_TO_CODE[rss[jx]]
  return b

INITIAL = parse('''
c l i w k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P P
F L I W K I L C
''')

	
class BC_state:
  def __init__(self, old_board=INITIAL, whose_move=WHITE):
    new_board = [r[:] for r in old_board]
    self.board = new_board
    self.whose_move = whose_move;

  def __repr__(self):
    s = ''
    for r in range(8):
      for c in range(8):
        s += CODE_TO_INIT[self.board[r][c]] + " "
      s += "\n"
    if self.whose_move==WHITE: s += "WHITE's move"
    else: s += "BLACK's move"
    s += "\n"
    return s

def test_starting_board():
  init_state = BC_state(INITIAL, WHITE)
  print(init_state)

def other(player):
  if player == WHITE:
    return BLACK
  else:
    return WHITE
  
  
# It should return a list of the form [[move, newState], newRemark].
# The move is a data item describing the chosen move.
# The newState is the result of making the move from the given currentState.
# The newRemark to be returned must be a string.
def makeMove(currentState, currentRemark, timelimit):
    successors = look_for_successors(currentState)
    
    if(len(successors) != 0):
      nextSuccessor = random.choice(successors)
    else:
      return [["can't move!", currentState], "Oh No!"]
    
    return [[nextSuccessor[0], BC_state(nextSuccessor[1], other(currentState.whose_move))], "Ah Ha!"]
    
def identifyPieces(currentState):
    our_pieces = []
    return

# This function should return a short version of the playing agent's name.
def nickname():
    return "Nobachess"

# This function will return a multiline string that introduces the player,
# giving its full name, the names and UWNetIDs of its creators.
def introduce():
    return "I'm Nobachess, I don't play baroque chess at this time."

def prepare(player2Nickname):
    pass

# This function will perform a static evaluation of the given state.
# The value returned should be high if the state is good for WHITE
# and low if the state is good for BLACK. 
def staticEval(state):
    output = random.randint(0,100)
    board = state[1]
    blackKing = False
    whiteKing = False
    
    for i in range(8): # look through row
      for j in range(8): # look through column
        current_piece = board[i][j]
        if (current_piece == 12):
          blackKing = True
        if (current_piece == 13):
          whiteKing = True
        
    if(blackKing == False):
      return 10000
    if(whiteKing == False):
      return -10000
    return output

    
    
    
def look_for_successors(state):
  board = state.board
  current_player = state.whose_move
  
  successors = []
  
  for i in range(8): # look through row
    for j in range(8): # look through column
      current_piece = board[i][j]
      if(who(current_piece) == current_player and current_piece != 0):
        #print("current_piece = " + CODE_TO_NAME[current_piece] + " (" + CODE_TO_INIT[current_piece] + "), (" + str(i) + ", " + str(j) + ")")
        #print()
        new_boards = analyze_piece(current_piece, i, j, board, current_player)
        #print(print_boards(new_boards)) # <<< FOR DEBUGGING
        #print()
        successors.extend(new_boards)
  return successors

def get_move_desc(piece, old_row, old_col, new_row, new_col):
  #print("get_move_desc(" + str(piece) + ", " + str(old_row) + ", " + str(old_col) + ", " + str(new_row) + ", " + str(new_col) + ")")
  if(new_col < 0):
    new_col = 0
  return CODE_TO_NAME[piece] + " from " +  COL_TO_LETTER[old_col] + str(8 - old_row) + " to " + COL_TO_LETTER[new_col] + str(8 - new_row)
  
def analyze_pincer_movement(piece, row, col, board, current_player):
  new_boards = []
  
  # checking horizontal movement to the 8th column
  k = 1
  while (col + k < 8):
    if(board[row][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col + k] = piece
      new_board[row][col] = 0
      apply_pincer_kill(piece, row, col + k, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row, col + k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking horizontal movement towards the 0th column
  k = 1
  while (col - k > -1):
    if(board[row][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col - k] = piece
      new_board[row][col] = 0
      apply_pincer_kill(piece, row, col - k, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row, col - k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking vertical movement towards the 8th row
  k = 1
  while (row + k < 8):
    if(board[row + k][col] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col] = piece
      new_board[row][col] = 0
      apply_pincer_kill(piece, row + k, col, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row + k, col)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking vertical movement towards the 0th row
  k = 1
  while (row - k > -1):
    if(board[row - k][col] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col] = piece
      new_board[row][col] = 0
      apply_pincer_kill(piece, row - k, col, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row - k, col)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  return new_boards
  
def apply_pincer_kill(piece, row, col, board, current_player):
  # squish towards 0th row
  if row > 1 and who(board[row-1][col]) != current_player and board[row-1][col] != 0 and who(board[row-2][col]) == current_player and board[row-2][col] != 0 :
    board[row-1][col] = 0
  # squish towards 8th row
  if row < 6 and who(board[row+1][col]) != current_player and board[row+1][col] != 0 and who(board[row+2][col]) == current_player and board[row+2][col] != 0 :
    board[row+1][col] = 0
  # squish towards 0th column
  if col > 1 and who(board[row][col-1]) != current_player and board[row][col-1] != 0 and who(board[row][col-2]) == current_player and board[row][col-2] != 0 :
    board[row][col-1] = 0
  # squish towards 8th column
  if col < 6 and who(board[row][col+1]) != current_player and board[row][col+1] != 0 and who(board[row][col+2]) == current_player and board[row][col+2] != 0 :
    board[row][col+1] = 0

def analyze_king_movement(piece, row, col, board, current_player):
  new_boards = []
  
  # checking horizontal movement toward the 8th column
  if(col < 7 and (who(board[row][col + 1]) != current_player or board[row][col + 1] == 0)):
    #add a state
    new_board = copy_board(board)
    new_board[row][col + 1] = piece
    new_board[row][col] = 0
    move_desc = get_move_desc(piece, row, col, row, col + 1)
    new_boards.append([move_desc, new_board])
    
  # checking horizontal movement toward the 0th column
  if(col > 0 and (who(board[row][col - 1]) != current_player or board[row][col - 1] == 0)):
    #add a state
    new_board = copy_board(board)
    new_board[row][col - 1] = piece
    new_board[row][col] = 0
    move_desc = get_move_desc(piece, row, col, row, col - 1)
    new_boards.append([move_desc, new_board])
    
  # checking vertical movement toward the 8th row
  if(row < 7 and (who(board[row + 1][col]) != current_player or board[row + 1][col] == 0)):
    #add a state
    new_board = copy_board(board)
    new_board[row + 1][col] = piece
    new_board[row][col] = 0
    move_desc = get_move_desc(piece, row, col, row + 1, col)
    new_boards.append([move_desc, new_board])
  
  # checking vertical movement toward the 0th row
  if(row > 0 and (who(board[row - 1][col]) != current_player or board[row - 1][col] == 0)):
    #add a state
    new_board = copy_board(board)
    new_board[row - 1][col] = piece
    new_board[row][col] = 0
    move_desc = get_move_desc(piece, row, col, row - 1, col)
    new_boards.append([move_desc, new_board])
  
  # checking diagonal movement towards the 8th column and 8th row
  if(col < 7 and row < 7 and (who(board[row + 1][col + 1]) != current_player or board[row + 1][col + 1] == 0)):
    #add a state
    new_board = copy_board(board)
    new_board[row + 1][col + 1] = piece
    new_board[row][col] = 0
    move_desc = get_move_desc(piece, row, col, row + 1, col + 1)
    new_boards.append([move_desc, new_board])
  
  # checking diagonal movement towards the 8th column and 0th row
  if(col < 7 and row > 0 and (who(board[row - 1][col + 1]) != current_player or board[row - 1][col + 1] == 0)):
    #add a state
    new_board = copy_board(board)
    new_board[row - 1][col + 1] = piece;
    new_board[row][col] = 0;
    move_desc = get_move_desc(piece, row, col, row - 1, col + 1)
    new_boards.append([move_desc, new_board])
  
  # checking diagonal movement towards the 0th column and 8th row
  if(col > 0 and row < 7 and (who(board[row + 1][col - 1]) != current_player or board[row + 1][col - 1] == 0)):
    #add a state
    new_board = copy_board(board)
    new_board[row + 1][col - 1] = piece
    new_board[row][col] = 0
    move_desc = get_move_desc(piece, row, col, row + 1, col - 1)
    new_boards.append([move_desc, new_board])
  
  # checking diagonal movement towards the 0th column and 0th row
  if(col > 0 and row > 0 and (who(board[row - 1][col - 1]) != current_player or board[row - 1][col - 1] == 0)):
    #add a state
    new_board = copy_board(board)
    new_board[row - 1][col - 1] = piece
    new_board[row][col] = 0
    move_desc = get_move_desc(piece, row, col, row - 1, col - 1)
    new_boards.append([move_desc, new_board])
  
  return new_boards

def analyze_withdrawer_movement(piece, row, col, board, current_player):
  new_boards = []
  
  # checking horizontal movement towards the 8th column
  k = 1
  while (col + k < 8):
    if(board[row][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col + k] = piece
      new_board[row][col] = 0
      # if moving away from enemy piece, kill it
      if (col > 0 and who(board[row][col - 1]) != current_player and board[row][col - 1] != 0):
        new_board[row][col - 1] = 0
      move_desc = get_move_desc(piece, row, col, row, col + k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking horizontal movement towards the 0th column
  k = 1
  while (col - k > -1):
    if(board[row][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col - k] = piece
      new_board[row][col] = 0
      # if moving away from enemy piece, kill it
      if (col < 7 and who(board[row][col + 1]) != current_player and board[row][col + 1] != 0):
        new_board[row][col + 1] = 0
      move_desc = get_move_desc(piece, row, col, row, col - k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1

  # checking vertical movement towards the 8th row
  k = 1
  while (row + k < 8):
    if(board[row + k][col] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col] = piece
      new_board[row][col] = 0
      # if moving away from enemy piece, kill it
      if (row > 0 and who(board[row - 1][col]) != current_player and board[row - 1][col] != 0):
        new_board[row - 1][col] = 0
      move_desc = get_move_desc(piece, row, col, row + k, col)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking vertical movement towards the 0th row
  k = 1
  while (row - k > -1):
    if(board[row - k][col] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col] = piece
      new_board[row][col] = 0
      # if moving away from enemy piece, kill it
      if (row < 7 and who(board[row + 1][col]) != current_player and board[row + 1][col] != 0):
        new_board[row + 1][col] = 0
      move_desc = get_move_desc(piece, row, col, row - k, col)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking diagonal movement towards the 8th column and 8th row
  k = 1
  while (k + row < 8 and k + col < 8):
    if(board[row + k][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col + k] = piece
      new_board[row][col] = 0
      # if moving away from enemy piece, kill it
      if (row > 0 and col > 0 and who(board[row - 1][col - 1]) != current_player and board[row - 1][col - 1] != 0):
        new_board[row - 1][col - 1] = 0
      move_desc = get_move_desc(piece, row, col, row + k, col + k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking diagonal movement towards the 8th column and 0th row
  k = 1
  while (row - k > -1 and col + k < 8):
    if(board[row - k][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col + k] = piece
      new_board[row][col] = 0
      # if moving away from enemy piece, kill it
      if (row < 7 and col > 0 and who(board[row + 1][col - 1]) != current_player and board[row + 1][col - 1] != 0):
        new_board[row + 1][col - 1] = 0
      move_desc = get_move_desc(piece, row, col, row - k, col + k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking diagonal movement towards the 0th column and 8th row
  k = 1
  while (k + row < 8 and col - k > -1):
    if(board[row + k][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col - k] = piece
      new_board[row][col] = 0
      # if moving away from enemy piece, kill it
      if (row > 0 and col < 7 and who(board[row - 1][col + 1]) != current_player and board[row - 1][col + 1] != 0):
        new_board[row - 1][col + 1] = 0
      move_desc = get_move_desc(piece, row, col, row + k, col - k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking diagonal movement towards the 0th column and 0th row
  k = 1
  while (row - k > -1 and col - k > -1):
    if(board[row - k][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col - k] = piece
      new_board[row][col] = 0
      # if moving away from enemy piece, kill it
      if (row < 7 and col < 7 and who(board[row + 1][col + 1]) != current_player and board[row + 1][col + 1] != 0):
        new_board[row + 1][col + 1] = 0
      move_desc = get_move_desc(piece, row, col, row - k, col - k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  return new_boards

def analyze_leaper_movement(piece, row, col, board, current_player):
  new_boards = []
  
  # checking horizontal movement towards the 8th column
  k = 1
  while (col + k < 8):
    if(board[row][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col + k] = piece
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row, col + k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (col + k < 7 and board[row][col + k + 1] == 0):
    # the piece to jump is the oponent's
    if (who(board[row][col + k]) != current_player and board[row][col + k] != 0):
      new_board = copy_board(board)
      new_board[row][col + k + 1] = piece
      new_board[row][col + k] = 0
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row, col + k + 1)
      new_boards.append([move_desc, new_board])
  
  # checking horizontal movement towards the 0th column
  k = 1
  while (col - k > -1):
    if(board[row][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col - k] = piece
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row, col - k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (col + k > 0 and board[row][col - k - 1] == 0):
    # the piece to jump is the oponent's
    if (who(board[row][col - k]) != current_player and board[row][col - k] != 0):
      new_board = copy_board(board)
      new_board[row][col - k - 1] = piece
      new_board[row][col - k] = 0
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row, col - k - 1)
      new_boards.append([move_desc, new_board])

  # checking vertical movement towards the 8th row
  k = 1
  while (row + k < 8):
    if(board[row + k][col] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col] = piece
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row + k, col)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row + k < 7 and board[row + k + 1][col] == 0):
    # the piece to jump is the oponent's
    if (who(board[row + k][col]) != current_player and board[row + k][col] != 0):
      new_board = copy_board(board)
      new_board[row + k + 1][col] = piece
      new_board[row + k][col] = 0
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row + k + 1, col)
      new_boards.append([move_desc, new_board])
  
  # checking vertical movement towards the 0th row
  k = 1
  while (row - k > -1):
    if(board[row - k][col] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col] = piece
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row - k, col)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row - k > 0 and board[row - k - 1][col] == 0):
    # the piece to jump is the oponent's
    if (who(board[row - k][col]) != current_player and board[row - k][col] != 0):
      new_board = copy_board(board)
      new_board[row - k - 1][col] = piece
      new_board[row - k][col] = 0
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row - k - 1, col)
      new_boards.append([move_desc, new_board])
  
  # checking diagonal movement towards the 8th column and 8th row
  k = 1
  while (k + row < 8 and k + col < 8):
    if(board[row + k][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col + k] = piece;
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row + k, col + k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row + k < 7 and col + k < 7 and board[row + k + 1][col + k + 1] == 0):
    # the piece to jump is the oponent's
    if (who(board[row + k][col + k]) != current_player and board[row + k][col + k] != 0):
      new_board = copy_board(board)
      new_board[row + k + 1][col + k + 1] = piece
      new_board[row + k][col + k] = 0
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row + k + 1, col + k + 1)
      new_boards.append([move_desc, new_board])
  
  # checking diagonal movement towards the 8th column and 0th row
  k = 1
  while (row - k > -1 and col + k < 8):
    if(board[row - k][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col + k] = piece;
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row - k, col + k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row - k > 0 and col + k < 7 and board[row - k - 1][col + k + 1] == 0):
    # the piece to jump is the oponent's
    if (who(board[row - k][col + k]) != current_player and board[row - k][col + k] != 0):
      new_board = copy_board(board)
      new_board[row - k - 1][col + k + 1] = piece
      new_board[row - k][col + k] = 0
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row - k - 1, col + k + 1)
      new_boards.append([move_desc, new_board])
  
  # checking diagonal movement towards the 0th column and 8th row
  k = 1
  while (k + row < 8 and col - k > -1):
    if(board[row + k][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col - k] = piece;
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row + k, col - k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row + k < 7 and col - k > 0 and board[row + k + 1][col - k - 1] == 0):
    # the piece to jump is the oponent's
    if (who(board[row + k][col - k]) != current_player and board[row + k][col - k] != 0):
      new_board = copy_board(board)
      new_board[row + k + 1][col - k - 1] = piece
      new_board[row + k][col - k] = 0
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row + k + 1, col - k - 1)
      new_boards.append([move_desc, new_board])
  
  # checking diagonal movement towards the 0th column and 0th row
  k = 1
  while (row - k > -1 and col - k > -1):
    if(board[row - k][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col - k] = piece;
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row - k, col - k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row - k > 0 and col - k > 0 and board[row - k - 1][col - k - 1] == 0):
    # the piece to jump is the oponent's
    if (who(board[row - k][col - k]) != current_player and board[row - k][col - k] != 0):
      new_board = copy_board(board)
      new_board[row - k - 1][col - k - 1] = piece
      new_board[row - k][col - k] = 0
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row - k - 1, col - k - 1)
      new_boards.append([move_desc, new_board])
  
  return new_boards

def analyze_coordinator_movement(piece, row, col, board, current_player):
  new_boards = []
  
  # checking horizontal movement towards the 8th column
  k = 1
  while (col + k < 8):
    if(board[row][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col + k] = piece
      new_board[row][col] = 0
      apply_coordinator_kill(piece, row, col + k, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row, col + k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking horizontal movement towards the 0th column
  k = 1
  while (col - k > -1):
    if(board[row][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col - k] = piece
      new_board[row][col] = 0
      apply_coordinator_kill(piece, row, col - k, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row, col - k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1

  # checking vertical movement towards the 8th row
  k = 1
  while (row + k < 8):
    if(board[row + k][col] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col] = piece
      new_board[row][col] = 0
      apply_coordinator_kill(piece, row + k, col, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row + k, col)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking vertical movement towards the 0th row
  k = 1
  while (row - k > -1):
    if(board[row - k][col] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col] = piece
      new_board[row][col] = 0
      apply_coordinator_kill(piece, row - k, col, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row - k, col)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking diagonal movement towards the 8th column and 8th row
  k = 1
  while (k + row < 8 and k + col < 8):
    if(board[row + k][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col + k] = piece;
      new_board[row][col] = 0
      apply_coordinator_kill(piece, row + k, col + k, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row + k, col + k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking diagonal movement towards the 8th column and 0th row
  k = 1
  while (row - k > -1 and col + k < 8):
    if(board[row - k][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col + k] = piece;
      new_board[row][col] = 0
      apply_coordinator_kill(piece, row - k, col + k, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row - k, col + k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking diagonal movement towards the 0th column and 8th row
  k = 1
  while (k + row < 8 and col - k > -1):
    if(board[row + k][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col - k] = piece;
      new_board[row][col] = 0
      apply_coordinator_kill(piece, row + k, col - k, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row + k, col - k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking diagonal movement towards the 0th column and 0th row
  k = 1
  while (row - k > -1 and col - k > -1):
    if(board[row - k][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col - k] = piece;
      new_board[row][col] = 0
      apply_coordinator_kill(piece, row - k, col - k, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row - k, col - k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  return new_boards

def apply_coordinator_kill(piece, row, col, board, current_player):
  # locate your king
  for i in range(8): # look through row
    for j in range(8): # look through column
      current_piece = board[i][j]
      # kill corners
      if (current_piece == 12 + current_player):
        if (who(board[row][j]) != current_player and board[row][j] != 0):
          board[row][j] = 0
        if (who(board[i][col]) != current_player and board[i][col] != 0):
          board[i][col] = 0
        # kill enemies in the same row
        if i == row :
          # kill towards the 0th row
          if col > j :
            k = j
            while col > k :
              if (who(board[i][k]) != current_player and board[i][k] != 0) :
                  board[i][k] = 0
              k = k + 1
          # kill towards the 8th row
          if col < j :
            k = j
            while col < k :
              if (who(board[i][k]) != current_player and board[i][k] != 0) :
                  board[i][k] = 0
              k = k - 1
        # kill enemies on the same collumn
        if j == col :
          # kill towards the 0th collumn
          if row > i :
            k = i
            while row > k :
              if (who(board[k][j]) != current_player and board[k][j] != 0) :
                  board[k][j] = 0
              k = k + 1
          # kill towards the 8th collumn
          if row < i :
            k = i
            while row < k :
              if (who(board[k][j]) != current_player and board[k][j] != 0) :
                  board[k][j] = 0
              k = k - 1
        return

def analyze_freezer_movement(piece, row, col, board, current_player):
  new_boards = []
  
  # checking horizontal movement towards the 8th column
  k = 1
  while (col + k < 8):
    if(board[row][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col + k] = piece
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row, col + k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking horizontal movement towards the 0th column
  k = 1
  while (col - k > -1):
    if(board[row][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col - k] = piece
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row, col - k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1

  # checking vertical movement towards the 8th row
  k = 1
  while (row + k < 8):
    if(board[row + k][col] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col] = piece
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row + k, col)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking vertical movement towards the 0th row
  k = 1
  while (row - k > -1):
    if(board[row - k][col] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col] = piece
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row - k, col)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking diagonal movement towards the 8th column and 8th row
  k = 1
  while (k + row < 8 and k + col < 8):
    if(board[row + k][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col + k] = piece;
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row + k, col + k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking diagonal movement towards the 8th column and 0th row
  k = 1
  while (row - k > -1 and col + k < 8):
    if(board[row - k][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col + k] = piece;
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row - k, col + k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking diagonal movement towards the 0th column and 8th row
  k = 1
  while (k + row < 8 and col - k > -1):
    if(board[row + k][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col - k] = piece;
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row + k, col - k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  
  # checking diagonal movement towards the 0th column and 0th row
  k = 1
  while (row - k > -1 and col - k > -1):
    if(board[row - k][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col - k] = piece;
      new_board[row][col] = 0
      move_desc = get_move_desc(piece, row, col, row - k, col - k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1

  return new_boards

def analyze_imitator_movement(piece, row, col, board, current_player):
  new_boards = []
  
  # checking horizontal movement towards the 8th column
  k = 1
  while (col + k < 8):
    if(board[row][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col + k] = piece
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (col > 0 and board[row][col - 1] == 11 - current_player):
        new_board[row][col - 1] = 0
      apply_imitator_coordinator_kill(piece, row, col + k, new_board, current_player)
      apply_imitator_pincer_kill(piece, row, col + k, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row, col + k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (col + k < 7 and board[row][col + k + 1] == 0):
    # the piece to jump is the oponent's leaper
    if (board[row][col + k] == 7 - current_player):
      new_board = copy_board(board)
      new_board[row][col + k + 1] = piece
      new_board[row][col + k] = 0
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (col > 0 and board[row][col - 1] == 11 - current_player):
        new_board[row][col - 1] = 0
      apply_imitator_coordinator_kill(piece, row, col + k + 1, new_board, current_player)
      apply_imitator_pincer_kill(piece, row, col + k + 1, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row, col + k + 1)
      new_boards.append([move_desc, new_board])
  # checking if next to an enemy king
  if(col < 7 and board[row][col + 1] == 13 - current_player):
    #add a state
    new_board = copy_board(board)
    new_board[row][col + 1] = piece
    new_board[row][col] = 0
    # if moving away from enemy withdrawer, kill it
    if (col > 0 and board[row][col - 1] == 11 - current_player):
      new_board[row][col - 1] = 0
    apply_imitator_coordinator_kill(piece, row, col + 1, new_board, current_player)
    apply_imitator_pincer_kill(piece, row, col + 1, new_board, current_player)
    move_desc = get_move_desc(piece, row, col, row, col + 1)
    new_boards.append([move_desc, new_board])
  
  # checking horizontal movement towards the 0th column
  k = 1
  while (col - k > -1):
    if(board[row][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col - k] = piece
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (col < 7 and board[row][col + 1] == 11 - current_player):
        new_board[row][col + 1] = 0
      apply_imitator_coordinator_kill(piece, row, col - k, new_board, current_player)
      apply_imitator_pincer_kill(piece, row, col - k, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row, col - k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (col + k > 0 and board[row][col - k - 1] == 0):
    # the piece to jump is the oponent's leaper
    if (board[row][col - k] == 7 - current_player):
      new_board = copy_board(board)
      new_board[row][col - k - 1] = piece
      new_board[row][col - k] = 0
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (col < 7 and board[row][col + 1] == 11 - current_player):
        new_board[row][col + 1] = 0
      apply_imitator_coordinator_kill(piece, row, col - k - 1, new_board, current_player)
      apply_imitator_pincer_kill(piece, row, col - k - 1, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row, col - k - 1)
      new_boards.append([move_desc, new_board])
  # checking if next to an enemy king
  if(col > 0 and board[row][col - 1] == 13 - current_player):
    #add a state
    new_board = copy_board(board)
    new_board[row][col - 1] = piece
    new_board[row][col] = 0
    # if moving away from enemy withdrawer, kill it
    if (col < 7 and board[row][col + 1] == 11 - current_player):
      new_board[row][col + 1] = 0
    apply_imitator_coordinator_kill(piece, row, col - 1, new_board, current_player)
    apply_imitator_pincer_kill(piece, row, col - 1, new_board, current_player)
    move_desc = get_move_desc(piece, row, col, row, col - 1)
    new_boards.append([move_desc, new_board])

  # checking vertical movement towards the 8th row
  k = 1
  while (row + k < 8):
    if(board[row + k][col] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col] = piece
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row > 0 and board[row - 1][col] == 11 - current_player):
        new_board[row - 1][col] = 0
      apply_imitator_coordinator_kill(piece, row + k, col, new_board, current_player)
      apply_imitator_pincer_kill(piece, row + k, col, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row + k, col)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row + k < 7 and board[row + k + 1][col] == 0):
    # the piece to jump is the oponent's leaper
    if (board[row + k][col] == 7 - current_player):
      new_board = copy_board(board)
      new_board[row + k + 1][col] = piece
      new_board[row + k][col] = 0
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row > 0 and board[row - 1][col] == 11 - current_player):
        new_board[row - 1][col] = 0
      apply_imitator_coordinator_kill(piece, row + k + 1, col, new_board, current_player)
      apply_imitator_pincer_kill(piece, row + k + 1, col, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row + k + 1, col)
      new_boards.append([move_desc, new_board])
  # checking if next to an enemy king
  if(row < 7 and board[row + 1][col] == 13 - current_player):
    #add a state
    new_board = copy_board(board)
    new_board[row + 1][col] = piece
    new_board[row][col] = 0
    # if moving away from enemy withdrawer, kill it
    if (row > 0 and board[row - 1][col] == 11 - current_player):
      new_board[row - 1][col] = 0
    apply_imitator_coordinator_kill(piece, row + 1, col, new_board, current_player)
    apply_imitator_pincer_kill(piece, row + 1, col, new_board, current_player)
    move_desc = get_move_desc(piece, row, col, row + 1, col)
    new_boards.append([move_desc, new_board])
  
  # checking vertical movement towards the 0th row
  k = 1
  while (row - k > -1):
    if(board[row - k][col] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col] = piece
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row < 7 and board[row + 1][col] == 11 - current_player):
        new_board[row + 1][col] = 0
      apply_imitator_coordinator_kill(piece, row - k, col, new_board, current_player)
      apply_imitator_pincer_kill(piece, row - k, col, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row - k, col)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row - k > 0 and board[row - k - 1][col] == 0):
    # the piece to jump is the oponent's
    if (board[row - k][col] == 7 - current_player):
      new_board = copy_board(board)
      new_board[row - k - 1][col] = piece
      new_board[row - k][col] = 0
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row < 7 and board[row + 1][col] == 11 - current_player):
        new_board[row + 1][col] = 0
      apply_imitator_coordinator_kill(piece, row - k - 1, col, new_board, current_player)
      apply_imitator_pincer_kill(piece, row - k - 1, col, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row - k - 1, col)
      new_boards.append([move_desc, new_board])
  # checking if next to an enemy king
  if(row > 0 and board[row - 1][col] == 13 - current_player):
    #add a state
    new_board = copy_board(board)
    new_board[row - 1][col] = piece
    new_board[row][col] = 0
    # if moving away from enemy withdrawer, kill it
    if (row < 7 and board[row + 1][col] == 11 - current_player):
      new_board[row + 1][col] = 0
    apply_imitator_coordinator_kill(piece, row - 1, col, new_board, current_player)
    apply_imitator_pincer_kill(piece, row - 1, col, new_board, current_player)
    move_desc = get_move_desc(piece, row, col, row - 1, col)
    new_boards.append([move_desc, new_board])
  
  # checking diagonal movement towards the 8th column and 8th row
  k = 1
  while (k + row < 8 and k + col < 8):
    if(board[row + k][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col + k] = piece;
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row > 0 and col > 0 and board[row - 1][col - 1] == 11 - current_player):
        new_board[row - 1][col - 1] = 0
      apply_imitator_coordinator_kill(piece, row + k, col + k, new_board, current_player)
      apply_imitator_pincer_kill(piece, row + k, col + k, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row + k, col + k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row + k < 7 and col + k < 7 and board[row + k + 1][col + k + 1] == 0):
    # the piece to jump is the oponent's
    if (board[row + k][col + k] == 7 - current_player):
      new_board = copy_board(board)
      new_board[row + k + 1][col + k + 1] = piece
      new_board[row + k][col + k] = 0
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row > 0 and col > 0 and board[row - 1][col - 1] == 11 - current_player):
        new_board[row - 1][col - 1] = 0
      apply_imitator_coordinator_kill(piece, row + k + 1, col + k + 1, new_board, current_player)
      apply_imitator_pincer_kill(piece, row + k + 1, col + k + 1, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row + k + 1, col + k + 1)
      new_boards.append([move_desc, new_board])
  # checking if next to an enemy king
  if(row < 7 and col < 7 and board[row + 1][col + 1] == 13 - current_player):
    #add a state
    new_board = copy_board(board)
    new_board[row + 1][col + 1] = piece
    new_board[row][col] = 0
    # if moving away from enemy withdrawer, kill it
    if (row > 0 and col > 0 and board[row - 1][col - 1] == 11 - current_player):
      new_board[row - 1][col - 1] = 0
    apply_imitator_coordinator_kill(piece, row + 1, col + 1, new_board, current_player)
    apply_imitator_pincer_kill(piece, row + 1, col + 1, new_board, current_player)
    move_desc = get_move_desc(piece, row, col, row + 1, col + 1)
    new_boards.append([move_desc, new_board])
  
  # checking diagonal movement towards the 8th column and 0th row
  k = 1
  while (row - k > -1 and col + k < 8):
    if(board[row - k][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col + k] = piece;
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row < 7 and col > 0 and board[row + 1][col - 1] == 11 - current_player):
        new_board[row + 1][col - 1] = 0
      apply_imitator_coordinator_kill(piece, row - k, col + k, new_board, current_player)
      apply_imitator_pincer_kill(piece, row - k, col + k, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row - k, col + k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row - k > 0 and col + k < 7 and board[row - k - 1][col + k + 1] == 0):
    # the piece to jump is the oponent's
    if (board[row - k][col + k] == 7 - current_player):
      new_board = copy_board(board)
      new_board[row - k - 1][col + k + 1] = piece
      new_board[row - k][col + k] = 0
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row < 7 and col > 0 and board[row + 1][col - 1] == 11 - current_player):
        new_board[row + 1][col - 1] = 0
      apply_imitator_coordinator_kill(piece, row - k - 1, col + k + 1, new_board, current_player)
      apply_imitator_pincer_kill(piece, row - k - 1, col + k + 1, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row - k - 1, col + k + 1)
      new_boards.append([move_desc, new_board])
  # checking if next to an enemy king
  if(row > 0 and col < 7 and board[row - 1][col + 1] == 13 - current_player):
    #add a state
    new_board = copy_board(board)
    new_board[row - 1][col + 1] = piece
    new_board[row][col] = 0
    # if moving away from enemy withdrawer, kill it
    if (row < 7 and col > 0 and board[row + 1][col - 1] == 11 - current_player):
      new_board[row + 1][col - 1] = 0
    apply_imitator_coordinator_kill(piece, row - 1, col + 1, new_board, current_player)
    apply_imitator_pincer_kill(piece, row - 1, col + 1, new_board, current_player)
    move_desc = get_move_desc(piece, row, col, row - 1, col + 1)
    new_boards.append([move_desc, new_board])
  
  # checking diagonal movement towards the 0th column and 8th row
  k = 1
  while (k + row < 8 and col - k > -1):
    if(board[row + k][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col - k] = piece;
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row > 0 and col < 7 and board[row - 1][col + 1] == 11 - current_player):
        new_board[row - 1][col + 1] = 0
      apply_imitator_coordinator_kill(piece, row + k, col - k, new_board, current_player)
      apply_imitator_pincer_kill(piece, row + k, col - k, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row + k, col - k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row + k < 7 and col - k > 0 and board[row + k + 1][col - k - 1] == 0):
    # the piece to jump is the oponent's
    if (board[row + k][col - k] == 7 - current_player):
      new_board = copy_board(board)
      new_board[row + k + 1][col - k - 1] = piece
      new_board[row + k][col - k] = 0
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row > 0 and col < 7 and board[row - 1][col + 1] == 11 - current_player):
        new_board[row - 1][col + 1] = 0
      apply_imitator_coordinator_kill(piece, row + k + 1, col - k - 1, new_board, current_player)
      apply_imitator_pincer_kill(piece, row + k + 1, col - k - 1, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row + k + 1, col - k - 1)
      new_boards.append([move_desc, new_board])
  # checking if next to an enemy king
  if(row > 7 and col > 0 and board[row + 1][col - 1] == 13 - current_player):
    #add a state
    new_board = copy_board(board)
    new_board[row + 1][col - 1] = piece
    new_board[row][col] = 0
    # if moving away from enemy withdrawer, kill it
    if (row > 0 and col < 7 and board[row - 1][col + 1] == 11 - current_player):
      new_board[row - 1][col + 1] = 0
    apply_imitator_coordinator_kill(piece, row + 1, col - 1, new_board, current_player)
    apply_imitator_pincer_kill(piece, row + 1, col - 1, new_board, current_player)
    move_desc = get_move_desc(piece, row, col, row + 1, col - 1)
    new_boards.append([move_desc, new_board])
   
  # checking diagonal movement towards the 0th column and 0th row
  k = 1
  while (row - k > -1 and col - k > -1):
    if(board[row - k][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col - k] = piece;
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row < 7 and col < 7 and board[row + 1][col + 1] == 11 - current_player):
        new_board[row + 1][col + 1] = 0
      apply_imitator_coordinator_kill(piece, row - k, col - k, new_board, current_player)
      apply_imitator_pincer_kill(piece, row - k, col - k, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row - k, col - k)
      new_boards.append([move_desc, new_board])
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row - k > 0 and col - k > 0 and board[row - k + 1][col - k - 1] == 0):
    # the piece to jump is the oponent's
    if (board[row - k][col - k] == 7 - current_player):
      new_board = copy_board(board)
      new_board[row - k - 1][col - k - 1] = piece
      new_board[row - k][col - k] = 0
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row < 7 and col < 7 and board[row + 1][col + 1] == 11 - current_player):
        new_board[row + 1][col + 1] = 0
      apply_imitator_coordinator_kill(piece, row - k - 1, col - k - 1, new_board, current_player)
      apply_imitator_pincer_kill(piece, row - k - 1, col - k - 1, new_board, current_player)
      move_desc = get_move_desc(piece, row, col, row - k - 1, col - k - 1)
      new_boards.append([move_desc, new_board])
  # checking if next to an enemy king
  if(row > 0 and col > 0 and board[row - 1][col - 1] == 13 - current_player):
    #add a state
    new_board = copy_board(board)
    new_board[row - 1][col - 1] = piece
    new_board[row][col] = 0
    # if moving away from enemy withdrawer, kill it
    if (row < 7 and col < 7 and board[row + 1][col + 1] == 11 - current_player):
      new_board[row + 1][col + 1] = 0
    apply_imitator_coordinator_kill(piece, row - 1, col - 1, new_board, current_player)
    apply_imitator_pincer_kill(piece, row - 1, col - 1, new_board, current_player)
    move_desc = get_move_desc(piece, row, col, row - 1, col - 1)
    new_boards.append([move_desc, new_board])
  
  return new_boards

def apply_imitator_pincer_kill(piece, row, col, board, current_player):
  # squish towards 0th row
  if row > 1 and board[row-1][col] == 3 - current_player and who(board[row-2][col]) == current_player and board[row-2][col] != 0 :
    board[row-1][col] = 0
  # squish towards 8th row
  if row < 6 and board[row+1][col] == 3 - current_player and who(board[row+2][col]) == current_player and board[row+2][col] != 0 :
    board[row+1][col] = 0
  # squish towards 0th column
  if col > 1 and board[row][col-1] == 3 - current_player and who(board[row][col-2]) == current_player and board[row][col-2] != 0 :
    board[row][col-1] = 0
  # squish towards 8th column
  if col < 6 and board[row][col+1] == 3 - current_player and who(board[row][col+2]) == current_player and board[row][col+2] != 0 :
    board[row][col+1] = 0

def apply_imitator_coordinator_kill(piece, row, col, board, current_player):
  # locate your king
  for i in range(8): # look through row
    for j in range(8): # look through column
      current_piece = board[i][j]
      # kill corners
      if (current_piece == 12 + current_player):
        if (board[row][j] == 5 - current_player):
          board[row][j] = 0
        if (board[i][col] == 5 - current_player):
          board[i][col] = 0
        return

def is_adjacent_too(piece, row, col, board, other, current_player):
  if(row > 0 and board[row - 1][col] == other - current_player):
    return True
  if(row < 7 and board[row + 1][col] == other - current_player):
    return True
  if(col > 0 and board[row][col - 1] == other - current_player):
    return True
  if(col < 7 and board[row][col + 1] == other - current_player):
    return True
  if(row > 0 and col > 0 and board[row - 1][col - 1] == other - current_player):
    return True
  if(row > 0 and col < 7 and board[row - 1][col + 1] == other - current_player):
    return True
  if(row < 7 and col > 0 and board[row + 1][col - 1] == other - current_player):
    return True
  if(row < 7 and col < 7 and board[row + 1][col + 1] == other - current_player):
    return True
  return False

def analyze_piece(piece, row, col, board, current_player):
  new_boards = []
  
  # check to see if this piece is frozen
  if is_adjacent_too(piece, row, col, board, 15, current_player):
    return new_boards
  
  # Pincer
  if(piece == 2 or piece == 3):
    new_boards.extend(analyze_pincer_movement(piece, row, col, board, current_player))
  
  # King
  if(piece == 12 or piece == 13):
    new_boards.extend(analyze_king_movement(piece, row, col, board, current_player))
  
  # Withdrawer
  if(piece == 10 or piece == 11):
    new_boards.extend(analyze_withdrawer_movement(piece, row, col, board, current_player))
  
  # Leaper
  if(piece == 6 or piece == 7):
    new_boards.extend(analyze_leaper_movement(piece, row, col, board, current_player))
  
  # Coordinator
  if(piece == 4 or piece == 5):
    new_boards.extend(analyze_coordinator_movement(piece, row, col, board, current_player))
  
  # Freezer
  if(piece == 14 or piece == 15):
    # freezer can be frozen by an imitator, check for that
    if is_adjacent_too(piece, row, col, board, 9, current_player):
      return new_boards
    new_boards.extend(analyze_freezer_movement(piece, row, col, board, current_player))
  
  # Imitator
  if(piece == 8 or piece == 9):
    new_boards.extend(analyze_imitator_movement(piece, row, col, board, current_player))
  
  return new_boards 
  
def print_boards(boards):
  s = ''
  for b in boards:
    s += b[0] + "\n"
    s += print_board(b[1])
  return s

# Wont work
def print_board(board):
  s = ''
  for r in range(8):
    for c in range(8):
      s += CODE_TO_INIT[board[r][c]] + " "
    s += "\n"
  s += "\n"
  return s
  
def copy_board(old_board):
  new_board = [[0,0,0,0,0,0,0,0] for r in range(8)]
  for i in range(8):
    for j in range(8):
      new_board[i][j] = old_board[i][j]
  return new_board


