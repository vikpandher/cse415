'''
Chloe Nash

This program runs EightPuzzleWithHeuristics and implements the given
heuristic.  Runs h_euclidean and puzzle2a as default parameters if no
arguments are passed in.
'''


# AStar.py
# Iterative Best-First Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET" file format.
# Examples of Usage:
# python3 AStar.py EightPuzzleWithHeuristics h_euclidean puzzle2a.py

import sys
# maintains the priority queue
from heapq import heappush, heappop 

if sys.argv==[''] or len(sys.argv)<2:
    import Pentaminoes2 as Problem
    Heuristic = 'h_custom'
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1])
  Heuristic = sys.argv[2]


print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}

def runAStar():
  initial_state = Problem.CREATE_INITIAL_STATE()
  print("Initial State:")
  print(Problem.DESCRIBE_STATE(initial_state))
  global COUNT, BACKLINKS
  COUNT = 0
  BACKLINKS = {}
  IterativeAStar(initial_state)
  print(str(COUNT)+" states examined.")

def IterativeAStar(initial_state):
    global COUNT, BACKLINKS
    OPEN = []
    heappush(OPEN, (Problem.HEURISTICS[Heuristic](initial_state), initial_state))
    CLOSED = []
    BACKLINKS[Problem.HASHCODE(initial_state)] = -1

    while OPEN != []:
        
        S = heappop(OPEN)[1]
        CLOSED.append(S)

        if Problem.GOAL_TEST(S):
          print(Problem.GOAL_MESSAGE_FUNCTION(S))
          backtrace(S)
          return

        COUNT += 1
        if (COUNT % 32)==0:
           print(".",end="")
           if (COUNT % 128)==0:
             print("COUNT = "+str(COUNT))
             print("len(OPEN)="+str(len(OPEN)))
             print("len(CLOSED)="+str(len(CLOSED)))
             
        for op in Problem.OPERATORS:
          #Optionally uncomment the following when debugging
          #a new problem formulation.
          #print("Trying operator: "+op.name)
          if op.precond(S):
            new_state = op.state_transf(S)
            if not occurs_in(new_state, CLOSED):
                heappush(OPEN, (Problem.HEURISTICS[Heuristic](new_state), new_state))              
                BACKLINKS[Problem.HASHCODE(new_state)] = S
                #Uncomment for debugging:
                #print(Problem.DESCRIBE_STATE(new_state))

def backtrace(S):
  global BACKLINKS
  path = []
  while not S == -1:
    print(S)
    path.append(S)
    S = BACKLINKS[Problem.HASHCODE(S)]
  path.reverse()
  print("Solution path: ")
  for s in path:
    print(Problem.DESCRIBE_STATE(s))
  return path    
  

def occurs_in(s1, lst):
  for s2 in lst:
    if Problem.DEEP_EQUALS(s1, s2): return True
  return False

if __name__=='__main__':
  runAStar()
