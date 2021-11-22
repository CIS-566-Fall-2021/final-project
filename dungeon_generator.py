import random
from enum import Enum

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class Room():
    def __init__(self):
        self.left, self.right, self.up, self.down = False, False, False, False

    def +
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
        self.w, self.h, self.p_corridor, self.p_door, self.num_types = w, h, p_corridor, p_door, num_types
        self.start = (h - 1, random.randint(0, w - 1))
        self.end = None
        self.board = [[None] * w for _ in range(h)]

        self.build_solution()
        self.fill_empty_rooms()
        self.fix_border_rooms()
        self.place_obstacles()
        self.place_artifacts()

    def build_solution(self):
        r, c = self.start
        room = self.board[r][c] = Room()
        room.left, room.right = True, True

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
                        room.up = True
                        r += 1
                    case Direction.LEFT:
                        c -= 1
                    case Direction.RIGHT:
                        c += 1
                room = self.board[r][c] = Room()
                room.left, room.right = True, True
                if direction is Direction.UP: room.down = True

    def fill_empty_rooms(self):
        for r in range(self.h):
            for c in range(self.w):
                if (self.board[r][c] is not None): continue
                room = self.board[r][c] = Room()
                if self.in_bounds(r, c - 1) and self.board[r][c - 1].right:
                    room.left = True
                if self.in_bounds(r, c + 1) and self.board[r][c + 1].left:
                    room.right = True
                if self.in_bounds(r - 1, c) and self.board[r - 1][c].down:
                    room.up = True
                if self.in_bounds(r + 1, c) and self.board[r + 1][c].up:
                    room.down = True

                for dir in Direction:


    def fix_border_rooms(self):
        ...

    def place_obstacles(self):
        ...

    def place_artifacts(self):
        ...

    def in_bounds(self, r, c):
        return 0 <= r < self.h and 0 <= c < self.w

    def __str__(self):
        ...
