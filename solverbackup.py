import rubik
import copy

def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    newStart = copy.deepcopy(start)
    newEnd = copy.deepcopy(end)
    startMoves = []
    startConfigs = []
    endMoves = []
    endConfigs = []
    allMoves = []
    isFirstPass = True

    if start == end:
        return []
    # Two-way BFS
    while not any(config in startConfigs for config in endConfigs) and not(start in endConfigs or end in startConfigs): 
        for i in range(6):
            startMoves.append(list(rubik.quarter_twists_names.values())[i])
            if isFirstPass:
                newStart = rubik.perm_apply(rubik.quarter_twists[i], start)
                startConfigs.append(newStart)
            else:
                newStart = rubik.perm_apply(rubik.quarter_twists[i], startConfigs[i-6])
                startConfigs.append(newStart)
            endMoves.append(list(rubik.quarter_twists_names.values())[i])
            if isFirstPass:
                newEnd = rubik.perm_apply(rubik.quarter_twists[i], end)
                endConfigs.append(newEnd)
            else:
                newEnd = rubik.perm_apply(rubik.quarter_twists[i], endConfigs[i-6])
                endConfigs.append(newEnd)
        isFirstPass = False

    magicStartIndex = 0
    magicEndIndex = 0
    for i in range(len(startConfigs)):
        for j in range(len(endConfigs)):
            if startConfigs[i] == endConfigs[j]:
                magicStartIndex = i
                magicEndIndex = j

    #Find the start list path
    move = ""
    i = 0
    iterator = magicStartIndex % 6
    while i < len(startMoves):
        if (i + iterator) < len(startMoves):  
            if(startMoves[i+iterator] == 'F'):
                move = rubik.F
            elif(startMoves[i+iterator] == 'Fi'):
                move = rubik.Fi
            elif(startMoves[i+iterator] == 'L'):
                move = rubik.L
            elif(startMoves[i+iterator] == 'Li'):
                move = rubik.Li
            elif(startMoves[i+iterator] == 'U'):
                move = rubik.U
            elif(startMoves[i+iterator] == 'Ui'):
                move = rubik.Ui
            allMoves.append(move)
        i += 6
    
    # Find the end list path
    i = 0
    inverseIterator = magicEndIndex % 6
    inverseList = []
    inverseMove = ""
    while i < len(endMoves):
        if (i + inverseIterator) < len(endMoves): 
            if(endMoves[i+inverseIterator] == 'F'):
                inverseMove = rubik.Fi
            elif(endMoves[i+inverseIterator] == 'Fi'):
                inverseMove = rubik.F
            elif(endMoves[i+inverseIterator] == 'L'):
                inverseMove = rubik.Li
            elif(endMoves[i+inverseIterator] == 'Li'):
                inverseMove = rubik.L
            elif(endMoves[i+inverseIterator] == 'U'):
                inverseMove = rubik.Ui
            elif(endMoves[i+inverseIterator] == 'Ui'):
                inverseMove = rubik.U
            inverseList.append(inverseMove)
        i+=6
            
    # Flip the list of end moves because we actually went backwards technically
    inverseList.reverse()

    # Add inverse list moves to the full moves list. 
    for i in range(len(inverseList)):
        allMoves.append(inverseList[i])
    return allMoves


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
    newStart = copy.deepcopy(start)
    newEnd = copy.deepcopy(end)

    startConfigs[start] = []
    endConfigs[end] = []
    startQueue = []
    startQueue.append(start)
    endQueue = []
    endQueue.append(end)
    currStartMoveList = []
    currEndMoveList = []
    finalMoveList = []

    for frontier in range(7):
    
        startNextQueue = []
        for pos in startQueue:
            for move in range(6):      
                # From start node
                currStartMoveList = startConfigs[pos]
                newStart = perm_apply(quarter_twists[move], pos)
                if newStart not in startConfigs:
                    currStartMoveList.append(quarter_twists[move])
                    startConfigs[newStart] = currStartMoveList
                    startNextQueue.append(newStart)
                    if newStart in endConfigs:
                        intersect = (set(startConfigs.keys())).intersection(set(endConfigs.keys()))
                        endList = (endConfigs[tuple(intersect)[0]])
                        endList.reverse()
                        print(endList)
                        return startConfigs[tuple(intersect)[0]] + endList

        startQueue = startNextQueue

        endNextQueue = []
        for pos in endQueue:
            for move in range(6):
                # From end node
                currEndMoveList = endConfigs[pos]
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
                        print(endList)
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