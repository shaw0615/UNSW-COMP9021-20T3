# COMP9021 20T3 - Rachid Hamadi
# Quiz 6 *** Due Friday Week 9 @ 10.00pm

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION

# Randomly generates a grid of 0s and 1s and determines
# the maximum number of "spikes" in a shape.
# A shape is made up of 1s connected horizontally or vertically (it can contain holes).
# A "spike" in a shape is a 1 that is part of this shape and "sticks out"
# (has exactly one neighbour in the shape).
# Neighbours are only considered vertically or horizontally (not diagonally).


from random import seed, randrange
import sys


dim = 10
flag = 0

def display_grid():
    for row in grid:
        print('   ', *row) 


# Returns the number of shapes we have discovered and "coloured".
# We "colour" the first shape we find by replacing all the 1s
# that make it with 2. We "colour" the second shape we find by
# replacing all the 1s that make it with 3.

def colour_shapes():
    global flag
    count = 2
    shape = []
    m,n = len(grid), len(grid[0])
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                dfs(i, j,count)
                #temp = flag
                shape.append([count,flag])
                flag = 0
                count += 1
    return shape

def max_number_of_spikes(nb_of_shapes):
    m,n = len(grid), len(grid[0])
    new_count = []
    temp = 0
    for i in range(m):
        for j in range(n):
            new_count.append(grid[i][j])
    for i in nb_of_shapes:
        if new_count.count(i[0]) > temp:
            temp = new_count.count(i[0])
            final = i[1]
    return final

def around(i,j):
    m, n = len(grid), len(grid[0])
    if i < 0 or i >= m or j < 0 or j >= n: return 0
    if grid[i][j] == 0: return 0
    if 0 <= i < m and 0 <= j < n and grid[i][j]: return 1

def dfs(i,j,count):
    global flag
    m, n = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] != 1: return 0
    if 0 <= i < m and 0 <= j < n and grid[i][j] == 1:
        grid[i][j] = count
        if around(i+1,j) + around(i-1,j) + around(i,j+1) + around(i,j-1) == 1:
            flag = flag + 1
        for d in directions:
            next_i = i + d[0]  
            next_j = j + d[1]  
            dfs(next_i, next_j,count)   

try: 
    for_seed, density = (int(x) for x in input('Enter two integers, the second '
                                               'one being strictly positive: '
                                              ).split()
                    )
    if density <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
grid = [[int(randrange(density) != 0) for _ in range(dim)]
            for _ in range(dim)
       ]
print('Here is the grid that has been generated:')
display_grid()
nb_of_shapes = colour_shapes()
print('The maximum number of spikes of some shape is:',
      max_number_of_spikes(nb_of_shapes)
     )
