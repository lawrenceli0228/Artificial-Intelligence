import sys

import numpy as np

class Node:
    def __init__(self, i, j, val, parNode = None, pathCostFromSatrt=0, distanceToeEnd = 0):
        self.i = i
        self.j = j
        self.val = val

        self.distanceToEnd = distanceToeEnd
        self.pathCostFromStart = pathCostFromSatrt
        self.parNode = parNode


    def getCost(self,parent):
        if self.val == 'X':
            return 99
        elif int(parent.value) > int(self.val):
            return 1
        else:
            return 1 + int(self.val) - int(parent.value)

    def setMHT_distance(self,  end):
        self.distanceToEnd = np.abs(self.i - end.i) + np.abs(self.j - end.j)

    def setELD_distance(self, end):
        self.distanceToEnd = np.sqrt(np.power(self.i-end.i, 2) + np.power((self.j-end.j), 2))




def readfile(openfile, nodeList,rows,cols ,order =''):
    n = 1
    rows = rows
    cols = cols
    startRow = 0
    startCol = 0
    endRow = 0
    endCol = 0


    for line in openfile:
       if n >= 4:
            c = 0
            line = line.replace('\n', '')
            #print(line)
            for v in line.split(' '):
                nodeList[n - 4].append(Node(val=v, i=n - 4, j=c))
                c += 1

       if 3 < n <= rows + 3:
            nodeList.append([])
       n += 1

    for h in range(rows):
        for l in range(cols):
            if order == "euclidean":
                nodeList[h][l].euclidean_dis(nodeList[endRow][endCol])
            elif order == "manhattan" :
                nodeList[h][l].manhattan_dis(nodeList[endRow][endCol])

            if 0 < h and nodeList[h - 1][l].value != 'X':
                nodeList[h][l].up = nodeList[h - 1][l]
            else:
                nodeList[h][l].up = None
            if h < rows - 1 and nodeList[h + 1][l].value != 'X':
                nodeList[h][l].down = nodeList[h + 1][l]
            else:
                nodeList[h][l].down = None
            if l > 0 and nodeList[h][l - 1].value != 'X':
                nodeList[h][l].dot_le = nodeList[h][l - 1]
            else:
                nodeList[h][l].dot_le = None
            if l < cols - 1 and nodeList[h][l + 1] != 'X':
                nodeList[h][l].dot_ri = nodeList[h][l + 1]
            else:
                nodeList[h][l].dot_ri = None


    return startRow, startCol, endRow,endCol, nodeList


def insert(node,fringe):
    fringe.append(node)


def test_goal(node,endNode):
    return node.i == endNode.i and node.j == endNode.j


def markPath(node):
    node.value = '*'
    if node.patDot is None:
        return
    markPath(node.patDot)



def printPath(nodelist):
    for line in nodelist:
        str = ''
        for node in line:
            str += node.value + ' '
        print(str)



def expand(node1,fringe,closed):
    successor = []

    if node1.up is not None and node1.up not in fringe and node1.up not in closed:
        successor.append(node1.up)

    if node1.down is not None and node1.down not in fringe and node1.down not in closed:
        successor.append(node1.down)

    if node1.dot_le is not None and node1.dot_le not in fringe and node1.dot_le not in closed:
        successor.append(node1.dot_le)

    if node1.dot_ri is not None and node1.dot_ri not in fringe and node1.dot_ri not in closed:
        successor.append(node1.dot_ri)

    for anode in successor:
        print(anode.i, anode.j, "parNode is ", node1.i, node1.j)
        anode.patDot = node1
        anode.mStart = anode._dot_g_Cost(anode.patDot) + anode.patDot.mStart
        print(anode.i, anode.j, "到节点 ", node1.i, node1.j, '花费是： ', anode._dot_g_Cost(anode.patDot), ' 路程总花费', anode.patDot.mStart)

    return successor


def bfs_graph_search(endNode, startNode,nodeList):
    closed = []
    fringe = []
    insert(startNode,fringe)

    while 1:

        if len(fringe) == 0:
            print("null")
            return
        if fringe[0].value != 'X':
            node = fringe[0]

        if test_goal(node, endNode):
            print("finished")
            markPath(node)
            printPath(nodeList)
            return
        if node not in closed and node.value != 'X':
            closed.append(node)
            for i in expand(node,fringe,closed):
                insert(i,fringe)
        fringe.remove(fringe[0])


def getG(node):
    if node.patDot is not None:
        return node._dot_g_Cost(node.patDot)
    else:
        return 0


def getGandH(node):
    if node.patDot is not None:
        return node.mStart + node.eToEnd
    else:
        return node.eToEnd


def astar_graph_search(endNode,startNode,nodelist):
    closed = []
    fringe = []
    insert(startNode,fringe)
    while True:
        if len(fringe) == 0:
            print("null")
            return

        fringe.sort(key=getGandH)
        node = fringe[0]
        if test_goal(node, endNode):
            print("finished")
            markPath(node)
            printPath(nodelist)
            return
        if node not in closed:
            closed.append(node)
            for i in expand(node, fringe, closed):
                insert(i, fringe)
        fringe.remove(fringe[0])


def ucs_graph_search(endNode, startNode,nodelist):
    closed = []
    fringe = []
    insert(startNode,fringe)

    while True:
        if len(fringe) == 0:
            print("null")
            return

        fringe.sort(key=getG)
        node = fringe[0]
        if test_goal(node, endNode):
            print("finished")
            markPath(node)
            printPath(nodelist)
            return
        if node not in closed:
            closed.append(node)
            for i in expand(node, fringe, closed):
                insert(i, fringe)
        fringe.remove(fringe[0])





def readInput():
    intext = sys.argv
    lenofIndex = len(intext)
    return intext, lenofIndex

def splitInput(openfile):
    lines = openfile.readlines()

    size = lines[0]
    start = lines[1]
    end = lines[2]
    rows = int(size.split(' ')[0])
    cols = int(size.split(' ')[1])
    startP_i = int(start.split(' ')[0]) - 1
    startP_j = int(start.split(' ')[1]) - 1
    endP_i = int(end.split(' ')[0]) - 1
    endP_j = int(end.split(' ')[1]) - 1

    print("mapSize",rows, cols)
    print("start point",startP_i, startP_j)
    print("end point",endP_j, endP_i)

    return rows, cols,startP_i, startP_j,endP_j, endP_i



def main():
    '''
    # 读参数 args: 0 : 文件名, 1：地图名，3搜索方法
    args = sys.argv
    file = open(args[1])
    # 构造一个地图
    nodeList = [[]]
    # 读txt文件 返回起点坐标和终点坐标
    start_i, start_j, end_i, end_j, alist = readfile(file, nodeList,args[3])
    astar_graph_search(nodeList[end_i][end_j], nodeList[start_i][start_j], nodeList)
    '''
    # 读参数 args: 0 : 文件名, 1：地图名，3搜索方法
    input, lenAgrs = readInput()
    openfile = open(input[1])

    #读前三行的东西
    o = open(input[1])
    #返回起点坐标和终点坐标
    rows, cols,startP_i, startP_j,endP_j, endP_i = splitInput(o)

    nodeList = [[]]
    readfile(openfile, nodeList, rows, cols)


    '''
    if lenAgrs > 3:
        readfile(openfile, nodeList, rows, cols,input[3])
        astar_graph_search(nodeList[endP_i][endP_j], nodeList[startP_i][startP_j], nodeList)
        print(input[3])
    else:
        readfile(openfile, nodeList, rows, cols)
        if input[2] == 'bfs':
            bfs_graph_search(nodeList[endP_i][endP_j], nodeList[startP_i][startP_j], nodeList)
        elif input[2] == 'ucs':
            ucs_graph_search(nodeList[endP_i][endP_j], nodeList[startP_i][startP_j], nodeList)
    '''
main()