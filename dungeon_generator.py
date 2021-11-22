import random
from collections import deque
from enum import Enum
from typing import List

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

def opposite(direction: Direction):
    match direction:
        case Direction.LEFT: return Direction.RIGHT
        case Direction.RIGHT: return Direction.LEFT
        case Direction.UP: return Direction.DOWN
        case Direction.DOWN: return Direction.UP

class CC():
    def __init__(self, rooms, idx):
        self.rooms, self.idx = rooms, idx
        self.adj = set()

class Corridor():
    def __init__(self, r1, r2, type):
        self.rooms, self.type = (r1, r2), type

class Room():
    def __init__(self):
        self.left, self.right, self.up, self.down = False, False, False, False
        self.corridors = {}
        self.cc: int | None = None

    def __getitem__(self, index: Direction):
        match index:
            case Direction.LEFT:
                return self.left
            case Direction.RIGHT:
                return self.right
            case Direction.UP:
                return self.up
            case Direction.DOWN:
                return self.down

    def __setitem__(self, index: Direction, value: bool):
        match index:
            case Direction.LEFT:
                self.left = value
            case Direction.RIGHT:
                self.right = value
            case Direction.UP:
                self.up = value
            case Direction.DOWN:
                self.down = value

    def __str__(self):
        return "(" + " ".join([direction.name if self[direction] else "XXXX" for direction in Direction]) + ")"

class Dungeon():
    '''
    w, the number of rooms per row
    h, the number of rooms per column
    p_corridor, probability of placing a corridor for non-solution rooms
    p_door, probability of placing a door
    num_types, number of obstacle types
    '''
    def __init__(self, w, h, p_corridor, p_door, num_types):
        assert(w > 3 < h)
        assert(0 <= p_corridor < 1 and 0 <= p_door < 1)
        assert(num_types > 0)
        self.w, self.h, self.p_corridor, self.p_door, self.num_types = w, h, p_corridor, p_door, num_types
        self.start = (h - 1, random.randint(0, w - 1))
        self.end = None
        self.board: List[List[Room | None]] = [[None] * w for _ in range(h)]
        self.corridors = set()
        self.obstacles = set()
        self.ccs = []
        self.start_cc_idx = None
        self.end_cc_idx = None
        self.build_solution()
        self.fill_empty_rooms()
        self.fix_border_rooms()
        self.insert_corridors()
        self.place_artifacts()

    def build_solution(self):
        r, c = self.start
        room = self.board[r][c] = Room()
        room[Direction.LEFT], room[Direction.RIGHT] = True, True
        while (self.end is not None):
            exits = [Direction.UP]
            if c != 0 and self.board[r][c - 1] is None:
                exits.append(Direction.LEFT)
            if c != self.w - 1 and self.board[r][c + 1] is None:
                exits.append(Direction.RIGHT)
            direction = random.choice(exits)
            if r == 0 and direction == Direction.UP:
                self.end = r, c
            else:
                match direction:
                    case Direction.UP:
                        room[Direction.UP] = True
                        r += 1
                    case Direction.LEFT: c -= 1
                    case Direction.RIGHT: c += 1
                room = self.board[r][c] = Room()
                room[Direction.LEFT], room[Direction.RIGHT] = True, True
                if direction is Direction.UP: room[Direction.DOWN] = True

    def fill_empty_rooms(self):
        for r in range(self.h):
            for c in range(self.w):
                if (self.board[r][c] is not None): continue
                room = self.board[r][c] = Room()
                for direction in Direction:
                    if adj := self.get_adj_room(r, c, direction):
                        room[opposite(direction)] = True
                    if not room[direction] and adj is None:
                        room[direction] = random.random() < self.p_corridor

    def fix_border_rooms(self):
        for room in self.board[0]:
            assert(room is not None)
            room[Direction.UP] = False
        for room in self.board[-1]:
            assert(room is not None)
            room[Direction.DOWN] = False
        for row in self.board:
            assert(row[0] is not None)
            row[0][Direction.LEFT] = False
            assert((end := row[-1]) is not None)
            end[Direction.RIGHT] = False

    '''
    Insert corridors, where a corridor is either obstacle-free (type = 0) or contains an obstacle (type > 0)
    '''
    def insert_corridors(self):
        for r in range(self.h):
            for c in range(self.w):
                room = self.board[r][c]
                assert(room is not None)
                for direction in (Direction.DOWN, Direction.RIGHT):
                    if room[direction]:
                        adj = self.get_adj_room(r, c, direction)
                        assert(adj)
                        corridor = Corridor(room, adj, random.randint(1, self.num_types) if random.random() < self.p_door else 0)
                        room.corridors[direction] = corridor
                        adj.corridors[opposite(direction)] = corridor
                        self.corridors.add(corridor)
                        if corridor.type > 0:
                            self.obstacles.add(corridor)

    def place_artifacts(self):
        idx = 0
        visited = set()
        for r in range(self.h):
            for c in range(self.w):
                if (r, c) in visited: continue
                cc = {(r, c)}
                visited.add((r, c))
                queue = deque([(r, c)])
                while queue:
                    r, c = queue.popleft()
                    room = self.board[r][c]
                    assert(room is not None)
                    room.cc = idx
                    for direction, corridor in room.corridors.items():
                        if corridor.type > 0: continue
                        adj = self.get_adj_room(r, c, direction)
                        if adj not in visited:
                            visited.add(adj)
                            queue.append(self.get_adj_coords(r, c, direction))
                if self.start in cc: self.start_cc_idx = idx
                if self.end in cc: self.end_cc_idx = idx
                self.ccs.append(CC(cc, idx))
                idx += 1
        for obstacle in self.obstacles:
            cc_1, cc_2 = [self.ccs[r.cc] for r in obstacle.rooms]
            cc_1.adj.add((cc_2, obstacle.type))
            cc_2.adj.add((cc_1, obstacle.type))
        #TODO: run BFS on graph of CCs to find shortest path from
        # source cc to destination cc and  place corresponding artifacts

    def in_bounds(self, r, c):
        return 0 <= r < self.h and 0 <= c < self.w
    
    def get_adj_room(self, r, c, direction: Direction):
        match direction:
            case Direction.LEFT: c -= 1
            case Direction.RIGHT: c += 1
            case Direction.UP: r -= 1
            case Direction.DOWN: r += 1
        return False if not self.in_bounds(r, c) else self.board[r][c]

    def get_adj_coords(self, r, c, direction: Direction):
        match direction:
            case Direction.LEFT: c -= 1
            case Direction.RIGHT: c += 1
            case Direction.UP: r -= 1
            case Direction.DOWN: r += 1
        return (r, c)

    # def __str__(self):
    #     ...
