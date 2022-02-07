# Puzzle-Solver

In this problem I are given a random puzzle and there are some slected number of moves I can make. Using these moves I are supposed to reach the goal state [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25] and ouput of the program should be list of moves I made inorder to reach the goal state.

The moves I are allowed to make are

1.sliding an entire row of tiles left or right one space, with the left- or right-most tile ‘wrapping around’ to the other side of the board 

2.sliding an entire column of tiles up or down one space, with the top- or bottom-most tile ‘wrapping around’ to the other side of the board

3.rotating the outer ‘ring’ of tiles either clockwise or counterclockwise

4.rotating the inner ring either clockwise or counterclockwise.

**Branching factor**: Branching factor for this problem is 24 since there are 24 successor states.

**If the solution can be reached in 7 moves, about how many states would I need to explore before I found it if I used BFS instead of A star search** : B^D states are explored where B is the branching factor and D is the depth = 24^7.if I find the solution at the begininng of 7th level then it would be 24^6. so it's in between these two depending on the case

To solve this Problem I are using A* Search. A* search works on the basis on the estimates of cost function. A* always visits the state with lowest cost. I are using A* algorithm algorithm 2 for this problem.The pseudo code for that is
```python
1.If GOAL?(initial-state) then return initial-state
2. INSERT(initial-node, FRINGE)
3. Repeat:
4. 	If empty(FRINGE) then return failure
5.		s <- REMOVE(FRINGE)
6.		If GOAL?(s) then return s and/or path
7.    For every state s’ in SUCC(s):

8.		    INSERT(s’, FRINGE)

```
The state I are removing above should be the state with minimium cost.So each time when I are poping a element from fringe, I have to check the fringe for the element with least cost. If I use an array to store the successors, This might have a serious consequences on the time complexity.

I can solve this problem in 2 ways, either by using heapq or PriorityQueue. At any point heapq or PriorityQueue always returns the element with the lowest value.
I used PriorityQueue for this problem. Now let's look the solve function.
```python
successor=successors(initial_board,"",0,0)
    fringe=PriorityQueue()
    for i in successor:
        fringe.put(i)
    while not fringe.empty():
        m=fringe.get()
        if is_goal(m[1]):
            print(m[1])
            return m[2][1:].split(" ")
        
        for i in successors(m[1],m[2],m[3],m[4]):
            fringe.put(i)
```
I are generating the successors for the initial state and pushing that into the fringe(PriorityQueue). Then I will pop the element with least cost and see if it's the goal state.If not I again repeat the same process until I find the goal. If I find the goal state I will return the moves it took to reach that state.

### Generating the successors
I have a total of 24 valid moves('L1','L2','L3','L4','L5','R1','R2','R3','R4','R5','U1','U2','U3','U4','U5','D1','D2','D3','D4','D5','Oc','Occ','Ic','Icc') for any given state. so I have 24 Successors for any given state. For Icc,Ic,Oc,Occ I hard coded the the successors. Since I already know the dimensions of the puzzle, This is the best way to reduce the time complexity.
```python
successor=[]
    parent=list(state)
    #getting all the patterns for columns up and down
    for c in range(5):
        parent[c],parent[5+c],parent[10+c],parent[15+c],parent[20+c]=parent[5+c],parent[10+c],parent[15+c],parent[20+c],parent[c]
        length_to_goal=LengthToGoal(parent,'U')
        successor.append((NoofstepsTaken+1+length_to_goal,parent,path+" "+'U'+str(c+1),NoofstepsTaken+1,length_to_goal))
        parent=list(state)
        parent[c],parent[5+c],parent[10+c],parent[15+c],parent[20+c]=parent[20+c],parent[c],parent[5+c],parent[10+c],parent[15+c]
        length_to_goal=LengthToGoal(parent,'D')
        successor.append((NoofstepsTaken+1+length_to_goal,parent,path+" "+'D'+str(c+1),NoofstepsTaken+1,length_to_goal))
        parent=list(state)
    #Getting all the pattern for rows left and right
    for r in range(5):
       parent[r*5+0],parent[r*5+1],parent[r*5+2],parent[r*5+3],parent[r*5+4]=parent[r*5+1],parent[r*5+2],parent[r*5+3],parent[r*5+4],parent[r*5+0]
       length_to_goal=LengthToGoal(parent,'L')
       successor.append((NoofstepsTaken+1+length_to_goal,parent,path+" "+'L'+str(r+1),NoofstepsTaken+1,length_to_goal))
       parent=list(state)
       parent[r*5+0],parent[r*5+1],parent[r*5+2],parent[r*5+3],parent[r*5+4]=parent[r*5+4],parent[r*5+0],parent[r*5+1],parent[r*5+2],parent[r*5+3]
       length_to_goal=LengthToGoal(parent,'R')
       successor.append((NoofstepsTaken+1+length_to_goal,parent,path+" "+'R'+str(r+1),NoofstepsTaken+1,length_to_goal))
       parent=list(state)
    #getting outer ring pattern both clockwise and counter clockwise
    #counter clockwise
    m=parent[0]
    parent[0],parent[1],parent[2],parent[3],parent[4]=parent[1],parent[2],parent[3],parent[4],parent[9]
    parent[9],parent[14],parent[19],parent[24]=parent[14],parent[19],parent[24],parent[23]
    parent[23],parent[22],parent[21],parent[20]=parent[22],parent[21],parent[20],parent[15]
    parent[15],parent[10],parent[5]=parent[10],parent[5],m
    length_to_goal=LengthToGoal(parent,'O')
    successor.append((NoofstepsTaken+1+length_to_goal,parent,path+" "+'Occ',NoofstepsTaken+1,length_to_goal))
    parent=list(state)
    #clockwise
    m=parent[4]
    parent[4],parent[3],parent[2],parent[1],parent[0]=parent[3],parent[2],parent[1],parent[0],parent[5]
    parent[5],parent[10],parent[15],parent[20]=parent[10],parent[15],parent[20],parent[21]
    parent[21],parent[22],parent[23],parent[24]=parent[22],parent[23],parent[24],parent[19]
    parent[19],parent[14],parent[9]=parent[14],parent[9],m
    length_to_goal=LengthToGoal(parent,'O')
    successor.append((NoofstepsTaken+1+length_to_goal,parent,path+" "+'Oc',NoofstepsTaken+1,length_to_goal))
    parent=list(state)
    
    #getting inner ring pattern both clockwise and counter clockwise
    #counter clockwise
    parent[6],parent[7],parent[8],parent[13],parent[18],parent[17],parent[16],parent[11]=parent[7],parent[8],parent[13],parent[18],parent[17],parent[16],parent[11],parent[6]
    length_to_goal=LengthToGoal(parent,'I')
    successor.append((NoofstepsTaken+1+length_to_goal,parent,path+" "+'Icc',NoofstepsTaken+1,length_to_goal))
    parent=list(state)
    #clockwise
    parent[6],parent[7],parent[8],parent[13],parent[18],parent[17],parent[16],parent[11]=parent[11],parent[6],parent[7],parent[8],parent[13],parent[18],parent[17],parent[16]
    length_to_goal=LengthToGoal(parent,'I')
    successor.append((NoofstepsTaken+1+length_to_goal,parent,path+" "+'Ic',NoofstepsTaken+1,length_to_goal))
    parent=list(state)  
    
    return successor
```
Using the function above, I are calculating all the successors and returning them to the solve function.
A node in the fringe is tuple.The each tuple has these elements

first element : Total cost

second element : state in the form of list

third element: steps taken in the form of a string

fourth element: g(s),g is cost of path from start state to present state S

fifth element: h(s), where h estimates the cost of reaching the goal state (heuristic cost)


### Finding the heuristic 
Biggest challange of this problem is finding the heuristic function which is admissible. You can go as far as to say this problem is all about finding the right heuristic. 
Intially I tried no of misplaced tiles. But It turned out not admissible.
Then I tried the manhattan distance. The problem with the Manhattan distance is, it always over estimates the no of moves required. Unlike the 8 Puzzle problem. I are moving the entire row or column or a ring here. So I have consider that too. So I Thought of dividing the Manhattan distamce with 16 since it is maximiun number of tiles I can move in a single move. But here comes the main problem, even when you divide the manhattan with 16. it's still over-estimating because it is failing to consider the wrapping conditions. For example let's say our is below one
```
2  18  3  4  1
6  7  8  9  10
11 12 13 14 15
16 17 5 19 20
21 22 23 24 25
```
I know that the goal state is
```
1  2  3  4  5
6  7  8  9  10
11 12 13 14 15
16 17 18 19 20
21 22 23 24 25
```
Let consider 18 in the present state. If I caluclate the number of moves it takes for 18 to reach the goal state, It would be 4. But I have a better solution I can use the set of moves U2,R5,U3. It would be done in 3 moves. If I calculate number of moves it takes for 1 to reach it's goal state using manhattan, It would be 4 but I can do that in one move R1. After careful observation, I observed there is a pattern for calculating the no of moves required by a single tile to reach it's goal position. I did this small problem called minimium distance between 2 elements in a circular array some time back. I was crucial for this problem. First I consider the all the rows and columns are circular. If I calculate the minimium distance between the row of the initial state and row of the goal state and add it to the minimium distance between the column of the initial state and column of the goal state, I get the exact no of moves I required to reach the goal state. let consider the same example above.

For 18 row is 0 and column is 1, i.e 18 at (0,1). It's goal state co-ordinates are (3,2) 

No of moves = circlic minimium distance between (0,3) + Circlic minimiun distance between (1,2)
            = 2+1  
            = 3
In this way I can compute the exactly no of numbers it takes to get to the goal state.
The function I used for this is
```python
def heuristic(state,turn):
    D_to_Goal=0
    for i in range(ROWS*COLS):
        #calculating the No of steps I need to take in terms of row which also include wrapping and circular conditions
        rowsteps=min(  ( (i//COLS) - ((state[i]-1)//COLS) )%ROWS, ( ((state[i]-1)//COLS) - (i//COLS) )%ROWS   )
        #calculating the No of steps I need to take in terms of columns which also include wrapping and circular conditions
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
    
    
```
Since I are using 1D array. I are using // and % operations to get the coordinates of elements in terms of a 2d matrix.

(i//Row,i%Row) are the co-ordinates of the present state

(state[i]-1)//ROWS,state[i]-1)%ROWS) are the co-ordinates of the goal state.

min(  ( (i//COLS) - ((state[i]-1)//COLS) )%ROWS, ( ((state[i]-1)//COLS) - (i//COLS) )%ROWS   ) finds the minimuim circulic distance between the rows.

min( ( (i%COLS) - ((state[i]-1)%COLS) )%COLS, ( ((state[i]-1)%COLS) -(i%COLS) )%COLS ) finds the minimium circulic distnace between the columns.

Using this function I are able the calculate the number of moves that a tile has to make in order to reach it's goal position. But when I are not moving a single tile. I are moving entire row, columns or rings. So I need to normalize that. To do that I are dividing the resultant distance with either 16 or 8 or 5 based on the move made.
I also tried dividing all moves with 16. It's way under-estimating the cost. So removed that. Then I tried using // instead of /. But it is assigning the zero cost to everytime which is less the value in the denominator. I also discarded it. I finally ended up using the function above which is Admissible.

