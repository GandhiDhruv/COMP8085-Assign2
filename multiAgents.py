# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState


def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 1)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """

        def minimax(state, agentIndex, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            numAgents = state.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth + 1 if nextAgent == 0 else depth

            actions = state.getLegalActions(agentIndex)

            if agentIndex == 0:
                return max(minimax(state.generateSuccessor(agentIndex, action), nextAgent, nextDepth)
                           for action in actions)
            else:
                return min(minimax(state.generateSuccessor(agentIndex, action), nextAgent, nextDepth)
                           for action in actions)

        actions = gameState.getLegalActions(0)
        return max(actions, key=lambda action: minimax(gameState.generateSuccessor(0, action), 1, 0))


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        def alphaBeta(state, agentIndex, depth, alpha, beta):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            numAgents = state.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth + 1 if nextAgent == 0 else depth

            if agentIndex == 0:
                return maxValue(state, agentIndex, nextAgent, nextDepth, alpha, beta)
            else:
                return minValue(state, agentIndex, nextAgent, nextDepth, alpha, beta)

        def maxValue(state, agentIndex, nextAgent, nextDepth, alpha, beta):
            v = float("-inf")
            for action in state.getLegalActions(agentIndex):
                v = max(v, alphaBeta(state.generateSuccessor(agentIndex, action), nextAgent, nextDepth, alpha, beta))
                if v > beta: return v
                alpha = max(alpha, v)
            return v

        def minValue(state, agentIndex, nextAgent, nextDepth, alpha, beta):
            v = float("inf")
            for action in state.getLegalActions(agentIndex):
                v = min(v, alphaBeta(state.generateSuccessor(agentIndex, action), nextAgent, nextDepth, alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v

        bestScore = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        bestAction = None

        for action in gameState.getLegalActions(0):
            score = alphaBeta(gameState.generateSuccessor(0, action), 1, 0, alpha, beta)
            if score > bestScore:
                bestScore = score
                bestAction = action
            if bestScore > beta:
                return bestAction
            alpha = max(alpha, bestScore)

        return bestAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """

        def expectimax(state, agentIndex, depth):

            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            numAgents = state.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth + 1 if nextAgent == 0 else depth
            actions = state.getLegalActions(agentIndex)

            if agentIndex == 0:
                return max(expectimax(state.generateSuccessor(agentIndex, action), nextAgent, nextDepth)
                           for action in actions)

            else:
                successorValues = [expectimax(state.generateSuccessor(agentIndex, action), nextAgent, nextDepth)
                                   for action in actions]
                return sum(successorValues) / len(successorValues)

        actions = gameState.getLegalActions(0)
        return max(actions, key=lambda action: expectimax(gameState.generateSuccessor(0, action), 1, 0))


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    score = currentGameState.getScore()

    foodList = food.asList()
    if foodList:
        minFoodDist = min([util.manhattanDistance(pos, f) for f in foodList])
        score += 10.0 / minFoodDist

    for i, ghost in enumerate(ghostStates):
        dist = util.manhattanDistance(pos, ghost.getPosition())
        if scaredTimes[i] > 0:
            score += 200.0 / (dist + 0.1)
        else:
            if dist < 2:
                score -= 500

    score -= 4 * len(foodList)
    score -= 20 * len(currentGameState.getCapsules())

    return score


better = betterEvaluationFunction
