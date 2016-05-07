BLACK = 0
WHITE = 1

INIT_TO_CODE = {'p':2, 'P':3, 'c':4, 'C':5, 'l':6, 'L':7, 'i':8, 'I':9,
  'w':10, 'W':11, 'k':12, 'K':13, 'f':14, 'F':15, '-':0}

CODE_TO_INIT = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}
  
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

PINCER_TEST_0 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - P - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

PINCER_TEST_1 = parse('''
- - - K - - - -
- - - i - - - -
- - - - - - - -
I p - P - i I -
- - - - - - - -
- - - p - - - -
- - I P I - - -
- - - I - - - -
''')

PINCER_TEST_2 = parse('''
- - - i - - - -
- - - i - - - -
- - - - - - - -
- p - P - i i -
- - - - - - - -
- I p - p I - -
- - - p - - - -
- - - I - - - -
''')

KING_TEST_0 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - K - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

KING_TEST_1 = parse('''
- - - - - - - -
- - - - - - - -
- - I I I - - -
- - I K I - - -
- - I I I - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

KING_TEST_2 = parse('''
- - - - - - - -
- - - - - - - -
- - i i i - - -
- - i K i - - -
- - i i i - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

WITHDRAWER_TEST_0 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - W - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

WITHDRAWER_TEST_1 = parse('''
- - - - - - - i
- i - i - - - -
- - - - - - - -
- - - W - i - -
- - - - - - - -
- i - - - i - -
- - - - - - - -
- - - i - - - -
''')

WITHDRAWER_TEST_2 = parse('''
- - - - - - - -
- - - - - - - -
- - i i i - - -
- - i W - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

WITHDRAWER_TEST_3 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - W p - - -
- - p p p - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

LEAPER_TEST_0 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - L - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

LEAPER_TEST_1 = parse('''
- - - - - - - -
- i - i - i - -
- - - - - - - -
- i - L - - i -
- - - - - - - -
- i - - - i - -
- - - i - - - -
- - - - - - - -
''')

LEAPER_TEST_2 = parse('''
- - - - - - - -
- I - I - I - -
- - - - - - - -
- I - L - - I -
- - - - - - - -
- I - - - I - -
- - - I - - - -
- - - - - - - -
''')

COORDINATOR_TEST_0 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - C - - - -
p - - K - p - -
- - - - - - - -
- - - p - - - -
- - - - - - - -
''')

FREEZER_TEST_0 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - F - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

FREEZER_TEST_1 = parse('''
- - - - - - - -
- K - - - - - -
- - - - - - - -
- - - P P P - -
- - - P f P - -
- - - P P K - -
- - - - - - - -
- - - - - - - -
''')

IMITATOR_TEST_0 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - I - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

IMITATOR_TEST_1 = parse('''
- - - - - - - -
- - - i - - - -
- i - - - i - -
- - - - - - - -
- i - I - - i -
- - i - - - - -
- - - i - i - -
- - - - - - - -
''')

IMITATOR_TEST_2 = parse('''
- - - - - - - -
- - - l - - - -
- l - - - l - -
- - - - - - - -
- l - I - - l -
- - l - - - - -
- - - l - l - -
- - - - - - - -
''')

IMITATOR_TEST_3 = parse('''
- - - - - - - -
- - - P - - - -
- - - p - - - -
- P p - - - - -
P p - I - p P -
- - - - - - - -
- - - p - - - -
- - - P - - - -
''')

IMITATOR_TEST_4 = parse('''
- - - - - - - -
- - - - - - - -
- - - - P - - -
- - - - p - - -
w I - l - p P -
- - - - p - - -
- - - - P - - -
K - - - c - - -
''')

IMITATOR_TEST_5 = parse('''
- - - - - - - -
- - - - - - - -
- - w w w - - -
- - w I - l - -
- - - - - - - -
- l - l - - - -
- - - - - - l -
- - - - - - - -
''')



class BC_state:
  def __init__(self, old_board=INITIAL, whose_move=WHITE):
    new_board = [r[:] for r in old_board]
    self.board = new_board
    self.whose_move = whose_move

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

CURRENT_PLAYER = WHITE;

def look_for_successors(state):
  board = state.board
  CURRENT_PLAYER = state.whose_move
  
  successors = []
  
  for i in range(8): # look through row
    for j in range(8): # look through column
      current_piece = board[i][j]
      if(who(current_piece) == CURRENT_PLAYER):
        print("current_piece = " + str(CODE_TO_INIT[current_piece]) + ", (" + str(i) + ", " + str(j) + ")")
        analyze_piece(current_piece, i, j, board)
        print()

def analyze_pincer_movement(piece, row, col, board):
  new_boards = []
  
  # checking horizontal movement to the 8th column
  k = 1
  while (col + k < 8):
    if(board[row][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col + k] = piece
      new_board[row][col] = 0
      apply_pincer_kill(piece, row, col + k, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      apply_pincer_kill(piece, row, col - k, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      apply_pincer_kill(piece, row + k, col, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      apply_pincer_kill(piece, row - k, col, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  
  print("return new_boards")
  return new_boards
  
def apply_pincer_kill(piece, row, col, board):
  # squish towards 0th row
  if row > 1 and who(board[row-1][col]) != CURRENT_PLAYER and board[row-1][col] != 0 and who(board[row-2][col]) == CURRENT_PLAYER :
    board[row-1][col] = 0
  # squish towards 8th row
  if row < 6 and who(board[row+1][col]) != CURRENT_PLAYER and board[row+1][col] != 0 and who(board[row+2][col]) == CURRENT_PLAYER :
    board[row+1][col] = 0
  # squish towards 0th column
  if col > 1 and who(board[row][col-1]) != CURRENT_PLAYER and board[row][col-1] != 0 and who(board[row][col-2]) == CURRENT_PLAYER :
    board[row][col-1] = 0
  # squish towards 8th column
  if col < 6 and who(board[row][col+1]) != CURRENT_PLAYER and board[row][col+1] != 0 and who(board[row][col+2]) == CURRENT_PLAYER :
    board[row][col+1] = 0

def analyze_king_movement(piece, row, col, board):
  new_boards = []
  
  # checking horizontal movement toward the 8th column
  if(col < 7 and who(board[row][col + 1]) != CURRENT_PLAYER):
    #add a state
    new_board = copy_board(board)
    new_board[row][col + 1] = piece
    new_board[row][col] = 0
    new_boards.append(new_board)
    print(print_board(new_board)) # <<< FOR DEBUGGING
    
  # checking horizontal movement toward the 0th column
  if(col > 0 and who(board[row][col - 1]) != CURRENT_PLAYER):
    #add a state
    new_board = copy_board(board)
    new_board[row][col - 1] = piece
    new_board[row][col] = 0
    new_boards.append(new_board)
    print(print_board(new_board)) # <<< FOR DEBUGGING
    
  # checking vertical movement toward the 8th row
  if(row < 7 and who(board[row + 1][col]) != CURRENT_PLAYER):
    #add a state
    new_board = copy_board(board)
    new_board[row + 1][col] = piece
    new_board[row][col] = 0
    new_boards.append(new_board)
    print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking vertical movement toward the 0th row
  if(row > 0 and who(board[row - 1][col]) != CURRENT_PLAYER):
    #add a state
    new_board = copy_board(board)
    new_board[row - 1][col] = piece
    new_board[row][col] = 0
    new_boards.append(new_board)
    print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking diagonal movement towards the 8th column and 8th row
  if(col < 7 and row < 7 and who(board[row + 1][col + 1]) != CURRENT_PLAYER):
    #add a state
    new_board = copy_board(board)
    new_board[row + 1][col + 1] = piece
    new_board[row][col] = 0
    new_boards.append(new_board)
    print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking diagonal movement towards the 8th column and 0th row
  if(col < 7 and row > 0 and who(board[row - 1][col + 1]) != CURRENT_PLAYER):
    #add a state
    new_board = copy_board(board)
    new_board[row - 1][col + 1] = piece;
    new_board[row][col] = 0;
    new_boards.append(new_board)
    print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking diagonal movement towards the 0th column and 8th row
  if(col > 0 and row < 7 and who(board[row + 1][col - 1]) != CURRENT_PLAYER):
    #add a state
    new_board = copy_board(board)
    new_board[row + 1][col - 1] = piece
    new_board[row][col] = 0
    new_boards.append(new_board)
    print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking diagonal movement towards the 0th column and 0th row
  if(col > 0 and row > 0 and who(board[row - 1][col - 1]) != CURRENT_PLAYER):
    #add a state
    new_board = copy_board(board)
    new_board[row - 1][col - 1] = piece
    new_board[row][col] = 0
    new_boards.append(new_board)
    print(print_board(new_board)) # <<< FOR DEBUGGING
  
  return new_boards

def analyze_withdrawer_movement(piece, row, col, board):
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
      if (col > 0 and who(board[row][col - 1]) != CURRENT_PLAYER):
        new_board[row][col - 1] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      if (col < 7 and who(board[row][col + 1]) != CURRENT_PLAYER):
        new_board[row][col + 1] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      if (row > 0 and who(board[row - 1][col]) != CURRENT_PLAYER):
        new_board[row - 1][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      if (row < 7 and who(board[row + 1][col]) != CURRENT_PLAYER):
        new_board[row + 1][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      if (row > 0 and col > 0 and who(board[row - 1][col - 1]) != CURRENT_PLAYER):
        new_board[row - 1][col - 1] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      if (row < 7 and col > 0 and who(board[row + 1][col - 1]) != CURRENT_PLAYER):
        new_board[row + 1][col - 1] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      if (row > 0 and col < 7 and who(board[row - 1][col + 1]) != CURRENT_PLAYER):
        new_board[row - 1][col + 1] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      if (row < 7 and col < 7 and who(board[row + 1][col + 1]) != CURRENT_PLAYER):
        new_board[row + 1][col + 1] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  
  return new_boards

def analyze_leaper_movement(piece, row, col, board):
  new_boards = []
  
  # checking horizontal movement towards the 8th column
  k = 1
  while (col + k < 8):
    if(board[row][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col + k] = piece
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (col + k < 7 and board[row][col + k + 1] == 0):
    # the piece to jump is the oponent's
    if (who(board[row][col + k]) != CURRENT_PLAYER):
      new_board = copy_board(board)
      new_board[row][col + k + 1] = piece
      new_board[row][col + k] = 0
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking horizontal movement towards the 0th column
  k = 1
  while (col - k > -1):
    if(board[row][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col - k] = piece
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (col + k > 0 and board[row][col - k - 1] == 0):
    # the piece to jump is the oponent's
    if (who(board[row][col - k]) != CURRENT_PLAYER):
      new_board = copy_board(board)
      new_board[row][col - k - 1] = piece
      new_board[row][col - k] = 0
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING

  # checking vertical movement towards the 8th row
  k = 1
  while (row + k < 8):
    if(board[row + k][col] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col] = piece
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row + k < 7 and board[row + k + 1][col] == 0):
    # the piece to jump is the oponent's
    if (who(board[row + k][col]) != CURRENT_PLAYER):
      new_board = copy_board(board)
      new_board[row + k + 1][col] = piece
      new_board[row + k][col] = 0
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking vertical movement towards the 0th row
  k = 1
  while (row - k > -1):
    if(board[row - k][col] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col] = piece
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row - k > 0 and board[row - k - 1][col] == 0):
    # the piece to jump is the oponent's
    if (who(board[row - k][col]) != CURRENT_PLAYER):
      new_board = copy_board(board)
      new_board[row - k - 1][col] = piece
      new_board[row - k][col] = 0
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking diagonal movement towards the 8th column and 8th row
  k = 1
  while (k + row < 8 and k + col < 8):
    if(board[row + k][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col + k] = piece;
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row + k < 7 and col + k < 7 and board[row + k + 1][col + k + 1] == 0):
    # the piece to jump is the oponent's
    if (who(board[row + k][col + k]) != CURRENT_PLAYER):
      new_board = copy_board(board)
      new_board[row + k + 1][col + k + 1] = piece
      new_board[row + k][col + k] = 0
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking diagonal movement towards the 8th column and 0th row
  k = 1
  while (row - k > -1 and col + k < 8):
    if(board[row - k][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col + k] = piece;
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row - k > 0 and col + k < 7 and board[row - k - 1][col + k + 1] == 0):
    # the piece to jump is the oponent's
    if (who(board[row - k][col + k]) != CURRENT_PLAYER):
      new_board = copy_board(board)
      new_board[row - k - 1][col + k + 1] = piece
      new_board[row - k][col + k] = 0
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking diagonal movement towards the 0th column and 8th row
  k = 1
  while (k + row < 8 and col - k > -1):
    if(board[row + k][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col - k] = piece;
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row + k < 7 and col - k > 0 and board[row + k + 1][col - k - 1] == 0):
    # the piece to jump is the oponent's
    if (who(board[row + k][col - k]) != CURRENT_PLAYER):
      new_board = copy_board(board)
      new_board[row + k + 1][col - k - 1] = piece
      new_board[row + k][col - k] = 0
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking diagonal movement towards the 0th column and 0th row
  k = 1
  while (row - k > -1 and col - k > -1):
    if(board[row - k][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col - k] = piece;
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row - k > 0 and col - k > 0 and board[row - k + 1][col - k - 1] == 0):
    # the piece to jump is the oponent's
    if (who(board[row - k][col - k]) != CURRENT_PLAYER):
      new_board = copy_board(board)
      new_board[row - k - 1][col - k - 1] = piece
      new_board[row - k][col - k] = 0
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
  
  return new_boards

def analyze_coordinator_movement(piece, row, col, board):
  new_boards = []
  
  # checking horizontal movement towards the 8th column
  k = 1
  while (col + k < 8):
    if(board[row][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col + k] = piece
      new_board[row][col] = 0
      apply_coordinator_kill(piece, row, col + k, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      apply_coordinator_kill(piece, row, col - k, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      apply_coordinator_kill(piece, row + k, col, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      apply_coordinator_kill(piece, row - k, col, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      apply_coordinator_kill(piece, row + k, col + k, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      apply_coordinator_kill(piece, row - k, col + k, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      apply_coordinator_kill(piece, row + k, col - k, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      apply_coordinator_kill(piece, row - k, col - k, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  
  return new_boards

def apply_coordinator_kill(piece, row, col, board):
  # locate your king
  for i in range(8): # look through row
    for j in range(8): # look through column
      current_piece = board[i][j]
      # kill corners
      if (current_piece == 12 + CURRENT_PLAYER):
        if (who(board[row][j]) != CURRENT_PLAYER and board[row][j] != 0):
          board[row][j] = 0
        if (who(board[i][col]) != CURRENT_PLAYER and board[i][col] != 0):
          board[i][col] = 0
        if i == row :
          if col > j:
            for k in range(col - j - 1):
              if (who(board[i][j+k]) != CURRENT_PLAYER and board[i][j+k] != 0) :
                board[i][j+k] = 0
          else:
            for k in range(col - j - 1):
              if (who(board[i][j-k]) != CURRENT_PLAYER and board[i][j-k] != 0) :
                board[i][j-k] = 0
        if j == col:
          if row > i:
            for k in range(row - i - 1):
              if (who(board[i+k][j]) != CURRENT_PLAYER and board[i+k][j] != 0) :
                board[i+k][j] = 0
          else:
            for k in range(row - i - 1):
              if (who(board[i-k][j]) != CURRENT_PLAYER and board[i-k][j] != 0) :
                board[i-k][j] = 0
        return

def analyze_freezer_movement(piece, row, col, board):
  new_boards = []
  
  # checking horizontal movement towards the 8th column
  k = 1
  while (col + k < 8):
    if(board[row][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col + k] = piece
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
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
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1

  return new_boards

# Need to implement King imitation
def analyze_imitator_movement(piece, row, col, board):
  new_boards = []
  '''
  # checking horizontal movement toward the 8th column for a king
  if(col < 7 and board[row][col + 1] == 13 - CURRENT_PLAYER):
    #add a state
    new_board = copy_board(board)
    new_board[row][col + 1] = piece
    new_board[row][col] = 0
    new_boards.append(new_board)
    print(print_board(new_board)) # <<< FOR DEBUGGING
    
  # checking horizontal movement toward the 0th column for a king
  if(col > 0 and board[row][col - 1] == 13 - CURRENT_PLAYER):
    #add a state
    new_board = copy_board(board)
    new_board[row][col - 1] = piece
    new_board[row][col] = 0
    new_boards.append(new_board)
    print(print_board(new_board)) # <<< FOR DEBUGGING
    
  # checking vertical movement toward the 8th row  for a king
  if(row < 7 and board[row + 1][col] == 13 - CURRENT_PLAYER):
    #add a state
    new_board = copy_board(board)
    new_board[row + 1][col] = piece
    new_board[row][col] = 0
    new_boards.append(new_board)
    print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking vertical movement toward the 0th row
  if(row > 0 and who(board[row - 1][col]) != CURRENT_PLAYER):
    #add a state
    new_board = copy_board(board)
    new_board[row - 1][col] = piece
    new_board[row][col] = 0
    new_boards.append(new_board)
    print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking diagonal movement towards the 8th column and 8th row
  if(col < 7 and row < 7 and who(board[row + 1][col + 1]) != CURRENT_PLAYER):
    #add a state
    new_board = copy_board(board)
    new_board[row + 1][col + 1] = piece
    new_board[row][col] = 0
    new_boards.append(new_board)
    print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking diagonal movement towards the 8th column and 0th row
  if(col < 7 and row > 0 and who(board[row - 1][col + 1]) != CURRENT_PLAYER):
    #add a state
    new_board = copy_board(board)
    new_board[row - 1][col + 1] = piece;
    new_board[row][col] = 0;
    new_boards.append(new_board)
    print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking diagonal movement towards the 0th column and 8th row
  if(col > 0 and row < 7 and who(board[row + 1][col - 1]) != CURRENT_PLAYER):
    #add a state
    new_board = copy_board(board)
    new_board[row + 1][col - 1] = piece
    new_board[row][col] = 0
    new_boards.append(new_board)
    print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking diagonal movement towards the 0th column and 0th row
  if(col > 0 and row > 0 and who(board[row - 1][col - 1]) != CURRENT_PLAYER):
    #add a state
    new_board = copy_board(board)
    new_board[row - 1][col - 1] = piece
    new_board[row][col] = 0
    new_boards.append(new_board)
    print(print_board(new_board)) # <<< FOR DEBUGGING
  '''
  
  
  # checking horizontal movement towards the 8th column
  k = 1
  while (col + k < 8):
    if(board[row][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col + k] = piece
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (col > 0 and board[row][col - 1] == 11 - CURRENT_PLAYER):
        new_board[row][col - 1] = 0
      apply_imitator_coordinator_kill(piece, row, col + k, new_board)
      apply_imitator_pincer_kill(piece, row, col + k, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (col + k < 7 and board[row][col + k + 1] == 0):
    # the piece to jump is the oponent's leaper
    if (board[row][col + k] == 7 - CURRENT_PLAYER):
      new_board = copy_board(board)
      new_board[row][col + k + 1] = piece
      new_board[row][col + k] = 0
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (col > 0 and board[row][col - 1] == 11 - CURRENT_PLAYER):
        new_board[row][col - 1] = 0
      apply_imitator_coordinator_kill(piece, row, col + k + 1, new_board)
      apply_imitator_pincer_kill(piece, row, col + k + 1, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking horizontal movement towards the 0th column
  k = 1
  while (col - k > -1):
    if(board[row][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row][col - k] = piece
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (col < 7 and board[row][col + 1] == 11 - CURRENT_PLAYER):
        new_board[row][col + 1] = 0
      apply_imitator_coordinator_kill(piece, row, col - k, new_board)
      apply_imitator_pincer_kill(piece, row, col - k, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (col + k > 0 and board[row][col - k - 1] == 0):
    # the piece to jump is the oponent's leaper
    if (board[row][col - k] == 7 - CURRENT_PLAYER):
      new_board = copy_board(board)
      new_board[row][col - k - 1] = piece
      new_board[row][col - k] = 0
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (col < 7 and board[row][col + 1] == 11 - CURRENT_PLAYER):
        new_board[row][col + 1] = 0
      apply_imitator_coordinator_kill(piece, row, col - k - 1, new_board)
      apply_imitator_pincer_kill(piece, row, col - k - 1, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING

  # checking vertical movement towards the 8th row
  k = 1
  while (row + k < 8):
    if(board[row + k][col] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col] = piece
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row > 0 and board[row - 1][col] == 11 - CURRENT_PLAYER):
        new_board[row - 1][col] = 0
      apply_imitator_coordinator_kill(piece, row + k, col, new_board)
      apply_imitator_pincer_kill(piece, row + k, col, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row + k < 7 and board[row + k + 1][col] == 0):
    # the piece to jump is the oponent's leaper
    if (board[row + k][col] == 7 - CURRENT_PLAYER):
      new_board = copy_board(board)
      new_board[row + k + 1][col] = piece
      new_board[row + k][col] = 0
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row > 0 and board[row - 1][col] == 11 - CURRENT_PLAYER):
        new_board[row - 1][col] = 0
      apply_imitator_coordinator_kill(piece, row + k + 1, col, new_board)
      apply_imitator_pincer_kill(piece, row + k + 1, col, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking vertical movement towards the 0th row
  k = 1
  while (row - k > -1):
    if(board[row - k][col] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col] = piece
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row < 7 and board[row + 1][col] == 11 - CURRENT_PLAYER):
        new_board[row + 1][col] = 0
      apply_imitator_coordinator_kill(piece, row - k, col, new_board)
      apply_imitator_pincer_kill(piece, row - k, col, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row - k > 0 and board[row - k - 1][col] == 0):
    # the piece to jump is the oponent's
    if (board[row - k][col] == 7 - CURRENT_PLAYER):
      new_board = copy_board(board)
      new_board[row - k - 1][col] = piece
      new_board[row - k][col] = 0
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row < 7 and board[row + 1][col] == 11 - CURRENT_PLAYER):
        new_board[row + 1][col] = 0
      apply_imitator_coordinator_kill(piece, row - k - 1, col, new_board)
      apply_imitator_pincer_kill(piece, row - k - 1, col, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking diagonal movement towards the 8th column and 8th row
  k = 1
  while (k + row < 8 and k + col < 8):
    if(board[row + k][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col + k] = piece;
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row > 0 and col > 0 and board[row - 1][col - 1] == 11 - CURRENT_PLAYER):
        new_board[row - 1][col - 1] = 0
      apply_imitator_coordinator_kill(piece, row + k, col + k, new_board)
      apply_imitator_pincer_kill(piece, row + k, col + k, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row + k < 7 and col + k < 7 and board[row + k + 1][col + k + 1] == 0):
    # the piece to jump is the oponent's
    if (board[row + k][col + k] == 7 - CURRENT_PLAYER):
      new_board = copy_board(board)
      new_board[row + k + 1][col + k + 1] = piece
      new_board[row + k][col + k] = 0
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row > 0 and col > 0 and board[row - 1][col - 1] == 11 - CURRENT_PLAYER):
        new_board[row - 1][col - 1] = 0
      apply_imitator_coordinator_kill(piece, row + k + 1, col + k + 1, new_board)
      apply_imitator_pincer_kill(piece, row + k + 1, col + k + 1, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking diagonal movement towards the 8th column and 0th row
  k = 1
  while (row - k > -1 and col + k < 8):
    if(board[row - k][col + k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col + k] = piece;
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row < 7 and col > 0 and board[row + 1][col - 1] == 11 - CURRENT_PLAYER):
        new_board[row + 1][col - 1] = 0
      apply_imitator_coordinator_kill(piece, row - k, col + k, new_board)
      apply_imitator_pincer_kill(piece, row - k, col + k, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row - k > 0 and col + k < 7 and board[row - k - 1][col + k + 1] == 0):
    # the piece to jump is the oponent's
    if (board[row - k][col + k] == 7 - CURRENT_PLAYER):
      new_board = copy_board(board)
      new_board[row - k - 1][col + k + 1] = piece
      new_board[row - k][col + k] = 0
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row < 7 and col > 0 and board[row + 1][col - 1] == 11 - CURRENT_PLAYER):
        new_board[row + 1][col - 1] = 0
      apply_imitator_coordinator_kill(piece, row - k - 1, col + k + 1, new_board)
      apply_imitator_pincer_kill(piece, row - k - 1, col + k + 1, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking diagonal movement towards the 0th column and 8th row
  k = 1
  while (k + row < 8 and col - k > -1):
    if(board[row + k][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row + k][col - k] = piece;
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row > 0 and col < 7 and board[row - 1][col + 1] == 11 - CURRENT_PLAYER):
        new_board[row - 1][col + 1] = 0
      apply_imitator_coordinator_kill(piece, row + k, col - k, new_board)
      apply_imitator_pincer_kill(piece, row + k, col - k, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row + k < 7 and col - k > 0 and board[row + k + 1][col - k - 1] == 0):
    # the piece to jump is the oponent's
    if (board[row + k][col - k] == 7 - CURRENT_PLAYER):
      new_board = copy_board(board)
      new_board[row + k + 1][col - k - 1] = piece
      new_board[row + k][col - k] = 0
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row > 0 and col < 7 and board[row - 1][col + 1] == 11 - CURRENT_PLAYER):
        new_board[row - 1][col + 1] = 0
      apply_imitator_coordinator_kill(piece, row + k + 1, col - k - 1, new_board)
      apply_imitator_pincer_kill(piece, row + k + 1, col - k - 1, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
  
  # checking diagonal movement towards the 0th column and 0th row
  k = 1
  while (row - k > -1 and col - k > -1):
    if(board[row - k][col - k] == 0):
      #add a state
      new_board = copy_board(board)
      new_board[row - k][col - k] = piece;
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row < 7 and col < 7 and board[row + 1][col + 1] == 11 - CURRENT_PLAYER):
        new_board[row + 1][col + 1] = 0
      apply_imitator_coordinator_kill(piece, row - k, col - k, new_board)
      apply_imitator_pincer_kill(piece, row - k, col - k, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
    # a piece is in the way
    else:
      break
    k = k + 1
  # there is space to jump
  if (row - k > 0 and col - k > 0 and board[row - k + 1][col - k - 1] == 0):
    # the piece to jump is the oponent's
    if (board[row - k][col - k] == 7 - CURRENT_PLAYER):
      new_board = copy_board(board)
      new_board[row - k - 1][col - k - 1] = piece
      new_board[row - k][col - k] = 0
      new_board[row][col] = 0
      # if moving away from enemy withdrawer, kill it
      if (row < 7 and col < 7 and board[row + 1][col + 1] == 11 - CURRENT_PLAYER):
        new_board[row + 1][col + 1] = 0
      apply_imitator_coordinator_kill(piece, row - k - 1, col - k - 1, new_board)
      apply_imitator_pincer_kill(piece, row - k - 1, col - k - 1, new_board)
      new_boards.append(new_board)
      print(print_board(new_board)) # <<< FOR DEBUGGING
  
  return new_boards

def apply_imitator_pincer_kill(piece, row, col, board):
  # squish towards 0th row
  if row > 1 and board[row-1][col] == 3 - CURRENT_PLAYER and who(board[row-2][col]) == CURRENT_PLAYER :
    board[row-1][col] = 0
  # squish towards 8th row
  if row < 6 and board[row+1][col] == 3 - CURRENT_PLAYER and who(board[row+2][col]) == CURRENT_PLAYER :
    board[row+1][col] = 0
  # squish towards 0th column
  if col > 1 and board[row][col-1] == 3 - CURRENT_PLAYER and who(board[row][col-2]) == CURRENT_PLAYER :
    board[row][col-1] = 0
  # squish towards 8th column
  if col < 6 and board[row][col+1] == 3 - CURRENT_PLAYER and who(board[row][col+2]) == CURRENT_PLAYER :
    board[row][col+1] = 0

def apply_imitator_coordinator_kill(piece, row, col, board):
  # locate your king
  for i in range(8): # look through row
    for j in range(8): # look through column
      current_piece = board[i][j]
      # kill corners
      if (current_piece == 12 + CURRENT_PLAYER):
        if (board[row][j] == 5 - CURRENT_PLAYER):
          board[row][j] = 0
        if (board[i][col] == 5 - CURRENT_PLAYER):
          board[i][col] = 0
        return



def analyze_piece(piece, row, col, board):
  new_boards = []
  
  # check to see if this piece is frozen
  if is_adjacent_too(piece, row, col, board, 15):
    return new_boards
  
  # Pincer
  if(piece == 2 or piece == 3):
    new_boards.extend(analyze_pincer_movement(piece, row, col, board))
  
  # King
  if(piece == 12 or piece == 13):
    new_boards.extend(analyze_king_movement(piece, row, col, board))
  
  # Withdrawer
  if(piece == 10 or piece == 11):
    new_boards.extend(analyze_withdrawer_movement(piece, row, col, board))
  
  # Leaper
  if(piece == 6 or piece == 7):
    new_boards.extend(analyze_leaper_movement(piece, row, col, board))
  
  # Coordinator
  if(piece == 4 or piece == 5):
    new_boards.extend(analyze_coordinator_movement(piece, row, col, board))
  
  # Freezer
  if(piece == 14 or piece == 15):
    # freezer can be frozen by an imitator, check for that
    if is_adjacent_too(piece, row, col, board, 9):
      return new_boards
    new_boards.extend(analyze_freezer_movement(piece, row, col, board))
  
  # Imitator
  if(piece == 8 or piece == 9):
    new_boards.extend(analyze_imitator_movement(piece, row, col, board))
  
  return new_boards 

def is_adjacent_too(piece, row, col, board, other):
  if(row > 0 and board[row - 1][col] == other - CURRENT_PLAYER):
    return True
  if(row < 7 and board[row + 1][col] == other - CURRENT_PLAYER):
    return True
  if(col > 0 and board[row][col - 1] == other - CURRENT_PLAYER):
    return True
  if(col < 7 and board[row][col + 1] == other - CURRENT_PLAYER):
    return True
  if(row > 0 and col > 0 and board[row - 1][col - 1] == other - CURRENT_PLAYER):
    return True
  if(row > 0 and col < 7 and board[row - 1][col + 1] == other - CURRENT_PLAYER):
    return True
  if(row < 7 and col > 0 and board[row + 1][col - 1] == other - CURRENT_PLAYER):
    return True
  if(row < 7 and col < 7 and board[row + 1][col + 1] == other - CURRENT_PLAYER):
    return True
  return False
  
def print_boards(boards):
  s = ''
  for b in boards:
    s += print_board(b)
  return s
  
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

test_state = BC_state(IMITATOR_TEST_5, WHITE)
print(test_state)
look_for_successors(test_state)
