# COMP9021 20T3 - Rachid Hamadi
# Quiz 1 *** Due Friday Week 3 @ 10.00pm

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION

import sys
from random import seed, randrange
from pprint import pprint

try:
    arg_for_seed, upper_bound = (abs(int(x)) + 1 for x in input('Enter two integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
mapping = {}
for i in range(1, upper_bound):
    r = randrange(-upper_bound // 8, upper_bound)
    if r > 0:
        mapping[i] = r
print('\nThe generated mapping is:')
print('  ', mapping)
# sorted() can take as argument a list, a dictionary, a set...
keys = sorted(mapping.keys())
print('\nThe keys are, from smallest to largest: ')
print('  ', keys)

cycles = []
reversed_dict_per_length = {}

# INSERT YOUR CODE HERE
def find_cycle(mapping):  # the main function
    cycle = []
    for x, y in mapping.items():

        temp_cycle = []
        temp_cycle.append(x)
        temp_cycle.append(y)
        next_key = y
        if x == y:  # key和value数值相等
            cycle.append(temp_cycle)
            continue
        while mapping.get(next_key) != None:
            temp_cycle.append(next_key)
            val = mapping[next_key]
            temp_cycle.append(val)
            next_key = val
            if val == x:
                cycle.append(temp_cycle)
                break
            if temp_cycle.count(temp_cycle[-1]) > 2 :
                break
    cycle = sort_cycle(cycle)
    cyc1e = del_data(cycle)

    return cyc1e

def sort_cycle(cycle):
    new_cycle = []
    for x in cycle:
        lis = sorted(set(x), key=x.index)
        new_cycle.append(lis)
    return new_cycle

def del_data(thislist):
    for i in range(len(thislist)):
        for j in range(i+1,len(thislist)):
            if thislist[j][0] in thislist[i]:
               thislist[j] = thislist[i]
    cycle = del_repe(thislist)
    return cycle

def del_repe(thislist):
    cycle = []
    for i in thislist:
        if not i in cycle:
            cycle.append(i)
    return cycle


def rev_dic(dic):
    newdic = {}
    for x in dic:
        if dic[x] not in newdic:
            newdic[dic[x]]=[x]
        else:
            if type(newdic[dic[x]]) != list:
                newdic[dic[x]]=[newdic[dic[x]], x]
            else:
                newdic[dic[x]].append(x)
    return newdic

def add_length(dic):
    count = 1;
    length = []
    dict_per_length = {}
    for x in dic:
        length.append(len(dic[x]))
    length = list(set(length))
    return length


def cons_multidict(dic,length):
    d1 = {}
    dic = dict(sorted(dic.items(), key=lambda x: x[0]))
    for i in length:
        for x in dic:
            if len(dic[x]) == i:
                d1.setdefault(i,{})[x] = dic[x]
    return d1


reversed_dict = rev_dic(mapping)
length = add_length(reversed_dict)
add_length(reversed_dict)
reversed_dict_per_length = cons_multidict(reversed_dict,length)
cycles=find_cycle(mapping)


print('\nProperly ordered, the cycles given by the mapping are: ')
print('  ', cycles)
print('\nThe (triply ordered) reversed dictionary per lengths is: ')
pprint(reversed_dict_per_length)
