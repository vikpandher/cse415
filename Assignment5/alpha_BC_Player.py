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
#import random

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

# It should return a list of the form [[move, newState], newRemark].
# The move is a data item describing the chosen move.
# The newState is the result of making the move from the given currentState.
# The newRemark to be returned must be a string.
def makeMove(currentState, currentRemark, timelimit):
    newMoveDesc = 'No move'
    newRemark = "I don't even know how to move!"
    return [[newMoveDesc, currentState], newRemark]
    
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
    return

test_starting_board()


