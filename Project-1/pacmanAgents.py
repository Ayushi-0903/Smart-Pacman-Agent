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

class OneStepLookAheadAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(admissibleHeuristic(state), action) for state, action in successors]
        # get best choice
        bestScore = min(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
#   Declare all the variables
        gostate = []
        went={}
        prv={}
        length={}
        length[state]=0
        sn = state
#   Appending in list of visited state (go_state)
        gostate.append((state,Directions.STOP))
#   Check if visited state is not empty and set first node of visited state(gostate) as current node(cn)
#   CHeck if current node is not win state
        while gostate:
            cn = gostate[0]
            del gostate[0]
            if cn[0].isWin():
                break
#   Get all legal actions for pacman         
            legal_actions = cn[0].getLegalPacmanActions()
#   Get all the successor state for these actions. Check if we have reached leaf node. If not then add element to visited node(went) 
#   Calculate depth(length) and append child to visit state(gostate).
#   Then store (current node, child) in 'previous' list. 
            sucsr_s = [(cn[0].generatePacmanSuccessor(action),action) for action in legal_actions]
            for sucsr in sucsr_s:
                if sucsr[0]==None:
                    break
                if sucsr[0] in went:
                    continue
                went[sucsr[0]]=True
                length[sucsr[0]] = length[cn[0]] + 1
                gostate.append(sucsr)
                prv[sucsr[0]] = (cn[0],sucsr[1])

#   Calculate the shortest path                
        p = []
        minimum=999999999
        for cn in prv:
            if admissibleHeuristic(cn)+length[cn]<minimum:
                minimum=admissibleHeuristic(cn)+length[cn]
                finalnode = cn
                
#   Store shorted path in p list        
        cn = finalnode
        while cn != sn:
            p.append((prv[cn][1],prv[cn][0]))
            cn = prv[cn][0]
#   Reverse the path  and return 
        soln = p[::-1]
        return soln[0][0]


class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
#   Calculate the path  
        length={}
        length[state]=0
        sn = state
        gostate = []
        went={}
        previous={}
#   Appending in list of visited state (go_state)
        gostate.append((state,Directions.STOP))
#   Check if visited state is not empty and set last element of visited state(gostate) as current node(cn)
#   Store the remaining cost from the curretn state to the goal state in Minimum.
#   Check if current node is not win state       
        while gostate:
            cn = gostate[-1]
            del gostate[-1]
            minimum = admissibleHeuristic(cn[0])
            if cn[0].isWin():
                break
#   Get all legal actions for pacman           
            legal_actions = cn[0].getLegalPacmanActions()
#   Get all the sucsr state for these actions. And check if it has reach the leaf node.
#   Mark value of child as True in visited node(went). And append it to the current value and successor list(successor)
#   Add (Current node, Successor) to the previous list.
            sucsr_s = [(cn[0].generatePacmanSuccessor(action),action) for action in legal_actions]
            for sucsr in sucsr_s:
                if sucsr[0]==None:
                    break
                if sucsr[0] in went:
                    continue
                length[sucsr[0]] = length[cn[0]] + 1
                went[sucsr[0]]=True
                gostate.append(cn)
                gostate.append(sucsr)
                previous[sucsr[0]] = (cn[0],sucsr[1])
#   Calculate the shortest path                  
        p = []
        minimum=999999999
        for cn in previous:
            if admissibleHeuristic(cn)+length[cn]<minimum:
                minimum=admissibleHeuristic(cn)+length[cn]
                finalnode = cn              
#   Store shorted path in p list         
        cn = finalnode
        while cn != sn:
            p.append((previous[cn][1],previous[cn][0]))
            cn = previous[cn][0]
#   Reverse the path  and return           
        soln = p[::-1]
        return soln[0][0]

class AStarAgent(Agent):
#   Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

#   GetAction Function: Called with every frame
    def getAction(self, state):
#   Declare all the variables
        cost_dict = {}
        length={}
        sn = state
        t_c=[]
        went={}
        previous={}
        cost_dict[state]=0
        length[state]=0
#   Appending in list of total cost (t_c)
        t_c.append((state,0))
#   Initializing minimum state
        m_s = state
#   Initializing minimum cost
        m_c = 99999999 + admissibleHeuristic(state)
#    Check if total cost list (t_c) is not empty. 
#    Then sorting current node and total cost using python internal sorting function and deleting total cost node.
#    Then calculating the cost of the path since the start node.
#    Check if current node is a win state or not. If it is not win then add element in the visited node by adding into went list.
    
        while len(t_c)!=0:
            cn = sorted(t_c,key=lambda x: x[1], reverse=True)[0][0]
            t_c = sorted(t_c,key=lambda x: x[1], reverse=True)
            del t_c[0]
            g_x_cn = cost_dict[cn]
            if cn.isWin():
                break
            if cn in went:
                continue
            went[cn]=True
#    Get the legal actions and successor actions.
#    Check if you have reached leaf node or not.
#    Calculate the total cost and cost of the path since the start node and assign values to min state(m_s) and min cost(m_c)
            legal_action = cn.getLegalPacmanActions()
            sucsr_s = [(cn.generatePacmanSuccessor(action),action) for action in legal_action]
            for successor in sucsr_s:
                if successor[0]==None:
                    break
                length[successor[0]] = length[cn] + 1
                g_x_successor = g_x_cn + length[successor[0]]
                f_x = g_x_successor + admissibleHeuristic(successor[0])
                if cost_dict.has_key(successor[0])==False or g_x_successor < cost_dict[successor[0]]: 
                    cost_dict[successor[0]] = g_x_successor
                    t_c.append((successor[0],f_x))
                    previous[successor[0]] = (cn,successor[1])
                if f_x <m_c:
                    m_s=successor[0]
                    m_c=f_x
#   Calculate the path      
        p = []                
        cn = m_s
        while cn != sn:
            p.append((previous[cn][1],previous[cn][0]))
            cn = previous[cn][0]
#   Reverse the path  and return 
        solution = p[::-1]
        return solution[0][0]
