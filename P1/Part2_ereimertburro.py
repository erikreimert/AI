from SearchEnum import SearchEnum
import Graph, sys
from limit import limit
from collections import OrderedDict
# Template for Project 1 of CS 4341 - A2020
explored = []
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
    initial = problem.getState(initialState)
    solution = problem.getState(finalState)
    lim = limit()
    lim.check(searchMethod)
    # Make_Queue, Make_Queue_Node, Remove_Front, Terminal_State, Expand, and expand_queue are to be implemented by the student.
    # Implementation of the below pseudocode may vary slightly depending on the data structures used.

    queue = Make_Queue(Make_Queue_Node(initial)) # Initialize the data structures to start the search at initialState
    global explored
    explored = []
    while len(queue) > 0:
        node = Remove_Front(queue) # Remove and return the node to expand from the queue
        print('\nExplored = ', nodeConvert(explored), '\n')
        printer(node, queue, initial, lim)
        if node[0] is solution: # solution is not a defined variable, but this statement represents checking whether you have expanded the goal node.
            lim.falseFlag()
            return node # If this is a solution, return the node containing the path to reach it.
        opened_nodes = Expand(node,problem, lim) # Get new nodes to add to the queue based on the expanded node.
        explored = [node[0]] + explored

        ##########################
        #Checks when opened_nodes is [] which means its the end of the map and adds next node to queue on ITERATIVE_DEEPENING_SEARCH
        if lim.flag or lim.bflag or SearchEnum.DEPTH_FIRST_SEARCH:
            while len(opened_nodes) == 0:
                node = Remove_Front(queue)
                opened_nodes = Expand(node,problem, lim)
                printer(node, queue, initial, lim)
        #########################
        opened_nodes = checkEx(opened_nodes, explored, queue, lim)
        queue = expand_queue(queue,opened_nodes,problem,searchMethod, lim)
    return False

#tool for printing out individual nodes and for debugging
def nodeConvert(node):
    pNode = []
    for x in node:
        pNode.append(x.name)
    return pNode

#prints stuff
def printer(pnode, pqueue, pinitial, plim):
    expanded = pnode[0].name
    pNode = nodeConvert(pnode)
    pQ = [pNode]
    c = 0
    for x in pqueue:
        pLocal = nodeConvert(x)
        pQ.append(pLocal)
    if plim.flag and expanded is pinitial.name:
        lc = plim.count - 2
        print("\nL=", lc, "   ",expanded,"\t\t",pQ)
    elif plim.uniFlag:
        NumQueue = [pnode] + pqueue
        for x in NumQueue:
            vals = cost(x)
            vals = [str(vals)]
            pQ[c] = vals + pQ[c]
            c+=1
        print("\t",expanded,"\t\t",pQ)
    elif plim.heurPrint:
        NumQueue = [pnode] + pqueue
        for x in NumQueue:
            vals = heur(x)
            vals = [str(vals)]
            pQ[c] = vals + pQ[c]
            c+=1
        print("\t",expanded,"\t\t",pQ)
    elif plim.hillPrint:
        NumQueue = [pnode] + pqueue
        for x in NumQueue:
            vals = heur(x)
            vals = [str(vals)]
            pQ[c] = vals + pQ[c]
            c+=1
        print("\t",expanded,"\t\t",pQ)
    elif plim.beamPrint:
        NumQueue = [pnode] + pqueue
        for x in NumQueue:
            vals = heur(x)
            vals = [str(vals)]
            pQ[c] = vals + pQ[c]
            c+=1
        print("\t",expanded,"\t\t",pQ)
    elif plim.aStarF:
        NumQueue = [pnode] + pqueue
        for x in NumQueue:
            vals = aStarisBorn(x)
            vals = [str(vals)]
            pQ[c] = vals + pQ[c]
            c+=1
        print("\t",expanded,"\t\t",pQ)
    else:
        print("\t",expanded,"\t\t",pQ)

def Make_Queue(node):
    return [node]

def Make_Queue_Node(state):
    return [state]

def Remove_Front(queue):
    this = queue[0]
    queue.remove(this)
    return this

def Expand(node, problem, lim):
    this = node[0].edges.keys()
    explore = []
    for x in this:
        that = problem.getState(x)
        if (not (that in node)):
            that = Make_Queue_Node(that)
            that+= node
            explore.append(that)
    if lim.alpha:
        explore = alphaSort(explore)
    return explore

#checks if the opened nodes exist in the explored list
def checkEx(node, explored, queue, lim):
    for x in range(len(node)):
        if node[x][0] not in explored:
            if x < len(node)-1:
                continue
            else:
                return node
        else:
            node.remove(node[x])
            if x < len(node)-1:
                continue
            else:
                return node
def alphaSort(newNodes):
    nodes = []
    ncopy = []
    qcpy = []
    for x in newNodes:
        qcpy+=[1]
        nodes.append(nodeConvert(x))
        ncopy.append(nodeConvert(x))
    ncopy.sort()
    # print(nodes)
    # print(ncopy)
    for x in range(len(ncopy)):
        index = ncopy.index(nodes[x])
        qcpy[index] = newNodes[x]
    onec = 0
    for x in qcpy:
        if x == 1:
            onec+=1
    for x in range(onec):
        qcpy.remove(1)
    return qcpy
#the father of all sorts
def infoSort(queue, lim):

    if lim.bflag:
        #pew pew
        queue, values = laserBeam(queue)
    else:
        #daddys spoiled little brat
        queue, values = childSort(queue, lim)
    repeats = []
    for x in range(len(values)-1):
        if values[x] is values[x+1]:
            repeats+=[x]
    if len(repeats) > 0:
        for x in range(len(repeats)-1):
            if queue[x][0] is not queue[x+1][0]:
                hold = [queue[x]] + [queue[x+1]]
                check = []
                check2 = []
                for y in hold:
                    a = nodeConvert(y)
                    check+=[a]
                    check2+=[a]
                    check.sort()
                    if check is not check2:
                        hold = queue[x]
                        queue[x] = queue[x+1]
                        queue[x+1] = hold
                continue
                if len(queue[x]) < len(queue[x+1]):
                    hold = queue[x]
                    queue[x] = queue[x+1]
                    queue[x+1] = hold
                    continue
                elif len(queue[x]) == len(queue[x+1]):
                    hold = [queue[x]] + [queue[x+1]]
                    check = []
                    check2 = []
                    for y in hold:
                        a = nodeConvert(y)
                        check+=[a]
                        check2+=[a]
                        check.sort()
                    if check is not check2:
                        hold = queue[x]
                        queue[x] = queue[x+1]
                        queue[x+1] = hold
    return queue
#gets a node and returns the cost of its path
def cost(node):
    vals = 0
    for y in range(len(node)-1):
        vals+= node[y].edges.get(node[y+1].name)
    return vals
#gets the heuristic of something
def heur(node):
    vals = node[0].heuristic
    return vals
#can you tell my sanity is dwindling with this assignment??
def aStarisBorn(node):
    hvals = heur(node)
    cvals = cost(node)
    fvals = hvals + cvals
    return fvals
#returns array of cost for every node in queue
#first gets the value of the path of every node, then copies it and sorts it. Uses the sorted list to get the index num in which the queue should be and orders the list as such
def childSort(queue, lim):
    values = []
    copy = []
    queueCpy = []

    for x in queue:
        queueCpy+=[1]
        if lim.uniFlag:
            lim.heurFlag = False #TODO odd error
            vals = cost(x)
        if lim.heurFlag:
            vals = heur(x)
        if lim.aStarF:
            vals = aStarisBorn(x)
        values.append(vals)
        copy.append(vals)
    copy.sort()
    for x in range(len(copy)):
        index = copy.index(values[x])
        queueCpy[index] = queue[x]
    onec = 0
    for x in queueCpy:
        if x == 1:
            onec+=1
    for x in range(onec):
        queueCpy.remove(1)

    return queueCpy, copy

#wilhelm scream
def laserBeam(queue):
    values = []
    smoll = [[]]
    for x in queue:
        vals = heur(x)
        values.append(vals)
    smallest = values[0]
    smaller = None
    for x in values[1:]:
        if x < smallest:
            smaller = smallest
            smallest = x
        elif smaller == None or smaller > x:
            smaller = x
    if values.index(smallest) < values.index(smaller):
        smoll.append(queue[values.index(smallest)])
        smoll.append(queue[values.index(smaller)])
        beamedVals = [smallest, smaller]
    else:
        smoll.append(queue[values.index(smaller)])
        smoll.append(queue[values.index(smallest)])
        beamedVals = [smaller, smallest]
    return smoll[1:], beamedVals

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
        return nodesToAddToQueue + queue

    elif searchMethod == SearchEnum.BREADTH_FIRST_SEARCH:
        return queue + nodesToAddToQueue

    elif searchMethod == SearchEnum.DEPTH_LIMITED_SEARCH:
        if len(nodesToAddToQueue) > 0 :
            if len(nodesToAddToQueue[0]) < 4:
                queue = nodesToAddToQueue + queue
        return queue

    elif searchMethod == SearchEnum.ITERATIVE_DEEPENING_SEARCH:
        iterations = []
        for x in nodesToAddToQueue:
            if len(x) < lim.count:
                iterations+=[x]
        queue = iterations + queue
        if queue == []:
            global explored
            explored = []
            lim.increase()
            return Make_Queue(Make_Queue_Node(problem.getState('S')))
        else:
            return queue

    elif searchMethod == SearchEnum.UNIFORM_COST_SEARCH:
        queue = nodesToAddToQueue + queue
        print(len(queue))
        removeq = []
        for x in range(len(queue)-1):
            if queue[x][0] == queue[x+1][0]:
                if cost(queue[x]) < cost(queue[x+1]):
                    removeq.append(queue[x+1])
                else:
                    removeq.append(queue[x])
        for x in removeq:
            queue.remove(x)
        queue = infoSort(queue, lim)
        return queue

    elif searchMethod == SearchEnum.GREEDY_SEARCH:
        queue = nodesToAddToQueue + queue
        removeq = []
        for x in range(len(queue)-1):
            if queue[x][0] == queue[x+1][0]:
                if heur(queue[x]) < heur(queue[x+1]):
                    removeq.append(queue[x+1])
                else:
                    removeq.append(queue[x])
        for x in removeq:
            queue.remove(x)
        queue = infoSort(queue, lim)
        return queue
    elif searchMethod == SearchEnum.A_STAR:
        queue = nodesToAddToQueue + queue
        removeq = []
        for x in range(len(queue)-1):
            if queue[x][0] == queue[x+1][0]:
                if aStarisBorn(queue[x]) < aStarisBorn(queue[x+1]):
                    removeq.append(queue[x+1])
                else:
                    removeq.append(queue[x])
        for x in removeq:
            queue.remove(x)
        queue = infoSort(queue, lim)
        return queue

    elif searchMethod == SearchEnum.HILL_CLIMBING:
        queue = nodesToAddToQueue + queue
        removeq = []
        for x in range(len(queue)-1):
            if queue[x][0] == queue[x+1][0]:
                if heur(queue[x]) < heur(queue[x+1]):
                    removeq.append(queue[x+1])
                else:
                    removeq.append(queue[x])
        for x in removeq:
            queue.remove(x)
        queue = infoSort(queue, lim)
        return [queue[0]]

    elif searchMethod == SearchEnum.BEAM_SEARCH:
        if queue == []:
            return nodesToAddToQueue
        queue+=nodesToAddToQueue
        c = 0
        if len(queue) >= 3:
            for x in range(len(queue)-1):
                c+=1
                if len(queue[x]) is not len(queue[x+1]):
                    return queue
                elif c == (len(queue) - 1):
                    removeq = []
                    for x in range(len(queue)-1):
                        if queue[x][0] == queue[x+1][0]:
                            if heur(queue[x]) < heur(queue[x+1]):
                                removeq.append(queue[x+1])
                            else:
                                removeq.append(queue[x])
                    for x in removeq:
                        queue.remove(x)
                    queue = infoSort(queue, lim)
                    return queue
        return queue


def main(filename):
    """
    Entry point for this program. Parses the input and then runs each search on the parsed graph.

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
