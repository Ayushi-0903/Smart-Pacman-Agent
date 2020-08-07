# pacmanAgents.py
# ---------------
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


from pacman import Directions
from game import Agent
from heuristics import *
import random
import math

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class RandomSequenceAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0,10):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        possible = state.getAllPossibleActions();
        for i in range(0,len(self.actionList)):
            self.actionList[i] = possible[random.randint(0,len(possible)-1)];
        tempState = state;
        for i in range(0,len(self.actionList)):
            if tempState.isWin() + tempState.isLose() == 0:
                tempState = tempState.generatePacmanSuccessor(self.actionList[i]);
            else:
                break;
        # returns random action from all the valide actions
        return self.actionList[0];

class HillClimberAgent(Agent):

    def registerInitialState(self, state):
        self.actionseq = 5
        self.randomaction = 50
        self.actionList = []
        for i in range(0,self.actionseq):
            self.actionList.append(Directions.STOP)                                        
        return 
    def getAction(self, state):
        actionseqtemp = self.actionList[:] 
        i=0
        self.p = state.getAllPossibleActions()                                     
        while i<(len(self.actionList)):
            self.actionList[i] = self.p[random.randint(0,len(self.p)-1)]
            i=i+1
        scores = scoreEvaluation(state)                                                
        forwardmodel = 1
        while(forwardmodel!= 0):
            statetemp = state
            j=0
            while j<(len(actionseqtemp)):
                nextsucc = statetemp.generatePacmanSuccessor(actionseqtemp[j]) 
                if(nextsucc == None):                                                
                    forwardmodel = 0
                    break
                elif(nextsucc.isLose()):                                     
                    break
                elif(nextsucc.isWin()):                                              
                    break
                else:
                   statetemp = nextsucc
                j=j+1
            if (scoreEvaluation(statetemp) >= scores):
                scores = scoreEvaluation(statetemp)
                self.actionList = actionseqtemp[:]
            if (forwardmodel == 0):                                                   
                if (scoreEvaluation(statetemp) >= scores):
                    self.actionList = actionseqtemp[:]
                break
            k=0
            while k<(len(actionseqtemp)):
                randomno = random.randint(1,100)                                      
                if (randomno >= self.randomaction):
                    actionseqtemp[k] = self.p[random.randint(0,len(self.p)-1)] 
                else:
                    actionseqtemp[k] = self.actionList[k]   
                k=k+1
        return self.actionList[0] 

class GeneticAgent(Agent):
    def __init__(self):
        self.actionseq = 5
        self.populationsize = 8
        self.crossingover = 70
        self.childcrossingover = 50
        self.MUTATE = 10

    def registerInitialState(self, state):
        self.actionList = []
        for i in range(self.actionseq):
            self.actionList.append(Directions.STOP)
        return

    def statelast(self,state):
        laststatesequence = []
        for i in range(self.populationsize):
            laststatesequence.append(state)
        return laststatesequence
            
    def initialize_parents(self,state):
        population = []
        self.p = state.getAllPossibleActions()
        for i in range(self.populationsize):
            for j in range(0,len(self.actionList)):
                self.actionList[j] = self.p[random.randint(0,len(self.p)-1)];
            population.append(self.actionList)
        return population

    def fitness_calculation(self, population, laststatesequence):
        fitness_of_population = []


        for i in range(self.populationsize):
            last_state_of_population = laststatesequence[i]
	    fitness_score = scoreEvaluation(last_state_of_population)
            fitness_of_population.append((fitness_score,population[i]))

        return fitness_of_population
        
    def rank_chromosome(self, fitness_of_population):
        fitness_of_population.sort()
        fitness_of_population.reverse()
        rank = 1
        chromosomes_rank_fitness = []
        for i in range(self.populationsize):
            chromosomes_rank_fitness.append((rank, fitness_of_population[i][1]))
            rank+=1
        return chromosomes_rank_fitness

    def generate_next_population(self, chromosomes_rank_fitness):
        generationnxt = []
        parent_selection = [0,0]
        for j in range(self.populationsize/2):
            
            for k in range(2): 
                rank_proportinality_selection = random.randint(1, 36)
                if ( 1 < rank_proportinality_selection <= 3):
                    parent_selection[k] = chromosomes_rank_fitness[6][1]
                elif ( 3 < rank_proportinality_selection <= 6):
                    parent_selection[k] = chromosomes_rank_fitness[5][1]
                elif ( 6 < rank_proportinality_selection <= 10):
                    parent_selection[k] = chromosomes_rank_fitness[4][1]
                elif ( 10 < rank_proportinality_selection <= 15):
                    parent_selection[k] = chromosomes_rank_fitness[3][1]
                elif ( 15 < rank_proportinality_selection <= 21):
                    parent_selection[k] = chromosomes_rank_fitness[2][1]
                elif ( 21 < rank_proportinality_selection <= 28):
                    parent_selection[k] = chromosomes_rank_fitness[1][1]
                elif ( 28 < rank_proportinality_selection <= 36):
                    parent_selection[k] = chromosomes_rank_fitness[0][1]
                elif ( 0 < rank_proportinality_selection <= 1):
                    parent_selection[k] = chromosomes_rank_fitness[7][1]
            if (random.randint(1,100) <= self.crossingover):
                child1, child2 = self.crossover(parent_selection)   
            else:
                child1 = parent_selection[0]
                child2 = parent_selection[1]
            generationnxt.append(child1)
            generationnxt.append(child2)
        return generationnxt
    def crossover(self, parent_selection):
        child1 = []
        child2 = []
        for i in range(self.actionseq):
            if random.randint(1, 100) <= self.childcrossingover:
                child1.append(parent_selection[0][i])
                child2.append(parent_selection[1][i])
            else:
                child1.append(parent_selection[1][i])
                child2.append(parent_selection[0][i])

        return child1, child2
        
    def mutate(self, generationnxt):
        for children in generationnxt:
                if random.randint(1, 100) <= self.MUTATE:
                    children[random.randint(0, len(children)-1)] = random.choice(self.p)
        return generationnxt
    def getAction(self, state):
        laststatesequence = self.statelast(state)                               
        forwardmodel = 1
        scored = []
        population = self.initialize_parents(state)
        statetemp = state
        self.prev_population = population[:][:]
        self.prev_laststatesequence = laststatesequence[:]


        while(forwardmodel != 0):

            for i in range(self.populationsize):
                statetemp = state
                for j in range(self.actionseq):
                    nextsucc = statetemp.generatePacmanSuccessor(population[i][j])
                    if(nextsucc == None):
                        forwardmodel = 0
                        break 
                    if(nextsucc.isWin()):
                        break  
                    if(nextsucc.isLose()):
                        break  
                    else:
                       statetemp = nextsucc
                laststatesequence[i] = statetemp
                if (forwardmodel == 0):
                    break
            if (forwardmodel == 0):
                break
            
            fitness_of_population = self.fitness_calculation(population, laststatesequence)
            chromosomes_rank_fitness = self.rank_chromosome(fitness_of_population)
            generationnxt = self.generate_next_population(chromosomes_rank_fitness)
            population = self.mutate(generationnxt)
            self.prev_population = population[:][:]
            self.prev_laststatesequence = laststatesequence[:]
        if (forwardmodel == 0):
            population = self.prev_population[:][:]
            laststatesequence = self.prev_laststatesequence[:]
        fitness_of_last_population = []
        for i in range(self.populationsize):
            last_state_of_population = laststatesequence[i]
	    fitness_score = scoreEvaluation(last_state_of_population)
            fitness_of_last_population.append(fitness_score)
        Max_score = max(fitness_of_last_population)
        
        sequence_index = fitness_of_last_population.index(Max_score)
        finding_first_action = population[sequence_index]
        return finding_first_action[0]

class Node():
    def __init__(self, state, parent = None, action = None):
        self.unexplored = state.getLegalPacmanActions()
        self.parent = parent
        self.children = []
        self.action = action
        self.result = 0
        self.visits = 0

class MCTSAgent(Agent):

    def registerInitialState(self, state):
        self.randomness = 5
        self.c = 1
        return

    def getAction(self, state):
        node = Node(state)
        self.forwardmodel = 1
        self.flag = 0
        i=0
        while(self.forwardmodel != 0):
            self.flag = 0
            next_node = self.tree(node, state)
            if (self.flag == 1):
                continue
            if (self.forwardmodel == 0):
                break
            delta = self.default_policy(next_node, state)
            if (self.forwardmodel == 0):
                break
            if (self.flag == 1):
                continue
            self.backup(next_node, delta)
        most_visited_times = 0
        best_node = node
        while i<len(node.children):
            child_node = node.children[i]
            if (child_node.visits > most_visited_times):
                most_visited_times = child_node.visits
                best_node = child_node
            i=i+1
        return best_node.action
    def tree(self, node, state):
        while(self.forwardmodel != 0):
            if (len(node.unexplored) > 0):
                return self.expand(node, state)
            else:
                prev_node = node
                node = self.select(node)
                if node is prev_node:
                    break
        return node
    def expand(self, node, state):
        tempNode = node
        statetemp = state
        back_actions = []
        allNodes = []
        while(node.parent != None):
            back_actions.append(node.action)
            allNodes.append(node)
            node = node.parent
        i=0
        while i<(len(back_actions)):
            reverse_action = back_actions.pop(-1)
            reverse_node = allNodes.pop(-1)
            child = statetemp.generatePacmanSuccessor(reverse_action)
            if (child == None):
                self.forwardmodel = 0
                return
            elif(child.isWin() + child.isLose() == 1):
                result = gameEvaluation(state, child)
                self.backup(reverse_node, result)
                self.flag = 1
                return reverse_node
            else:
                statetemp = child
            i=i+1
        action = random.choice(tempNode.unexplored)
        explore_child = statetemp.generatePacmanSuccessor(action)
        if (explore_child == None):
            self.forwardmodel = 0
            return
        elif(explore_child.isWin() + explore_child.isLose() == 1):
            result = gameEvaluation(state, explore_child)
            self.backup(tempNode, result)
            self.flag = 1
            return tempNode
        else:
            tempNode.unexplored.pop(tempNode.unexplored.index(action))
            next_node = Node(explore_child, tempNode, action)
            tempNode.children.append(next_node)
            return next_node

    def select(self, node):
        UCT_max = 0
        best_node = node
        for i in range(len(node.children)):
            child_node = node.children[i]
            UCT_score = (child_node.result/child_node.visits) + self.c*math.sqrt(2*math.log(node.visits)/child_node.visits)
            if UCT_score > UCT_max:
                UCT_max = UCT_score
                best_node = child_node
        return best_node
            

    def default_policy(self, node, state):
        tempNode = node
        statetemp = state
        back_actions = []
        allNodes = []
        i=0
        while(node.parent != None):
            back_actions.append(node.action)
            allNodes.append(node)
            node = node.parent
        while i<(len(back_actions)):
            action = back_actions.pop(-1)
            reverse_node = allNodes.pop(-1)
            child = statetemp.generatePacmanSuccessor(action)
            if (child == None):
                self.forwardmodel = 0
                return
            elif(child.isWin() + child.isLose() == 1):
                result = gameEvaluation(state, child)
                self.backup(reverse_node, result)
                self.flag = 1
                return result
            else:
                statetemp = child
            i=i+1
        for _ in range(self.randomness):
            legal_actions = statetemp.getLegalPacmanActions()
            action = random.choice(legal_actions)
            child = statetemp.generatePacmanSuccessor(action)
            if (child == None):
                self.forwardmodel = 0
                break
            elif(child.isWin() + child.isLose() == 1):
                result = gameEvaluation(state, child)
                self.backup(tempNode, result)
                self.flag = 1
                return result
            else:
                statetemp = child
        result = gameEvaluation(state, statetemp)
        return result
            
    def backup(self, node, result):
        while True:
            node.visits = node.visits + 1
            node.result = node.result + result
            if (node.parent == None):
                break
            node = node.parent 


