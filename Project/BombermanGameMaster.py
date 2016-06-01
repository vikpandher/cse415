'''BombermanGameMaster.py

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

if '-c' in sys.argv:
  custom_game = True
  sys.argv.remove('-c')
else:
  custom_game = False

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
    print("Bomberman v" + VERSION + "\n")
    
    print("!!!!!!!!!! BOMBER-MAN !!!!!!!!!!!\n")
    
    if(custom_game):
      print("ENTERING DEFAULTS...")
      board_size = int(input("Select BOARD_SIZE (15): "))
      bomb_blast_radius = int(input("Select BOMB_BLAST_RADIUS (2): "))
      bomb_count_start = int(input("Select BOMB_COUNT_START (4): "))
      initial_bomb_count = int(input("Select INITIAL_BOMB_COUNT (1): "))
      cave_in_tick = int(input("Select BOMB_COUNT_START (100): "))
      bs.set_defaults(board_size, bomb_blast_radius, bomb_count_start, initial_bomb_count, cave_in_tick)
    
    print(bs.INTRO_MESSAGE)
    
    currentState = bs.Bman_state(bs.create_initial_board(), 0, bs.PLAYER_A, [bs.INITIAL_BOMB_COUNT for x in range(bs.PLAYER_COUNT)])
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
        if (len(move) == 0):
          move = "Stay"
        elif (move[0] == bs.M_EAST):
          move = "East"
        elif (move[0] == bs.M_EAST_B):
          move = "B.East"
        elif (move[0] == bs.M_WEST):
          move = "West"
        elif (move[0] == bs.M_WEST_B):
          move = "B.West"
        elif (move[0] == bs.M_SOUTH):
          move = "South"
        elif (move[0] == bs.M_SOUTH_B):
          move = "B.South"
        elif (move[0] == bs.M_NORTH):
          move = "North"
        elif (move[0] == bs.M_NORTH_B):
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
