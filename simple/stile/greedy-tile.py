# simple bfs program to solve sliding tile
from collections import deque
#from random import shuffle
from time import sleep, time
from sys import stdin

def int2chr(t): # nonneg int to single in '0123456789ABCDEFGHIJ...'
  if t <= 9: return chr(t+ord('0'))
  else:      return chr(t-10 + ord('A'))

def chr2int(c): # chr in '0123456789ABCDEFGHIJ...' to int
  if c in '0123456789': return ord(c) - ord('0')
  else: return 10 + ord(c) - ord('A')

def list2str(L): # list nonneg ints to string monochars
  s = ''
  for x in L: s += int2chr(x)
  return s

def pretty(s,cols,monochar): # string to printable matrix
  # if monochar true: print elements as monochars 
  # else:             print elements as ints
  count, outstr, BLANK = 0, '', ' '
  for x in s:
    count += 1
    if monochar:  
      if x == '0': outstr += ' ' + BLANK
      else:        outstr += ' ' + x
    else:
      if   x == '0':          outstr += '  ' + BLANK     # blank
      elif x in ' 123456789': outstr += '  ' + x         # digit
      else:                   outstr += ' ' + str(chr2int(x))   # 2 digits
    if count%cols == 0: outstr += '\n'
  #sleep(.005)
  return outstr

def str_swap(s,lcn,shift): # swap chars at s[lcn], s[lcn+shift]
  a , b = min(lcn,lcn+shift), max(lcn,lcn+shift)
  return s[:a] + s[b] + s[a+1:b] + s[a] + s[b+1:]

class Tile:
  """a sliding tile class with simple search"""

  def __init__(self):
    # state will be the starting state of any computer search
    # initialized from stdin, 0 is blank, 
    # format: r c then tile entries, row by row, e.g.:
    # 2 3
    # 2 0 5
    # 4 1 3
    self.state = []
    for line in stdin:
      for elem in line.split():
        self.state.append(int(elem))
    # rows, cols are 1st 2 elements of list, so pop them
    self.rows, self.cols = self.state.pop(0), self.state.pop(0)
    # state now holds contents of tile in row-major order
    
    # assert 
    #   - at least 2 rows, at least 2 cols, 
    #   - all entries in [0 .. r*c-1], and
    #   - some entry 0
    assert(self.rows>=2 and self.cols>=2)
    for s in self.state: assert(s>=0 and s < self.rows*self.cols)
    ndx_min = self.state.index(min(self.state))
    assert(self.state[ndx_min] == 0)

    # these shifts of .state indices effect moves of the blank:
    self.LF, self.RT, self.UP, self.DN = -1, 1, -self.cols, self.cols
    self.shifts = [self.LF, self.RT, self.UP, self.DN] #left right up down

  def legal_shifts(self,psn): # list of legal shifts
    S = []
    c,r = psn % self.cols, psn // self.cols # column number, row number
    if c > 0:           S.append(self.LF)
    if c < self.cols-1: S.append(self.RT)
    if r > 0:           S.append(self.UP)
    if r < self.rows-1: S.append(self.DN)
    return S

  def compute_num_invers(self, input):
    count = 0
    L = list(input)
    L.remove('0')
    for x in range(len(L) - 1):
      for y in L[x + 1: ]:
        if L[x] > y:
          count += 1
    return count

  def targetlist(self, n):  # return target state, as list
    L = []
    for j in range(1, n): L.append(j)
    L.append(0)
    return L

  def greedy(self):
    start = list2str(self.state)
    target = list2str(self.targetlist(self.rows * self.cols))
    Parent = {start: start}
    iteration, nodes_this_level, Levels = 0, 1, [1]
    print("Start at position 2:")

    while True:
      print(pretty(start, self.cols, True))
      if start == target:
        print('Found solution.')
        break

      iteration += 1
      ndx0 = start.index('0')
      num_invers = []
      store_state = []
      direction = []

      for shift in self.legal_shifts(ndx0):
        nbr = str_swap(start, ndx0, shift)
        if nbr not in Parent:
          num_invers.append(self.compute_num_invers(nbr))
          store_state.append(nbr)
          dire = ndx0 - nbr.index('0')
          if dire == 1:
            direction.append('>')
          elif dire == -1:
            direction.append('<')
          elif dire == self.cols:
            direction.append('v')
          else:
            direction.append('^')

      if len(num_invers) == 0:
        print("\nThe greedy algorithm can't find the solution.")
        break

      for x in range(len(num_invers)):
        print( "Legal move direction is", direction[x], "has", num_invers[x], "inversions and the state", store_state[x])
      move = num_invers.index(min(num_invers))
      Parent[store_state[move]] = start
      start = store_state[move]
      print("Choice", direction[move], ", then the state below:")

    print("Total", iteration, "moves.\n")

st = Tile()
st.greedy()
