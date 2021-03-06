# mlLearningAgents.py
# parsons/27-mar-2017
#
# A stub for a reinforcement learning agent to work with the Pacman
# piece of the Berkeley AI project:
#
# http://ai.berkeley.edu/reinforcement.html
#
# As required by the licensing agreement for the PacMan AI we have:
#
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

# The agent here was written by Simon Parsons, based on the code in
# pacmanAgents.py
# learningAgents.py

from pacman import Directions
from game import Agent
import random
import game
import util

# QLearnAgent
#
class QLearnAgent(Agent):

    # Constructor, called when we start running the
    def __init__(self, alpha=0.2, epsilon=0.05, gamma=0.8, numTraining = 10):
        # alpha       - learning rate
        # epsilon     - exploration rate
        # gamma       - discount factor
        # numTraining - number of training episodes
        #
        # These values are either passed from the command line or are
        # set to the default values above. We need to create and set
        # variables for them
        self.alpha = float(alpha)
        self.epsilon = float(epsilon)
        self.gamma = float(gamma)
        self.numTraining = int(numTraining)
        # Count the number of games we have played
        self.episodesSoFar = 0
        # attributes added
        self.score = 0
        self.state = None
        self.action = None
        self.qValue = util.Counter()

    # Accessor functions for the variable episodesSoFars controlling learning
    def incrementEpisodesSoFar(self):
        self.episodesSoFar +=1

    def getEpisodesSoFar(self):
        return self.episodesSoFar

    def getNumTraining(self):
        return self.numTraining

    # Accessor functions for parameters
    def setEpsilon(self, value):
        self.epsilon = value

    def getAlpha(self):
        return self.alpha

    def setAlpha(self, value):
        self.alpha = value
        
    def getGamma(self):
        return self.gamma

    def getMaxAttempts(self):
        return self.maxAttempts

    # getAction
    #
    # The main method required by the game. Called every time that
    # Pacman is expected to move
    def getAction(self, state):

        # The data we have about the state of the game
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        #print "Legal moves: ", legal
        #print "Pacman position: ", state.getPacmanPosition()
        #print "Ghost positions:" , state.getGhostPositions()
        #print "Food locations: "
        #print state.getFood()
        #print "Score: ", state.getScore()
 
    ### added from here #######################################################

        # compute the reward pacman gained from the action and update q-value
        if self.state != None:
            reward = state.getScore() - self.score
            maxQ = self.getMaxQValue(state, legal)
            self.updateQValue(self.state, self.action, reward, maxQ)

        # e-greedy
        # use function flipCoin in util.py
        if util.flipCoin(self.epsilon):
            action = random.choice(legal)
        else:
        # pick an action with the maximum q-value
        # here I used the Counter class and its argMax function in util.py
            actionWithQValue = util.Counter()
            for action in legal:
                actionWithQValue[action] = self.getQValue(state, action)
            action = actionWithQValue.argMax()

        # update attributes for next action
        self.score = state.getScore()
        self.state = state
        self.action = action

    ###########################################################################

        # We have to return an action
        return action


    # Handle the end of episodes
    #
    # This is called by the game after a win or a loss.
    def final(self, state):

        print "A game just ended!"
        
    ### added from here #######################################################

        # compute the reward pacman gained from the state and update q-values
        reward = state.getScore() - self.score
        self.updateQValue(self.state, self.action, reward, 0)

    ###########################################################################

        # Keep track of the number of games played, and set learning
        # parameters to zero when we are done with the pre-set number
        # of training episodes
        self.incrementEpisodesSoFar()
        print self.getEpisodesSoFar()
        if self.getEpisodesSoFar() == self.getNumTraining():
            msg = 'Training Done (turning off epsilon and alpha)'
            print '%s\n%s' % (msg,'-' * len(msg))
            self.setAlpha(0)
            self.setEpsilon(0)

### functions added ###########################################################

    # accessor for q-value
    def getQValue(self, state, action):
        return self.qValue[(state, action)]

    # compute the q-value for each legal action and return the maximum
    def getMaxQValue(self, state, legal):
        qValueList = [self.getQValue(state, action) for action in legal]
        return max(qValueList)
    
    # update q-value
    def updateQValue(self, state, action, reward, maxQ):
        q = self.getQValue(state, action)
        self.qValue[(state, action)] = q + self.alpha * (reward + self.gamma * maxQ - q)