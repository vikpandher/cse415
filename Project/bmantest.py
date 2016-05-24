import time

INITIAL_STATE = ('''
X X X X X X X X X X X
X         #         X
X   X   X   X   X   X
X     #   #   #     X
X   X   X   X   X   X
X #   #   #   #   # X
X   X   X   X   X   X
X     #   #   #     X
X   X   X   X   X   X
X         #         X
X X X X X X X X X X X
''')


FINISHED = False



def runGame():
  currentState = INITIAL_STATE
  print("!!!!!!BOMBERMAN!!!!!!")
  while not FINISHED:
    print(currentState)
    time.sleep(1)
runGame()