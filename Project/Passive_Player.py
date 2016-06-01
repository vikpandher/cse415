'''
Player for Bomberman that just makes random moves, but won't drop bombs.
Dies from cave ins.
'''

import BombermanSource as bs
import random

CHOICES = ['Stay', 'East', 'West', 'South', 'North']

def makeMove(currentState):
  '''Moves, but doesn't drop bombs'''
  move = random.choice(CHOICES)
  
  return bs.make_move(currentState, move)