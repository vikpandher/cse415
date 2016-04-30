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
peice_a = [[0,1,1], [1,1,0], [0,1,0]]

def place(state, peice, row, col):
  peice_row_count = len(peice)
  peice_col_count = len(peice[0])
  for j in range(0, peice_col_count):
    for i in range(0, peice_row_count):
      state[i+col][j+row] = peice[i][j]
  return(state)
  
def can_place(state, peice, row, col):
  peice_row_count = len(peice)
  peice_col_count = len(peice[0])
  if(peice_row_count + col > STATE_HEIGHT) or (peice_col_count + row > STATE_WIDTH):
    return False;
  for j in range(0, peice_col_count):
    for i in range(0, peice_row_count):
      if(peice[i][j] != 0 and state[i+col][j+row] != 0):
        return False
  return True
  
STATE_WIDTH = 6
STATE_HEIGHT = 10

def generate_peices(peice):
  peices = [peice]
  peice90 = rotate(peice)
  peice180 = rotate(peice90)
  peice270 = rotate(peice180)
  peiceflip = flip(peice)
  peiceflip90 = rotate(peiceflip)
  peiceflip180 = rotate(peiceflip90)
  peiceflip270 = rotate(peiceflip180)
  peices.append(peice90)
  peices.append(peice180)
  peices.append(peice270)
  peices.append(peiceflip)
  peices.append(peiceflip90)
  peices.append(peiceflip180)
  peices.append(peiceflip270)
  return peices

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
PIECES = {"PIECE1" : generate_peices(PIECE1),
          "PIECE2" : generate_peices(PIECE2),
          "PIECE3" : generate_peices(PIECE3),
          "PIECE4" : generate_peices(PIECE4),
          "PIECE5" : generate_peices(PIECE5),
          "PIECE6" : generate_peices(PIECE6),
          "PIECE7" : generate_peices(PIECE7),
          "PIECE8" : generate_peices(PIECE8),
          "PIECE9" : generate_peices(PIECE9),
          "PIECE10" : generate_peices(PIECE10),
          "PIECE11" : generate_peices(PIECE11),
          "PIECE12" : generate_peices(PIECE12)}
INITIAL_STATE = [SPACE,["PIECE" + str(x) for x in range(1,13)]]
LOCATIONS = [(x, y) for x in range(STATE_WIDTH) for y in range(STATE_HEIGHT)]
OPERATORS = [Operator("Place pentamino " + str(PIECE1) + " in location " + str(x) + " " + str(y) + ".",
            
            lambda s,x=x,y=y : can_place(s[0],PIECE1,x,y),
            # The default value construct is needed
            # here to capture the values of p&q separately
            # in each iteration of the list comp. iteration.
            lambda s,x=x,y=y: place(s[0],PIECE1,x,y) )
            
            for (x, y) in LOCATIONS]
  
def generate_operators(available_peices):
  operators = []
  for peice_key in available_peices:
    peice_list = PIECES[peice_key]
    for peice in peice_list:
      operators.append(
      [Operator("Place pentamino " + str(peice) + " in location " +\
      str(x) + " " + str(y) + ".",
      
      lambda s,x=x,y=y : can_place(s[0],peice,x,y),
      # The default value construct is needed
      # here to capture the values of p&q separately
      # in each iteration of the list comp. iteration.
      lambda s,x=x,y=y: place(s[0],peice,x,y) )
      
      for (x, y) in LOCATIONS])
  return operators
  
print(len(generate_operators(INITIAL_STATE[1])))
print()
  
  
'''
def place(old_state, peice, x, y):
  STATE_WIDTH = len(old_state)
  STATE_HEIGHT = len(old_state[0])
  peice_row_count = len(peice)
  peice_col_count = len(peice[0])
  new_state = [[0 for x in range(STATE_HEIGHT)] for y in range(STATE_WIDTH)]
  for j in range(0, peice_col_count):
    for i in range(0, peice_row_count):
      new_state[i+x][j+y] = peice[i][j]
  return(new_state)
'''
'''
print(state_a)
print()
print(can_place(state_a, peice_a, 0, 0))
print()
print(place(state_a, peice_a, 0, 0))
print()
print(can_place(state_a, peice_a, 3, 7))
print()
print(place(state_a, peice_a, 3, 7))
print()
print(can_place(state_a, peice_a, 0, 0))
print()
print(place(state_a, peice_a, 0, 0))
print()
'''