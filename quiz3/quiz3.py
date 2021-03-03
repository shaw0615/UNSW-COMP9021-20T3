# COMP9021 20T3 - Rachid Hamadi
# Quiz 3 *** Due Friday Week 5 @ 10.00pm

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION

# Prompts the user for an arity (a natural number) n and a word.
# Call symbol a word consisting of nothing but alphabetic characters
# and underscores.
# Checks that the word is valid, in that it satisfies the following
# inductive definition:
# - a symbol, with spaces allowed at both ends, is a valid word;
# - a word of the form s(w_1,...,w_n) with s denoting a symbol and
#   w_1, ..., w_n denoting valid words, with spaces allowed at both ends and
#   around parentheses and commas, is a valid word.


import sys
import re
import time
time.sleep(0.0001)

def is_symbol(string):
    if re.match("^[A-Za-z_]*$", string):
        return True
    else:
        return False

def match_brackets(string):
    left_brackets = 0
    right_brackets = 0
    for str in string:
        if str == '(':
            left_brackets +=1
        if str == ')':
            right_brackets +=1
    if (left_brackets == right_brackets) and left_brackets >= 1 and right_brackets >= 1:
        return True
    return False

def split_to_words(string):
    string = string.replace(" ", "")
    temp = ""
    words = list()
    if match_brackets(string):
        begin = string.find("(")
        for i in range(begin+1, len(string)-1):
            if is_symbol(string[i]):
                temp = temp + string[i]
            if string[i] == ",":
                if len(temp) and "(" not in temp:
                    words.append(temp)
                    temp = ""
                elif len(temp) and "(" in temp:
                    temp = temp + ","
            if string[i] == "(":
                temp = temp + string[i]
            if string[i] == ")":
                if len(temp) and "(" in temp:
                    temp = temp + ")"
                    if temp.count("(") != temp.count(")"):
                        continue
                    else:
                        words.append(temp)
                        temp = ""
            if i == len(string)-2:
                if len(temp):
                    words.append(temp)
    return words

def judge_num(split_word, num):
    flag = True
    if num != len(split_word):
        flag = False
    elif num == len(split_word):
        for temp in split_word:
            if not is_symbol(temp):
                new_temp = split_to_words(temp)
                if not judge_num(new_temp, num):
                    flag = False
                    break
    return flag

def is_valid(word, arity):
    #return False
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE
    if arity == 0:
        return is_symbol(word)

    match_brackets(word)
    split_word = split_to_words(word)
    #print(len(split_word))
    return judge_num(split_word, arity)

try:
    arity = int(input('Input an arity : '))
    if arity < 0:
        raise ValueError
except ValueError:
    print('Incorrect arity, giving up...')
    sys.exit()
word = input('Input a word: ')
if is_valid(word, arity):
    print('The word is valid.')
else:
    print('The word is invalid.')
