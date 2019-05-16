from enum import Enum
from copy import deepcopy


class Tile(Enum):
    Block = "b-"
    Block0 = "b0"
    Block1 = "b1"
    Block2 = "b2"
    Block3 = "b3"
    Block4 = "b4"
    EmptyUnlit = "e-"
    EmptyLit = "e+"
    EmptyLamp = "e*"


class GameMap(object):

    def __init__(self, isizein):
        self.Map = []
        self.PointMap = []
        self.iSize = isizein
        for i in range(0, self.iSize):
            x = []
            x_points = []
            for j in range(0, self.iSize):
                x.append(Tile.EmptyUnlit)
                x_points.append(250)
            self.Map.append(x)
            self.PointMap.append(x_points)
    
    def copymap(self, gmap):
        if self.iSize != gmap.iSize:
            print("Cannot Copy maps of different sizes")
            return
        else:
            for i in range(0, self.iSize):
                for j in range(0, self.iSize):
                    self.PointMap[i][j] = gmap.PointMap[i][j]
                    if gmap.Map[i][j] == Tile.Block:
                        self.Map[i][j] = Tile.Block
                    elif gmap.Map[i][j] == Tile.Block0:
                        self.Map[i][j] = Tile.Block0
                    elif gmap.Map[i][j] == Tile.Block1:
                        self.Map[i][j] = Tile.Block1
                    elif gmap.Map[i][j] == Tile.Block2:
                        self.Map[i][j] = Tile.Block2
                    elif gmap.Map[i][j] == Tile.Block3:
                        self.Map[i][j] = Tile.Block3
                    elif gmap.Map[i][j] == Tile.Block4:
                        self.Map[i][j] = Tile.Block4
                    elif gmap.Map[i][j] == Tile.EmptyLamp:
                        self.Map[i][j] = Tile.EmptyLamp
                    elif gmap.Map[i][j] == Tile.EmptyLit:
                        self.Map[i][j] = Tile.EmptyLit
                    elif gmap.Map[i][j] == Tile.EmptyUnlit:
                        self.Map[i][j] = Tile.EmptyUnlit

    def printmapconsole(self):
        for i in range(0, self.iSize):
            for j in range(0, self.iSize):
                print(self.Map[i][j].value, end="")
                print(" ", end="")
            print("")

    def printpointconsole(self):
        for i in range(0, self.iSize):
            for j in range(0, self.iSize):
                print(self.PointMap[i][j], end="")
                if self.PointMap[i][j] < 10:
                    print(" ", end="")
                if self.PointMap[i][j] < 100:
                    print(" ", end="")
                print(" ", end="")
            print("")

    def loadmap(self, spath):
        print("Loading from file " + spath)
        iterator = 0
        try:

            with open(spath) as mapfile:
                while True:
                    tile = mapfile.read(1)

                    if tile == 'E':
                        self.Map[int(iterator / 7)][iterator % 7] = Tile.EmptyUnlit
                    elif tile == 'B':
                        self.Map[int(iterator / 7)][iterator % 7] = Tile.Block
                    elif tile == '0':
                        self.Map[int(iterator / 7)][iterator % 7] = Tile.Block0
                    elif tile == '1':
                        self.Map[int(iterator / 7)][iterator % 7] = Tile.Block1
                    elif tile == '2':
                        self.Map[int(iterator / 7)][iterator % 7] = Tile.Block2
                    elif tile == '3':
                        self.Map[int(iterator / 7)][iterator % 7] = Tile.Block3
                    elif tile == '4':
                        self.Map[int(iterator / 7)][iterator % 7] = Tile.Block4
                    iterator = iterator+1
                    if not tile:
                        break

        except IOError:
            print("Cannot open file...")
            return
        print("", end="")
    
    def placelamp(self, posrow, poscollumn):
        if self.Map[posrow][poscollumn] == Tile.EmptyLit:
            print("cannot place lamps in lit spaces...")
            return

        if self.isblock(posrow, poscollumn):
            print("cannot place lamps on blocks...")
            return

        if self.Map[posrow][poscollumn] == Tile.EmptyLamp:
            print("cannot place lamps on lamps...")
            return

        self.Map[posrow][poscollumn] = Tile.EmptyLamp
        # update lighting
        self.updatelighting(posrow, poscollumn)

    def updatelighting(self, posrow, poscollumn):
        # up
        for i in range(1, posrow + 1):
            if self.isblock(posrow - i, poscollumn):
                break
            else:
                self.Map[posrow - i][poscollumn] = Tile.EmptyLit
        # down
        for j in range(1, self.iSize - posrow):
            if self.isblock(posrow + j, poscollumn):
                break
            else:
                self.Map[posrow + j][poscollumn] = Tile.EmptyLit
        # left
        for i in range(1, poscollumn + 1):
            if self.isblock(posrow, poscollumn - i):
                break
            else:
                self.Map[posrow][poscollumn - i] = Tile.EmptyLit
        # right
        for j in range(1, self.iSize - poscollumn):
            if self.isblock(posrow, poscollumn + j):
                break
            else:
                self.Map[posrow][poscollumn + j] = Tile.EmptyLit
    
    def updatepointmap(self):
        print("Updating Point Map...")
        # set blocks, neighbours of 0 and lit places to max
        for row in range(0, self.iSize):
            for collumn in range(0, self.iSize):
                if self.isblock(row, collumn):
                    self.PointMap[row][collumn] = 256

                    if self.Map[row][collumn] == Tile.Block0:
                        if row > 0:
                            self.PointMap[row-1][collumn] = 256
                        if row+1 < self.iSize:
                            self.PointMap[row+1][collumn] = 256
                        if collumn > 0:
                            self.PointMap[row][collumn-1] = 256
                        if collumn+1 < self.iSize:
                            self.PointMap[row][collumn+1] = 256

                if self.Map[row][collumn] == Tile.EmptyLit or self.Map[row][collumn] == Tile.EmptyLamp:
                    self.PointMap[row][collumn] = 256

        # check for numbered blocks neighbours
        for rowB in range(0, self.iSize):
            for collumnB in range(0, self.iSize):
                if self.isblock(rowB, collumnB):
                    if self.Map[rowB][collumnB] == Tile.Block0 or self.Map[rowB][collumnB] == Tile.Block:
                        continue
                    a = 0  # aviable neighbours to this block
                    if rowB > 0:
                        if self.PointMap[rowB-1][collumnB] < 256:
                            a = a+1
                    if rowB+1 < self.iSize:
                        if self.PointMap[rowB+1][collumnB] < 256:
                            a = a+1
                    if collumnB > 0:
                        if self.PointMap[rowB][collumnB-1] < 256:
                            a = a+1
                    if collumnB+1 < self.iSize:
                        if self.PointMap[rowB][collumnB+1] < 256:
                            a = a+1

                    if self.Map[rowB][collumnB] == Tile.Block1:
                        x = 1

                    if self.Map[rowB][collumnB] == Tile.Block2:
                        x = 2

                    if self.Map[rowB][collumnB] == Tile.Block3:
                        x = 3

                    if self.Map[rowB][collumnB] == Tile.Block4:
                        x = 4

                    p = 25*(a-x)

                    if rowB > 0:
                        if self.PointMap[rowB-1][collumnB] < 256:
                            self.PointMap[rowB-1][collumnB] = p
                    if rowB+1 < self.iSize:
                        if self.PointMap[rowB+1][collumnB] < 256:
                            self.PointMap[rowB+1][collumnB] = p
                    if collumnB > 0:
                        if self.PointMap[rowB][collumnB-1] < 256:
                            self.PointMap[rowB][collumnB-1] = p
                    if collumnB+1 < self.iSize:
                        if self.PointMap[rowB][collumnB+1] < 256:
                            self.PointMap[rowB][collumnB+1] = p

    def checkmap(self):
        # print("Checking map...")
        for i in range(0, self.iSize):
            for j in range(0, self.iSize):

                if self.Map[i][j] == Tile.EmptyUnlit:
                    return False
                elif self.isblock(i, j):

                    done = False

                    if self.Map[i][j] == Tile.Block:
                        done = True
                    elif self.Map[i][j] == Tile.Block0:
                        if self.isblock0done(i, j):
                            done = True
                    elif self.Map[i][j] == Tile.Block1:
                        if self.isblock1done(i, j):
                            done = True
                    elif self.Map[i][j] == Tile.Block2:
                        if self.isblock2done(i, j):
                            done = True
                    elif self.Map[i][j] == Tile.Block3:
                        if self.isblock3done(i, j):
                            done = True
                    elif self.Map[i][j] == Tile.Block4:
                        if self.isblock4done(i, j):
                            done = True
                    if  done == False:
                        return False
        return True

    def isblock(self, posrow, poscollumn):
        if self.Map[posrow][poscollumn] == Tile.Block or self.Map[posrow][poscollumn] == Tile.Block0 or \
                self.Map[posrow][poscollumn] == Tile.Block1 or self.Map[posrow][poscollumn] == Tile.Block2 \
                or self.Map[posrow][poscollumn] == Tile.Block3 or self.Map[posrow][poscollumn] == Tile.Block4:
            return True
        else:
            return False
    
    def isblock0done(self, posrow, poscollumn):
        # check up
        if posrow > 0:
            if self.Map[posrow - 1][poscollumn] == Tile.EmptyLamp:
                return False
        # check down
        if posrow < (self.iSize - 1):
            if self.Map[posrow + 1][poscollumn] == Tile.EmptyLamp:
                return False
        # check right
        if poscollumn < (self.iSize - 1):
            if self.Map[posrow][poscollumn + 1] == Tile.EmptyLamp:
                return False
        # check left
        if poscollumn > 0:
            if self.Map[posrow][poscollumn - 1] == Tile.EmptyLamp:
                return False
        return True

    def isblock1done(self, posrow, poscollumn):
        i_lamps = 0
        # check up
        if posrow > 0:
            if self.Map[posrow - 1][poscollumn] == Tile.EmptyLamp:
                i_lamps = i_lamps+1
        # check down
        if posrow < (self.iSize - 1):
            if self.Map[posrow + 1][poscollumn] == Tile.EmptyLamp:
                i_lamps = i_lamps+1
        # check right
        if poscollumn < (self.iSize - 1):
            if self.Map[posrow][poscollumn + 1] == Tile.EmptyLamp:
                i_lamps = i_lamps+1
        # check left
        if poscollumn > 0:
            if self.Map[posrow][poscollumn - 1] == Tile.EmptyLamp:
                i_lamps = i_lamps+1
        if i_lamps == 1:
            return True
        else:
            return False

    def isblock2done(self, posrow, poscollumn):
        i_lamps = 0
        # check up
        if posrow > 0:
            if self.Map[posrow - 1][poscollumn] == Tile.EmptyLamp:
                i_lamps = i_lamps+1
        # check down
        if posrow < (self.iSize - 1):
            if self.Map[posrow + 1][poscollumn] == Tile.EmptyLamp:
                i_lamps = i_lamps+1
        # check right
        if poscollumn < (self.iSize - 1):
            if self.Map[posrow][poscollumn + 1] == Tile.EmptyLamp:
                i_lamps = i_lamps+1
        # check left
        if poscollumn > 0:
            if self.Map[posrow][poscollumn - 1] == Tile.EmptyLamp:
                i_lamps = i_lamps+1
        if i_lamps == 2:
            return True
        else:
            return False

    def isblock3done(self, posrow, poscollumn):
        i_lamps = 0
        # check up
        if posrow > 0:
            if self.Map[posrow - 1][poscollumn] == Tile.EmptyLamp:
                i_lamps = i_lamps+1
        # check down
        if posrow < (self.iSize - 1):
            if self.Map[posrow + 1][poscollumn] == Tile.EmptyLamp:
                i_lamps = i_lamps+1
        # check right
        if poscollumn < (self.iSize - 1):
            if self.Map[posrow][poscollumn + 1] == Tile.EmptyLamp:
                i_lamps = i_lamps+1
        # check left
        if poscollumn > 0:
            if self.Map[posrow][poscollumn - 1] == Tile.EmptyLamp:
                i_lamps = i_lamps+1
        if i_lamps == 3:
            return True
        else:
            return False

    def isblock4done(self, posrow, poscollumn):
        i_lamps = 0
        # check up
        if posrow > 0:
            if self.Map[posrow - 1][poscollumn] == Tile.EmptyLamp:
                i_lamps = i_lamps+1
        # check down
        if posrow < (self.iSize - 1):
            if self.Map[posrow + 1][poscollumn] == Tile.EmptyLamp:
                i_lamps = i_lamps+1
        # check right
        if poscollumn < (self.iSize - 1):
            if self.Map[posrow][poscollumn + 1] == Tile.EmptyLamp:
                i_lamps = i_lamps+1
        # check left
        if poscollumn > 0:
            if self.Map[posrow][poscollumn - 1] == Tile.EmptyLamp:
                i_lamps = i_lamps+1
        if i_lamps == 4:
            return True
        else:
            return False


class Node:
    state = None
    parent = None
    nodesToVisit = []
    steps = None
    visited = False

    def __init__(self, state, parent, steps):
        self.state = state
        self.parent = parent
        self.steps = steps

    # Push all available moves to the list in order from the best to worst according to points map
    def updatenodestovisitastar(self):
        self.nodesToVisit = []
        self.state.updatepointmap()

        tile_points = []

        def custom_sort(t):
            return t[1]

        for i in range(0, 49):
            tmp = list()
            tmp.append(i)
            tmp.append(self.state.PointMap[int(i/7)][i % 7])
            tile_points.append(tmp)

        tile_points.sort(key=custom_sort)
        tile_points.reverse()

        for g in range(len(tile_points)):
            print(str(tile_points[g][0]) + " " + str(tile_points[g][1]))

        for h in range(0, 49):
            k = tile_points[h][0]
            if self.state.Map[int(k/7)][k % 7] == Tile.EmptyUnlit:  # if the move is valid
                temp = Node(self.state, self.parent, self.steps)
                temp.state = deepcopy(self.state)
                temp.parent = deepcopy(self.parent)
                temp.steps = deepcopy(self.steps)
                temp.state.placelamp(int(k / 7), k % 7)  # Modify current state

                print()
                temp.state.printmapconsole()
                print()

                self.nodesToVisit.append(temp)

    def updatenodestovisit(self):  # Push all available moves to the stack

        self.nodesToVisit = []
        for y in range(0, 7):
            for x in range(0, 7):
                if self.state.Map[y][x] == Tile.EmptyUnlit:  # if the move is valid
                    temp = Node(self.state, self.parent, self.steps)
                    temp.state = deepcopy(self.state)
                    temp.parent = deepcopy(self.parent)
                    temp.steps = deepcopy(self.steps)
                    temp.state.placelamp(y, x)  # Modify current state
                    self.nodesToVisit.append(temp)


def depthfirstsearch(node):
    # initial
    root = Node(node.state, node.parent, node.steps)
    root.updatenodestovisit()
    visited = []
    a = root.nodesToVisit

    # main loop
    while a:
        x = a.pop()
        x.updatenodestovisit()
        if x.state.checkmap():
            return x
        # check for visited states
        flag = 0
        for r in visited:
            for p in x.nodesToVisit:
                if p.state == r.state:
                    flag = 1
                    print("flag")
        # if states were not visited append to stack
        if flag == 0:
            visited.append(x)
            for n in x.nodesToVisit:
                a.append(n)


def astar(node):
    print("A* based solver")

    root = Node(node.state, Node.parent, Node.steps)
    root.updatenodestovisitastar()
    visited = []
    a = root.nodesToVisit

    while a:
        x = a.pop()
        x.updatenodestovisitastar()
        if x.state.checkmap():
            return x
        # check for visited states
        flag = 0
        for r in visited:
            for p in x.nodesToVisit:
                if p.state == r.state:
                    flag = 1
                    print("flag")
        # if states were not visited append to stack
        if flag == 0:
            visited.append(x)
            for n in x.nodesToVisit:
                a.append(n)


def test():
    lightupmap = GameMap(7)
    lightupmap.loadmap("TestFile.txt")
    lightupmap.printmapconsole()
    root = Node(lightupmap, lightupmap, lightupmap)
    d = depthfirstsearch(root)
    print()
    d.state.printmapconsole()


test()
