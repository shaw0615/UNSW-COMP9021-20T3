# COMP9021 20T3 - Rachid Hamadi
# Quiz 4 *** Due Friday Week 7 @ 10.00pm

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION

# Implements a function that, based on the encoding of
# a single strictly positive integer that in base 2
# reads as b_1 ... b_n, as b_1b_1 ... b_nb_n, encodes
# a sequence of strictly positive integers N_1 ... N_k
# with k >= 1 as N_1* 0 ... 0 N_k* where for all 0 < i <= k,
# N_i* is the encoding of N_i.
#
# Implements a function to decode a strictly positive integer N
# into a sequence of (one or more) strictly positive
# integers according to the previous encoding scheme,
# or return None in case N does not encode such a sequence.


import sys

def encode(list_of_integers):
    res = []
    temp = ""
    for i in list_of_integers:
        int2bin = bin(i)[2:]
        for j in int2bin:
            res.append(j)
            res.append(j)
        res.append(0)
    res.pop()
    for i in res:
        temp = temp + str(i)
    return int(temp,2)

def decode(integer):
    int2bin = str(bin(integer)[2:])
    i = 0
    res = list()
    res_new = list()
    temp = ""
    while True:
        if len(int2bin) == 1:
            return None
        try:
            if int2bin[i] == int2bin[i+1]:
                temp = temp + str(int2bin[i])
                i = i + 2
            elif int2bin[i] != int2bin[i+1] and int2bin[i] == '0':
                i = i + 1
                res.append(temp)
                temp = ""
            else:
                return None
        except IndexError:
            return None

        if i > len(int2bin):
            break
    res.append(temp)
    for i in res:
        res_new.append(int(i,2))
    return res_new

# We assume that user input is valid. No need to check
# for validity, nor to take action in case it is invalid.
print('Input either a strictly positive integer')
the_input = eval(input('or a nonempty list of strictly positive integers: '))
if type(the_input) is int:
    print('  In base 2,', the_input, 'reads as', bin(the_input)[2 :])
    decoding = decode(the_input)
    if decoding is None:
        print('Incorrect encoding!')
    else:
        print('  It encodes: ', decode(the_input))
else:
    print('  In base 2,', the_input, 'reads as',
          f'[{", ".join(bin(e)[2: ] for e in the_input)}]'
         )
    print('  It is encoded by', encode(the_input))
