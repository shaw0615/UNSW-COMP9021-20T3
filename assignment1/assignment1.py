# COMP9021 20T3 - Rachid Hamadi
# Assignment 1 *** Due Monday 26 October (Week 7) @ 10.00pm

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION


import sys
import time


def judge_roman(input):
    for i, v in enumerate(reversed(input)):
        if input.count(v) >= 4:
            if input[input.index(v):len(input) - i] == v * 4:
                return True
    return False

def intToRoman(num,temp): 
    res = ""      
    num = int(num)
    hashmap = dict()
    hashmap = temp
    for k in hashmap:
        count = num // k
        num %= k
        res += hashmap[k] * count
    if judge_roman(res) == True:
        return False
    else:
        return res

def RomanToint(s,temp) : 
    Roman2Int = dict()
    Roman2Int = temp
    special = []
    res = 0
    for i in s:
        if Roman2Int.get(i) == None:
            return False
    for i in range(len(s)-1):
        if s[i] == s[i + 1]:
            n = Roman2Int.get(s[i])
            sf = str(n)
            if sf[0] == '5':
                return False
    for index in range(len(s)-1):
        if Roman2Int[s[index]] < Roman2Int[s[index + 1]]:
            res -= Roman2Int[s[index]]
        else:
            res += Roman2Int[s[index]]
    result = res + Roman2Int[s[-1]]
    return result


def isRoman(s):
    temp1 = {1000:'M',900:'CM', 500:'D', 400:'CD', 100:'C', 90:'XC', 50:'L', 40:'XL', 10:'X', 9:'IX', 5:'V', 4:'IV', 1:'I'}
    temp2 = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    num = RomanToint(s,temp2)

    if s == intToRoman(num,temp1):
        return True
    else:
        return False

def nomalCoding(s):   
    num = list()
    alphabet = list()
    if len(s) != len(set(s)):
        return False
    for index, str in enumerate(reversed(s)):
        if index%2 == 0:
            temp = int(pow(10, index/2))
            num.append(temp)
            alphabet.append(str)
        else:
            temp = int(pow(10, (index-1)/2)*5)
            num.append(temp)
            alphabet.append(str)
    init_map= list(zip(alphabet, num))
    hash_map = list()
    for i in init_map:
        hash_map.append(i)
    for i in range(0,len(init_map)-2):
        if i%2 == 0 and init_map[i+1]!= None and init_map[i+2]!=None:
            hash_map.append((init_map[i][0]+init_map[i+1][0], init_map[i+1][1]-init_map[i][1]))
            hash_map.append((init_map[i][0] + init_map[i + 2][0], init_map[i + 2][1] - init_map[i][1]))
    return hash_map

def s_in(string):
    return([string.index(i) for i in string])

def final_list(final_dict, std_dict,length):
    Roman2Int = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    temp = []
    res = []
    str_int = []
    l = length
    for final in final_dict:
        for std in std_dict:
            if std[1] == final[1]:
                temp.append([final[0],std[0]])
    final_dict.reverse()
    for i, v in enumerate(reversed(temp)):
        l = l - len(str(final_dict[i][1]))
        for j in range(len(v[0])):
            num = RomanToint(v[1][j],Roman2Int) * pow(10, l)
            res.append([v[0][j],num])
    new_res = []
    for i in res:
        if i not in new_res:
            new_res.append(i)
    return sorted(new_res, key=lambda x:x[1])


def final_string(f_list, compare_list):
    temp = ""
    f_dict = dict(f_list)
    f_dict_new = dict(zip(f_dict.values(), f_dict.keys()))
    i = 0
    while True:
        num = compare_list[i]
        if f_dict_new.get(num) != None:
            i += 1
        elif f_dict_new.get(num) == None:
            f_dict_new[num] = "_"
        if i == len(compare_list)-1:
            break
    for i in sorted(f_dict_new):
        temp += (f_dict_new[i])
    return temp[::-1]


def judge(string):
    if len(string) >= 4:
        for i in range(0,len(string)-4):
            if string[i] == string[i+2] and string[i+1] == string[i+3] and string[i+1] != string[i+2]:
                return False
            else:
                return True
    else:
        return True


def speciaCoding(string): 
    Roman2Int = {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C', 90: 'XC', 50: 'L', 40: 'XL', 10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'}
    Roman_std = list()
    Roman_std_index = list()
    intnum = list() 
    Roman_std_dict = list() 
    Roman_std_repeat = list()
    temp_list = list()
    for i in range(1, 101): 
        intnum.append(i)
        Roman_std.append(intToRoman(i, Roman2Int))

    for i in Roman_std:
        Roman_std_index.append([i.index(item) for item in i])

    Roman_std_dict = list(zip(Roman_std,intnum))
    repeat_str= list()
    r = len(string)-1
    i = 0
    restring = string[::-1]

    while i < len(string):    
        if string.count(string[i]) > 1:
            temp = restring.index(string[i])
            #print(temp)
            repeat_str.append(string[i:len(restring)-temp])
            i = len(restring)-temp
        else:
            repeat_str.append(string[i])
            i = i+1

    repeat_str = repeat_str[::-1] 

    index_repeat_str = list()
    final_str = list()
    temp = ""
    i = 0
    for i in range(0, len(repeat_str)):
        total = repeat_str[i] + temp
        if s_in(total) in Roman_std_index: 
            temp = total
        else:
            if s_in(temp) in Roman_std_index and temp != "":
                index_repeat_str.append(s_in(temp))
                final_str.append(temp)
                temp = repeat_str[i]
            else:
                print("Hey, ask me something that's not impossible to do!")
                return
        if i == len(repeat_str)-1 and s_in(temp) in Roman_std_index:
            index_repeat_str.append(s_in(temp))
            final_str.append(temp)
    index_repeat_str = index_repeat_str[::-1]
    num = ""
    num_list = list()
    for i in index_repeat_str:
        num = num + str(Roman_std_index.index(i)+1)
        num_list.append(Roman_std_index.index(i)+1)
    final_dict = list(zip(final_str,reversed(num_list)))
    f_list = final_list(final_dict,Roman_std_dict,len(str(num)))
    compare_list = []
    largest = f_list[len(f_list)-1][1]
    for i in range (1,len(str(largest))+1):
        compare_list.append(pow(10,i-1))
        compare_list.append(pow(10, i - 1) * 5)
        if compare_list[i] == largest:
            break
    final_s = final_string(f_list, compare_list)
    print("Sure! It is", num, "using", final_s)
    return True


def first_kind_of_input(str):
    temp1 = {1000:'M',900:'CM', 500:'D', 400:'CD', 100:'C', 90:'XC', 50:'L', 40:'XL', 10:'X', 9:'IX', 5:'V', 4:'IV', 1:'I'}
    temp2 = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    if str.isdigit():
        if str[0] > '0' and int(str) <= 3999:
            print("Sure! It is", intToRoman(str, temp1))
        else:
            print("Hey, ask me something that's not impossible to do!")
    if str.isalpha():
        if isRoman(str):
            print("Sure! It is", RomanToint(str, temp2))
        else:
            print("Hey, ask me something that's not impossible to do!")


def second_kind_of_input(str1, str2):
    temp = nomalCoding(str2)
    if temp:
        alp_dict = dict(sorted(temp, key=lambda x: x[1], reverse=True))
        num_dict = dict(zip(alp_dict.values(), alp_dict.keys()))
        if str1.isdigit() and str1[0] > '0' and intToRoman(str1, num_dict):
            print("Sure! It is", intToRoman(str1, num_dict))
        elif str1.isalpha() and not False in list(map(lambda r: r in str2, [i for i in str2])) and RomanToint(str1, alp_dict) and intToRoman(RomanToint(str1, alp_dict),num_dict) == str1:
            print("Sure! It is", RomanToint(str1, alp_dict))
        else:
            print("Hey, ask me something that's not impossible to do!")
    else:
        print("Hey, ask me something that's not impossible to do!")


def third_kind_of_input(str1):
    if judge(str1):
        speciaCoding(str1)
    else:
        print("Hey, ask me something that's not impossible to do!")


def examine_input(string):
    if string[0] == 'Please' and string[1] == 'convert' and len(string) == 3:
        if string[2].isdigit() or string[2].isalpha() :
            first_kind_of_input(string[2])
    elif string[0] == 'Please' and string[1] == 'convert' and string[3] == 'using' and len(string) == 5:
        second_kind_of_input(string[2], string[4])
    elif string[0] == 'Please' and string[1] == 'convert' and string[3] == 'minimally' and len(string) == 4:
        if string[2].isalpha():
            third_kind_of_input(string[2])
        else:
            print("Hey, ask me something that's not impossible to do!")
    else:
        raise IOError


try:
    string = input('How can I help you? ')
    text = string.split(" ")
    examine_input(text)
except IOError:
    print("I don't get what you want, sorry mate!")
    sys.exit()

time.sleep(0.001)
