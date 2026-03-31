import sys
import numpy as np


class Bot_information:
    def __init__(self, i, j, real_i, real_j, N ='1', E = '1',S = '1',W = '1', init_p=0.00, neighbor=[]):
        self.i = i
        self.j = j
        self.real_i = real_i
        self.real_j = real_j
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
    state_sp_K = 0  # free space
    observation_sp = []  # all the item in the map
    state_sp = []  # the space robot can put in
    senor_num = 0
    senor = []
    map_size = r.pop(0).split()
    error_r = float(r.pop())
    row = int(map_size[0])
    col = int(map_size[1])
    map_are = row * col
    map_lines = row
    for i in range(map_lines):
        line = r.pop(0).split()
        observation_sp.append(line)
        for j in range(len(line)):
            if line[j] == '0':
                state_sp.append(Bot_information(i + 1, j + 1, i, j))
                state_sp_K += 1
    P = 1.0 / state_sp_K
    senor_num = int(r.pop(0))
    for line in r:
        senor.append(line)
    for state in state_sp:
        set_node_connect(state, observation_sp, state_sp)
    return map_are, observation_sp, state_sp_K, state_sp, P, senor_num, senor, error_r



def initalize_Tm(row, col, state_sp):
    Tm = np.empty((row, col))
    Tm.fill(0.000)
    for i in range(len(state_sp)):
        for var in state_sp[i].neighbor:
            Tm[i][var] = state_sp[i].init_p
    Tm = Tm.T
    return Tm



def initalize_Em(row, col, error_rate, state_sp, senor):
    Em = np.empty((row, col))
    Em.fill(0.000)
    K = row
    T = col
    a_nesw = ""
    for t in range(T):
        for k in range(K):
            a_nesw = state_sp[k].N + state_sp[k].E + state_sp[k].S + state_sp[k].W
            error_m = getdiffer_max(senor[t], a_nesw)
            op1 = error_rate ** error_m
            op2 = (1 - error_rate) ** (4 - error_m)
            Em[k][t] = op1 * op2
    return Em




def initalize_trellis(row, col, P, Em):
    trellis = np.empty((row, col))
    state_sp_K = row
    senor_num = col
    probility = P
    a_Em = [i[0] for i in Em]
    #print(a)
    for i in range(state_sp_K):
        trellis[i][0] = probility * a_Em[i]
    #print(trellis)
    #quit()
    for j in range(1, senor_num):
        for i in range(0, state_sp_K):
            tmp = 0
            for k in range(0, state_sp_K):
                new_j = j - 1
                trellis_re = trellis[k][new_j] * Tm[i][k] * Em[i][j]
                tmp = max(tmp, trellis_re)
            trellis[i][j] = tmp
    return trellis


def set_node_connect(bot, observation_sp, state_sp):
    count = 0
    if bot.i > 1:
        if observation_sp[bot.real_i - 1][bot.real_j] == '0':
            bot.N = '0'  # North 北
            count += 1
    if bot.j < len(observation_sp[-1]):
        if observation_sp[bot.real_i][bot.j] == '0':
            bot.E = '0'  # East 东
            count += 1
    if bot.i < len(observation_sp):
        if observation_sp[bot.i][bot.real_j] == '0':
            bot.S = '0'  # South 南
            count += 1
    if bot.j > 1:
        if observation_sp[bot.real_i][bot.real_j - 1] == '0':
            bot.W = '0'  # West 西
            count += 1

    if count > 0:
        inti_possibility = 1.0 / count
    else:
        inti_possibility = 0
    bot.init_p = inti_possibility
    neighborhood = []
    for i_i in range(len(state_sp)):
        if abs(state_sp[i_i].i - bot.i) + abs(state_sp[i_i].j - bot.j) == 1:
            neighborhood.append(i_i)
        bot.neighbor = neighborhood



intext = sys.argv
r = read_file(intext[1])
map_area, observation_sp, state_sp_K, state_sp, P, senor_num, senor, error_r = parse_file(r)
Tm = initalize_Tm(state_sp_K, state_sp_K, state_sp)
Em = initalize_Em(state_sp_K, senor_num, error_r, state_sp, senor)
trellis = initalize_trellis(state_sp_K, senor_num, P,Em)

map_r = len(observation_sp)
map_c = int(map_area/len(observation_sp))
maps = []
for i in range(len(trellis.T)):
    map1 = np.zeros((map_r, map_c))
    for j in range(len(state_sp)):
        map1[state_sp[j].real_i][state_sp[j].real_j] = trellis[j][i]
    maps.append(map1)

print(maps)
np.savez("output.npz", *maps)



