import random
import copy
from optparse import OptionParser
import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        
        #print(self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks())        
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0 
        restartTimes = 0
        while True:
            if verbose:
                print("iteration %d" % i)
                print("restart times %d" % restartTimes)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            #if we have restarted over 30 times or no queen attacks each other, stop the iteration
            #you should break before assign a newBoard
            if restartTimes >= 30 or currentNumberOfAttacks==0:
                break
            #assign a newBoard to current board
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1
            #if a plateau situation has appeared and the iteration times has exceeded 50
            #we will restart by choosing a random queens distribution
            if  currentNumberOfAttacks <= newNumberOfAttacks and i>= 50:
                #reset the iteration times
                i = 0
                newBoard = Board([[]])
                restartTimes += 1
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray
          
    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s 

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For exmaple: 
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        #get the current board's square array 
        currentBoardArray = self.squareArray
        #get the current costboard's square array to choose a lowest-cost decision
        costboardArray = self.getCostBoard().squareArray
        #initialize a minimum cost
        minCost = 10000
        #initialize a minimum cost list to store all positions which will cause minimum cost
        minCost_List = []
        for x in range(len(costboardArray)):
            for y in range(len(costboardArray[0])):
                if costboardArray[x][y] <= minCost:
                    minCost = costboardArray[x][y]
                    newRow = x
                    newCol = y
                    #store all the positions which have the same minimum cost
                    minCost_List.append(((newRow,newCol),minCost))
                for i in minCost_List:
                    if i[1] > minCost:
                        minCost_List.remove(i)
        #randomly select one minimum cost position of minCost_List
        newRow, newCol = minCost_List[random.randint(0,len(minCost_List)-1)][0]
        #set all the values of new column to 0
        for i in currentBoardArray:
            i[newCol] = 0
        #set the value of new queen position to 1
        currentBoardArray[newRow][newCol] = 1
        #assign betterBoard to be an instance of Board class
        #note the difference between class Board and its attribute 'squareArray'
        betterBoard = Board(currentBoardArray)
        minNumOfAttack = betterBoard.getNumberOfAttacks()
        
        return (betterBoard,minNumOfAttack,newRow,newCol)
        util.raiseNotDefined()

    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        currentBoard = self.squareArray
        queensList = []
        numberOfAttacks = 0
        #find all the queens' position
        for y in range(len(currentBoard[0])):
            for x in range(len(currentBoard)):
                if currentBoard[x][y] == 1:
                    queensList.append((x,y))
        #calculate the cost of all the moves
        for i in range(len(queensList)):
            for j in range(i+1,len(queensList)):
                #check the number of queens locating the same row
                if queensList[i][0] == queensList[j][0]:
                    numberOfAttacks += 1
                #check the number of queens locating the same diagonal
                if abs(queensList[i][0]-queensList[j][0]) \
                      == abs(queensList[i][1]-queensList[j][1]):
                          numberOfAttacks += 1
        return numberOfAttacks
        util.raiseNotDefined()

if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    #random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
