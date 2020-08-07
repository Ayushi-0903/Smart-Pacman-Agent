###### Pacman Instructions ######

##Implement##
1. *Breadth-first search in the class BFSAgent*, 
2. *Depth-first search in the class DFSAgent*, 
3. *A* search in the class AStarAgent*,
within the in pacmanAgents.py file, using admissibleHeuristic as a heuristic function for the AStarAgent.


##Notes:##
⁃ Python 2.7 is required to run the Framework.
⁃ External libraries are not used.
⁃ I used these system functions:
  ⁃ state.getLegalPacmanActions(): return all the legal actions in this state
  ⁃ state.generatePacmanSuccessor(action): return the next state if pacman take a certain action (return a new copy, doesn’t modify the current state)
  ⁃ admissibleHeuristic(state): estimates the remaining cost from the current state to the goal state
  ⁃ state.isWin(): check if this state is win state
  ⁃ state.isLose(): check if this state is lose state
⁃ For A* algorithm: f(n) = g(n) + h(n)
⁃ f(n): the total cost of the next node
⁃ g(n): is the cost of the path since the start node (in this exercise, this cost is the depth of the current node, i.e. the number of actions from the start till that node)
⁃ h(n): is a heuristic function that estimates the remaining cost till the goal (in this exercise, this heuristic can be calculated using admissibleHeuristic(state) function on the current state)
⁃ For array sorting, you can use python internal sorting function. example: array.sort(key=lambda x: admissibleHeuristic(x)). This example sort the array based on the admissibleHeuristic function.


##How to run:##
⁃ To play pacman:
python pacman.py
⁃ To run a certain agent using graphics use the following command:
python pacman.py -p AgentName
