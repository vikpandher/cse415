'''Pentaminoes2.py
A QUIET Solving Tool problem formulation.
QUIET = Quetzal User Intelligence Enhancing Technology.
The XML-like tags used here serve to identify key sections of this 
problem formulation.  

CAPITALIZED constructs are generally present in any problem
formulation and therefore need to be spelled exactly the way they are.
Other globals begin with a capital letter but otherwise are lower
case or camel case.
'''

'''
Vikramjit Pandher, Chloe Nash, CSE 415, Spring 2016, University of Washington
Instructor:  S. Tanimoto.
Assignment 4 Option A: Pentaminoes2. 

Status of the implementation:
All required features working. Works with sample puzzles.

'''

#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Pentaminoes2"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['V. Pandher', 'C. Nash']
PROBLEM_CREATION_DATE = "25-APR-2016"
PROBLEM_DESC=\
'''This formulation of the Pentaminoes2 uses generic
Python 3 constructs and has been tested with Python 3.5.
It is designed to work accordingly to the QUIET tools interface.
'''
#</METADATA>

#<COMMON_CODE>

def DEEP_EQUALS(s1, s2):
  state1 = s1[0]
  state2 = s2[0]
  for row in range(0,STATE_HEIGHT):
    for col in range (0,STATE_WIDTH):
      if state1[row][col] != state2[row][col] :
        return False
  return True

def DESCRIBE_STATE(s):
  # Produces a textual description of a state.
  # Might not be needed in normal operation with GUIs.
  state = s[0]
  txt = ""
  for row in range(0,STATE_HEIGHT):
    for col in range (0,STATE_WIDTH):
      if state[row][col] < STATE_HEIGHT :
        txt += str(state[row][col]) + "  "
      else :
        txt += str(state[row][col]) + " "
    txt += "\n"
  available_pieces = s[1]
  for piece in available_pieces:
    txt += piece + " "
  
  return txt

# Make a string and return it as the hash code
def HASHCODE(s):
  '''The result should be an immutable object such as a string
  that is unique for the state s.'''
  state = s[0]
  hash = ""
  for row in range(0,STATE_HEIGHT):
    for col in range (0,STATE_WIDTH):
      hash += str(state[row][col])
  return hash

def copy_state(s):
  old_board = s[0]
  old_list = s[1]
  new_board = [[0 for x in range(STATE_WIDTH)] for y in range(STATE_HEIGHT)]
  new_list = []
  for row in range(0,STATE_HEIGHT):
    for col in range (0,STATE_WIDTH):
      new_board[row][col] = old_board[row][col]
  for piece in old_list:
    new_list.append(piece)
  new_state = [new_board, new_list]
  return new_state

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

def place(old_state, piece, orientation, row, col):
  state = copy_state(old_state)
  board = state[0]
  available_pieces = state[1]
  piece_row_count = len(orientation)
  piece_col_count = len(orientation[0])
  for j in range(0, piece_col_count):
    for i in range(0, piece_row_count):
      if(orientation[i][j] != 0):
        board[i+col][j+row] = orientation[i][j]
  available_pieces.remove(piece)
  return(state)
  
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
  
def is_available(available_pieces, piece):
  for p in available_pieces:
    if p == piece:
      return True
  return False

def goal_test(s):
  '''If the puzzle is completely full
  Then the goal is reached.'''
  state = s[0]
  for row in range(0,STATE_HEIGHT):
    for col in range (0,STATE_WIDTH):
      if state[row][col] == 0 :
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
STATE_WIDTH = 5
STATE_HEIGHT = 5
#</COMMON_DATA>
          
PIECE1 = [[3,0], [3,0], [3,0], [3,3]] 
PIECE2 = [[0,4], [4,4], [4,0], [4,0]] 
PIECE3 = [[7,0,7], [7,7,7]] 
PIECE4 = [[9,0,0], [9,9,0], [0,9,9]] 
PIECE5 = [[0,11], [11,11], [0,11], [0,11]] 

SPACE = [[0 for x in range(STATE_WIDTH)] for y in range(STATE_HEIGHT)]
PIECES = {"PIECE1" : generate_pieces(PIECE1),
          "PIECE2" : generate_pieces(PIECE2),
          "PIECE3" : generate_pieces(PIECE3),
          "PIECE4" : generate_pieces(PIECE4),
          "PIECE5" : generate_pieces(PIECE5)}


INITIAL_STATE = [SPACE,["PIECE" + str(x) for x in range(1,6)]]
CREATE_INITIAL_STATE = lambda: INITIAL_STATE
#</INITIAL_STATE>

#<OPERATORS>
LOCATIONS = [(x, y) for x in range(STATE_WIDTH) for y in range(STATE_HEIGHT)]

def generate_operators():
  operators = []
  for piece in ["PIECE" + str(x) for x in range(1,6)]:
    orientations = PIECES[piece]
    for orientation in orientations:
      this_operator = []
      this_operator.extend(
      [Operator("Place pentamino " + str(orientation) + " in location " +\
      str(x) + "," + str(y) + ".",
      lambda s,piece=piece,orientation=orientation,x=x,y=y : is_available(s[1], piece) and can_place(s[0],orientation,x,y),
      # The default value construct is needed
      # here to capture the values of p&q separately
      # in each iteration of the list comp. iteration.
      lambda s,piece=piece,orientation=orientation,x=x,y=y: place(s, piece, orientation, x, y) )
      for (x, y) in LOCATIONS])
      operators.extend(this_operator)
  return operators

OPERATORS = generate_operators()

#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
