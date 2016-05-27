import time
import random

PLAYER1 = 1
PLAYER2 = 2
PLAYER1_BOMBS = [5,4,3]
PLAYER2_BOMBS = [8,7,6]
EXPLODE = [2,5]
BARRIER = 20
EMPTY = 0
DEAD = 50
DROP_BOMB = 1
DONT_DROP_BOMB = 0
BOARD_SIZE = 11

ACTIONS = ['North', 'South', 'East', 'West', 'Stay']

INIT_TO_CODE = {'XX':10, '##':20, 'AA':1, 'BB':2, 'A3':5, 'A2':4,
                'A1':3, 'B3':8, 'B2':7, 'B1':6, '!!':50, '--':0}
CODE_TO_INIT = {10:'XX', 20:'##', 1:'AA', 2:'BB', 5:'A3', 4:'A2',
                3:'A1', 8:'B3', 7:'B2', 6:'B1', 50:'!!', 0:'--'}

def parse(bs): # bs is board string
  '''Translate a board string into the list of lists representation.'''
  b = [[0,0,0,0,0,0,0,0,0,0,0] for r in range(BOARD_SIZE)]
  rs12 = bs.split("\n")
  rs11 = rs12[1:] # eliminate the empty first item.
  for iy in range(BOARD_SIZE):
    rss = rs11[iy].split(' ');
    for jx in range(BOARD_SIZE):
      b[iy][jx] = INIT_TO_CODE[rss[jx]]
  return b

INITIAL = ('''
XX XX XX XX XX XX XX XX XX XX XX
XX AA -- -- -- ## -- -- -- -- XX
XX -- XX -- XX -- XX -- XX -- XX
XX -- -- ## -- ## -- ## -- -- XX
XX -- XX -- XX -- XX -- XX -- XX
XX ## -- ## -- ## -- ## -- ## XX
XX -- XX -- XX -- XX -- XX -- XX
XX -- -- ## -- ## -- ## -- -- XX
XX -- XX -- XX -- XX -- XX -- XX
XX -- -- -- -- ## -- -- -- BB XX
XX XX XX XX XX XX XX XX XX XX XX
''')

class Bman_state:
  def __init__(self, old_board=INITIAL, whose_move=PLAYER1):
    new_board = [r[:] for r in old_board]
    self.board = new_board
    self.whose_move = whose_move

  def __repr__(self):
    s = ''
    for r in range(BOARD_SIZE):
      for c in range(BOARD_SIZE):
        s += CODE_TO_INIT[self.board[r][c]] + " "
      s += "\n"
    if self.whose_move==PLAYER1: s+= "Player2's move"
    else: s+= "Player1's move"
    s+= "\n"
    return s

def makeMove(state):
  location = getPlayerLocation(state)
  possible_actions = canMove(state, location)
  possible_moves = canBomb(possible_actions, location)
  print("Possible actions:")
  print(str(possible_actions))
  print("Possible moves:")
  print(str(possible_moves))

  move = random.choice(possible_moves)
  print("chosen move: " + str(move))

  new_state = transformState(state, location, move)
  print("New state after making move:")
  print(new_state)
  return new_state

def transformState(old_state, old_location, move):
  new_board = [r[:] for r in old_state.board]
  new_location = move[0]
  oldx,oldy = old_location
  newx,newy = new_location
  new_board = transformDeaths(new_board)
  new_board[newx][newy] = new_board[oldx][oldy]
  if move[1] == DROP_BOMB:
    player_bomb = PLAYER1_BOMBS[0] 
    if old_state.whose_move == PLAYER2:
      player_bomb = PLAYER2_BOMBS[0] 
    new_board[oldx][oldy] = player_bomb
  elif old_location == move[0]:
    new_board[oldx][oldy] = new_board[oldx][oldy]
  else :
    new_board[oldx][oldy] = EMPTY
  new_state = transformBombs(Bman_state(new_board, old_state.whose_move))
  return new_state

def transformDeaths(board):
  new_board = [r[:] for r in board]
  for r in range(BOARD_SIZE):
    for c in range(BOARD_SIZE):
      if new_board[r][c] == DEAD:
        new_board[r][c] = EMPTY
  return new_board

def transformBombs(state):
  new_board = [r[:] for r in state.board]
  players = PLAYER1_BOMBS
  if state.whose_move == PLAYER2:
    players = PLAYER2_BOMBS
  for r in range(BOARD_SIZE):
    for c in range(BOARD_SIZE):
      if new_board[r][c] in players:
        new_bomb = new_board[r][c] - 1
        if new_bomb in EXPLODE:
          new_board = transformExplode(state, r, c)
        else:
          new_board[r][c] = new_bomb
  return Bman_state(new_board, state.whose_move)

def transformExplode(state, x, y):
  new_board = [r[:] for r in state.board]
  clear = True
  currx = x
  curry = y
  other_player = PLAYER2
  if state.whose_move == PLAYER2:
    other_player = PLAYER1
  new_board[currx][curry] = DEAD
  while clear:
    if currx + 1 < BOARD_SIZE - 1:
      currx += 1
      if new_board[currx][y] == EMPTY or new_board[currx][y] == other_player or new_board[currx][y] == BARRIER:
        new_board[currx][y] = DEAD
      else:
        break
    else:
      break
  currx = x
  while clear:
    if currx - 1 > 0:
      currx -= 1
      if new_board[currx][y] == EMPTY or new_board[currx][y] == other_player or new_board[currx][y] == BARRIER:
        new_board[currx][y] == DEAD
      else:
        break
    else:
      break
  while clear:
    if curry + 1 < BOARD_SIZE - 1:
      curry += 1
      if new_board[x][curry] == EMPTY or new_board[x][curry] == other_player or new_board[x][curry] == BARRIER:
        new_board[x][curry] = DEAD
      else:
        break
    else:
      break
  curry = y
  while clear:
    if curry - 1 > 0:
      curry -= 1
      if new_board[x][curry] == EMPTY or new_board[x][curry] == other_player or new_board[x][curry] == BARRIER:
        new_board[x][curry] = DEAD
      else:
        break
    else:
      break
  return new_board

# assumes player is in a legitimate board position and returns list of
# actions that the player can take
def canMove(state, player_location):
  x,y = player_location
  print("x: " + str(x) + " y: " + str(y))
  actions = [(x,y)]
  if state.board[x][y+1] == EMPTY:
    actions.append((x, y+1))
  if state.board[x+1][y] == EMPTY:
    actions.append((x+1, y))
  if state.board[x][y-1] == EMPTY:
    actions.append((x, y-1))
  if state.board[x-1][y] == EMPTY:
    actions.append((x-1, y))
  return actions

def canBomb(actions, player_location):
  moves = []
  for action in actions:
    if action != player_location:
      moves.append([action, DROP_BOMB])
      moves.append([action, DONT_DROP_BOMB])
    else: moves.append([action, DONT_DROP_BOMB])
  return moves

def getPlayerLocation(state):
  for r in range(BOARD_SIZE):
    for c in range(BOARD_SIZE):
      if state.board[r][c] == state.whose_move:
        return (r,c)
  return (0,0)

def checkWin(state, player):
  curr_board = state.board
  player_check = PLAYER2
  if player == PLAYER2:
    player_check = PLAYER1
  for r in range(BOARD_SIZE):
    for c in range(BOARD_SIZE):
      if curr_board[r][c] == player_check:
        return False
  print("Player" + str(player) + " won!")
  return True


def play():
  print("Initial board:")
  print(INITIAL)
  print("Board represented as array:")
  print(str(parse(INITIAL)))
  init_state = Bman_state(parse(INITIAL), PLAYER1)
  print("Board converted back to string:")
  print(init_state)

  #print("Check win function:")
  #checkWin(init_state, PLAYER1)

  curr = init_state
  move = 1
  while not checkWin(curr, PLAYER1):
    print("Make move function " + str(move) + " :")
    new = makeMove(curr)
    curr = new
    move += 1
  print("Took " + str(move) + " moves to win")

play()

FINISHED = False



def runGame():
  currentState = INITIAL_STATE
  print("!!!!!!BOMBERMAN!!!!!!")
  while not FINISHED:
    print(currentState)
    time.sleep(1)
#runGame()
