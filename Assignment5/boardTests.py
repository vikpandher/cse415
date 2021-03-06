INIT_TO_CODE = {'p':2, 'P':3, 'c':4, 'C':5, 'l':6, 'L':7, 'i':8, 'I':9,
  'w':10, 'W':11, 'k':12, 'K':13, 'f':14, 'F':15, '-':0}

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

# white pincer movement
W_PINCER_TEST_0 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - P - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

# black pincer movement
B_PINCER_TEST_0 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - p - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

# white pincer kill
W_PINCER_TEST_1 = parse('''
- - - K - - - -
- - - f - - - -
- - - - - - - -
I f - P - f I -
- - - - - - - -
- - - f - - - -
- - - P - - - -
- - - - - - - -
''')

# black pincer kill
B_PINCER_TEST_1 = parse('''
- - - i - - - -
- - - F - - - -
- - - - - - - -
i F - p - F i -
- - - - - - - -
- - - F - - - -
- - - i - - - -
- - - - - - - -
''')

# white pincer multi kill
W_PINCER_TEST_2 = parse('''
- - - f - - - -
- - - I - - - -
I f - - - - - -
I f - P - f I -
- - - - - - - -
- I f - f I - -
- - - f - - - -
- - - I - - - -
''')

# black pincer multi kill
B_PINCER_TEST_2 = parse('''
- - - i - - - -
- - - F - - - -
- i F - F i - -
i F - - - - - -
i F - p - F i -
- f I - I f - -
- - - F - - - -
- - - i - - - -
''')

# black pincer kill pincer
B_PINCER_TEST_2 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - p - - - -
- - - - - - - -
- - - P - - - -
- - - - - - - -
- - - - - - - -
''')

# white king movement
W_KING_TEST_0 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - K - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

# black king movement
B_KING_TEST_0 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - k - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

# white king kill
W_KING_TEST_1 = parse('''
- - - - - - - -
- - - - - - - -
- - i i i - - -
- - i K i - - -
- - i i i - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

# black king kill
B_KING_TEST_1 = parse('''
- - - - - - - -
- - - - - - - -
- - I I I - - -
- - I k I - - -
- - I I I - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

# white king no kill
W_KING_TEST_2 = parse('''
- - - - - - - -
- - - f - - - -
- - I I I - - -
- f I K I f - -
- - I I I - - -
- - - f - - - -
- - - - - - - -
- - - - - - - -
''')

# black king no kill
B_KING_TEST_2 = parse('''
- - - - - - - -
- - - F - - - -
- - i i i - - -
- F i k i F - -
- - i i i - - -
- - - F - - - -
- - - - - - - -
- - - - - - - -
''')

# white withdrawer movement
W_WITHDRAWER_TEST_0 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - W - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

# black withdrawer movement
B_WITHDRAWER_TEST_0 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - w - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

# white withdrawer movement collision
W_WITHDRAWER_TEST_1 = parse('''
i F - f - - - -
- - - I - - F -
- - - - - i - -
f I - W - - - -
- - I - - - - -
- - f - - - - -
- - - - - - i -
- - f I - - - F
''')

# black withdrawer movement collision
B_WITHDRAWER_TEST_1 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
f I - w - - i F
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

# white withdrawer kill
W_WITHDRAWER_TEST_2 = parse('''
- - - - - - - -
- - - - - - - -
- - W p - - - -
- p p p - - - -
- - - - i i i -
- - - - i W - -
- - - - - - - -
- - - - - - - -
''')

# black withdrawer kill
B_WITHDRAWER_TEST_2 = parse('''
- - - - - - - -
- - - - - - - -
- - w P - - - -
- P P P - - - -
- - - - I K C -
- - - - I w - -
- - - - - - - -
- - - - - - - -
''')

# white leaper movement collision
W_LEAPER_TEST_0 = parse('''
f F - f F - f -
- - - - - - F -
- - - - - - - -
F f - L - - F -
- - - - - - - f
- - - - - - - -
F - - - - - - f
f - - F f - - F
''')

# black leaper movement collision
B_LEAPER_TEST_0 = parse('''
f F - f F - f -
- - - - - - F -
- - - - - - - -
f F - l - - f -
- - - - - - - F
- - - - - - - -
F - - - - - - f
f - - F f - - F
''')

# white leaper kill
W_LEAPER_TEST_1 = parse('''
- - - - - - - -
- i - i - i - -
- - - - - - - -
- i - L - - i -
- - - - - - - -
- i - - - i - -
- - - i - - - -
- - - - - - - -
''')

# black leaper kill
B_LEAPER_TEST_1 = parse('''
- - - - - - - -
- P - P - P - -
- - - - - - - -
- P - l - - P -
- - - - - - - -
- P - - - P - -
- - - P - - - -
- - - - - - - -
''')

# white leaper shouldn't kill
W_LEAPER_TEST_2 = parse('''
F - - F - - F -
- f - f - f - -
- - - - - - - -
F f - L - - F f
- - - - - - - -
- F - - - F - -
f - - F - - f -
- - - f - - - -
''')

# black leaper shouldn't kill
B_LEAPER_TEST_2 = parse('''
F - - F - - F -
- f - f - f - -
- - - - - - - -
F f - l - - F f
- - - - - - - -
- F - - - F - -
f - - F - - f -
- - - f - - - -
''')

# white leaper shouldn't kill friendly
W_LEAPER_TEST_3 = parse('''
- - - - - - - -
- - - F f F - -
- f F - - - - -
- - F L - - F -
- - - - - - f -
- F - - - F - -
- - f F - - f -
- - - - - - - -
''')

# white freezer movement collision
W_FREEZER_TEST_0 = parse('''
f F - f F - f -
- - - - - - F -
- - - - - - - -
F f - F - - F -
- - - - - - - f
- - - - - - - -
F - - - - - - f
f - - F f - - F
''')

# black freezer movement collision
B_FREEZER_TEST_0 = parse('''
f F - f F - f -
- - - - - - F -
- - - - - - - -
f F - f - - f -
- - - - - - - F
- - - - - - - -
F - - - - - - f
f - - F f - - F
''')

# white coordinator kill
W_COORDINATOR_TEST_0 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - C - - - -
p - - K - p - -
- - - f - - - -
- - - p - - - -
- - - - - - - -
''')

# black coordinator kill
B_COORDINATOR_TEST_0 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - c - - - -
P - - k - P - -
- - - F - - - -
- - - P - - - -
- - - - - - - -
''')

# white coordinator kill row and col to 0
W_COORDINATOR_TEST_1 = parse('''
K f f - - - - -
f - - - - - - -
f - - - - - - -
- - - C - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

# white coordinator kill row and col to 8
W_COORDINATOR_TEST_2 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - C - - -
- - - - - - - f
- - - - - - - f
- - - - - f f K
''')

# black coordinator kill row and col to 0
B_COORDINATOR_TEST_1 = parse('''
k F F - - P - -
F - - - - - - -
F - - - - - - -
- - - c - - - -
- - - - - - - -
P - - - - - - -
- - - - - - - -
- - - - - - - -
''')

# black coordinator kill row and col to 8
B_COORDINATOR_TEST_2 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - P
- - - - - - - -
- - - - c - - -
- - - - - - - F
- - - - - - - F
- - P - - F F k
''')

# white imitator movement
W_IMITATOR_TEST_0 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - I - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

# black imitator movement
B_IMITATOR_TEST_0 = parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - i - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

# black imitator kill king, coordinator, withdrawer, leaper
B_IMITATOR_TEST_1 = parse('''
- - - - - - - -
- - - - - - - f
- - K W C - k F
- - L i K - - -
- - W K C - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
''')

# black imitator kill pincher
B_IMITATOR_TEST_2 = parse('''
- - F f - - - -
- F f P - - F -
F f P - - P f -
f P - i - - P f
- f P - - P f F
- F f P - - - -
- - F f - - - -
- - - - - - - -
''')

# test 2nd rows
QUEENS_TEST_0 = parse('''
c l i w k i l f
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
F L I W K I L C
''')

W_LEAPER_TEST_4 = parse('''
c l i w k i l f
p p p p p p - p
- - - - - - - P
- - - - C - - -
- - - - - - - -
- - - - - - p -
P P P P P P P L
F L I W K I - -
''')
