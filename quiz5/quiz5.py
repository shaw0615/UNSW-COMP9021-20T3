# COMP9021 20T3 - Rachid Hamadi
# Quiz 5 *** Due Friday Week 8 @ 10.00pm

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION

# Randomly fills an array of size 10x10 with 0s and 1s, and outputs the size of
# the largest parallelogram with horizontal sides.
# A parallelogram consists of a line with at least 2 consecutive 1s,
# with below at least one line with the same number of consecutive 1s,
# all those lines being aligned vertically in which case the parallelogram
# is actually a rectangle, e.g.
#      111
#      111
#      111
#      111
# or consecutive lines move to the left by one position, e.g.
#      111
#     111
#    111
#   111
# or consecutive lines move to the right by one position, e.g.
#      111
#       111
#        111
#         111
# The size is the number of 1s in the parallelogram. In the above examples, the size is 12.

from random import seed, randrange
import sys


dim = 10


def display_grid():
    for row in grid:
        print('   ', *row) 



def left_below(array, start, i, m, k):
    size = 0
    for j in range(m, k):
        if not array[i][j]:
            if i - start == 1:
                return 0
            else:
                return (i - start) * (k - m)
    if i == 9 or m == 0:
        size = max(size,(i - start + 1) * (k - m))
        return size
    size = max(size,left_below(array, start, i + 1, m - 1, k - 1))
    return size

def below(array, start, i, m, k):
    size = 0
    for j in range(m, k):
        if not array[i][j]:
            if i - start == 1:
                return 0
            else:
                return (i - start) * (k - m)
    if i == 9:
        size = max(size,(i - start + 1) * (k - m))
        return size
    size = max(size,below(array, start, i + 1, m, k))
    return size

def right_below(array, start, i, m, k):
    size = 0
    for j in range(m, k):
        if not array[i][j]:
            if i - start == 1:
                return 0
            else:
                return (i - start) * (k - m)
    if i == 9 or k == 10:
        size = max(size,(i - start + 1) * (k - m))
        return size
    size = max(size,right_below(array, start, i + 1, m + 1, k + 1))
    return size

def size_of_largest_parallelogram():
    count = 0
    array = []
    size, right, left, bottom = 0, 0, 0, 0

    for row in grid:
        temp = []
        for i in row:
            temp.append(i)
        array.append(temp)

    i = 0
    while(i + 2 <= 10):
        for k in range(10):
            if array[i][k] == 1:
                count = count + 1
                if count >= 2:
                    for l in range(k - count + 1, k):
                        for m in range(l, k):
                            bottom = below(array, i, i + 1, m, k + 1)
                            if k > count:
                                left = left_below(array, i, i + 1, m - 1, k)
                            if k <= 8:
                                right = right_below(array, i, i + 1, m + 1, k + 2)
                            size = max(size, right, left, bottom)
                if k == 9 or array[i][k + 1] == 0:
                    count = 0
                    continue
        i = i + 1
    return size



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
size = size_of_largest_parallelogram()
if size:
    print('The largest parallelogram with horizontal sides '
          f'has a size of {size}.'
         )
else:
    print('There is no parallelogram with horizontal sides.')
