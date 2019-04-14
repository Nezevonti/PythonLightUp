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


    def __init__(self,iSizeIn):
        self.Map = []
        self.PointMap = []
        self.iSize = iSizeIn
        for i in range(0,self.iSize):
            x = []
            x_points = []
            for j in range(0,self.iSize):
                x.append(Tile.EmptyUnlit)
                x_points.append(250)
            self.Map.append(x)
            self.PointMap.append(x_points)
    
    def CopyMap(self,GMap):
        if(self.iSize != GMap.iSize):
            print("Cannot Copy maps of different sizes")
            return
        else:
            for i in range(0,self.iSize):
                    for j in range(0,self.iSize):

                        self.PointMap[i][j] = GMap.PointMap[i][j]

                        if(GMap.Map[i][j] == Tile.Block):
                            self.Map[i][j] = Tile.Block
                        elif(GMap.Map[i][j]== Tile.Block0):
                            self.Map[i][j]=Tile.Block0
                        elif(GMap.Map[i][j]== Tile.Block1):
                            self.Map[i][j]=Tile.Block1
                        elif(GMap.Map[i][j]== Tile.Block2):
                            self.Map[i][j]=Tile.Block2
                        elif(GMap.Map[i][j]== Tile.Block3):
                            self.Map[i][j]=Tile.Block3
                        elif(GMap.Map[i][j]== Tile.Block4):
                            self.Map[i][j]=Tile.Block4
                        elif(GMap.Map[i][j]== Tile.EmptyLamp):
                            self.Map[i][j]=Tile.EmptyLamp
                        elif(GMap.Map[i][j]== Tile.EmptyLit):
                            self.Map[i][j]=Tile.EmptyLit
                        elif(GMap.Map[i][j]== Tile.EmptyUnlit):
                            self.Map[i][j]=Tile.EmptyUnlit

    #

    #Print

    def PrintMapConsole(self):
        for i in range(0,self.iSize):
            for j in range(0,self.iSize):
                print(self.Map[i][j].value,end="")
                print(" ",end="")
            print("")

    def PrintPointConsole(self):
        for i in range(0,self.iSize):
            for j in range(0,self.iSize):
                print(self.PointMap[i][j],end="")
                if(self.PointMap[i][j] < 10):
                    print(" ",end="")
                
                if(self.PointMap[i][j] < 100):
                    print(" ",end="")

                print(" ",end="")
            print("")


    def LoadMap(self,sPath):
        print("Loading from file " + sPath)

        tile = None
        iter = 0

        try:
            with open(sPath) as mapfile:
                while True:
                    tile = mapfile.read(1)

                    if(tile=='E'):
                        self.Map[(int)(iter/7)][iter%7] = Tile.EmptyUnlit
                    elif(tile=='B'):
                        self.Map[(int)(iter/7)][iter%7] = Tile.Block
                    elif(tile=='0'):
                        self.Map[(int)(iter/7)][iter%7] = Tile.Block0
                    elif(tile=='1'):
                        self.Map[(int)(iter/7)][iter%7] = Tile.Block1
                    elif(tile=='2'):
                        self.Map[(int)(iter/7)][iter%7] = Tile.Block2
                    elif(tile=='3'):
                        self.Map[(int)(iter/7)][iter%7] = Tile.Block3
                    elif(tile=='4'):
                        self.Map[(int)(iter/7)][iter%7] = Tile.Block4

                    iter=iter+1

                    if not tile:
                        break

       
        except IOError:
            print("Cannot open file...")
            return
        print("",end="")
    
    def PlaceLamp(self,PosRow,PosCollumn):
        if(self.Map[PosRow][PosCollumn] == Tile.EmptyLit):
            print("cannot place lamps in lit spaces...")
            return

        if(self.IsBlock(PosRow,PosCollumn)):
            print("cannot place lamps on blocks...")
            return

        if(self.Map[PosRow][PosCollumn] == Tile.EmptyLamp):
            print("cannot place lamps on lamps...")
            return

        #print("Placing lamp at " + str(PosRow) +","+ str(PosCollumn) + " ...")
        self.Map[PosRow][PosCollumn] = Tile.EmptyLamp
        #update lighting

        self.UpdateLighting(PosRow,PosCollumn)

    def UpdateLighting(self,PosRow,PosCollumn):
        #up
        for i in range(1,PosRow+1):
            #if(self.Map[PosRow-i][PosCollumn] == Tile.Block or self.Map[PosRow-i][PosCollumn] == Tile.Block0 or self.Map[PosRow-i][PosCollumn] == Tile.Block1 or self.Map[PosRow-i][PosCollumn] == Tile.Block2 or self.Map[PosRow-i][PosCollumn] == Tile.Block3 or self.Map[PosRow-i][PosCollumn] == Tile.Block4):
            if(self.IsBlock(PosRow-i,PosCollumn)):
                break
            else:
                self.Map[PosRow-i][PosCollumn] = Tile.EmptyLit
        #down
        for j in range(1,self.iSize-PosRow): 
            #i = j - self.iSize
            #if(self.Map[PosRow+j][PosCollumn] == Tile.Block or self.Map[PosRow+j][PosCollumn] == Tile.Block0 or self.Map[PosRow+j][PosCollumn] == Tile.Block1 or self.Map[PosRow+j][PosCollumn] == Tile.Block2 or self.Map[PosRow+j][PosCollumn] == Tile.Block3 or self.Map[PosRow+j][PosCollumn] == Tile.Block4):
            if(self.IsBlock(PosRow+j,PosCollumn)):
                break
            else:
                self.Map[PosRow+j][PosCollumn] = Tile.EmptyLit
            #self.PrintMap()
            #print("")
        #left
        for i in range(1,PosCollumn+1):
            #if(self.Map[PosRow][PosCollumn-i] == Tile.Block or self.Map[PosRow][PosCollumn-i] == Tile.Block0 or self.Map[PosRow][PosCollumn-i] == Tile.Block1 or self.Map[PosRow][PosCollumn-i] == Tile.Block2 or self.Map[PosRow][PosCollumn-i] == Tile.Block3 or self.Map[PosRow][PosCollumn-i] == Tile.Block4):
            if(self.IsBlock(PosRow,PosCollumn-i)):
                break
            else:
                self.Map[PosRow][PosCollumn-i] = Tile.EmptyLit
        #right
        for j in range(1,self.iSize-PosCollumn): #Make sure it works the way its supposed to!
            #i = j - self.iSize
            #if(self.Map[PosRow][PosCollumn-i] == Tile.Block or self.Map[PosRow][PosCollumn-i] == Tile.Block0 or self.Map[PosRow][PosCollumn-i] == Tile.Block1 or self.Map[PosRow][PosCollumn-i] == Tile.Block2 or self.Map[PosRow][PosCollumn-i] == Tile.Block3 or self.Map[PosRow][PosCollumn-i] == Tile.Block4):
            if(self.IsBlock(PosRow,PosCollumn+j)):
                break
            else:
                self.Map[PosRow][PosCollumn+j] = Tile.EmptyLit
    
    def UpdatePointMap(self):
        print("Updating Point Map...")

        #set blocks, neighbours of 0 and lit places to max
        for row in range(0,self.iSize):
            for collumn in range(0,self.iSize):
                if(self.IsBlock(row,collumn)):
                    self.PointMap[row][collumn] = 256

                    if(self.Map[row][collumn]==Tile.Block0):
                        if(row>0):
                            self.PointMap[row-1][collumn] = 256
                        if(row+1<self.iSize):
                            self.PointMap[row+1][collumn] = 256
                        if(collumn>0):
                            self.PointMap[row][collumn-1] = 256
                        if(collumn+1<self.iSize):
                            self.PointMap[row][collumn+1] = 256

                if(self.Map[row][collumn] == Tile.EmptyLit or self.Map[row][collumn] == Tile.EmptyLamp):
                    self.PointMap[row][collumn] = 256

        #check for numbered blocks neighbours
        for rowB in range(0,self.iSize):
            for collumnB in range(0,self.iSize):
                if(self.IsBlock(rowB,collumnB)):
                    if(self.Map[rowB][collumnB] == Tile.Block0 or self.Map[rowB][collumnB] == Tile.Block):
                        continue
                    A=0 #aviable neighbours to this block
                    if(rowB>0):
                        if(self.PointMap[rowB-1][collumnB] < 256):
                            A=A+1
                    if(rowB+1<self.iSize):
                        if(self.PointMap[rowB+1][collumnB] < 256):
                            A=A+1
                    if(collumnB>0):
                        if(self.PointMap[rowB][collumnB-1] < 256):
                            A=A+1
                    if(collumnB+1<self.iSize):
                        if(self.PointMap[rowB][collumnB+1] < 256):
                            A=A+1

                    if(self.Map[rowB][collumnB] == Tile.Block1):
                        X = 1

                    if(self.Map[rowB][collumnB] == Tile.Block2):
                        X = 2

                    if(self.Map[rowB][collumnB] == Tile.Block3):
                        X = 3

                    if(self.Map[rowB][collumnB] == Tile.Block4):
                        X = 4

                    P = 25*(A-X)

                    if(rowB>0):
                        if(self.PointMap[rowB-1][collumnB] < 256):
                            self.PointMap[rowB-1][collumnB] = P
                    if(rowB+1<self.iSize):
                        if(self.PointMap[rowB+1][collumnB] < 256):
                            self.PointMap[rowB+1][collumnB] = P
                    if(collumnB>0):
                        if(self.PointMap[rowB][collumnB-1] < 256):
                            self.PointMap[rowB][collumnB-1] = P
                    if(collumnB+1<self.iSize):
                        if(self.PointMap[rowB][collumnB+1] < 256):
                            self.PointMap[rowB][collumnB+1] = P
    

    #

    #Check Map


    def CheckMap(self):
        #print("Checking map...")
        for i in range(0,self.iSize):
            for j in range(0,self.iSize):

                if(self.Map[i][j]== Tile.EmptyUnlit):
                    return False
                elif(self.IsBlock(i,j)):

                    Done = False

                    if(self.Map[i][j]==Tile.Block):
                        Done = True
                    elif(self.Map[i][j]==Tile.Block0):
                        if(self.IsBlock0Done(i,j)):
                            Done = True
                    elif(self.Map[i][j] == Tile.Block1):
                        if(self.IsBlock1Done(i,j)):
                            Done = True
                    elif(self.Map[i][j] == Tile.Block2):
                        if(self.IsBlock2Done(i,j)):
                            Done = True
                    elif(self.Map[i][j] == Tile.Block3):
                        if(self.IsBlock3Done(i,j)):
                            Done = True
                    elif(self.Map[i][j] == Tile.Block4):
                        if(self.IsBlock4Done(i,j)):
                            Done = True

                    if(Done == False):
                        return False

        return True

    def IsBlock(self,PosRow,PosCollumn):
        if(self.Map[PosRow][PosCollumn] == Tile.Block or self.Map[PosRow][PosCollumn] == Tile.Block0 or self.Map[PosRow][PosCollumn] == Tile.Block1 or self.Map[PosRow][PosCollumn] == Tile.Block2 or self.Map[PosRow][PosCollumn] == Tile.Block3 or self.Map[PosRow][PosCollumn] == Tile.Block4):
            return True
        else:
            return False
    
    def IsBlock0Done(self,PosRow,PosCollumn):
        #check up
        if(PosRow>0):
            if(self.Map[PosRow-1][PosCollumn] == Tile.EmptyLamp):
                return False
        #check down
        if(PosRow<(self.iSize-1)):
            if(self.Map[PosRow+1][PosCollumn] == Tile.EmptyLamp):
                return False
        #check right
        if(PosCollumn < (self.iSize-1)):
            if(self.Map[PosRow][PosCollumn+1] == Tile.EmptyLamp):
                return False
        #check left
        if(PosCollumn > 0):
            if(self.Map[PosRow][PosCollumn-1] == Tile.EmptyLamp):
                return False

        return True

    def IsBlock1Done(self,PosRow,PosCollumn):
        iLamps = 0
        #check up
        if(PosRow>0):
            if(self.Map[PosRow-1][PosCollumn] == Tile.EmptyLamp):
                iLamps = iLamps+1
        #check down
        if(PosRow<(self.iSize-1)):
            if(self.Map[PosRow+1][PosCollumn] == Tile.EmptyLamp):
                iLamps = iLamps+1
        #check right
        if(PosCollumn < (self.iSize-1)):
            if(self.Map[PosRow][PosCollumn+1] == Tile.EmptyLamp):
                iLamps = iLamps+1
        #check left
        if(PosCollumn > 0):
            if(self.Map[PosRow][PosCollumn-1] == Tile.EmptyLamp):
                iLamps = iLamps+1

        if(iLamps == 1):
            return True
        else:
            return False

    def IsBlock2Done(self,PosRow,PosCollumn):
        iLamps = 0
        #check up
        if(PosRow>0):
            if(self.Map[PosRow-1][PosCollumn] == Tile.EmptyLamp):
                iLamps = iLamps+1
        #check down
        if(PosRow<(self.iSize-1)):
            if(self.Map[PosRow+1][PosCollumn] == Tile.EmptyLamp):
                iLamps = iLamps+1
        #check right
        if(PosCollumn < (self.iSize-1)):
            if(self.Map[PosRow][PosCollumn+1] == Tile.EmptyLamp):
                iLamps = iLamps+1
        #check left
        if(PosCollumn > 0):
            if(self.Map[PosRow][PosCollumn-1] == Tile.EmptyLamp):
                iLamps = iLamps+1

        if(iLamps == 2):
            return True
        else:
            return False
    

    def IsBlock3Done(self,PosRow,PosCollumn):
        iLamps = 0
        #check up
        if(PosRow>0):
            if(self.Map[PosRow-1][PosCollumn] == Tile.EmptyLamp):
                iLamps = iLamps+1
        #check down
        if(PosRow<(self.iSize-1)):
            if(self.Map[PosRow+1][PosCollumn] == Tile.EmptyLamp):
                iLamps = iLamps+1
        #check right
        if(PosCollumn < (self.iSize-1)):
            if(self.Map[PosRow][PosCollumn+1] == Tile.EmptyLamp):
                iLamps = iLamps+1
        #check left
        if(PosCollumn > 0):
            if(self.Map[PosRow][PosCollumn-1] == Tile.EmptyLamp):
                iLamps = iLamps+1

        if(iLamps == 3):
            return True
        else:
            return False

    def IsBlock4Done(self,PosRow,PosCollumn):
        iLamps = 0
        #check up
        if(PosRow>0):
            if(self.Map[PosRow-1][PosCollumn] == Tile.EmptyLamp):
                iLamps = iLamps+1
        #check down
        if(PosRow<(self.iSize-1)):
            if(self.Map[PosRow+1][PosCollumn] == Tile.EmptyLamp):
                iLamps = iLamps+1
        #check right
        if(PosCollumn < (self.iSize-1)):
            if(self.Map[PosRow][PosCollumn+1] == Tile.EmptyLamp):
                iLamps = iLamps+1
        #check left
        if(PosCollumn > 0):
            if(self.Map[PosRow][PosCollumn-1] == Tile.EmptyLamp):
                iLamps = iLamps+1

        if(iLamps == 4):
            return True
        else:
            return False


# Node

class Node():
    state = None
    parent = None
    nodesToVisit = []
    steps = None
    visited = False

    def __init__(self, state, parent, steps):
        self.state = state
        self.parent = parent
        self.steps = steps

    
    def UpdateNodesToVisitA(self):  # Push all available moves to the stack
        self.nodesToVisit= []
        self.state.UpdatePointMap()

        tile_points = []

        def custom_sort(t):
            return t[1]

        for i in range(0,49):
            tmp = []
            tmp.append(i)
            tmp.append(self.state.PointMap[(int)(i/7)][i%7])
            tile_points.append(tmp)

        tile_points.sort(key=custom_sort)

        for g in range(len(tile_points)):
            print(str(tile_points[g][0]) + " " + str(tile_points[g][1]))

        for h in range(0,49):
            k = tile_points[h][0]
            if self.state.Map[(int)(k/7)][k%7] == Tile.EmptyUnlit:  # if the move is valid
                temp = Node(self.state, self.parent, self.steps)
                temp.state = deepcopy(self.state)
                temp.parent = deepcopy(self.parent)
                temp.steps = deepcopy(self.steps)
                temp.state.PlaceLamp((int)(k/7),k%7)  # Modify current state

                print()
                temp.state.PrintMapConsole()
                print()

                self.nodesToVisit.append(temp)
        
    
    #

    #DF

    def UpdateNodesToVisit(self):  # Push all available moves to the stack
        self.nodesToVisit= []
        for y in range(0, 7):
            for x in range(0, 7):
                if self.state.Map[y][x] == Tile.EmptyUnlit:  # if the move is valid
                    temp = Node(self.state, self.parent, self.steps)
                    temp.state = deepcopy(self.state)
                    temp.parent = deepcopy(self.parent)
                    temp.steps = deepcopy(self.steps)
                    temp.state.PlaceLamp(y, x)  # Modify current state

                    #print()
                    #temp.state.PrintMapConsole()
                    #print()

                    self.nodesToVisit.append(temp)
    
#



def depthfirstsearch(node):
    # initial
    root = Node(node.state, node.parent, node.steps)
    root.UpdateNodesToVisit()
    visited = []
    a = root.nodesToVisit

    print()
    root.state.PrintMapConsole()
    print()

    # main loop
    while a:
        x = a.pop()
        x.UpdateNodesToVisit()
        if x.state.CheckMap():
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
        

#A*

def Astar(node):
    print("A* based solver")

    root = Node(node.state,Node.parent,Node.steps)
    root.UpdateNodesToVisitA()
    visited = []
    a = root.nodesToVisit

    #root.state.UpdatePointMap()

    while a:
        x=a.pop()
        x.UpdateNodesToVisitA()

        #x.state.UpdatePointMap()

        if x.state.CheckMap():
            return x
        
        a = x.nodesToVisit

#MainGameLoop


def GameLoop():
    print("loop start...")

    gameFinished = False
    gameinputs = [[4,5,6,5,6,2,0,1,3],[2,1,2,3,6,0,5,1,4]]
    iterator = 0
    #initialize map
    Map = GameMap(7)
    #load map
    Map.LoadMapOld()
    #while gamefinished == False
    while (gameFinished==False):
        Map.PrintMapConsole()
        print("")
        #LampPosRow = int(input("Row : "))
        #LampPosCollumn = int(input("Collumn : "))
        LampPosRow = int(gameinputs[0][iterator])
        LampPosCollumn = int(gameinputs[1][iterator])
        iterator = iterator+1
        print("")
        #place lamp
        Map.PlaceLamp(LampPosRow,LampPosCollumn)
            #check if lamp can be placed
        #light spaces up
            #From PosX,PosY
        #check if game is completed
        if(Map.CheckMap() == True):
            gameFinished = True
            #check if all empty spaces are EmptyLit or EmptyLamp
    print("")
    print("")
    Map.PrintMapConsole()
    print("")
    print("")
    print("GameFinished")
    print("")
    print("")


def main():

    Map = GameMap(7)
    Map.LoadMap("TestFile.txt")
    Map.PrintMapConsole()
    Map.UpdatePointMap()
    Map.PrintPointConsole()




#GameLoop()

    
def Test():
    map = GameMap(7)
    map.LoadMap("TestFile.txt")
    map.PrintMapConsole()
    root = Node(map,map,map)
    d = Astar(root)
    d.state.PrintMapConsole()

Test()

#main()
