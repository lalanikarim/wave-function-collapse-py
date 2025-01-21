import numpy as np
import random
import pygame

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 800
GRID_WIDTH, GRID_HEIGHT = 50, 50
TILE_SIZE = WIDTH // GRID_WIDTH

# Colors for each tile
COLORS = {
    'deep_water': (0, 0, 139), # Blue
    'water': (173, 216, 230),   # Light Blue
    'sand': (243, 196, 89),     # Light Brown
    'grass': (34, 139, 34),     # Green
    'tree': (34, 102, 34),      # Darker Green
    'mud': (255, 69, 0)         # Orange
}

# Define the constraints
tile_constraints = {
    'deep_water': ['deep_water', 'water'],
    'water': ['water', 'sand', 'deep_water'],
    'sand': ['water', 'grass'],
    'grass': ['mud', 'tree', 'sand'],
    'tree': ['grass', 'mud'],
    'mud': ['mud', 'grass', 'tree']
}

# Wave Function Collapse Class
class WaveFunctionCollapse:
    def __init__(self, width, height, constraints):
        self.width = width
        self.height = height
        self.constraints = constraints
        self.tile_names = list(constraints.keys())
        self.wave = np.ones((height, width, len(constraints)), dtype=bool)
        self.stack = []

    def observe(self):
        while True:
            min_entropy = float('inf')
            collapse_candidates = []
            for y in range(self.height):
                for x in range(self.width):
                    possible_tiles = np.sum(self.wave[y, x])
                    if possible_tiles == 0:
                        raise ValueError("Contradiction in the wave function!")
                    if possible_tiles == 1:
                        continue
                    if possible_tiles < min_entropy:
                        min_entropy = possible_tiles
                        collapse_candidates = [(y, x)]
                    elif possible_tiles == min_entropy:
                        collapse_candidates.append((y, x))

            if not collapse_candidates:
                break

            y, x = random.choice(collapse_candidates)
            tile_idx = np.random.choice(np.flatnonzero(self.wave[y, x]))
            self.collapse(y, x, tile_idx)

    def collapse(self, y, x, tile_idx):
        self.wave[y, x] = False
        self.wave[y, x, tile_idx] = True
        self.stack.append((y, x))
        self.propagate()

    def propagate(self):
        while self.stack:
            y, x = self.stack.pop()
            for direction in ['up', 'down', 'left', 'right']:
                ny, nx = self.get_neighbor(y, x, direction)
                if 0 <= ny < self.height and 0 <= nx < self.width:
                    current_tile_idx = np.flatnonzero(self.wave[y, x])
                    if len(current_tile_idx) == 1:
                        current_tile = self.tile_names[current_tile_idx[0]]
                        valid_neighbors = set(self.constraints[current_tile])
                        for tile_name in self.tile_names:
                            tile_idx = self.tile_names.index(tile_name)
                            if tile_name not in valid_neighbors and self.wave[ny, nx, tile_idx]:
                                self.wave[ny, nx, tile_idx] = False
                                if np.sum(self.wave[ny, nx]) == 1:
                                    new_tile_idx = np.flatnonzero(self.wave[ny, nx])
                                    self.collapse(ny, nx, new_tile_idx[0])

    def get_neighbor(self, y, x, direction):
        if direction == 'up':
            return y - 1, x
        elif direction == 'down':
            return y + 1, x
        elif direction == 'left':
            return y, x - 1
        elif direction == 'right':
            return y, x + 1

    def get_output_grid(self):
        output_grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                possible_tiles = np.flatnonzero(self.wave[y, x])
                if len(possible_tiles) != 1:
                    raise ValueError("Grid not fully collapsed!")
                row.append(self.tile_names[possible_tiles[0]])
            output_grid.append(row)
        return output_grid

    def optimize(self):
        for y in range(self.height):
            for x in range(self.width):
                possible_tiles = np.flatnonzero(self.wave[y, x])
                if len(possible_tiles) == 1:
                    current_tile_idx = possible_tiles[0]
                    current_tile = self.tile_names[current_tile_idx]
                    neighbors = [
                        self.get_neighbor(y, x, 'up'),
                        self.get_neighbor(y, x, 'down'),
                        self.get_neighbor(y, x, 'left'),
                        self.get_neighbor(y, x, 'right')
                    ]
                    surrounding_tiles = set()
                    for ny, nx in neighbors:
                        if 0 <= ny < self.height and 0 <= nx < self.width:
                            possible_surrounding_tiles = np.flatnonzero(self.wave[ny, nx])
                            if len(possible_surrounding_tiles) == 1:
                                surrounding_tiles.add(self.tile_names[possible_surrounding_tiles[0]])
                    if len(surrounding_tiles) == 1 and current_tile not in surrounding_tiles:
                        new_tile = list(surrounding_tiles)[0]
                        new_tile_idx = self.tile_names.index(new_tile)
                        self.wave[y, x] = False
                        self.wave[y, x, new_tile_idx] = True

# Create and observe the wave function collapse with retries
max_retries = 5
for attempt in range(max_retries):
    try:
        wfc = WaveFunctionCollapse(GRID_WIDTH, GRID_HEIGHT, tile_constraints)
        wfc.observe()
        wfc.optimize()
        output_grid = wfc.get_output_grid()
        break
    except ValueError as e:
        if attempt == max_retries - 1:
            raise e

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wave Function Collapse")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the grid
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            tile = output_grid[y][x]
            color = COLORS[tile]
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
