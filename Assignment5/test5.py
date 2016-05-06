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
  
def look_for_successors(state):
  board = state.board
  player = state.whose_move
  
  successors = []
  
  for i in range(8): # look through row
    for j in range(8): # look through collumn
      current_piece = board[i][j]
      if(who(current_piece) == player):
        print("current_piece = " + str(CODE_TO_INIT[current_piece]) + ", (" + str(i) + ", " + str(j) + ")")
        analyze_piece(current_piece, i, j, board, player)
        print()

'''
READ THIS:
  ok, so far the pincer movement is done, but it's killing is not included in
  this.
  the king's movement is done and since it was so simple, the kings killing is
  done too.
  the withdrawer's movement is done, but it's killing is not
  the leaper's movement and killing is done.
  
  I haven't taken into account the imobalizer yet.
'''
def analyze_piece(piece, row, col, board, player):
  new_boards = []
  
  # Pincer
  if(piece == 3 or piece == 4):
    # checking horizontal movement to the 8th collumn
    for i in range(col + 1, 8):
      #print("H8: " + str(board[row][i]))
      if(board[row][i] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row][i] = piece
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
        
        #print("ADDING STATE H8: " + str(row) + ", " + str(i))
      else:
        #print("break")
        break
    # checking horizontal movement to the 0th collumn
    for i in range(col - 1, -1, -1):
      #print("H0: " + str(board[row][i]))
      if(board[row][i] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row][i] = piece
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
        
        #print("ADDING STATE H0: " + str(row) + ", " + str(i))
      else:
        #print("break")
        break
    # checking vertical movement to the 8th row
    for j in range(row + 1, 8):
      #print("V8: " + str(board[j][col]))
      if(board[j][col] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[j][col] = piece
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
        
        #print("ADDING STATE V8: " + str(j) + ", " + str(col))
      else:
        #print("break")
        break
    # checking vertical movement to the 0th row
    for j in range(row - 1, -1, -1):
      #print("V0: " + str(board[j][col]))
      if(board[j][col] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[j][col] = piece
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
        
        #print("ADDING STATE V0: " + str(j) + ", " + str(col))
      else:
        #print("break")
        break
  
  # King
  if(piece == 13 or piece == 14):
    # checking horizontal movement toward the 8th collumn
    if(col < 7 and who(board[row][col + 1]) != player):
      #add a state
      new_board = copy_board(board)
      new_board[row][col + 1] = piece
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board))
      
    # checking horizontal movement toward the 0th collumn
    if(col > 0 and who(board[row][col - 1]) != player):
      #add a state
      new_board = copy_board(board)
      new_board[row][col - 1] = piece
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board))
      
    # checking vertical movement toward the 8th row
    if(row < 7 and who(board[row + 1][col]) != player):
      #add a state
      new_board = copy_board(board)
      new_board[row + 1][col] = piece
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board))
    
    # checking vertical movement toward the 0th row
    if(row > 0 and who(board[row - 1][col]) != player):
      #add a state
      new_board = copy_board(board)
      new_board[row - 1][col] = piece
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board))
    
    # checking diagonal movement towards the 8th collumn and 8th row
    if(col < 7 and row < 7 and who(board[row + 1][col + 1]) != player):
      #add a state
      new_board = copy_board(board)
      new_board[row + 1][col + 1] = piece
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board))
    
    # checking diagonal movement towards the 8th collumn and 0th row
    if(col < 7 and row > 0 and who(board[row - 1][col + 1]) != player):
      #add a state
      new_board = copy_board(board)
      new_board[row - 1][col + 1] = piece;
      new_board[row][col] = 0;
      new_boards.append(new_board)
      print(print_board(new_board))
    
    # checking diagonal movement towards the 0th collumn and 8th row
    if(col > 0 and row < 7 and who(board[row + 1][col - 1]) != player):
      #add a state
      new_board = copy_board(board)
      new_board[row + 1][col - 1] = piece
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board))
    
    # checking diagonal movement towards the 0th collumn and 0th row
    if(col > 0 and row > 0 and who(board[row - 1][col - 1]) != player):
      #add a state
      new_board = copy_board(board)
      new_board[row - 1][col - 1] = piece
      new_board[row][col] = 0
      new_boards.append(new_board)
      print(print_board(new_board))
      
  # Withdrawer
  if(piece == 11 or piece == 12):
    # checking horizontal movement towards the 8th collumn
    for i in range(col + 1, 8):
      if(board[row][i] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row][i] = piece
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
      # a piece is in the way
      else:
        break
    
    # checking horizontal movement towards the 0th collumn
    for i in range(col - 1, -1, -1):
      if(board[row][i] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row][i] = piece
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
        
      # a piece is in the way
      else:
        break
    
    # checking vertical movement towards the 8th row
    for j in range(row + 1, 8):
      if(board[j][col] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[j][col] = piece
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
      
      # a piece is in the way
      else:
        break
    
    # checking vertical movement towards the 0th row
    for j in range(row - 1, -1, -1):
      if(board[j][col] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[j][col] = piece
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
        
      # a piece is in the way
      else:
        break
    
    # checking diagonal movement towards the 8th collumn and 8th row
    k = 1
    while (k + row < 8 and k + col < 8):
      if(board[row + k][col + k] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row + k][col + k] = piece
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
      # a piece is in the way
      else:
        break
      k = k + 1
    
    # checking diagonal movement towards the 8th collumn and 0th row
    k = 1
    while (row - k > -1 and col + k < 8):
      if(board[row - k][col + k] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row - k][col + k] = piece
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
      # a piece is in the way
      else:
        break
      k = k + 1
      
    # checking diagonal movement towards the 0th collumn and 8th row
    k = 1
    while (k + row < 8 and col - k > -1):
      if(board[row + k][col - k] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row + k][col - k] = piece
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
      # a piece is in the way
      else:
        break
      k = k + 1
      
    # checking diagonal movement towards the 0th collumn and 0th row
    k = 1
    while (row - k > -1 and col - k > -1):
      if(board[row - k][col - k] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row - k][col - k] = piece
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
      # a piece is in the way
      else:
        break
      k = k + 1
    
  # Leaper
  if(piece == 6 or piece == 7):
    # checking horizontal movement towards the 8th collumn
    k = 1
    while (col + k < 8):
      if(board[row][col + k] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row][col + k] = piece
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
      # a piece is in the way
      else:
        break
      k = k + 1
    # there is space to jump
    if (col + k < 7 and board[row][col + k + 1] == 0):
      # the piece to jump is the oponent's
      if (who(board[row][col + k]) != player):
        new_board = copy_board(board)
        new_board[row][col + k + 1] = piece
        new_board[row][col + k] = 0
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
    
    # checking horizontal movement towards the 0th collumn
    k = 1
    while (col - k > -1):
      if(board[row][col - k] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row][col - k] = piece
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
      # a piece is in the way
      else:
        break
      k = k + 1
    # there is space to jump
    if (col + k > 0 and board[row][col - k - 1] == 0):
      # the piece to jump is the oponent's
      if (who(board[row][col - k]) != player):
        new_board = copy_board(board)
        new_board[row][col - k - 1] = piece
        new_board[row][col - k] = 0
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))

    # checking vertical movement towards the 8th row
    k = 1
    while (row + k < 8):
      if(board[row + k][col] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row + k][col] = piece
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
      # a piece is in the way
      else:
        break
      k = k + 1
    # there is space to jump
    if (row + k < 7 and board[row + k + 1][col] == 0):
      # the piece to jump is the oponent's
      if (who(board[row + k][col]) != player):
        new_board = copy_board(board)
        new_board[row + k + 1][col] = piece
        new_board[row + k][col] = 0
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
    
    # checking vertical movement towards the 0th row
    k = 1
    while (row - k > -1):
      if(board[row - k][col] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row - k][col] = piece
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
      # a piece is in the way
      else:
        break
      k = k + 1
    # there is space to jump
    if (row - k > 0 and board[row - k - 1][col] == 0):
      # the piece to jump is the oponent's
      if (who(board[row - k][col]) != player):
        new_board = copy_board(board)
        new_board[row - k - 1][col] = piece
        new_board[row - k][col] = 0
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
    
    # checking diagonal movement towards the 8th collumn and 8th row
    k = 1
    while (k + row < 8 and k + col < 8):
      if(board[row + k][col + k] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row + k][col + k] = piece;
        new_board[row][col] = 0;
        new_boards.append(new_board)
        print(print_board(new_board))
      # a piece is in the way
      else:
        break
      k = k + 1
    # there is space to jump
    if (row + k < 7 and col + k < 7 and board[row + k + 1][col + k + 1] == 0):
      # the piece to jump is the oponent's
      if (who(board[row + k][col + k]) != player):
        new_board = copy_board(board)
        new_board[row + k + 1][col + k + 1] = piece
        new_board[row + k][col + k] = 0
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
    
    # checking diagonal movement towards the 8th collumn and 0th row
    k = 1
    while (row - k > -1 and col + k < 8):
      if(board[row - k][col + k] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row - k][col + k] = piece;
        new_board[row][col] = 0;
        new_boards.append(new_board)
        print(print_board(new_board))
      # a piece is in the way
      else:
        break
      k = k + 1
    # there is space to jump
    if (row - k > 0 and col + k < 7 and board[row - k - 1][col + k + 1] == 0):
      # the piece to jump is the oponent's
      if (who(board[row - k][col + k]) != player):
        new_board = copy_board(board)
        new_board[row - k - 1][col + k + 1] = piece
        new_board[row - k][col + k] = 0
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
    
    # checking diagonal movement towards the 0th collumn and 8th row
    k = 1
    while (k + row < 8 and col - k > -1):
      if(board[row + k][col - k] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row + k][col - k] = piece;
        new_board[row][col] = 0;
        new_boards.append(new_board)
        print(print_board(new_board))
      # a piece is in the way
      else:
        break
      k = k + 1
    # there is space to jump
    if (row + k < 7 and col - k > 0 and board[row + k + 1][col - k - 1] == 0):
      # the piece to jump is the oponent's
      if (who(board[row + k][col - k]) != player):
        new_board = copy_board(board)
        new_board[row + k + 1][col - k - 1] = piece
        new_board[row + k][col - k] = 0
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
    
    # checking diagonal movement towards the 0th collumn and 0th row
    k = 1
    while (row - k > -1 and col - k > -1):
      if(board[row - k][col - k] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row - k][col - k] = piece;
        new_board[row][col] = 0;
        new_boards.append(new_board)
        print(print_board(new_board))
      # a piece is in the way
      else:
        break
      k = k + 1
    # there is space to jump
    if (row - k > 0 and col - k > 0 and board[row - k + 1][col - k - 1] == 0):
      # the piece to jump is the oponent's
      if (who(board[row - k][col - k]) != player):
        new_board = copy_board(board)
        new_board[row - k - 1][col - k - 1] = piece
        new_board[row - k][col - k] = 0
        new_board[row][col] = 0
        new_boards.append(new_board)
        print(print_board(new_board))
  
  return new_boards 
          
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

test_state = BC_state(LEAPER_TEST_1, WHITE)
print(test_state)
look_for_successors(test_state)