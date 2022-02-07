#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

import sys
from queue import PriorityQueue 

ROWS=5
COLS=5


def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

def heuristic(state,turn):
    D_to_Goal=0
    for i in range(ROWS*COLS):
        #calculating the No of steps we need to take in terms of row which also include wrapping and circular conditions
        rowsteps=min(  ( (i//COLS) - ((state[i]-1)//COLS) )%ROWS, ( ((state[i]-1)//COLS) - (i//COLS) )%ROWS   )
        #calculating the No of steps we need to take in terms of columns which also include wrapping and circular conditions
        columnsteps= min( ( (i%COLS) - ((state[i]-1)%COLS) )%COLS, ( ((state[i]-1)%COLS) -(i%COLS) )%COLS )
        
        #Adding row and column steps to D_to_Goal to calculate the total no of steps
        D_to_Goal=D_to_Goal+ + rowsteps+ columnsteps
        
    #Normalizing the Heuristic based on the move
    if turn=='O':
        D_to_Goal=D_to_Goal/16
    elif turn=='I':
        D_to_Goal=D_to_Goal/8
    else:
        D_to_Goal=D_to_Goal/5
    
    return D_to_Goal
    
    
        
        


# return a list of possible successor states
def successors(state,path,NoofstepsTaken,lenthtogoalstate):
    successor=[]
    parent=list(state)
    #getting all the patterns for columns up and down
    for c in range(5):
        parent[c],parent[5+c],parent[10+c],parent[15+c],parent[20+c]=parent[5+c],parent[10+c],parent[15+c],parent[20+c],parent[c]
        length_to_goal=heuristic(parent,'U')
        successor.append((NoofstepsTaken+1+length_to_goal,parent,path+" "+'U'+str(c+1),NoofstepsTaken+1,length_to_goal))
        parent=list(state)
        parent[c],parent[5+c],parent[10+c],parent[15+c],parent[20+c]=parent[20+c],parent[c],parent[5+c],parent[10+c],parent[15+c]
        length_to_goal=heuristic(parent,'D')
        successor.append((NoofstepsTaken+1+length_to_goal,parent,path+" "+'D'+str(c+1),NoofstepsTaken+1,length_to_goal))
        parent=list(state)
    #Getting all the pattern for rows left and right
    for r in range(5):
       parent[r*5+0],parent[r*5+1],parent[r*5+2],parent[r*5+3],parent[r*5+4]=parent[r*5+1],parent[r*5+2],parent[r*5+3],parent[r*5+4],parent[r*5+0]
       length_to_goal=heuristic(parent,'L')
       successor.append((NoofstepsTaken+1+length_to_goal,parent,path+" "+'L'+str(r+1),NoofstepsTaken+1,length_to_goal))
       parent=list(state)
       parent[r*5+0],parent[r*5+1],parent[r*5+2],parent[r*5+3],parent[r*5+4]=parent[r*5+4],parent[r*5+0],parent[r*5+1],parent[r*5+2],parent[r*5+3]
       length_to_goal=heuristic(parent,'R')
       successor.append((NoofstepsTaken+1+length_to_goal,parent,path+" "+'R'+str(r+1),NoofstepsTaken+1,length_to_goal))
       parent=list(state)
    #getting outer ring pattern both clockwise and counter clockwise
    #counter clockwise
    m=parent[0]
    parent[0],parent[1],parent[2],parent[3],parent[4]=parent[1],parent[2],parent[3],parent[4],parent[9]
    parent[9],parent[14],parent[19],parent[24]=parent[14],parent[19],parent[24],parent[23]
    parent[23],parent[22],parent[21],parent[20]=parent[22],parent[21],parent[20],parent[15]
    parent[15],parent[10],parent[5]=parent[10],parent[5],m
    length_to_goal=heuristic(parent,'O')
    successor.append((NoofstepsTaken+1+length_to_goal,parent,path+" "+'Occ',NoofstepsTaken+1,length_to_goal))
    parent=list(state)
    #clockwise
    m=parent[4]
    parent[4],parent[3],parent[2],parent[1],parent[0]=parent[3],parent[2],parent[1],parent[0],parent[5]
    parent[5],parent[10],parent[15],parent[20]=parent[10],parent[15],parent[20],parent[21]
    parent[21],parent[22],parent[23],parent[24]=parent[22],parent[23],parent[24],parent[19]
    parent[19],parent[14],parent[9]=parent[14],parent[9],m
    length_to_goal=heuristic(parent,'O')
    successor.append((NoofstepsTaken+1+length_to_goal,parent,path+" "+'Oc',NoofstepsTaken+1,length_to_goal))
    parent=list(state)
    
    #getting inner ring pattern both clockwise and counter clockwise
    #counter clockwise
    parent[6],parent[7],parent[8],parent[13],parent[18],parent[17],parent[16],parent[11]=parent[7],parent[8],parent[13],parent[18],parent[17],parent[16],parent[11],parent[6]
    length_to_goal=heuristic(parent,'I')
    successor.append((NoofstepsTaken+1+length_to_goal,parent,path+" "+'Icc',NoofstepsTaken+1,length_to_goal))
    parent=list(state)
    #clockwise
    parent[6],parent[7],parent[8],parent[13],parent[18],parent[17],parent[16],parent[11]=parent[11],parent[6],parent[7],parent[8],parent[13],parent[18],parent[17],parent[16]
    length_to_goal=heuristic(parent,'I')
    successor.append((NoofstepsTaken+1+length_to_goal,parent,path+" "+'Ic',NoofstepsTaken+1,length_to_goal))
    parent=list(state)
    
    
    
    
    return successor

# check if we've reached the goal
def is_goal(state):
    if(state==[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]):
        return True
    return False

def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    
    successor=successors(initial_board,"",0,0)
    # initializing the priority queue 
    fringe=PriorityQueue()
    # appending into the queue
    for i in successor:
        fringe.put(i)
    while not fringe.empty():
        # Getting the node with minimium cost
        m=fringe.get()
        if is_goal(m[1]):
            print(m[1])
            return m[2][1:].split(" ")
        #Pushing the successors into the fringe
        for i in successors(m[1],m[2],m[3],m[4]):
            fringe.put(i)
                
                        
    print(initial_board)
    return []

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]
    print(start_state)

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
