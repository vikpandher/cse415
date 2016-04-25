'''Jigsaw.py
Vikramjit Pandher, Chloe Nash, CSE 415, Spring 2016, University of Washington
Instructor:  S. Tanimoto.
Assignment 4 Option B: Uncommon Puzzles. 

Status of the implementation:
All required features working. Works with sample puzzles.

'''

#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Jigsaw Puzzle"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['V. Pandher', 'C. Nash']
PROBLEM_CREATION_DATE = "25-APR-2016"
PROBLEM_DESC=\
'''This formulation of the Jigsaw Puzzel uses generic
Python 3 constructs and has been tested with Python 3.5.
'''
#</METADATA>

#<COMMON_CODE>

# Compare all 8 positions in two states. If any is different,
# they're not equal
def DEEP_EQUALS(p1, p2):
  result = True
  for i in range(9):
    result = result and (p1[i] == p2[i])
  return result

def DESCRIBE_STATE(s):
  # Produces a textual description of a state.
  # Might not be needed in normal operation with GUIs.
  txt = "[" + str(s[0]) + ", " + str(s[1]) + ", " + str(s[2]) + "]\n" +\
        "[" + str(s[3]) + ", " + str(s[4]) + ", " + str(s[5]) + "]\n" +\
        "[" + str(s[6]) + ", " + str(s[7]) + ", " + str(s[8]) + "]\n"
  return txt

# Make a string and return it as the hash code
def HASHCODE(s):
  '''The result should be an immutable object such as a string
  that is unique for the state s.'''
  hash = ""
  for i in range(9):
    hash += str(s[i])
  return hash

def copy_state(s):
  # Performs an appropriately deep copy of a state,
  # for use by operators in creating new states.
  new = []
  for i in range(9):
    new.append(s[i])
  return new

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

def goal_test(s):
  '''If the puzzle looks like: [0, 1, 2, 3, 4, 5, 6, 7, 8]
  Then the goal is reached.'''
  result = True
  for i in range(9):
    result = result and (s[i] == i)
  return result

def goal_message(s):
  return "The Basic Eight Puzzle is Solved!"

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

#<INITIAL_STATE>
#INITIAL_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 8] # puzzle0
#INITIAL_STATE = [1, 0, 2, 3, 4, 5, 6, 7, 8] # puzzle1a
#INITIAL_STATE = [3, 1, 2, 4, 0, 5, 6, 7, 8] # puzzle2a
INITIAL_STATE = [1, 4, 2, 3, 7, 0, 6, 8, 5] # puzzle4a
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
OPERATORS = [Operator("Move square from location " + str(p) +\
            " to location "+ str(q),
            lambda s,p=p,q=q: can_move(s,p,q),
            # The default value construct is needed
            # here to capture the values of p&q separately
            # in each iteration of the list comp. iteration.
            lambda s,p=p,q=q: move(s,p,q) )
            for (p, q) in combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
