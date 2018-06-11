#################################################################################
#     File Name           :     solveTicTacToe.py
#     Created By          :     Chen Guanying 
#     Creation Date       :     [2017-03-18 19:17]
#     Last Modified       :     [2017-03-18 19:17]
#     Description         :      
#################################################################################

import copy
import util 
import sys
import random
import time
from optparse import OptionParser

class GameState:
    """
      Game state of 3-Board Misere Tic-Tac-Toe
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your search agents. Please do not remove anything, 
      however.
    """
    def __init__(self):
        """
          Represent 3 boards with lists of boolean value 
          True stands for X in that position
        """
        self.boards = [[False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False]]

    def generateSuccessor(self, action):
        """
          Input: Legal Action
          Output: Successor State
        """
        suceessorState = copy.deepcopy(self)
        ASCII_OF_A = 65
        boardIndex = ord(action[0]) - ASCII_OF_A
        pos = int(action[1])
        suceessorState.boards[boardIndex][pos] = True
        return suceessorState

    # Get all valid actions in 3 boards
    def getLegalActions(self, gameRules):
        """
          Input: GameRules
          Output: Legal Actions (Actions not in dead board) 
        """
        ASCII_OF_A = 65
        actions = []
        for b in range(3):
            if gameRules.deadTest(self.boards[b]): continue
            for i in range(9):
                if not self.boards[b][i]:
                    actions.append( chr(b+ASCII_OF_A) + str(i) )
        return actions

    # Print living boards
    def printBoards(self, gameRules):
        """
          Input: GameRules
          Print the current boards to the standard output
          Dead boards will not be printed
        """
        titles = ["A", "B", "C"]
        boardTitle = ""
        boardsString = ""
        for row in range(3):
            for boardIndex in range(3):
                # dead board will not be printed
                if gameRules.deadTest(self.boards[boardIndex]): continue
                if row == 0: boardTitle += titles[boardIndex] + "      "
                for i in range(3):
                    index = 3 * row + i
                    if self.boards[boardIndex][index]: 
                        boardsString += "X "
                    else:
                        boardsString += str(index) + " "
                boardsString += " "
            boardsString += "\n"
        print(boardTitle)
        print(boardsString)

class GameRules:
    """
      This class defines the rules in 3-Board Misere Tic-Tac-Toe. 
      You can add more rules in this class, e.g the fingerprint (patterns).
      However, please do not remove anything.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}
        #generate a monoid Q
        self.monoid_Q = self.generateQ()[0]
        self.relationOfElements_Q = self.generateQ()[1]
        self.p_Position = self.generateQ()[2]
        self.qOfPosition = self.generateQ()[3]
        #print(self.qOfPosition)
    def generateQ(self):
        #assign a prime number to do calculation
        a = 2
        b = 3
        c = 5
        d = 7
        relationOfElements_Q = {str(a**2):1, str(b**3): b, str(b**2 * c): c, str(c**3): a*c**2,\
                    str(b**2 * d): d, str(c*d): a*d, str(d**2): c**2}
        monoid_Q = set([1, a, b, a*b, b**2, a*b**2, c, a*c, b*c, a*b*c, c**2, a*c**2, b*c**2,\
                        a*b*c**2, d, a*d, b*d, a*b*d])
        #the set of p position which means second player to move wins
        p_Position = set([a, b**2, b*c, c**2])
        qOfPosition_Dict = self.getQOfPosition(a, b, c, d)
        return (monoid_Q, relationOfElements_Q, p_Position, qOfPosition_Dict)
    
    def rotateBoard(self, board):
        """
        this function will rotate the board by 90 degrees
        """
        #board is a list of boolean value to show the position of "X"
        return [board[6], board[3], board[0], board[7], board[4], board[1], board[8],\
                board[5], board[2]]
        
    def reflectBoard(self, board):
        """
        this function will generate the reflection of a board
        """
        #board is a list of boolean value to show the position of "X"
        return [board[6], board[7], board[8], board[3], board[4], board[5], board[0],\
                board[1], board[2]]
    
    def simplifyToMonoid(self, boardsValue):
        """
        this function will simplify the boardsValue to a element of monoid Q
        """
        while boardsValue not in self.monoid_Q:
            #if boardsValue is not in Q, we need to simplify it by using relation of Q
            for i in self.relationOfElements_Q:
                #check if boardsValue is multiplied by i
                if boardsValue % float(i) == 0:
                    boardsValue = boardsValue / float(i) * self.relationOfElements_Q[i]
        #if boardsValue is already in monoid_Q, then return it directly
        return boardsValue           
    
    def getBoardsValue(self, boards):
        """
        given a board this function can return a corresponding Q value
        """
        boardsValue = 1
        for board in boards:
            #if the board is dead then the value is 1
            if self.deadTest(board):
                boardValue = 1
            else:
                #if the board is not dead we need to find the corresponding q value in qOfPosition
                boardKey = str()
                #board is a list of eight boolean values
                boardKey = self.transferBoardToString(board)
                boardValue = self.qOfPosition[boardKey]
            #note the difference between of boardsValue and boardValue
            boardsValue = boardsValue * boardValue
        return boardsValue
    
    def getQOfPosition(self,a, b, c, d):
        """can be used to simplify generateQ function"""
        '''
        the initial list of qOfPosition given by the paper "The Secrets of Notakto" Figure 6,\
        the first element is the board position and second is corresponding value
        '''
        qOfPosition_List = \
        [ #"""row 1"""
          #row 1 column 1
          [[False, False, False, False, False, False, False, False, False],c],\
          #row 1 column 2
          [[True, False, False, False, False, False, False, False, False],1],\
          #row 1 column 3
          [[False, True, False, False, False, False, False, False, False],1],\
          #row 1 column 4
          [[False, False, False, False, True, False, False, False, False],c**2],\
          #row 1 column 5
          [[True, True, False, False, False, False, False, False, False],a*d],\
          #row 1 column 6
          [[True, False, True, False, False, False, False, False, False],b],\
          #row 1 column 7
          [[True, False, False, False, True, False, False, False, False],b],\
          #row 1 column 8
          [[True, False, False, False, False, True, False, False, False],b],\
          #row 1 column 9
          [[True, False, False, False, False, False, False, False, True],a],\
          #"""row 2"""
          #row 2 column 1
          [[False, True, False, True, False, False, False, False, False],a],\
          #row 2 column 2
          [[False, True, False, False, True, False, False, False, False],b],\
          #row 2 column 3
          [[False, True, False, False, False, False, False, True, False],a],\
          #row 2 column 4 is a dead board, we will skip it     
          #row 2 column 5
          [[True, True, False, True, False, False, False, False, False],b],\
          #row 2 column 6
          [[True, True, False, False, True, False, False, False, False],a*b],\
          #row 2 column 7
          [[True, True, False, False, False, True, False, False, False],d],\
          #row 2 column 8
          [[True, True, False, False, False, False, True, False, False],a],\
          #row 2 column 9
          [[True, True, False, False, False, False, False, True, False],d],\
          #"""row 3"""
          #row 3 column 1
          [[True, True, False, False, False, False, False, False, True],d],\
          #row 3 column 2
          [[True, False, True, False, True, False, False, False, False],a],\
          #row 3 column 3
          [[True, False, True, False, False, False, True, False, False],a*b],\
          #row 3 column 4
          [[True, False, True, False, False, False, False, True, False],a],\
          #row 3 column 5
          [[True, False, False, False, True, True, False, False, False],a],\
          #row 3 column 6 is a dead board, we will skip it      
          #row 3 column 7
          [[True, False, False, False, False, True, False, True, False],1],\
          #row 3 column 8
          [[False, True, False, True, True, False, False, False, False],a*b],\
          #row 3 column 9
          [[False, True, False, True, False, True, False, False, False],b],\
          #"""row 4"""
          #row 4 column 1, 2, 3, 4, 5 are all dead boards, we will skip them   
          #row 4 column 6     
          [[True, True, False, True, True, False, False, False, False],a],\
          #row 4 column 7
          [[True, True, False, True, False, True, False, False, False],a],\
          #row 4 column 8
          [[True, True, False, True, False, False, False, False, True],a],\
          #row 4 column 9
          [[True, True, False, False, True, True, False, False, False],b],\
          #"""row 5"""
          #row 5 column 1
          [[True, True, False, False, True, False, True, False, False],b],\
          #row 5 column 2,3 are dead boards
          #row 5 column 4
          [[True, True, False, False, False, True, True, False, False],b],\
          #row 5 column 5
          [[True, True, False, False, False, True, False, True, False],a*b],\
          #row 5 column 6     
          [[True, True, False, False, False, True, False, False, True],a*b],\
          #row 5 column 7
          [[True, True, False, False, False, False, True, True, False],b],\
          #row 5 column 8
          [[True, True, False, False, False, False, True, False, True],b],\
          #row 5 column 9
          [[True, True, False, False, False, False, False, True, True],a],\
          #"""row 6"""
          #row 6 column 1 is a dead board
          #row 6 column 2
          [[True, False, True, False, True, False, False, True, False],b],\
          #row 6 column 3
          [[True, False, True, False, False, False, True, False, True],a],\
          #row 6 column 4
          [[True, False, False, False, True, True, False, True, False],b],\
          #row 6 column 5 is a dead board    
          #row 6 column 6     
          [[False, True, False, True, False, True, False, True, False],a],\
          #row 6 column 7,8,9 are dead boards
          #"""row 7"""    
          #row 7 column 1-8 are dead boards
          #row 7 column 9     
          [[True, True, False, True, False, True, False, True, False],b],\
          #"""row 8"""
          #row 8 column 1
          [[True, True, False, True, False, True, False, False, True],b],\
          #row 8 column 2
          [[True, True, False, False, True, True, True, False, False],a],\
          #row 8 column 3-7 are dead boards
          #row 8 column 8
          [[True, True, False, False, False, True, True, True, False],a],\
          #row 8 column 9
          [[True, True, False, False, False, True, True, False, True],a],\
          #"""row 9 are all dead boards"""
          #"""row 10"""
          #row 10 column 1-6, 8, 9 are dead boards       
          #row 10 column 7
          [[True, True, False, True, False, True, False, True, True],a]
          #the rest are all dead boards
              ]#boundary of qOfPosition_List
        '''
        the above list doesn't consider all the situations, we need to add\
        the rotated and reflected versions into them. we use a dictionary \
        to store the (board, value) pair
        '''
        qOfPosition_Dict = {}
        for boardAndValue in qOfPosition_List:
            board = boardAndValue[0]
            boardValue = boardAndValue[1]
            #get the reflected version, the second one is the same as the initial one
            for i in range(2):
                board = self.reflectBoard(board)
                #get the rotated version, we need to call rotateBoard function four times
                #the fourth one is the same as initial one
                for j in range(4):
                    #update the board by rotating
                    board = self.rotateBoard(board)
                    #transfer the board to a string for making a key
                    boardKey = self.transferBoardToString(board)
                    #check if the key has already existed
                    if boardKey in qOfPosition_Dict:
                        pass
                    else:
                        #if not exist, store the (boardKey, boardValue into the qOfPosition_Dict)
                        qOfPosition_Dict.update({boardKey: boardValue})
        #print(len(qOfPosition_Dict))
        return qOfPosition_Dict
    def transferBoardToString(self,board):
        """
        this function will transfer board list to a binary value sequence
        """
        #int(False) will be 0
        outputString = str()
        for i in board:
            outputString = outputString + str(int(i))
        return outputString
    
    def deadTest(self, board):
        """
          Check whether a board is a dead board
        """
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        for i in range(3):
            #check every row
            row = i * 3
            if board[row] and board[row+1] and board[row+2]:
                return True
            #check every column
            if board[i] and board[i+3] and board[i+6]:
                return True
        return False

    def isGameOver(self, boards):
        """
          Check whether the game is over  
        """
        return self.deadTest(boards[0]) and self.deadTest(boards[1]) and self.deadTest(boards[2])

class TicTacToeAgent():
    """
      When move first, the TicTacToeAgent should be able to chooses an action to always beat 
      the second player.

      You have to implement the function getAction(self, gameState, gameRules), which returns the 
      optimal action (guarantee to win) given the gameState and the gameRules. The return action
      should be a string consists of a letter [A, B, C] and a number [0-8], e.g. A8. 

      You are welcome to add more helper functions in this class to help you. You can also add the
      helper function in class GameRules, as function getAction() will take GameRules as input.
      
      However, please don't modify the name and input parameters of the function getAction(), 
      because autograder will call this function to check your algorithm.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}

    def getAction(self, gameState, gameRules):
        #the version using p position
        
        #get a list of legal actions
        legalActions = gameState.getLegalActions(gameRules)
        #find the best action
        for action in legalActions:
            #get the successor boards of the current boards(i.e. gameState)
            newBoards = gameState.generateSuccessor(action).boards
            newBoardsValue = gameRules.getBoardsValue(newBoards)
            #simplify the newBoardsValue to be an element of monoid Q
            newBoardsValue = gameRules.simplifyToMonoid(newBoardsValue)
            if newBoardsValue in gameRules.p_Position:
                #print("--------- P-position action exist-----------")
                return action
            else:
                pass
        
        #if all legal actions cannot lead the successor to be a P-position, then randomly choose one
        return random.choice(legalActions)
        util.raiseNotDefined()
            
class randomAgent():
    """
      This randomAgent randomly choose an action among the legal actions
      You can set the first player or second player to be random Agent, so that you don't need to
      play the game when debugging the code. (Time-saving!)
      If you like, you can also set both players to be randomAgent, then you can happily see two 
      random agents fight with each other.
    """
    
    def getAction(self, gameState, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return random.choice(actions)
    

class keyboardAgent():
    """
      This keyboardAgent return the action based on the keyboard input
      It will check whether the input actions is legal or not.
    """
    def checkUserInput(self, gameState, action, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return action in actions

    def getAction(self, gameState, gameRules):
        action = input("Your move: ")
        while not self.checkUserInput(gameState, action, gameRules):
            print("Invalid move, please input again")
            action = input("Your move: ")
        return action 

class Game():
    """
      The Game class manages the control flow of the 3-Board Misere Tic-Tac-Toe
    """
    def __init__(self, numOfGames, muteOutput, randomAI, AIforHuman):
        """
          Settings of the number of games, whether to mute the output, max timeout
          Set the Agent type for both the first and second players. 
        """
        self.numOfGames  = numOfGames
        self.muteOutput  = muteOutput
        self.maxTimeOut  = 30 

        self.AIforHuman  = AIforHuman
        self.gameRules   = GameRules()
        self.AIPlayer    = TicTacToeAgent()

        if randomAI:
            self.AIPlayer = randomAgent()
        else:
            self.AIPlayer = TicTacToeAgent()
        if AIforHuman:
            self.HumanAgent = randomAgent()
        else:
            self.HumanAgent = keyboardAgent()

    def run(self):
        """
          Run a certain number of games, and count the number of wins
          The max timeout for a single move for the first player (your AI) is 30 seconds. If your AI 
          exceed this time limit, this function will throw an error prompt and return. 
        """
        numOfWins = 0;
        for i in range(self.numOfGames):
            gameState = GameState()
            agentIndex = 0 # 0 for First Player (AI), 1 for Second Player (Human)
            while True:
                if agentIndex == 0: 
                    timed_func = util.TimeoutFunction(self.AIPlayer.getAction, int(self.maxTimeOut))
                    try:
                        start_time = time.time()
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (agentIndex, self.maxTimeOut))
                        return False

                    if not self.muteOutput:
                        print("Player 1 (AI): %s" % action)
                else:
                    action = self.HumanAgent.getAction(gameState, self.gameRules)
                    if not self.muteOutput:
                        print("Player 2 (Human): %s" % action)
                gameState = gameState.generateSuccessor(action)
                if self.gameRules.isGameOver(gameState.boards):
                    break
                if not self.muteOutput:
                    gameState.printBoards(self.gameRules)

                agentIndex  = (agentIndex + 1) % 2
            if agentIndex == 0:
                print("****player 2 wins game %d!!****" % (i+1))
            else:
                numOfWins += 1
                print("****Player 1 wins game %d!!****" % (i+1))

        print("\n****Player 1 wins %d/%d games.**** \n" % (numOfWins, self.numOfGames))


if __name__ == "__main__":
    """
      main function
      -n: Indicates the number of games
      -m: If specified, the program will mute the output
      -r: If specified, the first player will be the randomAgent, otherwise, use TicTacToeAgent
      -a: If specified, the second player will be the randomAgent, otherwise, use keyboardAgent
    """
    # Uncomment the following line to generate the same random numbers (useful for debugging)
    #random.seed(1)  
    parser = OptionParser()
    parser.add_option("-n", dest="numOfGames", default=1, type="int")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False)
    parser.add_option("-r", dest="randomAI", action="store_true", default=False)
    parser.add_option("-a", dest="AIforHuman", action="store_true", default=False)
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.numOfGames, options.muteOutput, options.randomAI, options.AIforHuman)
    ticTacToeGame.run()
