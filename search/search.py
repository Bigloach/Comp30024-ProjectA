# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part A: Single Player Freckers

import heapq
from .core import CellState, Coord, Direction, MoveAction, BOARD_N

DIRECTION = [
    Direction.Down,
    Direction.DownLeft,
    Direction.DownRight,
    Direction.Left,
    Direction.Right,
]

COST = 1

def a_star_search(board:dict[Coord, CellState]) -> list[MoveAction] | None:
    """
    Using A* search to find the shortest path to the goal state 
    in the board, storing the parent node the directions of each 
    node in a path dict
    
    If a goal state is reached, reverse the path dict to 
    return the final path as a list of MoveActions
    """

    goals = get_goals(board) 
    red =  [cord for cord, state in board.items() if state == CellState.RED][0]
    herustic = calculate_herustic(board)
    distance = {red: 0}
    path = {red: None}
    queue = []
    
    heapq.heappush(queue, (0, 0, red))
    
    while queue:
        _, curr_cost, curr_pos = heapq.heappop(queue)
        
        if curr_pos in goals:
            result = []
            while path[curr_pos]: 
                result.append(path[curr_pos])
                curr_pos = path[curr_pos].coord

            return result[::-1] 

        for move in get_valid_moves(board, goals, curr_pos):
            next_pos, dir = move.coord, move._directions 
            next_cost = curr_cost + COST

            if next_pos not in distance or distance[next_pos] > next_cost:
                distance[next_pos] = next_cost
                path[next_pos] = MoveAction(curr_pos, dir)
                f = next_cost + herustic[next_pos] 
                heapq.heappush(queue, (f, next_cost, next_pos))

    return None  
        

def get_valid_moves(board, goals, red) -> list[MoveAction]:
    """
    Retrive all possible positions that the current red frog
    can move to, including one step jump and seris of cross jumps
    """
    valid_moves = []

    for dir in DIRECTION:
        if (0 <= (red.r + dir.r) < BOARD_N) and (0 <= (red .c + dir.c) < BOARD_N) \
            and (red + dir) in board and board[red + dir] == CellState.LILY_PAD:
            valid_moves.append(MoveAction(red + dir, dir))
        
    for dest, paths in get_cross_jumps(red, [], [], board, goals, {}).items():
        for path in paths:
            valid_moves.append(MoveAction(dest, path))

    return valid_moves
        
def get_cross_jumps(
        curr_pos, visited, path, board, goals, result
        ) -> dict[Coord, list[Direction]]:
    """
    Using dfs and backtracking to get all the possible cross jump paths 
    from the current position

    Backtrack to explore every possible path after visiting
    the neighbours of current position
    """
    for dir in DIRECTION:
        if  (0 <= (curr_pos.r + dir.r) < BOARD_N) and (0 <= (curr_pos.c + dir.c) < BOARD_N) \
              and (curr_pos + dir) in board and board[curr_pos + dir] == CellState.BLUE:
            move = curr_pos + dir 
            if (0 <= (move.r + dir.r) < BOARD_N) and (0 <= (move.c + dir.c) < BOARD_N) and \
                (move + dir) in board and board[move + dir] == CellState.LILY_PAD:
                
                dest = move + dir

                if dest not in visited:
                    visited.append(dest)
                    path.append(dir)
                    
                    if dest not in result:
                        result[dest] = []
                    result[dest].append(path[:])


                    get_cross_jumps(dest, visited, path, board, goals, result)
                    visited.pop()
                    path.pop()

    return result 
                
def calculate_herustic(board:dict[Coord, CellState]) -> dict[Coord, int]:
    """
    Calculate the herustic, which is 
    the minmum manhattan distance of every Lily Pads to the 
    target Lily Pads among the last row of the board
    """
    manhattan_distance = {}
    lily_pads = get_lily_pads(board)
    goals = get_goals(board)

    for pad in lily_pads:
        distances = []
        for goal in goals:
            distances.append(abs(pad.c - goal.c) + abs(pad.r - goal.r))

        manhattan_distance[pad] = min(distances)

    return manhattan_distance 

def get_lily_pads(board:dict[Coord, CellState]):
    return [cord for cord, state in board.items() if state == CellState.LILY_PAD] 

def get_goals(board:dict[Coord, CellState]): 
   return {cord for cord in get_lily_pads(board) if cord.r == BOARD_N -1}




