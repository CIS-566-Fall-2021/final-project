import random
from typing import List, Tuple
from dungeon_generator import Direction

class TiledRoom:
    
    def __init__(self, room: List[List[str]]) -> None:
        self.room: List[List[str]] = room
        self.free_tiles: List[Tuple(int, int)] = [(row, col) for row in range(len(self.room)) for col in range(len(self.room[row])) if self.room[row][col] == '_']
        self.artifact: bool = False

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
                    self.room[row][col] = '_' if obstacle == 0 else obstacle
                    return True
        return False
    
    def place_artifact(self, artifact: int):
        row, col = random.choice(self.free_tiles)
        self.room[row][col] = artifact
        self.artifact = True

class PresetRooms:
    '''
    Preset rooms are of size 5x5 and therefore have at most 3x3 of room tiles since the exterior must be walls
    '''
    def __init__(self) -> None:
        self.rooms = {}
        self.rooms['L'] = [
            [
            ['x', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'x'],
            ['<', '_', '_', '_', 'x'],
            ['x', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'x'],],
        ]
        self.rooms['R'] = [
            [
            ['x', 'x', 'x', 'x', 'x'],
            ['x', '_', '_', 'x', 'x'],
            ['x', '_', '_', '_', '>'],
            ['x', '_', '_', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'x'],],
        ]
        self.rooms['LR'] = [
            [
            ['x', 'x', 'x', 'x', 'x'],
            ['x', '_', '_', '_', 'x'],
            ['<', '_', 'x', '_', '>'],
            ['x', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'x'],],
        ]
        self.rooms['U'] = [
            [
            ['x', 'x', '^', 'x', 'x'],
            ['x', 'x', '_', '_', 'x'],
            ['x', 'x', 'x', '_', 'x'],
            ['x', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'x'],],
        ]
        self.rooms['LU'] = [
            [
            ['x', 'x', '^', 'x', 'x'],
            ['x', 'x', '_', '_', 'x'],
            ['<', '_', 'x', '_', 'x'],
            ['x', '_', '_', '_', 'x'],
            ['x', 'x', 'x', 'x', 'x'],],
        ]
        self.rooms['RU'] = [
            [
            ['x', 'x', '^', 'x', 'x'],
            ['x', '_', '_', 'x', 'x'],
            ['x', '_', '_', '_', '>'],
            ['x', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'x'],],
        ]
        self.rooms['LRU'] = [
            [
            ['x', 'x', '^', 'x', 'x'],
            ['x', '_', '_', '_', 'x'],
            ['<', '_', '_', '_', '>'],
            ['x', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'x'],],
        ]
        self.rooms['D'] = [
            [
            ['x', 'x', 'x', 'x', 'x'],
            ['x', '_', '_', '_', 'x'],
            ['x', '_', '_', '_', 'x'],
            ['x', 'x', '_', 'x', 'x'],
            ['x', 'x', '|', 'x', 'x'],],
        ]
        self.rooms['LD'] = [
            [
            ['x', 'x', 'x', 'x', 'x'],
            ['x', '_', '_', '_', 'x'],
            ['<', '_', 'x', '_', 'x'],
            ['x', 'x', '_', '_', 'x'],
            ['x', 'x', '|', 'x', 'x'],],
        ]
        self.rooms['RD'] = [
            [
            ['x', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', '_', 'x'],
            ['x', 'x', 'x', '_', '>'],
            ['x', 'x', '_', '_', 'x'],
            ['x', 'x', '|', 'x', 'x'],],
        ]
        self.rooms['LRD'] = [
            [
            ['x', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'x'],
            ['<', '_', 'x', '_', '>'],
            ['x', '_', '_', '_', 'x'],
            ['x', 'x', '|', 'x', 'x'],],
        ]
        self.rooms['UD'] = [
            [
            ['x', 'x', '^', 'x', 'x'],
            ['x', 'x', '_', 'x', 'x'],
            ['x', 'x', '_', 'x', 'x'],
            ['x', 'x', '_', 'x', 'x'],
            ['x', 'x', '|', 'x', 'x'],],
        ]
        self.rooms['LUD'] = [
            [
            ['x', 'x', '^', 'x', 'x'],
            ['x', 'x', '_', 'x', 'x'],
            ['<', '_', '_', 'x', 'x'],
            ['x', 'x', '_', 'x', 'x'],
            ['x', 'x', '|', 'x', 'x'],],
        ]
        self.rooms['RUD'] = [
            [
            ['x', 'x', '^', 'x', 'x'],
            ['x', 'x', '_', '_', 'x'],
            ['x', 'x', '_', '_', '>'],
            ['x', 'x', '_', '_', 'x'],
            ['x', 'x', '|', 'x', 'x'],],
        ]
        self.rooms['LRUD'] = [
            [
            ['x', 'x', '^', 'x', 'x'],
            ['x', '_', '_', '_', 'x'],
            ['<', '_', 'x', '_', '>'],
            ['x', '_', '_', '_', 'x'],
            ['x', 'x', '|', 'x', 'x'],],
        ]

    def get_room(self, type: str) -> TiledRoom:
        return TiledRoom(random.choice(self.rooms[type]))

test = PresetRooms()
room = test.get_room("L")
print(room)
print(test.get_room("L").free_tiles)
print(room.place_obstacle(0, Direction.LEFT))
print(room)
print(room.place_artifact(1))
print(room)