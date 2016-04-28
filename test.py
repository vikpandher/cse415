list_a = [['a', 'b'], ['c', 'd'], ['e', 'f']]

def rotate(old_list):
  old_row_count = len(old_list)
  old_col_count = len(old_list[0])
  new_row_count = old_col_count
  new_col_count = old_row_count
  new_list = [[0 for x in range(new_col_count)] for y in range(new_row_count)]
  for j in range(0, new_col_count):
    for i in range(0, new_row_count):
      new_list[i][j] = old_list[new_row_count-j][i]
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
  STATE_HEIGHT = len(state)
  STATE_WIDTH = len(state[0])
  peice_row_count = len(peice)
  peice_col_count = len(peice[0])
  for j in range(0, peice_col_count):
    for i in range(0, peice_row_count):
      state[i+col][j+row] = peice[i][j]
  return(state)
  
  
def can_place(state, peice, row, col):
  STATE_HEIGHT = len(state)
  STATE_WIDTH = len(state[0])
  peice_row_count = len(peice)
  peice_col_count = len(peice[0])
  if(peice_row_count + col > STATE_HEIGHT) or (peice_col_count + row > STATE_WIDTH):
    return False;
  for j in range(0, peice_col_count):
    for i in range(0, peice_row_count):
      if(peice[i][j] != 0 and state[i+col][j+row] != 0):
        return False
  return True

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
