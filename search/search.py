import heapq
from .core import CellState, Coord, Direction, MoveAction, BOARD_N

# def valid_jump(red, pos):
#     for dir in Direction:
#         if red + dir == pos:
#             return True
for dir in Direction:
    if board[red + dir] == CellState.LILY_PAD:
        valid_pos = board[red + dir] 
    if board[red + dir] == CellState.BLUE:
        if board[red + dir + dir] == CellState.LILY_PAD:
            valid_pos = board[red + dir + dir]

def calculate_h(board:dict[Coord, CellState]):
    man_distance = {}
    lily_pads = get_lily_pads(board)
    goals = get_goals(board)
    for pad in lily_pads:
        distances = []
        if (pad.r != BOARD_N - 1):
            for goal in goals:
                distances.append(abs(pad.c - goal.c) + abs(pad.r - goal.r))
        if distances:
            man_distance[pad] = min(distances)
    return man_distance 

def get_lily_pads(board:dict[Coord, CellState]):
    return [cord for cord, state in board.items() if state == CellState.LILY_PAD] 

def get_goals(board:dict[Coord, CellState]): 
   return [cord for cord in get_lily_pads(board) if cord.r == BOARD_N -1] 




