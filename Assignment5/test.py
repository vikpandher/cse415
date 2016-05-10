BLACK = 0
WHITE = 1

INIT_TO_CODE = {'p':2, 'P':3, 'c':4, 'C':5, 'l':6, 'L':7, 'i':8, 'I':9,
  'w':10, 'W':11, 'k':12, 'K':13, 'f':14, 'F':15, '-':0}

CODE_TO_INIT = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}

CODE_TO_VALUE = {0:0,2:-10,3:10,4:-60,5:60,6:-80,7:80,8:-70,9:70,
                 10:-40,11:40,12:-100,13:100,14:-50,15:50}

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

TEST_5 = parse('''
- - - - - - - -
- - - - - - - -
- - w w w - - -
- - w I - l - -
- - - - - - - -
- l - l - - - -
- - - - - - l -
- - - - - - - -
''')

PINCER_TEST_2 = parse('''
- - - i - - - -
- - - i - - - -
- - - - - - - -
- p - P - i i -
- - - - - - - -
- I p - p I - -
- - - p - - - -
- - - I - - - -
''')

class BC_state:
  def __init__(self, old_board=INITIAL, whose_move=WHITE):
    new_board = [r[:] for r in old_board]
    self.board = new_board
    self.whose_move = whose_move

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

def staticEval(state):
  value = 0
  board = state.board
  B_IsCheckMate = True
  W_IsCheckMate = True
  for row in range(8):
    for col in range(8):
      if board[row][col] == 12:
        B_IsCheckMate = False
      if board[row][col] == 13:
        W_IsCheckMate = False
      value += CODE_TO_VALUE[board[row][col]]
  if B_IsCheckMate:
    value += 1000
  if W_IsCheckMate:
    value -= 1000
  return value

print(PINCER_TEST_2)
print(staticEval(BC_state(PINCER_TEST_2, WHITE)))
