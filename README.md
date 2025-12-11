# Villager Grid Pathfinding Game

A 2D grid-based pathfinding game where a Minecraft-style villager needs to navigate through a grid to reach tilled dirt tiles to plant seeds.

## Features

- **Multiple Grid Sizes**: Support for 10x10, 20x20, and 50x50 grids
- **Tile Types**:
  - Empty land (`""`) - Villager can walk through
  - Tilled dirt (`"T"`) - Target destination for planting seeds
  - Fence (`"F"`) - Obstacle that blocks the villager
- **Pathfinding Algorithms**:
  - A* (A-star) algorithm for optimal pathfinding
  - BFS (Breadth-First Search) algorithm
- **Smart Navigation**: Automatically finds the nearest tilled dirt tile

## File Structure

```
├── grid_map.py       # Grid map representation and tile management
├── pathfinding.py    # Pathfinding algorithms (A* and BFS)
├── main.py           # Main game file with demos and examples
└── README.md         # This file
```

## Installation

No external dependencies required! This project uses only Python standard library.

Simply clone or download the files to your directory.

## Usage

### Running the Demos

Run the main file to see all demos:

```bash
python main.py
```

This will run demonstrations for:
- 10x10 grid
- 20x20 grid
- 50x50 grid
- Custom game scenario

### Basic Example

```python
from grid_map import GridMap
from pathfinding import PathFinder

# Create a 10x10 grid
grid = GridMap(10, 10)

# Place tilled dirt at position (8, 8)
grid.place_tilled_dirt(8, 8)

# Generate some random fences (15% density)
grid.generate_random_obstacles(0.15)

# Create pathfinder
pathfinder = PathFinder(grid)

# Find path from (0, 0) to (8, 8)
start = (0, 0)
goal = (8, 8)
path = pathfinder.find_path_astar(start, goal)

if path:
    print(f"Path found with {len(path)-1} steps!")
    pathfinder.visualize_path(path, start, goal)
else:
    print("No path found!")
```

### Using the Game Class

```python
from main import VillagerGame

# Create a 20x20 game
game = VillagerGame(20, 20)

# Set up the game
villager_start = (0, 0)
tilled_positions = [(18, 18), (10, 10)]
game.setup_game(villager_start, tilled_positions, fence_density=0.15)

# Display the game state
game.display_game()

# Find path to nearest tilled dirt
result = game.find_nearest_tilled()
if result:
    goal, path = result
    print(f"Nearest tilled dirt at {goal}")
    game.pathfinder.visualize_path(path, villager_start, goal)
```

## API Reference

### GridMap Class

#### Methods:
- `__init__(columns, rows)` - Create a new grid map
- `set_tile(row, col, tile_type)` - Set a tile to "", "T", or "F"
- `get_tile(row, col)` - Get the tile type at a position
- `is_walkable(row, col)` - Check if a position is walkable (not a fence)
- `place_tilled_dirt(row, col)` - Place tilled dirt at position
- `generate_random_obstacles(fence_density)` - Generate random fences
- `find_tilled_tiles()` - Get all tilled dirt positions
- `display(villager_pos)` - Display the grid in console
- `get_neighbors(row, col)` - Get 4-directional neighboring positions

### PathFinder Class

#### Methods:
- `__init__(grid_map)` - Create pathfinder for a grid map
- `find_path_astar(start, goal)` - Find optimal path using A* algorithm
- `find_path_bfs(start, goal)` - Find path using BFS algorithm
- `find_nearest_tilled(start)` - Find nearest tilled dirt and path to it
- `get_path_length(path)` - Get the number of steps in a path
- `visualize_path(path, start, goal)` - Display the path on the grid

### VillagerGame Class

#### Methods:
- `__init__(columns, rows)` - Create a new game
- `setup_game(villager_pos, tilled_positions, fence_density)` - Set up the game
- `find_path_to_goal(goal)` - Find path to specific goal
- `find_nearest_tilled()` - Find nearest tilled dirt
- `move_villager(new_position)` - Move villager to new position
- `display_game()` - Display current game state

## Grid Coordinate System

- **Row**: Vertical position (0 at top)
- **Column**: Horizontal position (0 at left)
- **Position format**: `(row, column)`

Example for a 5x5 grid:
```
     0  1  2  3  4  (columns)
  0  .  .  .  .  .
  1  .  .  T  .  .
  2  .  #  #  #  .
  3  .  .  .  .  .
  4  .  .  .  .  .
(rows)
```

Position `(1, 2)` is the tilled dirt tile `T`

## Pathfinding Algorithms

### A* Algorithm
- **Optimal**: Always finds the shortest path
- **Efficient**: Uses heuristic to guide search
- **Best for**: Most scenarios, especially larger grids

### BFS Algorithm
- **Complete**: Finds a path if one exists
- **Simple**: No heuristic needed
- **Best for**: Small grids or when all paths have equal cost

## Visualization Legend

When displaying the grid:
- `.` = Empty land
- `T` = Tilled dirt (goal)
- `#` = Fence (obstacle)
- `V` = Villager position
- `S` = Start position (in path visualization)
- `G` = Goal position (in path visualization)
- `*` = Path tiles (in path visualization)

## Future Implementation Ideas

Since pathfinding is ready but not yet fully integrated, you can:
1. Add real-time villager movement animation
2. Implement multiple villagers
3. Add seed planting mechanics
4. Create a GUI interface
5. Add different terrain types with varying costs
6. Implement diagonal movement (8-directional)
7. Add dynamic obstacles that appear/disappear
8. Create a level editor

## Performance Notes

- **10x10 grid**: Instant pathfinding
- **20x20 grid**: Very fast (< 0.1 seconds)
- **50x50 grid**: Fast (< 0.5 seconds for most scenarios)

The A* algorithm is optimized for performance and should handle even 100x100 grids efficiently.

## License

Free to use for any purpose.

## Contributing

Feel free to extend this project with additional features!
