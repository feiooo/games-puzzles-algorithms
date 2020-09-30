#!/usr/bin/env python3
from paint import paint
import sys
from time import sleep
import numpy as np
"""
# Sample format to answer pattern questions 
# assuming the pattern would be frag0:
..*
**.
.**
#############################################
# Reread the instructions for assignment 1: make sure
# that you have the version with due date SUNDAY.
# Every student submits their own assignment.
* Delete the names and ccids below, and put
# the names and ccids of all members of your group, including you. 
# name                         ccid
Fei Yang                       fei5
Tianying Xia                   txia
JingZeng Xie                   jingzeng

#############################################
# Your answer to question 1-a:

*.*
.**
.*.

#############################################
# Your answer to question 1-b:

********.*****...***......*******.*****

#############################################
# Your answer to question 2:
1) What happened to num_nbrs in life-np.py?
    num_nbrs in life.py is rewrited to line 84-92 in life-np.py.
    num_nbrs in life.py is using 1-d list. Every c (c is the number
    of columns) grids are treated as a row. Compared with life.py, 
    life-np.py is using 2-d list to check whether A[j,k]'s neighbours 
    are alive and store the the number of alive neighbours. (j iterates 
    through the row of list and k runs through the column.) In life-np.py,
    because there is no guarded board, line 84-92 also do border check.
    
2) How an infinite grid is implemented in life.py?
    Modified the pad function can implement the infinite grid in life.py.
    (a)if there is any alive cell in first row(non-guard):
            create a new array with column-number size filled with dead cells;
            add the new row before the first cell of the array(first non-guard row);
            row number += 1;
            
       if there is any alive cell in last row(non-guard):
            create a new array with column-number size filled with dead cells;
            add the new row after the last cell of the array(last non-guard row);
            row number += 1;
            
       if there is any alive cell in first column(non-guard):
            create a new array with row-number size filled with dead cells;
            from the first cell of the array, add each new cell every 
            column-number cells (eg. if there are 3 columns, then add one new 
            cell every 3 cells:
            old: [*...**...]    new: [.*....**....]);
            column number += 1;
       if there is any alive cell in last column(non-guard):
            create a new array with row-number size filled with dead cells;
            from the (column)th cell of the array, add each new cell every 
            column-number cells (eg. if there are 3 columns, then add one new 
            cell every 3 cells:
            old: [*...**...]    new: [*....**.....]);        
            column number += 1;
            
    (add new alive cells and add guarded board in other functions, this function 
    is just expand the board)
            

3) How the use of a guarded board simplifies num_nbrs?
    With guarded board, num_nbrs don't need to check whether j will be 
    out of range.


#############################################
# Follow the assignment 1 instructions and
# make the changes requested in question 3.
# Then come back and fill in the answer to
# question 3-c:

....*.........
..*.*.........
...**.........
..............
..............

#############################################
"""
"""
based on life-np.py from course repo
"""


PTS = '.*#'
DEAD, ALIVE, WALL = 0, 1, 2
DCH, ACH, GCH = PTS[DEAD], PTS[ALIVE], PTS[WALL]


def point(r, c, cols): return c + r*cols

"""
board functions
  * represent board as 2-dimensional array
"""


def get_board():
    B = []
    print(sys.argv[1])
    with open(sys.argv[1]) as f:
        for line in f:
            B.append(line.rstrip().replace(' ', ''))
        rows, cols = len(B), len(B[0])
        for j in range(1, rows):
            assert(len(B[j]) == cols)
        return B, rows, cols


def convert_board(B, r, c):  # from string to numpy array
    A = np.zeros((r, c), dtype=np.int8)
    for j in range(r):
        for k in range(c):
            if B[j][k] == ACH:
                A[j, k] = ALIVE
    return A


def expand_grid(A, r, c, t):  # add t empty rows and columns on each side
    N = np.zeros((r+2*t, c+2*t), dtype=np.int8)
    for j in range(r):
        for k in range(c):
            if A[j][k] == ALIVE:
                N[j+t, k+t] = ALIVE
    return N, r+2*t, c+2*t


def print_array(A, r, c):
    print('')
    for j in range(r):
        out = ''
        for k in range(c):
            out += ACH if A[j, k] == ALIVE else DCH
        print(out)


def show_array(A, r, c):
    for j in range(r):
        line = ''
        for k in range(c):
            line += str(A[j, k])
        print(line)
    print('')


""" 
Conway's next-state formula
"""


def next_state(A, r, c):
    
    N = np.zeros((r, c), dtype=np.int8)
    changed = False
    for j in range(r):
        for k in range(c):
            num = 0
            if j > 0 and k > 0 and A[j-1, k-1] == ALIVE:
                num += 1
            if j > 0 and A[j-1, k] == ALIVE:
                num += 1
            if j > 0 and k < c-1 and A[j-1, k+1] == ALIVE:
                num += 1
            if k > 0 and A[j, k-1] == ALIVE:
                num += 1
            if k < c-1 and A[j, k+1] == ALIVE:
                num += 1
            if j < r-1 and k > 0 and A[j+1, k-1] == ALIVE:
                num += 1
            if j < r-1 and A[j+1, k] == ALIVE:
                num += 1
            if j < r-1 and k < c-1 and A[j+1, k+1] == ALIVE:
                num += 1
            if A[j, k] == ALIVE:
                if num > 1 and num < 4:
                    N[j, k] = ALIVE
                else:
                    N[j, k] = DEAD
                    changed = True
            else:
                if num == 3:
                    N[j, k] = ALIVE
                    changed = True
                else:
                    N[j, k] = DEAD
    return N, changed


#############################################
""" 
Provide your code for the function 
next_state2 that (for the usual bounded
rectangular grid) calls the function num_nbrs2,
and delete the raise error statement:
"""


def next_state2(A, r, c):
    N = np.zeros((r, c), dtype=np.int8)
    changed = False
    for j in range(r):
        for k in range(c):
            num = num_nbrs2(A,j,k,r,c)
            if A[j, k] == ALIVE:
                if num > 1 and num < 4:
                    N[j, k] = ALIVE
                else:
                    N[j, k] = DEAD
                    changed = True
            else:
                if num == 3:
                    N[j, k] = ALIVE
                    changed = True
                else:
                    N[j, k] = DEAD
    return N, changed

    #raise NotImplementedError()
#############################################


#############################################
""" 
Provide your code for the function 
num_nbrs2 here and delete the raise error
statement:
"""


def num_nbrs2(A,j,k,r,c):
    num = 0
    if j > 0 and k > 0 and A[j-1, k-1] == ALIVE:
        num += 1
    if j > 0 and A[j-1, k] == ALIVE:
        num += 1
    if j > 0 and k < c-1 and A[j-1, k+1] == ALIVE:
        num += 1
    if k > 0 and A[j, k-1] == ALIVE:
        num += 1
    if k < c-1 and A[j, k+1] == ALIVE:
        num += 1
    if j < r-1 and k > 0 and A[j+1, k-1] == ALIVE:
        num += 1
    if j < r-1 and A[j+1, k] == ALIVE:
        num += 1
    if j < r-1 and k < c-1 and A[j+1, k+1] == ALIVE:
        num += 1
    return num

    #raise NotImplementedError()
#############################################


#############################################
""" 
Provide your code for the function 
next_state_torus here and delete the raise 
error statement:
"""


def next_state_torus(A, r, c):
    N = np.zeros((r, c), dtype=np.int8)
    changed = False
    for j in range(r):
        for k in range(c):
            num = num_nbrs_torus(A,j,k,r,c)
            if A[j, k] == ALIVE:
                if num > 1 and num < 4:
                    N[j, k] = ALIVE
                else:
                    N[j, k] = DEAD
                    changed = True
            else:
                if num == 3:
                    N[j, k] = ALIVE
                    changed = True
                else:
                    N[j, k] = DEAD
    return N, changed
    #raise NotImplementedError()
    
#############################################


#############################################
""" 
Provide your code for the function 
num_nbrs_torus here and delete the raise 
error statement:
"""


def num_nbrs_torus(A,j,k,r,c):
    num = 0
    if A[(j-1+r)%r, (k-1+c)%c] == ALIVE:
        num +=1
    if A[(j-1+r)%r, k] == ALIVE:
        num +=1
    if A[(j-1+r)%r, (k+1+c)%c] == ALIVE:
        num +=1
    if A[j, (k-1+c)%c] == ALIVE:
        num +=1
    if A[j, (k+1+c)%c] == ALIVE:
        num +=1
    if A[(j+1+r)%r, (k-1+c)%c] == ALIVE:
        num +=1
    if A[(j+1+r)%r, k] == ALIVE:
        num +=1
    if A[(j+1+r)%r, (k+1+c)%c] == ALIVE:
        num +=1             
    return num
    #raise NotImplementedError()
#############################################


"""
input, output
"""

pause = 0.2

#############################################
""" 
Modify interact as necessary to run the code:
"""
#############################################


def interact(max_itn):
    itn = 0
    B, r, c = get_board()
    print(B)
    X = convert_board(B, r, c)
    A, r, c = expand_grid(X, r, c, 0)
    print_array(A, r, c)
    while itn <= max_itn:
        sleep(pause)
        #newA, delta = next_state(A, r, c)
        newA, delta = next_state_torus(A, r, c)
        if not delta:
            break
        itn += 1
        A = newA
        print_array(A, r, c)
    print('\niterations', itn)


def main():
    interact(177)


if __name__ == '__main__':
    main()
