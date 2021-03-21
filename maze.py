import os
import sys
from random import randint
while True:
    try:
        rowsmaze = int(input("How TALL do you want your maze to be? "))
        colsmaze = int(input("How WIDE do you want your maze to be? "))
        break
    except:
        print('nope')

rowstotal = rowsmaze + 2
colstotal = colsmaze + 2
rowsinit = rowstotal
colsinit = colstotal

samprowinit = []
board = []
frontierpoints = [] 

recentincluded =[rowstotal-1,1]
x = rowstotal-1
y = 1
#what the walls look like
wall = '▓▓'
#what the paths look like
path = '  '

global localInd
localInd = []

# first, the randomly selected frontier point becomes an index, I_
# new frontiers are selected from that point, frontier points are points adjacent to indexed points
# new indexed point removed from the list of frontier points
# see checkInd for more information
# randomly selects an adjacent index point, with the help of checkInd, to be the source of a new indexed point
# changes the value of the newly indexed point to reflect its source (ID means its source is below it, IU means its source is above it, etc...)
# clears the list of adjacent indexed points to ensure that new indexes can't reference old adjacent points
def addIndex(x, y):
    board[x][y] = 'I_'
    addFrontiers(x, y)
    frontierpoints.remove((x, y))
    checkInd(x-1, y) 
    checkInd(x+1, y)
    checkInd(x, y-1)
    checkInd(x, y+1)
    pickInd = localInd[(randint(0, len(localInd)-1))]
    if x - pickInd[0] == 1:
        board[x][y] = 'ID'
    if x - pickInd[0] == -1:
        board[x][y] = 'IU'
    if y - pickInd[1] == 1:
        board[x][y] = 'IL'
    if y - pickInd[1] == -1:
        board[x][y] = 'IR'
    while (len(localInd)) > 0:
        localInd.pop(0)

# after a frontier point is indexed, we need to figure out which point it will create a path from
# this point has to be an adjacent indexed point, sometimes there is only 1, but other times there are 2 or even 3 so we have to pick one randomly
# checkInd adds each adjacent index point to a list which is then chosen from randomly in addIndex
def checkInd(x,y):
    try:
        if 'I' in board[x][y]:
            localInd.append((x,y))
    except:
        return

# checks the state of each possible surrounding point, the checkState function actually changes the points themselves to frontier points
def addFrontiers(x, y):
    #check if x-1,y is indexd or in actual board
    checkState(x-1, y) 
    checkState(x+1, y)
    checkState(x, y-1)
    checkState(x, y+1)

# checks to see if points next to a new index point are already indexed points or frontier points, if not, make them a frontier point
def checkState(x, y):
    try:
        if x != 0 and x != rowstotal-1 and y != 0 and y != colstotal-1:
            if 'I' not in board[x][y] and board[x][y] != 'FF':
                if (x,y) not in frontierpoints:
                    frontierpoints.append((x,y))
                    board[x][y] = 'FF'
    except:
        return

# removes the wall between every index point and its source, also erases itself to make the maze path
def removePaths():
	for y in range (len(maze[0])):
		for x in range(len(maze)):
			if maze[x][y] == 'IU':
				maze[x][y] = path
				maze[x+1][y] = path
			if maze[x][y] == 'IL':
				maze[x][y] = path
				maze[x][y-1] = path
			if maze[x][y] == 'ID':
				maze[x][y] = path
				maze[x-1][y] = path
			if maze[x][y] == 'IR':
				maze[x][y] = path
				maze[x][y+1] = path
'''
A. create the coordinate system
    1. declare start point
    2. full size grid
    3. declare frontier points based on current included (start point)
    4. randomly select one frontier point and add to included
    5. check everything around that point for included points, if there are more than one, randomly select which one is its root
    6. declare that frontier point as included in respect to its root. (ID, IU, IL, IR)
    7. create new frontier points which are non-included, non-zero points
    8. repeat until
    9. complete
B. build a wall
    1. between every coordinate point make a block
    2. erase blocks between connected points (if a point is IL, remove the wall to the left of it, if the point is IU, remove the wall above it, etc...)
    3. build a border to close in the maze
C. make it pretty
'''


board = [[wall]*colstotal for i in range(rowstotal)]


# this point had to start as I- because the 'I' was used to let the code know that it was an indexed point
# it was not, however, defined by any other points, so it couldnt be IU, ID, IL, or IR
board[rowstotal-1][1] = 'I-'

# add frontier points from the start point
addFrontiers(x,y)


count = 0
# this code creates new index points until every point in the grid has become an index.
while count < ((rowstotal-2)*(colstotal-2)):
    newIndex = frontierpoints[randint(0,len(frontierpoints)-1)]
    addIndex(newIndex[0],newIndex[1])
    count += 1
board[0][colstotal-2] = 'IU'


# this code prints the skeletal structure of the maze, the actual information used to make the maze
# points are either IL, IR, ID, or IU depending on the direction from which they are included in the maze's path
# when the maze is ultimately printed, it is done so upside down but you can still match up the points on the skeleton to the maze itself

z = rowstotal
while z > 0:
    print(board[z-1])
    z -=1 
print('\n')


# creates every point in the new maze, which is a larger grid than the skeleton
# every point begins as a wall, and are slowly changed to empty spaces depending on the information in the skeleton
maze = [[wall]*((colstotal * 2) - 3)for i in range((rowstotal * 2) - 1)]

# this code puts the values from the skeleton into every other position in the maze, leaving us with a bunch of points surrounded by walls on each side
for y in range (0 , len(maze[0]), 2):
    for x in range (0, len(maze), 2):
        maze[(x)][(y-1)] = board[int(x*.5)][int(y*.5)]

removePaths()

# this line redefines the start point, which was originally I_, to blank space
maze[len(maze)-1][1] = path


# prints the maze, removes commas and apostrophes and aligns the maze properly
z = 0
while z < len(maze):
    w = 0
    while w < len(maze[0]):
        print(maze[z][w], end = '')
        w += 1 
    print('')
    z += 1
