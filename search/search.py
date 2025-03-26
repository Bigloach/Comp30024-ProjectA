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
    valid_moves = []

    for dir in DIRECTION:
        move = red + dir
        if move in board and board[move] == CellState.LILY_PAD:
            valid_moves.append(MoveAction(move, dir))
        
    for dest, paths in get_cross_jumps(red, [], [], board, goals, {}).items():
        for path in paths:
            valid_moves.append(MoveAction(dest, path))

    return valid_moves
        
def get_cross_jumps(
        curr_pos, visited, path, board, goals, result
        ) -> dict[Coord, list[Direction]]:
    for dir in DIRECTION:
        if (curr_pos + dir) in board and board[curr_pos + dir] == CellState.BLUE:
            dest = curr_pos + dir + dir 
            if (dest in board and 
                board[dest] == CellState.LILY_PAD and
                dest not in visited):

                visited.append(dest)
                path.append(dir)
                
                if dest not in result:
                    result[dest] = []
                result[dest].append(path[:])

                if dest in goals:
                    return result

                get_cross_jumps(dest, visited, path, board, goals, result)
                visited.pop()
                path.pop()

    return result 
                
def calculate_herustic(board:dict[Coord, CellState]) -> dict[Coord, int]:
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




