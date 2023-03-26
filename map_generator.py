from hex import Hex
import random

DIRECTIONS = [(0, -1, 1), (1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1)]

class Walker:
    
    def __init__(self):
        self.location = (0, 0, 0)
    
    def step(self, map) -> bool:
        rand_direction = DIRECTIONS[random.randint(0, 5)]
        self.location = tuple(x + y for x, y in zip(self.location, rand_direction))

        if self.location not in map.keys():
            self.location = (0, 0, 0)
            return False

        if map[self.location].type == "stone":
            map[self.location] = Hex("grass")
            return True
        else:
            return False

def generate_map(radius: int = 10, num_lands: int = 80, num_walkers: int = 10) -> dict[tuple[int, int, int], Hex]:
    # Generate a map of all stone
    map = {}

    for q in range(-radius, radius + 1):
        for r in range(-radius, radius + 1):
            for s in range(-radius, radius + 1):
                if q + r + s == 0:
                    map[(q, r, s)] = Hex("stone")
    
    # Set center tile to grass
    map[(0, 0, 0)] = Hex("grass")

    # Use random walkers to generate grass tiles
    walkers = [Walker()] * num_walkers

    lands_placed = 0
    while lands_placed < num_lands:
        for walker in walkers:
            if walker.step(map):
                lands_placed += 1
                if lands_placed == num_lands:
                    break
    
    return map