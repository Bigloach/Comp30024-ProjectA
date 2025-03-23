import heapq
from .core import CellState, Coord, Direction, MoveAction, BOARD_N

def a_star_search(board:dict[Coord, CellState]):
    goals = get_goals(board) 
    red =  [cord for cord, state in board.items() if state == CellState.RED][0]
    h = calculate_h(board)
    distance = {red: 0}
    visited = set()
    min_path = []
    queue = []
    
    heapq.heappush(queue, (0, red))
    
    while queue:
        curr_cost, curr_pos = heapq.heappop(queue)
        
        if curr_pos in goals:
            return 

        if curr_pos in visited:
            continue
        
        visited.add(curr_pos)

        valid_moves = get_valid_moves
        for move in valid_moves:
            next_pos, dir = move.coord, move._directions 
            f = curr_cost + h[next_pos] + 1
            if type(dir) == list:
                
                
            heapq.heappush(queue, (f, next_pos))
        
        

def get_valid_moves(board, red):
    valid_moves = []
    is_cross = True
    for dir in Direction:
        move = red + dir
        if move in board and board[move] == CellState.LILY_PAD:
            valid_moves.append(MoveAction(move, dir))
        
        if move in board and board[move] == CellState.BLUE:
            cross_move = move + dir
            if cross_move in board and board[cross_move] == CellState.LILY_PAD:
                dir_list = []
                dir_list.append(dir)
                valid_moves.append((MoveAction(cross_move, dir_list)))
    
    return valid_moves

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




