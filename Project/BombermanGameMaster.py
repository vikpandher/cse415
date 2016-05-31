'''BombermanGameMaster.py based on TimedGameMaster.py based on GameMaster.py 
 which in turn is based on code from RunKInARow.py

V. Pandher

'''
VERSION = '1.0-ALPHA'

import BombermanSource as bs

# Get names of players and from the command line.
import sys

#print(len(sys.argv))
#print(sys.argv[0])

'''
NOTE:
For a match between two computers enter:
python BombermanGameMaster.py [plyer file name] [plyer file name]
ex: python BombermanGameMaster.py Random_Player Random_Player

For a match against a computer enter:
python BombermanGameMaster.py [plyer file name]
ex: python BombermanGameMaster.py Random_Player

'''

if len(sys.argv) > 2:
  import importlib
  human_match = False
  cpuA = importlib.import_module(sys.argv[1])
  cpuB = importlib.import_module(sys.argv[2])
elif len(sys.argv) > 1:
  import importlib
  human_match = True
  cpuA = None
  cpuB = importlib.import_module(sys.argv[1])
else:
  human_match = True
  cpuA = None
  import Passive_Player as cpuB

CURRENT_PLAYER = bs.PLAYER_A

FINISHED = False
def runGame():
    currentState = bs.Bman_state()
    print("Bomberman v" + VERSION + "\n")
    
    print("!!!!!!!!!! BOMBER-MAN !!!!!!!!!!!\n")
    print(bs.INTRO_MESSAGE)
    
    whosTurn = currentState.player
    global FINISHED
    FINISHED = False
    
    turnLimit = -1
    
    while not FINISHED and turnLimit != 0:
      turnLimit -= 1
      whosTurn = currentState.player
      print(currentState)
      
      whoWon = bs.win_check(currentState)
      if(whoWon != -1):
        print(bs.win_message(whoWon))
        break
      
      if (human_match and whosTurn == bs.PLAYER_A):
        move = input("Enter your move:")
        if (move == "e"):
          move = "East"
        elif (move == "E"):
          move = "B.East"
        elif (move == "w"):
          move = "West"
        elif (move == "W"):
          move = "B.West"
        elif (move == "s"):
          move = "South"
        elif (move == "S"):
          move = "B.South"
        elif (move == "n"):
          move = "North"
        elif (move == "N"):
          move = "B.North"
        else:
          move = "Stay"
        print(move)
        currentState = bs.make_move(currentState, move)
      elif (whosTurn == bs.PLAYER_A):
        currentState = cpuA.makeMove(currentState)
      elif (whosTurn == bs.PLAYER_B):
        currentState = cpuB.makeMove(currentState)
       
runGame()
