# COMP9021 20T3 - Rachid Hamadi
# Quiz 2 *** Due Friday Week 4 @ 10.00pm

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION


# Reading the number written in base 8 from right to left,
# keeping the leading 0's, if any:
# 0: move N     1: move NE    2: move E     3: move SE
# 4: move S     5: move SW    6: move W     7: move NW
#
# We start from a position that is the unique position
# where the switch is on.
#
# Moving to a position switches on to off, off to on there.

import sys
import time
time.sleep(0.001)

on = '\u26aa'
off = '\u26ab'
code = input('Enter a non-strictly negative integer: ').strip()
try:
    if code[0] == '-':
        raise ValueError
    int(code)
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
nb_of_leading_zeroes = 0
for i in range(len(code) - 1):
    if code[i] == '0':
        nb_of_leading_zeroes += 1
    else:
        break
print("Keeping leading 0's, if any, in base 8,", code, 'reads as',
      '0' * nb_of_leading_zeroes + f'{int(code):o}.')
print()


# INSERT YOUR CODE HERE
# Change position on to off or off to on
def change_status(result_matrix, row, col):
    result_matrix[row][col] = off if result_matrix[row][col] == on else on


# Extended the front or back columns of the matrix
def extend_col(result_matrix, front):
    for i in range(0, len(result_matrix)):
        if front:
            result_matrix[i].insert(0, off)
        else:
            result_matrix[i].append(off)


# Extended the front or back row of the matrix
def extend_row(result_matrix, front):
    col_num = len(result_matrix[0])
    to_extend_row = [off] * col_num
    if front:
        result_matrix.insert(0, to_extend_row)
    else:
        result_matrix.append(to_extend_row)


# Reverse 8-based code string
reverse_code = ('0' * nb_of_leading_zeroes + f'{int(code):o}')[::-1]
result = [[on]]
current_row = 0
current_col = 0
for code in reverse_code:
    # Move east
    if code == '2':
        if len(result[current_row]) - 1 == current_col:
            extend_col(result, False)

        current_col += 1
        change_status(result, current_row, current_col)
    # Move west
    elif code == '6':
        if current_col == 0:
            extend_col(result, True)

        current_col = 0 if current_col == 0 else current_col - 1
        change_status(result, current_row, current_col)
    # Move north
    elif code == '0':
        if current_row == 0:
            extend_row(result, True)

        current_row = 0 if current_row == 0 else current_row - 1
        change_status(result, current_row, current_col)
    # Move south:
    elif code == '4':
        if len(result) - 1 <= current_row:
            extend_row(result, False)

        current_row += 1
        change_status(result, current_row, current_col)
    # Move north-east
    elif code == '1':
        if len(result[0]) - 1 == current_col:
            extend_col(result, False)
        if current_row == 0:
            extend_row(result, True)

        current_row = 0 if current_row == 0 else current_row - 1
        current_col += 1
        change_status(result, current_row, current_col)
    elif code == '3':
        if len(result[0]) - 1 == current_col:
            extend_col(result, False)
        if len(result) - 1 == current_row:
            extend_row(result, False)

        current_row += 1
        current_col += 1
        change_status(result, current_row, current_col)
    elif code == '5':
        if current_col == 0:
            extend_col(result, True)
        if len(result) - 1 == current_row:
            extend_row(result, False)

        current_row += 1
        current_col = 0 if current_col == 0 else current_col - 1
        change_status(result, current_row, current_col)
    elif code == '7':
        if current_col == 0:
            extend_col(result, True)
        if current_row == 0:
            extend_row(result, True)

        current_row = 0 if current_row == 0 else current_row - 1
        current_col = 0 if current_col == 0 else current_col - 1
        change_status(result, current_row, current_col)

#def single_row(result_matrix):
#    new_result = []
#    for i in range(0, len(result_matrix)):
#        for j in range(0, len(result_matrix[i])):
#            if result_matrix[i][j] == on:
#                new_result.append(result_matrix[i][j])
#    for x in new_result:
#        if x == ' ':
#            new_result.remove(' ')
#    return new_result

#if len(result[0]) == 1:
#    result = single_row(result)

for i in range(0, len(result)):
    for j in range(0, len(result[i])):
        print(result[i][j], end='')
    print()
