import heapq
from .core import CellState, Coord, Direction, MoveAction, BOARD_N

DIRECTION = [
    Direction.Up,
    Direction.UpLeft,
    Direction.UpRight,
    Direction.Left,
    Direction.Right,
]

def a_star_search(board:dict[Coord, CellState]):
    goals = get_goals(board) 
    red =  [cord for cord, state in board.items() if state == CellState.RED][0]
    h = calculate_h(board)
    distance = {red: 0}
    queue = []
    
    heapq.heappush(queue, (0, 0, red))
    
    while queue:
        _, curr_cost, curr_pos = heapq.heappop(queue)
        
        if curr_pos in goals:
            return 

        if curr_pos not in distance or distance[curr_pos] > curr_cost:
            distance[curr_pos] = curr_cost

            for move in get_valid_moves(board, curr_pos):
                next_pos, dir = move.coord, move._directions 
                next_cost = curr_cost + 1
                f = next_cost + h[next_pos] 
                heapq.heappush(queue, (f, next_cost, next_pos))

    return None  
        

def get_valid_moves(board, red):
    valid_moves = []

    for dir in DIRECTION:
        move = red + dir
        if move in board and board[move] == CellState.LILY_PAD:
            valid_moves.append(MoveAction(move, dir))
        
    for dest, paths in get_cross_jumps(red, [], board, {}).items():
        for path in paths:
            valid_moves.append(MoveAction(dest, path))

    return valid_moves
        
def get_cross_jumps(curr_pos, visited, board, result):
    for dir in DIRECTION:
        if (curr_pos + dir) in board and board[curr_pos + dir] == CellState.BLUE:
            dest = curr_pos + 2 * dir 
            if (dest in board and 
                board[dest] == CellState.LILY_PAD and
                dest not in visited):

                visited.append(dest)
                
                if dest not in result:
                    result[dest] = []
                result[dest].append(visited[:])

                get_cross_jumps(dest, visited, board, result)
                visited.pop()

    return result 
                
def calculate_h(board:dict[Coord, CellState]) -> dict[Coord, int]:
    man_distance = {}
    lily_pads = get_lily_pads(board)
    goals = get_goals(board)

    for pad in lily_pads:
        if pad.r != BOARD_N - 1:
            distances = []
            for goal in goals:
                distances.append(abs(pad.c - goal.c) + abs(pad.r - goal.r))

            man_distance[pad] = min(distances)

    return man_distance 

def get_lily_pads(board:dict[Coord, CellState]):
    return [cord for cord, state in board.items() if state == CellState.LILY_PAD] 

def get_goals(board:dict[Coord, CellState]): 
   return [cord for cord in get_lily_pads(board) if cord.r == BOARD_N -1] 




