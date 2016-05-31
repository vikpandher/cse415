import BombermanSource as bs
import random

def makeMove(currentState):
  '''Make a random move.'''
  successors = bs.look_for_successors(currentState)
  
  if(len(successors) != 0):
    nextSuccessor = random.choice(successors)
    return nextSuccessor
  
  print("Oh no!")
  return currentState