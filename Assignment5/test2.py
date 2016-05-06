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

def check_kill_pawn(board, row, col, player):
  new_board = copy_board(board)
  if row > 1 and who(board[row-1][col]) != player and board[row-1][col] != 0 and who(board[row-2][col]) == player :
    new_board[row-1][col] = 0
  if row < 6 and who(board[row+1][col]) != player and board[row+1][col] != 0 and who(board[row+2][col]) == player :
    new_board[row+1][col] = 0
  if col > 1 and who(board[row][col-1]) != player and board[row][col-1] != 0 and who(board[row][col-2]) == player :
    new_board[row][col-1] = 0
  if col < 6 and who(board[row][col+1]) != player and board[row][col+1] != 0 and who(board[row][col+2]) == player :
    new_board[row][col+1] = 0
  return new_board

def analyze_piece(piece, row, col, board, player):
  new_boards = []
  if(piece == 3 or piece == 4):
    # checking horizortal movement to the 8th collumn
    for i in range(col + 1, 8):
      print("H8: " + str(board[row][i]))
      if(board[row][i] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row][i] = piece;
        new_board[row][col] = 0;
        updated_board = check_kill_pawn(new_board, row, i, player)
        print("updated:")
        print(print_board(updated_board))
        new_boards.append(updated_board)
        
        print("ADDING STATE H8: " + str(row) + ", " + str(i))
      else:
        print("break")
        break
    for i in range(col - 1, -1, -1):
      print("H0: " + str(board[row][i]))
      if(board[row][i] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[row][i] = piece;
        new_board[row][col] = 0;
        updated_board = check_kill_pawn(new_board, row, i, player)
        print("updated:")
        print(print_board(updated_board))
        new_boards.append(updated_board)
        
        print("ADDING STATE H0: " + str(row) + ", " + str(i))
      else:
        print("break")
        break
    for j in range(row + 1, 8):
      print("V8: " + str(board[j][col]))
      if(board[j][col] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[j][col] = piece;
        new_board[row][col] = 0;
        updated_board = check_kill_pawn(new_board, j, col, player)
        print("updated:")
        print(print_board(updated_board))
        new_boards.append(updated_board)
        
        print("ADDING STATE V8: " + str(j) + ", " + str(col))
      else:
        print("break")
        break
    for j in range(row - 1, -1, -1):
      print("V0: " + str(board[j][col]))
      if(board[j][col] == 0):
        #add a state
        new_board = copy_board(board)
        new_board[j][col] = piece;
        new_board[row][col] = 0;
        updated_board = check_kill_pawn(new_board, j, col, player)
        print("updated:")
        print(print_board(updated_board))
        new_boards.append(updated_board)
        
        print("ADDING STATE V0: " + str(j) + ", " + str(col))
      else:
        print("break")
        break
    return new_boards 
          
def print_boards(boards):
  s = ''
  for b in boards:
    for r in range(8):
      for c in range(8):
        s += CODE_TO_INIT[b[r][c]] + " "
      s += "\n"
    s += "\n"
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

init_state = BC_state(INITIAL, WHITE)
print(init_state)
look_for_successors(init_state)
