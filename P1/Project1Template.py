from SearchEnum import SearchEnum
import Graph, sys
from limit import limit
from collections import OrderedDict
# Template for Project 1 of CS 4341 - A2020
def General_Search(problem, searchMethod):
    """
    Return the solution path or failure to reach state G from state S.

    Parameters
    ----------
    problem : Graph.Graph
        The graph to search from S to G.
    searchMethod : SearchEnum
        The search method to use to search the graph.
    """
    print("\n\tExpanded\tQueue")
    initialState = 'S' # name of the initial state
    finalState = 'G' # Name of the final state
    solution = problem.getState(finalState)
    lim = limit()

    # Make_Queue, Make_Queue_Node, Remove_Front, Terminal_State, Expand, and expand_queue are to be implemented by the student.
    # Implementation of the below pseudocode may vary slightly depending on the data structures used.

    queue = Make_Queue(Make_Queue_Node(problem.getState(initialState))) # Initialize the data structures to start the search at initialState
    while len(queue) > 0:
        node = Remove_Front(queue) # Remove and return the node to expand from the queue
        if node[0] is solution: # solution is not a defined variable, but this statement represents checking whether you have expanded the goal node.
            return node # If this is a solution, return the node containing the path to reach it.
        printer(node, queue)
        opened_nodes = Expand(node,problem) # Get new nodes to add to the queue based on the expanded node.
        queue = expand_queue(queue,opened_nodes,problem,searchMethod, lim)
    return False

def nodeConvert(node):
    pNode = []
    for x in node:
        pNode.append(x.name)
    return pNode
def printer(node, queue):
    expanded = node[0].name
    pNode = nodeConvert(node)
    pQ = [pNode]
    for x in queue:
        pLocal = []
        for y in x:
            name = y.name
            pLocal.append(name)
        pQ.append(pLocal)
    print("\t",expanded,"\t\t",pQ)
def Make_Queue(node):
    return [node]

def Make_Queue_Node(state):
    return [state]

def Remove_Front(queue):
    this = queue[0]
    queue.remove(this)
    return this

def Expand(node, problem):
    this = node[0].edges.keys()
    explore = []
    for x in this:
        that = problem.getState(x)
        if (not (that in node)):
            that = Make_Queue_Node(that)
            that = that + node
            explore.append(that)
    return explore

def expand_queue(queue, nodesToAddToQueue, problem, searchMethod, lim):
    """
    Add the new nodes created from the opened nodes to the queue based on the search strategy.

    Parameters
    ----------
    queue
        The queue containing the possible nodes to expand upon for the search.
    newNodesToAddToQueue : list
        The list of nodes to add to the queue.
    problem : Graph.Graph
        The graph to search from S to G.
    searchMethod : SearchEnum
        The search method to use to search the graph.
    """

#Fill in the below if and elif bodies to implement how the respective searches add new nodes to the queue.
    if searchMethod == SearchEnum.DEPTH_FIRST_SEARCH:
        if (queue is []):
            queue = nodesToAddToQueue
        else:
            queue = nodesToAddToQueue + queue
        return queue

    elif searchMethod == SearchEnum.BREADTH_FIRST_SEARCH:
        if (queue is []):
            queue = nodesToAddToQueue
        else:
            queue = queue + nodesToAddToQueue
        return queue

    elif searchMethod == SearchEnum.DEPTH_LIMITED_SEARCH:
        if (queue is []):
            queue = nodesToAddToQueue
        elif len(nodesToAddToQueue[0]) < 4:
            queue = nodesToAddToQueue + queue
        else:
            queue = queue

        return queue

    elif searchMethod == SearchEnum.ITERATIVE_DEEPENING_SEARCH:
        if (lim.count == 2):
            queue = Make_Queue(Make_Queue_Node(problem.getState('S')))
            lim.setcount()
        elif (queue is []):
            queue = nodesToAddToQueue
        else:
            print(lim.count - 1)
            # print(nodesToAddToQueue)
            if len(nodesToAddToQueue[0]) < lim.count:
                print("here")
                queue = nodesToAddToQueue + queue
            elif(queue == []):
                lim.setcount()
                queue = Make_Queue(Make_Queue_Node(problem.getState('S')))
                print("here2")
            else:
                print('putamadre')
                queue = queue

        return queue

    # elif searchMethod == SearchEnum.UNIFORM_COST_SEARCH:

    # elif searchMethod == SearchEnum.GREEDY_SEARCH:

    # elif searchMethod == SearchEnum.A_STAR:

    # elif searchMethod == SearchEnum.HILL_CLIMBING:

    # elif searchMethod == SearchEnum.BEAM_SEARCH:-

def main(filename):
    """
    Entry point for this progrlam. Parses the input and then runs each search on the parsed graph.

    Parameters
    ----------
    filename : str
        The name of the file with graph input to search
    """

    graph = readInput(filename)
    for search in SearchEnum:
        print(search.value)
        node = General_Search(graph, search)
        if (not node):
            print("failure to find path between S and G")
        else:
            print("\tgoal reached!")
            # Print solution path here
            print("\nSolution found: ", nodeConvert(node)[::-1],"\n" )
def readInput(filename):
    """
    Build the graph from the given input file.

    Parameters
    ----------
    filename : str
        The name of the file with input to parse into a graph.
    """

    parsedGraph = Graph.Graph()
    isHeuristicSection = False # True if processing the heuristic values for the graph. False otherwise.
    sectionDivider = "#####"
    minCharsInLine = 3 # Each line with data must have at least 3 characters
    with open(filename, 'r') as input:
        for line in input.readlines():
            if (len(line) > minCharsInLine):
                line = line.strip()
                if(sectionDivider in line):
                    isHeuristicSection = True
                elif(isHeuristicSection):
                    state, heurStr = line.split(' ')
                    heuristic = float(heurStr)
                    parsedGraph.setHeuristic(state, heuristic)
                else:
                    state1, state2, costStr = line.split(' ')
                    cost = float(costStr)
                    parsedGraph.addStatesAndEdge(state1,state2, cost)
    for state_key in parsedGraph.states:
        state = parsedGraph.states[state_key]
        state.edges = OrderedDict(sorted(state.edges.items()))
    return parsedGraph
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Must input the filename with the graph input to search.")
