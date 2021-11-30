import random
from enum import Enum
from collections import deque
from collections import defaultdict
from typing import Dict, List, Set, Tuple
from copy import deepcopy

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
    def __init__(self, rooms: Set['Room'], idx: int):
        self.rooms: Set[Room] = rooms
        self.idx: int = idx
        self.adj: Dict[CC, Set[int]] = defaultdict(lambda: set())
        self.parent: CC | None = None
        self.artifacts: Set[int] = set()
    
    def get_path(self) -> List['CC']:
        curr = self
        path = deque()
        while curr is not None:
            path.appendleft(curr)
            curr = curr.parent
        return list(path)

class Corridor():
    def __init__(self, r1: 'Room', r2: 'Room', type: int):
        self.rooms: Tuple[Room, Room] = (r1, r2) 
        self.type: int = type

class TiledRoom:
    def __init__(self, room: List[List[str]]) -> None:
        self.room: List[List[str]] = deepcopy(room)
        self.free_tiles: List[Tuple(int, int)] = [(row, col) for row in range(len(self.room)) for col in range(len(self.room[row])) if self.room[row][col] == '_']

    def __repr__(self) -> str:
        return self.room.__repr__()
    
    def place_obstacle(self, obstacle: int, direction: Direction):
        match direction:
            case Direction.LEFT:
                exit_char = '<'
            case Direction.RIGHT:
                exit_char = '>'
            case Direction.UP:
                exit_char = '^'
            case Direction.DOWN:
                exit_char = '|'
            case _:
                return False
        
        for row in range(len(self.room)):
            for col in range(len(self.room[row])):
                if self.room[row][col] == exit_char:
                    self.room[row][col] = '_' if obstacle == 0 else str(obstacle)
                    return True
        return False
    
    def place_artifact(self, artifact: int | str):
        row, col = random.choice(self.free_tiles)
        self.room[row][col] = str(artifact)
        self.free_tiles.remove((row, col))

class PresetRooms:
    '''
    Preset rooms are of size 5x5 and therefore have at most 3x3 of room tiles since the exterior must be walls
    '''
    def __init__(self) -> None:
        self.rooms = {
            'L' : [
                [
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],
                ['<', '_', '_', '_', 'x'],
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],],
            ],
            'R' : [
                [
                ['x', 'x', 'x', 'x', 'x'],
                ['x', '_', '_', 'x', 'x'],
                ['x', '_', '_', '_', '>'],
                ['x', '_', '_', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],],
            ],
            'LR' : [
                [
                ['x', 'x', 'x', 'x', 'x'],
                ['x', '_', '_', '_', 'x'],
                ['<', '_', 'x', '_', '>'],
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],],
            ],
            'U' : [
                [
                ['x', 'x', '^', 'x', 'x'],
                ['x', 'x', '_', '_', 'x'],
                ['x', 'x', 'x', '_', 'x'],
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],],
            ],
            'LU' : [
                [
                ['x', 'x', '^', 'x', 'x'],
                ['x', 'x', '_', '_', 'x'],
                ['<', '_', 'x', '_', 'x'],
                ['x', '_', '_', '_', 'x'],
                ['x', 'x', 'x', 'x', 'x'],],
            ],
            'RU' : [
                [
                ['x', 'x', '^', 'x', 'x'],
                ['x', '_', '_', 'x', 'x'],
                ['x', '_', '_', '_', '>'],
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],],
            ],
            'LRU' : [
                [
                ['x', 'x', '^', 'x', 'x'],
                ['x', '_', '_', '_', 'x'],
                ['<', '_', '_', '_', '>'],
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],],
            ],
            'D' : [
                [
                ['x', 'x', 'x', 'x', 'x'],
                ['x', '_', '_', '_', 'x'],
                ['x', '_', '_', '_', 'x'],
                ['x', 'x', '_', 'x', 'x'],
                ['x', 'x', '|', 'x', 'x'],],
            ],
            'LD' : [
                [
                ['x', 'x', 'x', 'x', 'x'],
                ['x', '_', '_', '_', 'x'],
                ['<', '_', 'x', '_', 'x'],
                ['x', 'x', '_', '_', 'x'],
                ['x', 'x', '|', 'x', 'x'],],
            ],
            'RD' : [
                [
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', '_', 'x'],
                ['x', 'x', 'x', '_', '>'],
                ['x', 'x', '_', '_', 'x'],
                ['x', 'x', '|', 'x', 'x'],],
            ],
            'LRD' : [
                [
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],
                ['<', '_', 'x', '_', '>'],
                ['x', '_', '_', '_', 'x'],
                ['x', 'x', '|', 'x', 'x'],],
            ],
            'UD' : [
                [
                ['x', 'x', '^', 'x', 'x'],
                ['x', 'x', '_', 'x', 'x'],
                ['x', 'x', '_', 'x', 'x'],
                ['x', 'x', '_', 'x', 'x'],
                ['x', 'x', '|', 'x', 'x'],],
            ],
            'LUD' : [
                [
                ['x', 'x', '^', 'x', 'x'],
                ['x', 'x', '_', 'x', 'x'],
                ['<', '_', '_', 'x', 'x'],
                ['x', 'x', '_', 'x', 'x'],
                ['x', 'x', '|', 'x', 'x'],],
            ],
            'RUD' : [
                [
                ['x', 'x', '^', 'x', 'x'],
                ['x', 'x', '_', '_', 'x'],
                ['x', 'x', '_', '_', '>'],
                ['x', 'x', '_', '_', 'x'],
                ['x', 'x', '|', 'x', 'x'],],
            ],
            'LRUD' : [
                [
                ['x', 'x', '^', 'x', 'x'],
                ['x', '_', '_', '_', 'x'],
                ['<', '_', 'x', '_', '>'],
                ['x', '_', '_', '_', 'x'],
                ['x', 'x', '|', 'x', 'x'],],
            ]
        }
    
    def get_room(self, type: str) -> TiledRoom:
        return TiledRoom(random.choice(self.rooms[type]))

class Room():
    presets = {
            '' : [
                [
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],],
            ],
            'L' : [
                [
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],
                ['<', '_', '_', '_', 'x'],
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],],
            ],
            'R' : [
                [
                ['x', 'x', 'x', 'x', 'x'],
                ['x', '_', '_', 'x', 'x'],
                ['x', '_', '_', '_', '>'],
                ['x', '_', '_', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],],
            ],
            'LR' : [
                [
                ['x', 'x', 'x', 'x', 'x'],
                ['x', '_', '_', '_', 'x'],
                ['<', '_', 'x', '_', '>'],
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],],
            ],
            'U' : [
                [
                ['x', 'x', '^', 'x', 'x'],
                ['x', 'x', '_', '_', 'x'],
                ['x', 'x', 'x', '_', 'x'],
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],],
            ],
            'LU' : [
                [
                ['x', 'x', '^', 'x', 'x'],
                ['x', 'x', '_', '_', 'x'],
                ['<', '_', 'x', '_', 'x'],
                ['x', '_', '_', '_', 'x'],
                ['x', 'x', 'x', 'x', 'x'],],
            ],
            'RU' : [
                [
                ['x', 'x', '^', 'x', 'x'],
                ['x', '_', '_', 'x', 'x'],
                ['x', '_', '_', '_', '>'],
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],],
            ],
            'LRU' : [
                [
                ['x', 'x', '^', 'x', 'x'],
                ['x', '_', '_', '_', 'x'],
                ['<', '_', '_', '_', '>'],
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],],
            ],
            'D' : [
                [
                ['x', 'x', 'x', 'x', 'x'],
                ['x', '_', '_', '_', 'x'],
                ['x', '_', '_', '_', 'x'],
                ['x', 'x', '_', 'x', 'x'],
                ['x', 'x', '|', 'x', 'x'],],
            ],
            'LD' : [
                [
                ['x', 'x', 'x', 'x', 'x'],
                ['x', '_', '_', '_', 'x'],
                ['<', '_', 'x', '_', 'x'],
                ['x', 'x', '_', '_', 'x'],
                ['x', 'x', '|', 'x', 'x'],],
            ],
            'RD' : [
                [
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', '_', 'x'],
                ['x', 'x', 'x', '_', '>'],
                ['x', 'x', '_', '_', 'x'],
                ['x', 'x', '|', 'x', 'x'],],
            ],
            'LRD' : [
                [
                ['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', 'x'],
                ['<', '_', 'x', '_', '>'],
                ['x', '_', '_', '_', 'x'],
                ['x', 'x', '|', 'x', 'x'],],
            ],
            'UD' : [
                [
                ['x', 'x', '^', 'x', 'x'],
                ['x', 'x', '_', 'x', 'x'],
                ['x', 'x', '_', 'x', 'x'],
                ['x', 'x', '_', 'x', 'x'],
                ['x', 'x', '|', 'x', 'x'],],
            ],
            'LUD' : [
                [
                ['x', 'x', '^', 'x', 'x'],
                ['x', 'x', '_', 'x', 'x'],
                ['<', '_', '_', 'x', 'x'],
                ['x', 'x', '_', 'x', 'x'],
                ['x', 'x', '|', 'x', 'x'],],
            ],
            'RUD' : [
                [
                ['x', 'x', '^', 'x', 'x'],
                ['x', 'x', '_', '_', 'x'],
                ['x', 'x', '_', '_', '>'],
                ['x', 'x', '_', '_', 'x'],
                ['x', 'x', '|', 'x', 'x'],],
            ],
            'LRUD' : [
                [
                ['x', 'x', '^', 'x', 'x'],
                ['x', '_', '_', '_', 'x'],
                ['<', '_', 'x', '_', '>'],
                ['x', '_', '_', '_', 'x'],
                ['x', 'x', '|', 'x', 'x'],],
            ]
        }

    def __init__(self):
        self.left: bool = False
        self.right: bool = False
        self.up: bool = False
        self.down: bool = False
        self.corridors: Dict[Direction, Corridor] = {}
        self.cc: int = None #type: ignore
        self.artifact: int | None = None

        self.start = False
        self.end = False

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

    def get_dirs(self) -> str:
        def get_str(d: str):
            match d:
                case 'L': return 'L' if self.left else ''
                case 'R': return 'R' if self.right else ''
                case 'U': return 'U' if self.up else ''
                case 'D': return 'D' if self.down else ''
        return "".join([get_str(d) for d in 'LRUD'])

    def __repr__(self):
        return "(" + " ".join([direction.name if self[direction] else "XXXX" for direction in Direction]) + ")"
    
    def get_txt_repr(self):
        rooms = Room.presets[self.get_dirs()]
        
        tiled_room = TiledRoom(random.choice(rooms))
        for direction, corridor in self.corridors.items():
            tiled_room.place_obstacle(corridor.type, direction)
        if self.artifact:
            tiled_room.place_artifact(self.artifact)
        if self.start:
            tiled_room.place_artifact('*')
        if self.end:
            tiled_room.place_artifact('$')

        tup = tuple(["".join(row) + " " for row in tiled_room.room])
        return tup

class Dungeon():
    '''
    w, the number of rooms per row
    h, the number of rooms per column
    p_corridor, probability of placing a corridor for non-solution rooms
    p_door, probability of placing a door
    num_types, number of obstacle types
    '''
    def __init__(self, w: int, h: int, p_corridor: int | float, p_door: int | float, num_types: int):
        assert(w >= 3 <= h)
        assert(0 <= p_corridor <= 1 and 0 <= p_door <= 1)
        assert(num_types > 0)
        self.w: int = w
        self.h: int = h
        self.p_corridor: float | int = p_corridor
        self.p_door: float | int = p_door
        self.num_types: int = num_types
        self.start: Tuple[int, int] = (h - 1, random.randint(0, w - 1))
        self.end: Tuple[int, int] = None #type: ignore
        self.board: List[List[Room]] = [[None] * w for _ in range(h)] #type: ignore
        self.corridors: Set[Corridor] = set()
        self.obstacles: Set[Corridor] = set()
        self.ccs: List[CC] = []
        self.start_cc_idx: int = None #type: ignore
        self.end_cc_idx: int = None #type: ignore
        self.build_solution()
        self.fill_empty_rooms()
        self.fix_border_rooms()
        self.insert_corridors()
        self.find_connected_components()
        self.place_artifacts()

        self.board[self.start[0]][self.start[1]].start = True
        self.board[self.end[0]][self.end[1]].end = True

    def build_solution(self):
        r, c = self.start
        room = self.board[r][c] = Room()
        room[Direction.LEFT], room[Direction.RIGHT] = True, True
        while (self.end is None):
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
                        r -= 1
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
                    if (adj := self.get_adj_room(r, c, direction)) and adj[opposite(direction)]:
                        room[direction] = True
                    if not room[direction] and adj is None:
                        room[direction] = random.random() < self.p_corridor

    def fix_border_rooms(self):
        for room in self.board[0]:
            room[Direction.UP] = False
        for room in self.board[-1]:
            room[Direction.DOWN] = False
        for row in self.board:
            row[0][Direction.LEFT] = False
            row[-1][Direction.RIGHT] = False

    '''
    Insert corridors, where a corridor is either obstacle-free (type = 0) or contains an obstacle (type > 0)
    '''
    def insert_corridors(self):
        for r in range(self.h):
            for c in range(self.w):
                room = self.board[r][c]
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

    def find_connected_components(self):
        idx = 0
        visited: Set[Tuple[int, int]] = set()
        for _r in range(self.h):
            for _c in range(self.w):
                if (_r, _c) == (1, 2):
                    pass
                if (_r, _c) in visited: continue
                cc = set()
                visited.add((_r, _c))
                queue = deque([(_r, _c)])
                while queue:
                    r, c = queue.popleft()
                    room = self.board[r][c]
                    room.cc = idx
                    cc.add((r, c))
                    for direction, corridor in room.corridors.items():
                        if corridor.type > 0: continue
                        nxt = self.get_adj_coords(r, c, direction)
                        if nxt not in visited:
                            visited.add(nxt)
                            queue.append(nxt)
                if self.start in cc: self.start_cc_idx = idx
                if self.end in cc: self.end_cc_idx = idx
                self.ccs.append(CC(cc, idx))
                idx += 1
        assert(len(visited) == self.w * self.h)
        for obstacle in self.obstacles:
            cc_1, cc_2 = [self.ccs[room.cc] for room in obstacle.rooms]
            cc_1.adj[cc_2].add(obstacle.type)
            cc_2.adj[cc_1].add(obstacle.type)

    def place_artifacts(self):
        curr_cc = self.ccs[self.start_cc_idx]
        visited = {curr_cc}
        queue = deque([curr_cc])
        while queue:
            curr_cc = queue.popleft()
            for neighbor in curr_cc.adj:
                if neighbor in visited: continue
                neighbor.parent = curr_cc
                visited.add(neighbor)
                queue.append(neighbor)
        path = self.ccs[self.end_cc_idx].get_path()
        assert(path[0].idx == self.start_cc_idx)
        placed_keys: Set[int] = set()
        for cc1, cc2 in zip(path, path[1:]):
            if cc1.adj[cc2].intersection(placed_keys): continue
            artifact = random.choice(list(cc1.adj[cc2]))
            placed_keys.add(artifact)
            cc1.artifacts.add(artifact)
            r, c = random.choice(list(cc1.rooms))
            room = self.board[r][c]
            room.artifact = artifact
        # TODO: Add more artifacts to the graph that have not been placed yet

    def in_bounds(self, r: int, c: int):
        return 0 <= r < self.h and 0 <= c < self.w
    
    def get_adj_room(self, r: int, c: int, direction: Direction):
        match direction:
            case Direction.LEFT: c -= 1
            case Direction.RIGHT: c += 1
            case Direction.UP: r -= 1
            case Direction.DOWN: r += 1
        return False if not self.in_bounds(r, c) else self.board[r][c]

    def get_adj_coords(self, r: int, c: int, direction: Direction):
        match direction:
            case Direction.LEFT: c -= 1
            case Direction.RIGHT: c += 1
            case Direction.UP: r -= 1
            case Direction.DOWN: r += 1
        return (r, c)

def gen_txt(dungeon: Dungeon, filename: str):
    with open(filename, 'w') as f:
        for row in dungeon.board:
            for line in zip(*(room.get_txt_repr() for room in row)):
                f.write("".join(line) + '\n')
            f.write('\n')

if __name__ == '__main__':
    random.seed(1)
    'w, h, p_corridor, p_door, num_types'
    dungeon = Dungeon(4, 4, 0.5, 0.5, 4)
    gen_txt(dungeon, 'dungeon.txt')
    print('yay')