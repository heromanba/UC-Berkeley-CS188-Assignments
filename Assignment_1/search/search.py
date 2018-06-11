"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    #initial state of your self-defined state space
    startState = problem.getStartState()
    #set used to store explored nodes
    explored = set()
    Frontier = util.Stack()
    #for one frontier it has some previous states which can lead agent to the frontier, this structure is similiar to (successor,action,stepCost)
    Frontier.push([[startState,None,0]])
    while not Frontier.isEmpty():
        #pop the last (successor,action,stepCost) of the Frontier, i.e. the latest frontier
        StateTriples = Frontier.pop()
        #node = StateTriples.pop()[0], cannot use this because of the following comments
        #StateTriples[-1][0] will duplicate the list while pop() will remove the element
        node = StateTriples[-1][0]
        #goal test
        if problem.isGoalState(node):
            #initialize the solution path list
            solution = []
            #the first element of i[1] is None, so there will be a key error:None
            #thus we start from the action of second frontier
            for i in StateTriples[1:]:
                solution = solution + [i[1]]
            return solution
        if node not in explored:
            explored.add(node)
            for i in problem.getSuccessors(node):
                Frontier.push(StateTriples+[list(i)])
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    explored = set()
    Frontier = util.Queue()
    Frontier.push([[startState,None,0]])
    while not Frontier.isEmpty():
        StateTriples = Frontier.pop()
        node = StateTriples[-1][0]
        if problem.isGoalState(node):
            solution = []
            for i in StateTriples[1:]:
                solution = solution + [i[1]]
            return solution
        if node not in explored:
            explored.add(node)
            for i in problem.getSuccessors(node):
                Frontier.push(StateTriples+[list(i)])
    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    #the result of resolution is related to the cost function
    #for example, the result of SearchAgent and StayWestSearchAgent is very different
    startState = problem.getStartState()
    explored = set()
    Frontier = util.PriorityQueue()
    Frontier.push([[startState,None,0]],0)
    while not Frontier.isEmpty():
        StateTriples = Frontier.pop()
        node = StateTriples[-1][0]
        if problem.isGoalState(node):
            solution = []
            for i in StateTriples[1:]:
                solution = solution + [i[1]]
            return solution
        if node not in explored:
            explored.add(node)
            totalCost = 0
            #calculate the total cost of current path 
            for i in StateTriples:
                totalCost = totalCost + i[2]
            for i in problem.getSuccessors(node):
                #i[2] is the cost to get successor state
                #totalCost+i[2] is the total cost of next path, which is used as priority
                Frontier.push(StateTriples+[list(i)],totalCost+i[2])
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    explored = set()
    Frontier = util.PriorityQueue()
    Frontier.push([[startState,None,0]],0)
    while not Frontier.isEmpty():
        StateTriples = Frontier.pop()
        node = StateTriples[-1][0]
        if problem.isGoalState(node):
            solution = []
            for i in StateTriples[1:]:
                solution = solution + [i[1]]
            return solution
        if node not in explored:
            explored.add(node)
            totalCost = 0
            for i in StateTriples:
                totalCost = totalCost + i[2]
            for i in problem.getSuccessors(node):
                #h is the heuristic value of successor state
                h = heuristic(i[0],problem)
                #the sum of total cost to get successor state and its heuristic value is used as priority
                Frontier.push(StateTriples+[list(i)],totalCost+i[2]+h)
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
