# Wave Function Collapse Algorithm Implementation

## Overview

This repository contains an implementation of the Wave Function Collapse (WFC) algorithm using Python and Pygame. The WFC algorithm is a procedural generation technique that can be used to create complex patterns from simple rules, often resembling natural textures or structures.

## Features

- **Wave Function Collapse Algorithm**: Generates a grid based on predefined tile constraints.
- **Pygame Integration**: Visualizes the generated grid in real-time.
- **Retry Logic**: Handles contradictions in the wave function by retrying up to 5 times.

## Requirements

- Python 3.6+
- Pygame
- NumPy

You can install the required packages using pip:

pip install pygame numpy

## Usage

1. Clone the Repository

   git clone https://github.com/lalanikarim/wave-function-collapse-py.git
   cd wave-function-collapse-py

2. Run the Application

   python app.py

   This will start the application and display a window with the generated grid.

## Configuration

- **Grid Size**: You can change the GRID_WIDTH and GRID_HEIGHT constants in app.py to adjust the size of the generated grid.
- **Tile Constraints**: Modify the tile_constraints dictionary in app.py to define how different tiles can be placed next to each other.

## Example

Here is an example of how the tile constraints are defined:

tile_constraints = {
    'deep_water': ['deep_water', 'water'],
    'water': ['water', 'sand', 'deep_water'],
    'sand': ['water', 'grass'],
    'grass': ['mud', 'tree', 'sand'],
    'tree': ['grass', 'mud'],
    'mud': ['mud', 'grass', 'tree']
}

This configuration specifies which tiles can be adjacent to each other.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests with improvements or new features.
