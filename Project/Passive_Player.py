import BombermanSource as bs
import random

CHOICES = ['Stay', 'East', 'West', 'South', 'North']

def makeMove(currentState):
  '''Moves, but doesn't drop bombs'''
  successors = bs.look_for_successors(currentState)
  
  move = random.choice(CHOICES)
  
  return bs.make_move(currentState, move)