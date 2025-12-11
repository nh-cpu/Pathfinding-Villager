"""
Villager Grid Pathfinding Game - Main Game File
Example implementation of the villager pathfinding system.
"""

import random
from typing import List, Tuple, Optional
from grid_map import GridMap
from pathfinding import PathFinder


class VillagerGame:
    """
    Main game class that manages the villager, grid, and pathfinding.
    """
    
    def __init__(self, columns: int, rows: int):
        """
        Initialize the game with a grid of specified size.
        
        Args:
            columns: Number of columns in the grid
            rows: Number of rows in the grid
        """
        self.grid_map = GridMap(columns, rows)
        self.pathfinder = PathFinder(self.grid_map)
        self.villager_position = None
    
    def setup_game(self, villager_pos: Tuple[int, int], 
                   tilled_positions: List[Tuple[int, int]] = None,
                   fence_density: float = 0.15):
        """
        Set up the game with villager position, tilled dirt, and obstacles.
        
        Args:
            villager_pos: Starting position of the villager (row, col)
            tilled_positions: List of positions for tilled dirt tiles
            fence_density: Density of fence obstacles (0.0 to 1.0)
        """
        self.villager_position = villager_pos
        
        # Place tilled dirt tiles
        if tilled_positions:
            for pos in tilled_positions:
                self.grid_map.place_tilled_dirt(pos[0], pos[1])
        
        # Generate random fences
        self.grid_map.generate_random_obstacles(fence_density)
        
        # Ensure villager start position is walkable (aligned with Section 7.1)
        if self.grid_map.get_tile(villager_pos[0], villager_pos[1]) == "F":
            self.grid_map.set_tile(villager_pos[0], villager_pos[1], "")
    
    def find_path_to_goal(self, goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Find a path from the villager to a specific goal.
        
        Args:
            goal: Target position (row, col)
            
        Returns:
            Path as list of positions, or None if no path exists
        """
        if self.villager_position is None:
            print("Villager position not set!")
            return None
        
        return self.pathfinder.find_path_astar(self.villager_position, goal)
    
    def find_nearest_tilled(self) -> Optional[Tuple[Tuple[int, int], List[Tuple[int, int]]]]:
        """
        Find the nearest tilled dirt tile and path to it.
        
        Returns:
            Tuple of (goal_position, path) or None
        """
        if self.villager_position is None:
            print("Villager position not set!")
            return None
        
        return self.pathfinder.find_nearest_tilled(self.villager_position)
    
    def move_villager(self, new_position: Tuple[int, int]) -> bool:
        """
        Move the villager to a new position.
        
        Args:
            new_position: New position (row, col)
            
        Returns:
            True if move was successful, False otherwise
        """
        if not self.grid_map.is_walkable(new_position[0], new_position[1]):
            return False
        
        self.villager_position = new_position
        return True
    
    def display_game(self):
        """Display the current game state."""
        self.grid_map.display(self.villager_position)


def demo_small_grid():
    """Demonstrate the game with a 10x10 grid."""
    print("=" * 60)
    print("DEMO: 10x10 Grid")
    print("=" * 60)
    
    game = VillagerGame(10, 10)
    
    # Set up the game
    villager_start = (0, 0)
    tilled_positions = [(8, 8), (5, 5), (2, 7)]
    
    game.setup_game(villager_start, tilled_positions, fence_density=0.15)
    
    # Display the initial state
    print("\nInitial Game State:")
    game.display_game()
    
    # Find path to nearest tilled dirt
    result = game.find_nearest_tilled()
    if result:
        goal, path = result
        print(f"\n\nNearest tilled dirt found at: {goal}")
        game.pathfinder.visualize_path(path, villager_start, goal)
    else:
        print("\nNo reachable tilled dirt found!")


def demo_medium_grid():
    """Demonstrate the game with a 20x20 grid."""
    print("\n\n" + "=" * 60)
    print("DEMO: 20x20 Grid")
    print("=" * 60)
    
    game = VillagerGame(20, 20)
    
    # Set up the game
    villager_start = (0, 0)
    tilled_positions = [(18, 18), (10, 10), (5, 15)]
    
    game.setup_game(villager_start, tilled_positions, fence_density=0.12)
    
    # Display the initial state
    print("\nInitial Game State:")
    game.display_game()
    
    # Find path to specific tilled dirt
    goal = (18, 18)
    path = game.find_path_to_goal(goal)
    if path:
        print(f"\n\nPath to tilled dirt at {goal}:")
        game.pathfinder.visualize_path(path, villager_start, goal)
    else:
        print(f"\nNo path found to {goal}!")


def demo_large_grid():
    """Demonstrate the game with a 50x50 grid."""
    print("\n\n" + "=" * 60)
    print("DEMO: 50x50 Grid")
    print("=" * 60)
    
    game = VillagerGame(50, 50)
    
    # Set up the game
    villager_start = (0, 0)
    # Place multiple tilled dirt tiles
    tilled_positions = [(45, 45), (25, 25), (10, 40), (40, 10)]
    
    game.setup_game(villager_start, tilled_positions, fence_density=0.1)
    
    print("\nGame created with 50x50 grid")
    print(f"Villager position: {villager_start}")
    print(f"Tilled dirt positions: {tilled_positions}")
    
    # Find path to nearest tilled dirt
    result = game.find_nearest_tilled()
    if result:
        goal, path = result
        print(f"\nNearest tilled dirt: {goal}")
        print(f"Path length: {game.pathfinder.get_path_length(path)} steps")
        print(f"Path: {path[:10]}..." if len(path) > 10 else f"Path: {path}")
    else:
        print("\nNo reachable tilled dirt found!")


def custom_game_example():
    """Example of creating a custom game scenario."""
    print("\n\n" + "=" * 60)
    print("CUSTOM GAME EXAMPLE")
    print("=" * 60)
    
    # Create a 15x15 grid
    game = VillagerGame(15, 15)
    
    # Custom setup
    villager_start = (7, 7)  # Start in the middle
    
    # Create a ring of tilled dirt around the edges
    tilled_positions = [
        (0, 7), (14, 7),  # Top and bottom
        (7, 0), (7, 14)   # Left and right
    ]
    
    game.setup_game(villager_start, tilled_positions, fence_density=0.2)
    
    print("\nCustom Game State:")
    game.display_game()
    
    # Find all paths to each tilled dirt
    print("\n\nFinding paths to all tilled dirt tiles:")
    for i, tilled_pos in enumerate(tilled_positions, 1):
        path = game.find_path_to_goal(tilled_pos)
        if path:
            print(f"\nPath {i} to {tilled_pos}: {len(path)-1} steps")
        else:
            print(f"\nPath {i} to {tilled_pos}: BLOCKED!")


def run_barrier_experiment(
    columns=16,
    rows=16,
    fence_densities=(0.05, 0.10, 0.15, 0.20, 0.25, 0.30),
    runs_per_density=10,
):
    """
    Experiment runner for Section 7.1: Systematically vary obstacles
    and measure visited nodes, route length, and computation time.
    
    This aligns with Candra's Table 2 methodology.
    
    Args:
        columns: Grid width
        rows: Grid height
        fence_densities: Tuple of fence density values to test
        runs_per_density: Number of runs per density level
    """
    print("\n" + "="*70)
    print("BARRIER EXPERIMENT (Section 7.1 - Obstacle Effects)")
    print("="*70)
    print(f"Grid size: {columns}x{rows}")
    print(f"Fence densities: {fence_densities}")
    print(f"Runs per density: {runs_per_density}")
    print("="*70)
    
    for density in fence_densities:
        print("\n" + "="*70)
        print(f"Fence density: {density:.2f} ({int(density*100)}%)")
        print("="*70)

        route_lengths = []
        visited_counts = []
        times = []
        barrier_counts = []

        for run in range(runs_per_density):
            # Create fresh grid for each run
            grid = GridMap(columns, rows)

            # Fixed start and goal positions
            start = (0, 0)
            goal = (rows - 1, columns - 1)
            grid.place_tilled_dirt(goal[0], goal[1])

            # Generate random obstacles
            grid.generate_random_obstacles(density)

            # Ensure start and goal are walkable
            if grid.get_tile(start[0], start[1]) == "F":
                grid.set_tile(start[0], start[1], "")
            # generate_random_obstacles already avoids overwriting "T"

            # Count actual barriers placed
            barriers = sum(
                1
                for r in range(rows)
                for c in range(columns)
                if grid.get_tile(r, c) == "F"
            )

            # Run A* with stats
            pf = PathFinder(grid)
            stats = pf.run_astar_with_stats(start, goal)

            if stats["path"] is None:
                print(f"  Run {run+1}: NO PATH (barriers={barriers})")
                continue

            route_lengths.append(stats["route_length"])
            visited_counts.append(stats["visited_nodes"])
            times.append(stats["time"])
            barrier_counts.append(barriers)

            print(
                f"  Run {run+1}: barriers={barriers:3d}, "
                f"route={stats['route_length']:3d}, "
                f"visited={stats['visited_nodes']:4d}, "
                f"time={stats['time']*1000:7.3f}ms"
            )

        # Print summary statistics
        if route_lengths:
            print("\n  AVERAGES for this density:")
            print(f"    Barriers     = {sum(barrier_counts)/len(barrier_counts):6.1f}")
            print(f"    Route length = {sum(route_lengths)/len(route_lengths):6.2f}")
            print(f"    Visited      = {sum(visited_counts)/len(visited_counts):6.2f}")
            print(f"    Time         = {sum(times)/len(times)*1000:7.3f}ms")
            print(f"    Success rate = {len(route_lengths)}/{runs_per_density} ({100*len(route_lengths)/runs_per_density:.0f}%)")
        else:
            print("\n  (All runs were blocked - no paths found)")
    
    print("\n" + "="*70)
    print("Experiment completed!")
    print("="*70)


def demo_nearest_tilled():
    """
    Demonstration of nearest tilled tile selection.
    Parallels Candra's Section 3.3 "Nearest Tree Route" example.
    """
    print("\n\n" + "=" * 60)
    print("NEAREST TILLED TILE DEMO (Candra Section 3.3)")
    print("=" * 60)
    
    game = VillagerGame(12, 12)
    
    villager_start = (1, 1)
    # Place multiple tilled tiles at various distances
    tilled_positions = [(10, 10), (5, 9), (8, 3)]
    
    game.setup_game(villager_start, tilled_positions, fence_density=0.1)
    
    print("\nGame State:")
    game.display_game()
    
    print("\n\nComparing paths to each tilled tile:")
    print(f"Villager at: {villager_start}\n")
    
    shortest_distance = float('inf')
    nearest_tile = None
    
    for i, tilled_pos in enumerate(tilled_positions, 1):
        path = game.find_path_to_goal(tilled_pos)
        if path:
            path_length = len(path) - 1
            manhattan = abs(tilled_pos[0] - villager_start[0]) + abs(tilled_pos[1] - villager_start[1])
            print(f"  Tile {i} at {tilled_pos}:")
            print(f"    Manhattan distance: {manhattan}")
            print(f"    Actual route length: {path_length}")
            print(f"    Visited nodes: {game.pathfinder.visited_nodes}")
            
            if path_length < shortest_distance:
                shortest_distance = path_length
                nearest_tile = tilled_pos
        else:
            print(f"  Tile {i} at {tilled_pos}: BLOCKED")
    
    if nearest_tile:
        print(f"\n  → Nearest tile chosen: {nearest_tile} (distance: {shortest_distance})")


if __name__ == "__main__":
    import sys
    
    # Check if experiment mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == "--experiment":
        # Run the barrier experiment for Section 7.1 data collection
        run_barrier_experiment(
            columns=16,
            rows=16,
            fence_densities=(0.05, 0.10, 0.15, 0.20, 0.25, 0.30),
            runs_per_density=10
        )
    elif len(sys.argv) > 1 and sys.argv[1] == "--nearest":
        # Run the nearest tilled tile demo
        demo_nearest_tilled()
    else:
        # Run all standard demos
        demo_small_grid()
        demo_medium_grid()
        demo_large_grid()
        custom_game_example()
        
        print("\n\n" + "=" * 60)
        print("All demos completed!")
        print("=" * 60)
        print("\nTo run experiments:")
        print("  python main.py --experiment  (Section 7.1 barrier experiment)")
        print("  python main.py --nearest     (Nearest tile demo)")
