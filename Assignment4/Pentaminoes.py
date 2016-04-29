'''Jigsaw.py
Vikramjit Pandher, Chloe Nash, CSE 415, Spring 2016, University of Washington
Instructor:  S. Tanimoto.
Assignment 4 Option A: Pentaminoes. 

Status of the implementation:
All required features working. Works with sample puzzles.

'''

#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Pentaminoes"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['V. Pandher', 'C. Nash']
PROBLEM_CREATION_DATE = "25-APR-2016"
PROBLEM_DESC=\
'''This formulation of the Pentaminoes uses generic
Python 3 constructs and has been tested with Python 3.5.
'''
#</METADATA>

#<COMMON_CODE>

def DEEP_EQUALS(s1, s2):
  for row in range(0,10):
    for col in range (0,6):
      if s1{row][col] != s2[row][col] :
        return False
  return True

def DESCRIBE_STATE(s):
  # Produces a textual description of a state.
  # Might not be needed in normal operation with GUIs.
  for row in range(0,10):
    for col in range (0,6):
      if s[row][col] < 10 :
        txt += str(s[row][col]) + "  "
      else :
        txt += str(s[row][col]) + " "
    txt += "\n"
  return txt

# Make a string and return it as the hash code
def HASHCODE(s):
  '''The result should be an immutable object such as a string
  that is unique for the state s.'''
  hash = ""
  for row in range(0,10):
    for col in range (0,6):
      hash += str(s[row][col])
  return hash

def copy_state(s):
  new = [[0 for x in range(6)] for y in range(10)]
  for row in range(0,10):
    for col in range (0,6):
      new[row][col] = s[row][col]
  return new

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

def can_move(s,From,To):
  '''Tests whether it's legal to move a number in state s
     from the From location to the To location.'''
  try:
    # Can only move from a 0. No other check needed since operators
    # only has valid move combinations
    if s[From] == 0: return True
    return False
  except (Exception) as e:
    print(e)

def move(s,From,To):
  '''Assuming it's legal to make the move, this computes
     the new state resulting from moving.'''
  new = copy_state(s) # start with a deep copy.
  temp = new[To]
  new[To] = new[From]
  new[From] = temp
  return new # return new state

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

def goal_test(s):
  '''If the puzzle is completely full
  Then the goal is reached.'''
  for row in range(0,10):
    for col in range (0,6):
      if s[row][col] == 0 :
        return False
  return True

def goal_message(s):
  return "Pentaminoes is Solved!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

#</COMMON_CODE>

#<COMMON_DATA>
STATE_WIDTH = 6
STATE_HEIGHT = 10
#</COMMON_DATA>

SPACE = [[0 for x in range(STATE_WIDTH)] for y in range(STATE_HEIGHT)]
PIECES = {"PIECE1" : PIECE1,
          "PIECE2" : PIECE2,
          "PIECE3" : PIECE3,
          "PIECE4" : PIECE4,
          "PIECE5" : PIECE5,
          "PIECE6" : PIECE6,
          "PIECE7" : PIECE7,
          "PIECE8" : PIECE8,
          "PIECE9" : PIECE9,
          "PIECE10" : PIECE10,
          "PIECE11" : PIECE11,
          "PIECE12" : PIECE12}
          
PEICE1 = [[0,1,1], [1,1,0], [0,1,0]]
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

INITIAL_STATE = [SPACE,["PIECE" + str(x) for x in range(1,13)]]
CREATE_INITIAL_STATE = lambda: INITIAL_STATE
#</INITIAL_STATE>

#<OPERATORS>
combinations = [(0, 1), (0, 3),
                (1, 0), (1, 2), (1, 4),
                (2, 1), (2, 5),
                (3, 0), (3, 4), (3, 6),
                (4, 1), (4, 3), (4, 5), (4, 7),
                (5, 2), (5, 4), (5, 8),
                (6, 3), (6, 7),
                (7, 4), (7, 6), (7, 8),
                (8, 5), (8, 7)]
locations = [(x, y) for x in range(STATE_WIDTH) for y in range(STATE_HEIGHT)]
OPERATORS = [Operator("Place pentamino " + str(mino) + " in location " + str(x) + " " + str(y) + ".",
            
            lambda s,mino=mino, x=x, y=y : can_place(s,mino,x,y),
            # The default value construct is needed
            # here to capture the values of p&q separately
            # in each iteration of the list comp. iteration.
            lambda s,mino=mino,x=x,y=y: place(s,mino,x,y) )
            
            for (p, q) in combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
