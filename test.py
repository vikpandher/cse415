list_a = [['a', 'b'], ['c', 'd'], ['e', 'f']]

def rotate(old_list):
  old_row_count = len(old_list)
  old_col_count = len(old_list[0])
  new_row_count = old_col_count
  new_col_count = old_row_count
  new_list = [[0 for x in range(new_col_count)] for y in range(new_row_count)]
  for j in range(0, new_col_count):
    for i in range(0, new_row_count):
      new_list[i][j] = old_list[old_row_count-1-j][i]
  return(new_list)

def flip(old_list):
  old_row_count = len(old_list)
  old_col_count = len(old_list[0])
  new_list = [[0 for x in range(old_col_count)] for y in range(old_row_count)]
  for j in range(0, old_col_count):
    for i in range(0, old_row_count):
      new_list[i][j] = old_list[i][old_col_count-1-j]
  return(new_list)

state_a = [[0 for x in range(6)] for y in range(10)]
piece_a = [[0,1,1], [1,1,0], [0,1,0]]

# UPDATED
def place(state, piece, row, col):
  board = state[0]
  available_pieces = state[1]
  piece_row_count = len(piece)
  piece_col_count = len(piece[0])
  for j in range(0, piece_col_count):
    for i in range(0, piece_row_count):
      board[i+col][j+row] = piece[i][j]
  available_pieces.remove(piece)
  return(state)

# UPDATED
def can_place(board, piece, row, col):
  piece_row_count = len(piece)
  piece_col_count = len(piece[0])
  if(piece_row_count + col > STATE_HEIGHT) or (piece_col_count + row > STATE_WIDTH):
    return False;
  for j in range(0, piece_col_count):
    for i in range(0, piece_row_count):
      if(piece[i][j] != 0 and board[i+col][j+row] != 0):
        return False
  return True

# NEW
def is_available(list, piece):
  for p in list:
    if p == piece:
      return True
  return False

  
STATE_WIDTH = 6
STATE_HEIGHT = 10

def generate_pieces(piece):
  pieces = [piece]
  piece90 = rotate(piece)
  piece180 = rotate(piece90)
  piece270 = rotate(piece180)
  pieceflip = flip(piece)
  pieceflip90 = rotate(pieceflip)
  pieceflip180 = rotate(pieceflip90)
  pieceflip270 = rotate(pieceflip180)
  pieces.append(piece90)
  pieces.append(piece180)
  pieces.append(piece270)
  pieces.append(pieceflip)
  pieces.append(pieceflip90)
  pieces.append(pieceflip180)
  pieces.append(pieceflip270)
  return pieces

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)
  
SPACE = [[0 for x in range(STATE_WIDTH)] for y in range(STATE_HEIGHT)]
PIECE1 = [[0,1,1], [1,1,0], [0,1,0]]
PIECE2 = [[2], [2], [2], [2], [2]]
PIECE3 = [[3,0], [3,0], [3,0], [3,3]]
PIECE4 = [[0,4], [4,4], [4,0], [4,0]]
PIECE5 = [[0,5], [5,5], [5,5]]
PIECE6 = [[6,6,6], [0,6,0], [0,6,0]]
PIECE7 = [[7,0,7], [7,7,7]]
PIECE8 = [[8,0,0], [8,0,0], [8,8,8]]
PIECE9 = [[9,0,0], [9,9,0], [0,9,9]]
PIECE10 = [[0,10,0], [10,10,10], [0,10,0]]
PIECE11 = [[0,11], [11,11], [0,11], [0,11]]
PIECE12 = [[12,12,0], [0,12,0], [0,12,12]]
PIECES = {"PIECE1" : generate_pieces(PIECE1),
          "PIECE2" : generate_pieces(PIECE2),
          "PIECE3" : generate_pieces(PIECE3),
          "PIECE4" : generate_pieces(PIECE4),
          "PIECE5" : generate_pieces(PIECE5),
          "PIECE6" : generate_pieces(PIECE6),
          "PIECE7" : generate_pieces(PIECE7),
          "PIECE8" : generate_pieces(PIECE8),
          "PIECE9" : generate_pieces(PIECE9),
          "PIECE10" : generate_pieces(PIECE10),
          "PIECE11" : generate_pieces(PIECE11),
          "PIECE12" : generate_pieces(PIECE12)}
INITIAL_STATE = [SPACE,["PIECE" + str(x) for x in range(1,13)]]
LOCATIONS = [(x, y) for x in range(STATE_WIDTH) for y in range(STATE_HEIGHT)]
OPERATORS = [Operator("Place pentamino " + str(PIECE1) + " in location " + str(x) + " " + str(y) + ".",
            
            lambda s,x=x,y=y : can_place(s[0],PIECE1,x,y),
            # The default value construct is needed
            # here to capture the values of p&q separately
            # in each iteration of the list comp. iteration.
            lambda s,x=x,y=y: place(s[0],PIECE1,x,y) )
            
            for (x, y) in LOCATIONS]

# UPDATED
def generate_operators():
  operators = []
  piece_list = PIECES.values();
  for piece in piece_list:
    for orientation in piece:
      operators.append(
      [Operator("Place pentamino " + str(orientation) + " in location " +\
      str(x) + " " + str(y) + ".",
      
      lambda s,x=x,y=y : is_available(s[1], orientation) and can_place(s[0],orientation,x,y),
      # The default value construct is needed
      # here to capture the values of p&q separately
      # in each iteration of the list comp. iteration.
      lambda s,x=x,y=y: place(s,orientation,x,y) )
      
      for (x, y) in LOCATIONS])
  return operators

print(len(generate_operators())) # Thats 96 operators
print()
  
  
'''
def place(old_state, piece, x, y):
  STATE_WIDTH = len(old_state)
  STATE_HEIGHT = len(old_state[0])
  piece_row_count = len(piece)
  piece_col_count = len(piece[0])
  new_state = [[0 for x in range(STATE_HEIGHT)] for y in range(STATE_WIDTH)]
  for j in range(0, piece_col_count):
    for i in range(0, piece_row_count):
      new_state[i+x][j+y] = piece[i][j]
  return(new_state)
'''
'''
print(state_a)
print()
print(can_place(state_a, piece_a, 0, 0))
print()
print(place(state_a, piece_a, 0, 0))
print()
print(can_place(state_a, piece_a, 3, 7))
print()
print(place(state_a, piece_a, 3, 7))
print()
print(can_place(state_a, piece_a, 0, 0))
print()
print(place(state_a, piece_a, 0, 0))
print()
'''