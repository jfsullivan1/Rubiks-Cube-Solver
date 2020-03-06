from rubik import *
import copy

def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    if start == end:
        return []
    startConfigs = {}
    endConfigs = {}
    newStart = start
    newEnd = end

    startConfigs[start] = []
    endConfigs[end] = []
    startQueue = []
    startQueue.append(start)
    endQueue = []
    endQueue.append(end)
    currStartMoveList = []
    currEndMoveList = []

    for frontier in range(7):
    
        startNextQueue = []
        for pos in startQueue:
            for move in range(6):      
                # From start node
                currStartMoveList = copy.copy(startConfigs[pos]) #needs to be copied so we don't modify original value
                newStart = perm_apply(quarter_twists[move], pos)
                if newStart not in startConfigs:
                    currStartMoveList.append(quarter_twists[move])
                    startConfigs[newStart] = currStartMoveList
                    startNextQueue.append(newStart)
                    if newStart in endConfigs:
                        intersect = (set(startConfigs.keys())).intersection(set(endConfigs.keys()))
                        endList = (endConfigs[tuple(intersect)[0]])
                        endList.reverse()
                        return startConfigs[tuple(intersect)[0]] + endList

        startQueue = startNextQueue

        endNextQueue = []
        for pos in endQueue:
            for move in range(6):
                # From end node
                currEndMoveList = copy.copy(endConfigs[pos])
                newEnd = perm_apply(quarter_twists[move], pos)
                if newEnd not in endConfigs:
                    inverseMove = switchPosition(quarter_twists[move])
                    currEndMoveList.append(inverseMove)
                    endConfigs[newEnd] = currEndMoveList
                    endNextQueue.append(newEnd)
                    if newEnd in startConfigs:
                        intersect = (set(startConfigs.keys())).intersection(set(endConfigs.keys()))
                        endList = (endConfigs[tuple(intersect)[0]])
                        endList.reverse()
                        return startConfigs[tuple(intersect)[0]] + endList
        endQueue = endNextQueue

    #This should only happen if there is no solution
    return None


        
def switchPosition(move):
    newMove = ()
    if(move == F):
        newMove = Fi
    elif(move == Fi):
        newMove = F
    elif(move == L):
        newMove = Li
    elif(move == Li):
        newMove = L
    elif(move == U):
        newMove = Ui
    elif(move == Ui):
        newMove = U
    return newMove