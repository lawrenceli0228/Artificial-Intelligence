import sys
import numpy as np



class Position:
    def __init__(self, i, j, N ='1', E = '1',S = '1',W = '1', init_p=0.00, neighbor=[]):
        self.i = i
        self.j = j
        self.N = N
        self.E = E
        self.S = S
        self.W = W
        self.init_p = init_p
        self.neighbor = neighbor


# read_file
def read_file(file):
    file = open(file)
    dataSet = file.read().splitlines()
    return dataSet




def getdiffer_max(Y, a):
    differ_max = 4
    for i in range(4):
        if a[i] == Y[i]:
            differ_max -= 1
    return differ_max



def parse_file(r):
    K = 0  # free space
    O = []  # all the item in the map
    S = []  # the space robot can put in
    T = 0
    Y = []
    inti_possibility = 0
    #print(r_len)
    map_size = r.pop(0).split()
    error_rat = float(r.pop())
    row = int(map_size[0])
    col = int(map_size[1])
    N = row * col
    map_lines = row
    #print(map_lines)
    for i in range(map_lines):
        line = r.pop(0).split()
        O.append(line)
        for j in range(len(line)):
            if line[j] == '0':
                S.append(Position(i+1, j + 1))
                K += 1
    P = np.array([1.0 / K] * K)
    T = int(r.pop(0))
    for line in r:
        Y.append(line)
    for state in S:
        set_node(state,O,S)
    return N, O, K, S, P, T, Y, error_rat



def initalize_Tm(row,col,S):
    Tm = np.empty((row, col))
    Tm.fill(0.000)
    for i in range(len(S)):
        for var in S[i].neighbor:
            Tm[i][var] = S[i].init_p
    Tm = Tm.T
    return Tm



def initalize_Em(row, col,error_rate, S, Y):
    Em = np.empty((row, col))
    Em.fill(0.000)
    K = row
    T = col
    a_nesw = ""
    for t in range(T):
        for k in range(K):
            a_nesw = S[k].N + S[k].E + S[k].S + S[k].W
            error_m = getdiffer_max(Y[t], a_nesw)
            Em[k][t] = pow(error_rate, error_m) * pow(1 - error_rate, 4 - error_m)
    return Em




def initalize_trellis(row,col, P):
    trellis = np.empty((row, col))
    for i in range(K):
        trellis[i][0] = P[i] * Em[i][0]
    return trellis


def set_node(state, O, S):
    count = 0
    if state.i > 1 and O[state.i - 2][state.j - 1] == '0':
        state.N = '0'  # North 北
        count += 1
    if state.j < len(O[-1]) and O[state.i - 1][state.j] == '0':
        state.E = '0'  # East 东
        count += 1
    if state.i < len(O) and O[state.i][state.j - 1] == '0':
        state.S = '0'  # South 南
        count += 1
    if state.j > 1 and O[state.i - 1][state.j - 2] == '0':
        state.W = '0'  # West 西
        count += 1
    if count > 0:
        inti_possibility = 1.0 / count
    else:
        inti_possibility = 0
    state.init_p = inti_possibility
    neighborhood = []
    for i_i in range(len(S)):
        if abs(S[i_i].i - state.i) + abs(S[i_i].j - state.j) == 1:
            neighborhood.append(i_i)
        state.neighbor = neighborhood

    #print(state.neighbor)


# def initialize_list(row,col):
#     twod_list = []
#     for i in range(0, 10):
#         new = []
#         for j in range(0, 10):
#             new.append(0.001)
#         twod_list.append(new)

intext = sys.argv
r = read_file(intext[1])
N, O, K, S, P, T, Y, error_rate = parse_file(r)
Tm = initalize_Tm(K, K, S)
Em = initalize_Em(K, T, error_rate, S, Y)
trellis = initalize_trellis(K, T, P)

# N, O, K, S, P, T, Y, error_rate = parseFileContent(r)
# print(Y)  # observation space
# print(T)  # observation times
# print(P)  # array of initial probabilities
# print(len(S))  # state space
# print(K)  # free space
# print(O)  # map item
# print(N)  # map size
# quit()


# Tm = np.empty((K, K))
# Tm.fill(0.000)
# a = [x[:] for x in [[0.01] * K] * K]
# print(a)



# Tm = np.arange(K * K).reshape((K, K))
# Tm = np.zeros_like(a=Tm, dtype=float)
# print(Tm)
# print(a)
# quit()

# trellis = np.arange(K * T, dtype=float, ).reshape((K, T))
# trellis = np.zeros_like(a=trellis, dtype=float)
#
# for i in range(K):
#     trellis[i][0] = P[i] * Em[i][0]




for j in range(1,T):
    for i in range(K):
        tmp = 0
        for k in range(K):
            tmp = max(tmp, trellis[k][j-1] * Tm[i][k] * Em[i][j])
        trellis[i][j] = tmp

print(trellis)
quit()

map1 = np.arange(N).reshape(len(O), int(N/len(O)))
maps = []

for i in range(len(trellis.T)):
    map1 = np.zeros_like(a=map1, dtype=float)
    for j in range(len(S)):
        map1[S[j].i-1][S[j].j-1] = trellis[j][i]
    maps.append(map1)

print(maps)
np.savez("output.npz", *maps)


# Tm = np.empty((K, K))
# Tm.fill(0.000)
# a = [x[:] for x in [[0.01] * K] * K]
# print(a)



# Tm = np.arange(K * K).reshape((K, K))
# Tm = np.zeros_like(a=Tm, dtype=float)
# print(Tm)
# print(a)
# quit()

# trellis = np.arange(K * T, dtype=float, ).reshape((K, T))
# trellis = np.zeros_like(a=trellis, dtype=float)
#
# for i in range(K):
#     trellis[i][0] = P[i] * Em[i][0]


#print(trellis)

# for j in range(1,T):
#     for i in range(K):
#         tmp = 0
#         for k in range(K):
#             tmp = max(tmp, trellis[k][j-1] * Tm[i][k] * Em[i][j])
#         trellis[i][j] = tmp








# for i in range(len(dataSet)):
#     print(dataSet[i])

#
# def read_file1(file):
#     file_c = []
#     with open(file) as f:
#         for line in f:
#            file_c.append(line.strip())
#     f.closed
#return file_c

# def parseFileContent(file_content):
#     K = 0   # free space
#     O = []  # all the item in the map
#     S = []  # the space robot can put in
#     map_lines = 0
#     #index = 0
#     #Z = []
#     f_len = len(file_content)
#     for i in range(f_len):
#         if i == 0:
#             map_size = file_content[i].split()
#             # print(map_size)
#             # quit()
#             row = int(map_size[0])
#             col = int(map_size[1])
#             N = row * col
#             map_lines = row
#         elif i < map_lines + 1:
#             map_l = file_content[i].split()
#             O.append(map_l)
#             for j in range(len(map_l)):
#                 if map_l[j] == '0':
#                     S.append(Position(i,j+1))
#                     K += 1
#                     #print(S[index].i,S[index].j)
#                     #index += 1
#             #print(len(S))
#
#         elif i == map_lines + 1:
#             T = int(file_content[i])
#             Y = [0] * T
#         elif i <= map_lines + T + 1:
#             Y[i - map_lines - 2] = file_content[i]
#             # print(Y)
#             # Z.append(file_content[i])
#             # print()
#             # print(Z)
#
#         else:
#             error_rate = float(file_content[i])
#             #print(error_rate)
#
#     P = np.array([1.0/K] * K)
#     for state in S:
#         if state.i > 1 and O[state.i - 2][state.j - 1] == '0':
#             state.N = '0'
#         if state.j < len(O[state.i - 1]) and O[state.i - 1][state.j] == '0':
#             state.E = '0'
#         if state.i < len(O) and O[state.i][state.j - 1] == '0':
#             state.S = '0'
#         if state.j > 1 and O[state.i - 1][state.j - 2] == '0':
#             state.W = '0'
#     return N, O, K, S, P, T, Y, error_rate

# def getInitProbalitiy(item,s):
#     indexed = []
#     #  find the item 's neighborhood
#     for i_i in range(len(s)):
#         if s[i_i].i == item.i + 1 and s[i_i].j == item.j:
#             indexed.append(i_i)
#         if s[i_i].i == item.i - 1 and s[i_i].j == item.j:
#             indexed.append(i_i)
#         if s[i_i].i == item.i and s[i_i].j == item.j + 1:
#             indexed.append(i_i)
#         if s[i_i].i == item.i and s[i_i].j == item.j - 1:
#             indexed.append(i_i)
#     return indexed

# for i in range(len(S)):
#     b = getInitProbalitiy(S[i], S)
#     print(b)
#     for j in b:
#         Tm[i][j] = S[i].init_p
# for i in range(len(S)):
#     for var in S[i].neighbor:
#         Tm[i][var] = S[i].init_p

# print(Tm)
# quit()
# Tm = Tm.T


# Em = np.arange(K * T).reshape((K,T))
# Em = np.zeros_like(a=Em, dtype=float)
#
#
# for t in range(T):
#     for k in range(K):
#         errorMun = getErrorNumByYt(Y[t], S[k])
#         #print(errorMun)
#         Em[k][t] = pow(error_rate, errorMun) * pow(1 - error_rate, 4 - errorMun)
# def initialize_list(row,col):
#     twod_list = []
#     for i in range(0, 10):
#         new = []
#         for j in range(0, 10):
#             new.append(0.001)
#         twod_list.append(new)
#print(Em)
# print(state.neighbor)