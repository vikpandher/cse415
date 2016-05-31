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

if len(sys.argv) > 2:
  import importlib
  human_match = False
  cpuA = importlib.import_module(sys.argv[1])
  cpuB = importlib.import_module(sys.argv[2])
elif len(sys.argv) > 1:
  import importlib
  human_match = True
  cpuA = importlib.import_module(sys.argv[1])
  cpuB = None
else:
  human_match = True
  import Random_Player as playerA
  cpuB = None





CURRENT_PLAYER = bs.PLAYER_A

FINISHED = False
def runGame():
    currentState = bs.Bman_state()
    print("Bomberman v" + VERSION + "\n")
    
    print("!!!!!!!!!! BOMBER-MAN !!!!!!!!!!!")
    print(currentState)
    
    whosTurn = 0
    global FINISHED
    FINISHED = False
    '''
    while not FINISHED:
        result = whosTurn.makeMove(currentState)
        
        if(endCheck )
    
    
    
    
        who = currentState.whose_move
        if who==bcs.WHITE:
            side = 'WHITE'
        else:
            side = 'BLACK'
        global CURRENT_PLAYER
        CURRENT_PLAYER = who
        if VALIDATE_MOVES:
            legal_states = bcs.successors(currentState)
            if legal_states==[]:
                print("Stalemate: "+side+" has no moves!"); break
        if WHITEsTurn:
            playerResult = timeout(player1.makeMove,args=(currentState, currentRemark, TIME_PER_MOVE), kwargs={}, timeout_duration=TIME_PER_MOVE, default=(None,"I give up!"));
            name = player1.nickname()
            WHITEsTurn = False
        else:
            playerResult = timeout(player2.makeMove,args=(currentState, currentRemark, TIME_PER_MOVE), kwargs={}, timeout_duration=TIME_PER_MOVE, default=(None,"I give up!"));
            name = player2.nickname()
            WHITEsTurn = True
        moveAndState, currentRemark = playerResult
        if moveAndState==None:
            FINISHED = True; continue
        if VALIDATE_MOVES:
            if not OCCURS_IN(moveAndState[1], legal_states):
                print("Illegal move by "+side+" as "+str(moveAndState[0]))
                print("Returned state is:")
                print(moveAndState[1])
                break
        move, currentState = moveAndState
        moveReport = "Turn "+str(turnCount)+": Move is by "+side+" as "+str(move)
        print(moveReport)
        utteranceReport = name +' says: '+currentRemark
        print(utteranceReport)
        possibleWin = winTester(currentState)
        if possibleWin != "No win":
            FINISHED = True
            print(currentState)
            print(possibleWin)
            return
        print(currentState)
        turnCount += 1
        #if turnCount == 9: FINISHED=True
    print(currentState)
    print("Game over.")
'''

import sys
import time
from traceback import print_exc
def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    '''This function will spawn a thread and run the given function using the args, kwargs and 
    return the given default value if the timeout_duration is exceeded 
    ''' 
    import threading
    class PlayerThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = default
        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except:
                print("Seems there was a problem with the time.")
                print_exc()
                self.result = default

    pt = PlayerThread()
    #print("timeout_duration = "+str(timeout_duration))
    pt.start()
    started_at = time.time()
    #print("makeMove started at: " + str(started_at))
    pt.join(timeout_duration)
    ended_at = time.time()
    #print("makeMove ended at: " + str(ended_at))
    diff = ended_at - started_at
    print("Time used in makeMove: %0.4f seconds out of " % diff, timeout_duration)
    if pt.isAlive():
        print("Took too long.")
        print("We are now terminating the game.")
        print("Player "+PLAYER_MAP[CURRENT_PLAYER]+" loses.")
        if USE_HTML: gameToHTML.reportResult("Player "+PLAYER_MAP[CURRENT_PLAYER]+" took too long (%04f seconds) and thus loses." % diff)
        if USE_HTML: gameToHTML.endHTML()
        exit()
    else:
        print("Within the time limit -- nice!")
        return pt.result


def OCCURS_IN(state, listOfStates):
  for s in listOfStates:
    if DEEP_EQUALS(state, s):
        return True
  return False

def DEEP_EQUALS(s1, s2):
  if s1.whose_move != s2.whose_move:
    return False
  b1 = s1.board
  b2 = s2.board
  for i in range(8):                  
    for j in range(8):                  
      if b1[i][j] != b2[i][j]: return False
  return True
                      
runGame()
