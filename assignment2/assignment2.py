# COMP9021 20T3 - Rachid Hamadi
# Assignment 2 *** Due Sunday Week 10 @ 10.00pm

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION


# IMPORT ANY REQUIRED MODULE

import re
import copy

class MazeError(Exception):
    def __init__(self, message):
        self.message = message

class Maze:
    def __init__(self, filename):
        self.filename = filename
        self.martrix = open_txt(self.filename)
        if self.martrix == None:
            raise MazeError('Incorrect input.')
        elif self.martrix is False :
            raise MazeError('Input does not represent a maze.')
        else:
            self.zero = maze_zero(self.martrix)
            self.door = find_gates(self.martrix)
            self.walls = find_walls(self.martrix)
            self.martrix_copy = copy.deepcopy(self.martrix)
            self.pillar = find_pillar(self.martrix_copy)
            self.inner_list = build_inner_points(self.martrix)
            self.inner = copy.deepcopy(self.inner_list)
            self.accessible_areas = find_accessible_area(self.door, self.inner_list, self.martrix)
            self.inaccessible_inner_points = find_no_inner_points(self.inner_list)

            self.temp1, temp = build_cul_de_sacs(self.martrix, self.inner_list, self.inaccessible_inner_points)
            temp2 = change_point_count(self.martrix, self.temp1, self.inner_list, temp)
            self.cul_de_sacs = get_number_cul_de_sacs(temp2, self.martrix, self.inner_list)
            if self.zero: self.path = []
            else: self.path = final_path(self.door, self.martrix, self.inner, self.temp1, self.inner_list)

    # POSSIBLY DEFINE OTHER METHODS

    def analyse(self):
        if not len(self.door):
            print('The maze has no gate.')
        elif len(self.door) == 1:
            print('The maze has a single gate.')
        else:
            print('The maze has ' + str((len(self.door))) + ' gates.')

        if len(self.walls) == 0:
            print('The maze has no wall.')
        elif len(self.walls) == 1:
            print('The maze has walls that are all connected.')
        else:
            print('The maze has ' + str(len(self.walls)) + ' sets of walls that are all connected.')

        if len(self.inaccessible_inner_points) == 0:
            print('The maze has no inaccessible inner point.')
        elif len(self.inner_list) == 1:
            print('The maze has a unique inaccessible inner point.')
        else:
            print('The maze has ' + str(len(self.inaccessible_inner_points)) + ' inaccessible inner points.')

        if self.accessible_areas == 0:
            print('The maze has no accessible area.')
        elif self.accessible_areas == 1:
            print('The maze has a unique accessible area.')
        else:
            print('The maze has ' + str(self.accessible_areas) + ' accessible areas.')

        if self.cul_de_sacs == 0:
            print('The maze has no accessible cul-de-sac.')
        elif self.cul_de_sacs == 1:
            print('The maze has accessible cul-de-sacs that are all connected.')
        else:
            print('The maze has ' + str(self.cul_de_sacs) + ' sets of accessible cul-de-sacs that are all connected.')

        if len(self.path) == 1:
            print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        elif len(self.path) == 0:
            print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print('The maze has ' + str(len(self.path)) + ' entry-exit paths with no intersections not to cul-de-sacs.')

    def display(self):
        with open(self.filename.split('.')[0] + '.tex', 'w') as f:
            f.write(r'\documentclass[10pt]{article}' + '\n')
            f.write(r'\usepackage{tikz}' + '\n')
            f.write(r'\usetikzlibrary{shapes.misc}' + '\n')
            f.write(r'\usepackage[margin=0cm]{geometry}' + '\n')
            f.write(r'\pagestyle{empty}' + '\n')
            f.write(r'\tikzstyle{every node}=[cross out, draw, red]' + '\n')
            f.write('\n')
            f.write(r'\begin{document}' + '\n')
            f.write('\n')
            f.write(r'\vspace*{\fill}' + '\n')
            f.write(r'\begin{center}' + '\n')
            f.write(r'\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]' + '\n')

            f.write(r'% Walls' + '\n')
            temp1 = []
            temp2 = []
            for i in range(len(self.martrix)):
                for j in range(len(self.martrix[0])):
                    temp = []
                    if (j, i) not in temp1:
                        if self.martrix[i][j] == '1' or self.martrix[i][j] == '3':
                            temp1.append((j,i))
                            temp.append((j,i))
                            right(self.martrix, i, j, temp, temp1)
                            f.write(f'    \draw ({temp[0][0]},{temp[0][1]}) -- ({temp[len(temp) - 1][0]},{temp[len(temp) - 1][1]});' + '\n')
            for j in range(len(self.martrix[0])):
                for i in range(len(self.martrix)):
                    temp = []
                    if (j, i) not in temp2:
                        if self.martrix[i][j] == '2' or self.martrix[i][j] == '3':
                            temp2.append((j, i))
                            temp.append((j,i))
                            down(self.martrix, i, j, temp, temp2)
                            f.write(f'    \\draw ({temp[0][0]},{temp[0][1]}) -- ({temp[len(temp) - 1][0]},{temp[len(temp) - 1][1]});' + '\n')

            f.write(r'% Pillars' + '\n')
            for i in range(len(self.martrix)):
                for j in range(len(self.martrix[0])):
                    if (i, j) in self.pillar:
                        f.write(f'    \\fill[green] ({j},{i}) circle(0.2);'+'\n')

            f.write(r'% Inner points in accessible cul-de-sacs' + '\n')
            for i in range(len(self.martrix)):
                for j in range(len(self.martrix[0])):
                    if (i, j) in self.temp1:
                        f.write(f'    \\node at ({j+0.5}, {i+0.5})' + r'{};' + '\n')

            f.write(r'% Entry-exit paths without intersections' + '\n')
            #for i

            f.write(r'\end{tikzpicture}' + '\n')
            f.write(r'\end{center}' + '\n')
            f.write(r'\vspace*{\fill}' + '\n')
            f.write('\n')
            f.write(r'\end{document}' + '\n')

def right(martrix, i, j , temp, temp1):
    if True:
        temp1.append((j, i))
        temp.append((j + 1, i))
        if martrix[i][j + 1] == '1' or martrix[i][j + 1] == '3':
            right(martrix, i, j+1, temp, temp1)


def down(martrix, i, j, temp, temp2):
    if True:
        temp2.append((j, i))
        temp.append((j, i + 1))
        if martrix[i + 1][j] == '2' or martrix[i + 1][j] == '3':
            down(martrix, i+1, j, temp, temp2)

def maze_zero(martrix):
    for i in range(len(martrix)):
        for j in range(len(martrix[0])):
            if martrix[i][j] != '0':
                return False
    return True

def open_txt(filename):
    martrix = []
    final = []
    for line in open(filename):
        if re.fullmatch(r'[ \s]*', line):
            continue
        else:
            martrix.append(line)
    for i in range(len(martrix)):
        martrix[i] = martrix[i].rstrip('\n')
        martrix[i] = martrix[i].strip(' ')
    for i in range(len(martrix)):
        temp = []
        for j in martrix[i]:
            if re.match('[0-3]', j):
                temp.append(j)
            else:
                continue
        final.append(temp)
    if len(final) < 2 or len(final) > 41:
        return None
    if len(final[0]) < 2 or len(final[0]) > 31:
        return None
    for i in range(len(final)):
        if i < len(final) -1 and len(final[i]) != len(final[i+1]):
            return None
    for i in range(len(final)):
        if final[i][len(final[i])-1] == '1' or final[i][len(final[i])-1] == '3':
            return False
    for i in final[len(final) - 1]:
        if i == '2' or i == '3':
            return False
    return final

def find_gates(martrix):
    #print(martrix)
    length = len(martrix) - 1
    width = len(martrix[0]) - 1
    gates_list = []
    for i in range(width):
        if martrix[0][i] == '0' or martrix[0][i] == '2':
            gates_list.append((0, i))
        if martrix[length][i] == '0':
            gates_list.append((length - 1, i))

    for i in range(length):
        if martrix[i][0] == '0' or martrix[i][0] == '1':
            gates_list.append((i, 0))
        if martrix[i][width] == '0':
            gates_list.append((i,width - 1))
    #print(gates_list)
    return gates_list


def find_walls(martrix):
    array = copy.deepcopy(martrix)
    walls_list = []
    for i in range(len(martrix)):
        for j in range(len(martrix[0])):
            temp = []
            if array[i][j] == '1' or array[i][j] == '2' or array[i][j] == '3':
                array[i][j] = '0'
                temp.append((i, j))
                if i > 0:
                    wall_up(martrix, array, temp, i-1, j)
                if i < len(array) -1:
                    if martrix[i][j] != '1':   #2和3时向下
                        wall_down(martrix, array, temp, i+1, j)
                if j > 0:
                    wall_left(martrix, array, temp, i, j-1)
                if j < len(martrix[0]) - 1:
                    if martrix[i][j] != '2':   #1和3时向右
                        wall_right(martrix, array, temp, i, j+1)
                walls_list.append(temp)

    return walls_list

def wall_up(martrix, array, temp, i, j): #向上只有2和3可行
    if array[i][j] == '2' or array[i][j] == '3':
        array[i][j] = '0'
        temp.append((i, j))
        if i > 0:
            wall_up(martrix, array, temp, i - 1, j)
        if j > 0:
            wall_left(martrix, array, temp, i, j - 1)
        if j < len(array[0]) - 1:
            if martrix[i][j] == '3':
                wall_right(martrix, array, temp, i, j + 1)
        if i < len(array) - 1:
            if martrix[i][j] != '1':  # 2和3时向下
                wall_down(martrix, array, temp, i + 1, j)

def wall_down(martrix, array, temp, i, j):
    if True:
        array[i][j] = '0'
        temp.append((i, j))
    if j != 0:
        wall_left(martrix, array, temp, i, j - 1)
    if i < len(array) - 1:
        if martrix[i][j] != '1':
            if martrix[i][j] != '0':
                wall_down(martrix, array, temp, i + 1, j)
    if j < len(array[0]) - 1:
        if martrix[i][j] != '2':
            if martrix[i][j] != '0':
                wall_right(martrix, array, temp, i, j + 1)
    if i > 0:
        wall_up(martrix, array, temp, i - 1, j)

def wall_left(martrix, array, temp, i, j):
    if array[i][j] == '1' or array[i][j] == '3':
        temp.append((i, j))
        array[i][j] = '0'
        if j != 0:
            wall_left(martrix, array, temp, i, j - 1)
        if i != 0:
            wall_up(martrix, array, temp, i - 1, j)
        if i != len(array) - 1:
            if martrix[i][j] == '3':
                wall_down(martrix, array, temp, i + 1, j)
        if j < len(array[0]) - 1:
            if martrix[i][j] != '2':
                if martrix[i][j] != '0':
                    wall_right(martrix, array, temp, i, j + 1)

def wall_right(martrix, array, temp, i, j):
    if True:
        temp.append((i, j))
        array[i][j] = '0'
    if i != 0:
        wall_up(martrix, array, temp, i - 1, j)
    if j < len(array[0]) - 1:
        if martrix[i][j] == '1' or martrix[i][j] == '3':
            wall_right(martrix, array, temp, i, j + 1)
    if i < len(array) - 1:
        if martrix[i][j] == '2' or martrix[i][j] == '3':
            wall_down(martrix, array, temp, i + 1, j)
    if j != 0:
        wall_left(martrix, array, temp, i, j - 1)


def find_pillar(martrix):
    pillar = []
    if True:
        if martrix[0][0] == '0':
            pillar.append((0, 0))
    for i in range(1, len(martrix)):
        if True:
            if martrix[i][0] == '0':
                if martrix[i - 1][0] == '1' or martrix[i - 1][0] == '0':
                    martrix.append((i, 0))
    for i in range(1, len(martrix)):
        for j in range(1, len(martrix[i])):
            if True:
                if martrix[i][j] == '0':
                    if martrix[i][j - 1] == '2' or martrix[i][j - 1] == '0':
                        if martrix[i - 1][j] == '1' or martrix[i - 1][j] == '0':
                            pillar.append((i, j))
    for i in range(1, len(martrix[0])):
        if True:
            if martrix[0][i] == '0':
                if martrix[0][i - 1] == '2' or martrix[0][i - 1] == '0':
                    pillar.append((0, i))
    return pillar


def build_inner_points(martrix):
    #print(martrix)
    class elements:
        def __init__(self, value, right_value, down_value):
            self.value = value
            self.right_value = right_value
            self.down_value = down_value
            self.dir = [True, True, True, True]
            if self.value == '1':
                self.dir[0] = False
            elif self.value == '2':
                self.dir[2] = False
            elif self.value == '3':
                self.dir[0] = False
                self.dir[2] = False
            if self.right_value == '2' or self.right_value == '3':
                self.dir[3] = False
            if self.down_value == '1' or self.down_value == '3':
                self.dir[1] = False
            self.visit = False

    inner_list= []
    for i in range(len(martrix)):
        row = []
        for j in range(len(martrix[0])):
            row.append(None)
        inner_list.append(row)

    for i in range(len(martrix)):
        for j in range(len(martrix[0])):
            if i == len(martrix)-1 and j == len(martrix[0]) - 1:
                inner_list[i][j] = elements(martrix[i][j], 0, 0)
            elif i < len(martrix)-1 and j == len(martrix[0])-1:
                inner_list[i][j] = elements(martrix[i][j], 0, martrix[i + 1][j])
            elif i == len(martrix)-1 and j <= len(martrix[0])-1:
                inner_list[i][j] = elements(martrix[i][j], martrix[i][j + 1], 0)
            else:
                inner_list[i][j] = elements(martrix[i][j], martrix[i][j + 1], martrix[i + 1][j])

    return inner_list

#inner_list = build_inner_points(martrix)

def dfs_elements(i, j, inner_list, martrix):
    if i >= 0 and i <= len(martrix)-2:
        if j >= 0 and j <= len(martrix[0]) - 2:
            if not inner_list[i][j].visit:
                inner_list[i][j].visit = True
                if inner_list[i][j].dir[0]:
                    dfs_elements(i - 1, j,inner_list, martrix)
                if inner_list[i][j].dir[1]:
                    dfs_elements(i + 1, j, inner_list, martrix)
                if inner_list[i][j].dir[2]:
                    dfs_elements(i, j - 1, inner_list, martrix)
                if inner_list[i][j].dir[3]:
                    dfs_elements(i, j + 1, inner_list, martrix)

def find_accessible_area(gates, inner_list, martrix):
    area = 0
    for i in range(len(martrix)):
        for j in range(len(martrix[0])):
            if (i,j) in gates and inner_list[i][j].visit == False:
                dfs_elements(i, j, inner_list, martrix)
                area += 1
    return area

def find_no_inner_points(inner_list):
    inaccessible_inner_points= []
    for i in range(len(inner_list)-1):
        for j in range(len(inner_list[0])-1):
            if inner_list[i][j].visit == False:
                inaccessible_inner_points.append((i, j))
    return  inaccessible_inner_points

def build_cul_de_sacs(martrix, inner_list, inaccessible_inner_points):
    dead_end_list = copy.deepcopy(inner_list)
    cul_count_list = []
    class cul_elements:
        def __init__(self, value):
            self.value = value
            self.visit = False
    for i in range(len(martrix)):
        for j in range(len(martrix[0])):
            #print((i,j))
            count = 0
            if (i, j) not in inaccessible_inner_points:
                #count = 0
                for k in inner_list[i][j].dir:
                    if k == True:
                        count += 1
                #print(count)
                dead_end_list[i][j] = cul_elements(count)
                cul_count_list.append((i,j))
            dead_end_list[i][j] = cul_elements(count)
    return dead_end_list, cul_count_list

def check(dead_end_list, martrix):
    for i in range(len(martrix)):
        for j in range(len(martrix[0])):
            if dead_end_list[i][j].value == 1:
                return False
    return True

def change_point_count(martrix, dead_end_list, inner_list, cul_count_list):
    while not check(dead_end_list, martrix):
        for i in range(len(martrix)):
            for j in range(len(martrix[0])):
                if dead_end_list[i][j].value == 1:
                    dead_end_list[i][j].value -= 2
                    if inner_list[i][j].dir[0]:
                        if (i - 1, j) in cul_count_list:
                            dead_end_list[i - 1][j].value -= 1
                    if inner_list[i][j].dir[1]:
                        if (i + 1, j) in cul_count_list:
                            dead_end_list[i + 1][j].value -= 1
                    if inner_list[i][j].dir[2]:
                        if (i, j - 1) in cul_count_list:
                            dead_end_list[i][j - 1].value -= 1
                    if inner_list[i][j].dir[3]:
                        if (i, j + 1) in cul_count_list:
                            dead_end_list[i][j + 1].value -= 1
    return dead_end_list

def dfs_cul_de_sacs(i, j, temp,dead_end_list, martrix, inner_list):
    if i >= 0 and i <= len(martrix) - 2:
        if j >= 0 and j <= len(martrix[0]) - 2:
            if dead_end_list[i][j].value < 0:
                if not dead_end_list[i][j].visit:
                    dead_end_list[i][j].visit = True
                    if inner_list[i][j].dir[0]:
                        dfs_cul_de_sacs(i - 1, j, temp, dead_end_list, martrix, inner_list)
                    if inner_list[i][j].dir[1]:
                        dfs_cul_de_sacs(i + 1, j, temp, dead_end_list, martrix, inner_list)
                    if inner_list[i][j].dir[2]:
                        dfs_cul_de_sacs(i, j - 1, temp, dead_end_list, martrix, inner_list)
                    if inner_list[i][j].dir[3]:
                        dfs_cul_de_sacs(i, j + 1, temp, dead_end_list, martrix, inner_list)
                    temp.append((i, j))

def get_number_cul_de_sacs(dead_end_list, martrix, inner_list):
    temp = []
    final = []
    cul_de_sacs = 0
    for i in range(len(dead_end_list)):
        for j in range(len(dead_end_list[0])):
            if dead_end_list[i][j].value < 0:
                if not dead_end_list[i][j].visit:
                    dfs_cul_de_sacs(i, j, temp, dead_end_list, martrix, inner_list)
                    cul_de_sacs += 1

    return cul_de_sacs

def find_path(i, j, temp, accessible_gates_point, martrix, dead_end_list, inner_list):
    if i >= 0:
        if i <= len(martrix) - 2:
            if j >= 0:
                if j <= len(martrix[0]) - 2:
                    if (i, j) not in temp:
                        if dead_end_list[i][j].value == 2:
                            if not dead_end_list[i][j].visit:
                                dead_end_list[i][j].visit = True
                                if True:
                                    if inner_list[i][j].dir[0]:
                                        find_path(i - 1, j, temp, accessible_gates_point, martrix, dead_end_list, inner_list)
                                    if inner_list[i][j].dir[1]:
                                        find_path(i + 1, j, temp, accessible_gates_point, martrix, dead_end_list, inner_list)
                                    if inner_list[i][j].dir[2]:
                                        find_path(i, j - 1, temp, accessible_gates_point, martrix, dead_end_list, inner_list)
                                    if inner_list[i][j].dir[3] :
                                        find_path(i, j + 1, temp, accessible_gates_point, martrix, dead_end_list, inner_list)
                                    accessible_gates_point.append((i, j))


def final_path(gates, martrix, inner, dead_end_list, inner_list):
    route = []
    temp = []
    accessible_gates_point = []
    gates_copy = copy.deepcopy(gates)
    for i in range(len(inner_list)):
        for j in range(len(inner_list[0])):
            if (i, j) in gates_copy:
                if not inner[i][j].visit:
                    gates_copy.remove((i, j))
                    find_path(i, j, temp, accessible_gates_point, martrix, dead_end_list, inner_list)
                    x = [k for k in accessible_gates_point if k in gates_copy]
                    if len(x) == 1:
                        route.append(accessible_gates_point)
                        accessible_gates_point = []
                    else:
                        accessible_gates_point = []
                        continue

    final_route = []
    for i in route:
        final_route.append(i[::-1])
    return final_route
