import sys
import numpy as np


class Dot:
    def __init__(self, i, j, value, patDot=None, mStart=0, eToEnd=0):
        self.i = i
        self.j = j
        self.value = value
        self.eToEnd = eToEnd
        self.mStart = mStart
        self.patDot = patDot
        # 四个方向邻居，全部初始化为 None
        self.up = None
        self.down = None
        self.dot_le = None
        self.dot_ri = None

    def _dot_g_Cost(self, patDot):
        # 按作业公式: 上坡 cost = 1 + diff, 平路/下坡 cost = 1
        if patDot.value == 'X' or self.value == 'X':
            return 99
        if int(patDot.value) > int(self.value):
            # 从高处到低处 (下坡), cost = 1
            return 1
        else:
            # 平路或上坡, cost = 1 + (目标高度 - 当前高度)
            return 1 + int(self.value) - int(patDot.value)

    def manhattan_dis(self, end):
        self.eToEnd = np.abs(self.i - end.i) + np.abs(self.j - end.j)

    def euclidean_dis(self, end):
        self.eToEnd = np.sqrt(np.power(self.i - end.i, 2) + np.power(self.j - end.j, 2))


def set_distance(r, c, order, nodeList, endRow, endCol):
    if order == "euclidean":
        nodeList[r][c].euclidean_dis(nodeList[endRow][endCol])
    elif order == "manhattan":
        nodeList[r][c].manhattan_dis(nodeList[endRow][endCol])


def set_connect(dol1st, r, c, rows, cols):
    # 上: 有上方节点且不是 X
    if r > 0 and dol1st[r - 1][c].value != 'X':
        dol1st[r][c].up = dol1st[r - 1][c]
    else:
        dol1st[r][c].up = None

    # 下
    if r < rows - 1 and dol1st[r + 1][c].value != 'X':
        dol1st[r][c].down = dol1st[r + 1][c]
    else:
        dol1st[r][c].down = None

    # 左
    if c > 0 and dol1st[r][c - 1].value != 'X':
        dol1st[r][c].dot_le = dol1st[r][c - 1]
    else:
        dol1st[r][c].dot_le = None

    # 右: 修复原来少了 .value 的 bug
    if c < cols - 1 and dol1st[r][c + 1].value != 'X':
        dol1st[r][c].dot_ri = dol1st[r][c + 1]
    else:
        dol1st[r][c].dot_ri = None


def re_rfile(openfile, do1ist, rows, cols, endP_i, endP_j, order=''):
    n_rows = 1
    for line in openfile:
        if n_rows >= 4:
            col = 0
            line = line.replace('\n', '')
            do1ist.append([])
            for value in line.split(' '):
                do1ist[n_rows - 4].append(Dot(value=value, i=n_rows - 4, j=col))
                col += 1
        n_rows += 1

    for h_r in range(rows):
        for l_c in range(cols):
            set_distance(h_r, l_c, order, do1ist, endP_i, endP_j)
            set_connect(do1ist, h_r, l_c, rows, cols)

    return do1ist


def sh_path(nodelist):
    for line in nodelist:
        row_str = ''
        for node in line:
            row_str += node.value
        print(' '.join(row_str))


def expand(node1, fringe, closed, order):
    temoL1st = []
    # 作业要求展开顺序: 上、下、左、右
    neighbors = [node1.up, node1.down, node1.dot_le, node1.dot_ri]

    for neighbor in neighbors:
        if neighbor is None or neighbor in closed:
            continue

        new_g_cost = neighbor._dot_g_Cost(node1) + node1.mStart

        if order == 'bfs':
            # BFS 只关心是否已发现，不更新代价
            if neighbor not in fringe:
                neighbor.patDot = node1
                temoL1st.append(neighbor)
        else:
            # UCS / A*: 若节点不在 fringe 则加入；若在 fringe 但找到更便宜路径则更新
            if neighbor not in fringe:
                neighbor.patDot = node1
                neighbor.mStart = new_g_cost
                temoL1st.append(neighbor)
            elif new_g_cost < neighbor.mStart:
                # 找到更优路径，原地更新，无需重新加入
                neighbor.patDot = node1
                neighbor.mStart = new_g_cost

    return temoL1st


def ucsMagic(node):
    # UCS 按累计路径代价排序
    return node.mStart


def astartMagic(node):
    # A* 按 f = g + h 排序
    return node.mStart + node.eToEnd


def splitInput(openfile):
    lines = openfile.readlines()
    rows = int(lines[0].split(' ')[0])
    cols = int(lines[0].split(' ')[1])
    startP_i = int(lines[1].split(' ')[0]) - 1
    startP_j = int(lines[1].split(' ')[1]) - 1
    endP_i = int(lines[2].split(' ')[0]) - 1
    endP_j = int(lines[2].split(' ')[1]) - 1
    return rows, cols, startP_i, startP_j, endP_i, endP_j


def ma_path(dot, startNode, nodeList):
    dot.value = '*'
    if dot.patDot is None:
        if dot.i == startNode.i and dot.j == startNode.j:
            sh_path(nodeList)
        else:
            print("null")
        return
    ma_path(dot.patDot, startNode, nodeList)


def pathSearch(endNode, startNode, nodeList, order):
    closed = []
    fringe = [startNode]

    while fringe:
        if order == 'ucs':
            fringe.sort(key=ucsMagic)
        elif order == 'astar':
            fringe.sort(key=astartMagic)

        node = fringe.pop(0)

        if node.i == endNode.i and node.j == endNode.j:
            ma_path(node, startNode, nodeList)
            return

        if node not in closed:
            closed.append(node)
            for i in expand(node, fringe, closed, order):
                fringe.append(i)

    # fringe 耗尽仍未到终点，无解
    print("null")


def main():
    inputinfm = sys.argv
    lenAgrs = len(inputinfm)

    if lenAgrs < 3:
        print("null")
        return

    openfile = open(inputinfm[1])
    o = open(inputinfm[1])
    rows, cols, startP_i, startP_j, endP_i, endP_j = splitInput(o)

    dot_ls = []

    # astar 需要第 4 个参数 heuristic
    if lenAgrs > 3:
        re_rfile(openfile, dot_ls, rows, cols, endP_i, endP_j, inputinfm[3])
    else:
        re_rfile(openfile, dot_ls, rows, cols, endP_i, endP_j)

    pathSearch(dot_ls[endP_i][endP_j], dot_ls[startP_i][startP_j], dot_ls, inputinfm[2])


main()
