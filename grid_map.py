"""
Grid Map for 2D Villager Pathfinding Game
Represents a grid-based game map with different tile types.
"""

import random
from typing import List, Tuple, Optional


class GridMap:
    """
    Represents a 2D grid map for the villager pathfinding game.
    
    Tile Types:
    - "" (empty string): Empty land - villager can walk through
    - "T": Tilled dirt - target destination for planting seeds
    - "F": Fence - villager cannot pass through
    """
    
    def __init__(self, columns: int, rows: int):
        """
        Initialize a grid map with specified dimensions.
        
        Args:
            columns: Number of columns (width)
            rows: Number of rows (height)
        """
        self.columns = columns
        self.rows = rows
        self.grid: List[List[str]] = [["" for _ in range(columns)] for _ in range(rows)]
        
    def set_tile(self, row: int, col: int, tile_type: str) -> bool:
        """
        Set a tile at the specified position.
        
        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            tile_type: Type of tile ("", "T", or "F")
            
        Returns:
            True if tile was set successfully, False otherwise
        """
        if not self.is_valid_position(row, col):
            return False
        
        if tile_type not in ["", "T", "F"]:
            return False
            
        self.grid[row][col] = tile_type
        return True
    
    def get_tile(self, row: int, col: int) -> Optional[str]:
        """
        Get the tile type at the specified position.
        
        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            
        Returns:
            Tile type or None if position is invalid
        """
        if not self.is_valid_position(row, col):
            return None
        return self.grid[row][col]
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """
        Check if a position is within the grid boundaries.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            True if position is valid, False otherwise
        """
        return 0 <= row < self.rows and 0 <= col < self.columns
    
    def is_walkable(self, row: int, col: int) -> bool:
        """
        Check if a tile is walkable (not a fence and within bounds).
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            True if tile is walkable, False otherwise
        """
        if not self.is_valid_position(row, col):
            return False
        return self.grid[row][col] != "F"
    
    def find_tilled_tiles(self) -> List[Tuple[int, int]]:
        """
        Find all tilled dirt tiles on the map.
        
        Returns:
            List of (row, col) tuples for all tilled tiles
        """
        tilled_positions = []
        for row in range(self.rows):
            for col in range(self.columns):
                if self.grid[row][col] == "T":
                    tilled_positions.append((row, col))
        return tilled_positions
    
    def generate_random_obstacles(self, fence_density: float = 0.15):
        """
        Generate random fence obstacles on the map.
        
        Args:
            fence_density: Percentage of tiles to be fences (0.0 to 1.0)
        """
        num_fences = int(self.rows * self.columns * fence_density)
        
        for _ in range(num_fences):
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.columns - 1)
            # Don't overwrite tilled tiles
            if self.grid[row][col] != "T":
                self.grid[row][col] = "F"
    
    def place_tilled_dirt(self, row: int, col: int) -> bool:
        """
        Place a tilled dirt tile at the specified position.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            True if placement was successful, False otherwise
        """
        return self.set_tile(row, col, "T")
    
    def display(self, villager_pos: Optional[Tuple[int, int]] = None):
        """
        Display the grid map in console.
        
        Args:
            villager_pos: Optional (row, col) tuple for villager position
        """
        print(f"\nGrid Map ({self.columns}x{self.rows}):")
        print("  ", end="")
        for col in range(self.columns):
            print(f"{col:2}", end=" ")
        print()
        
        for row in range(self.rows):
            print(f"{row:2} ", end="")
            for col in range(self.columns):
                if villager_pos and villager_pos == (row, col):
                    print(" V", end=" ")
                else:
                    tile = self.grid[row][col]
                    if tile == "":
                        print(" .", end=" ")
                    elif tile == "T":
                        print(" T", end=" ")
                    elif tile == "F":
                        print(" #", end=" ")
            print()
        
        print("\nLegend:")
        print("  . = Empty land")
        print("  T = Tilled dirt (goal)")
        print("  # = Fence (obstacle)")
        print("  V = Villager")
    
    def clear(self):
        """Clear the entire grid to empty land."""
        self.grid = [["" for _ in range(self.columns)] for _ in range(self.rows)]
    
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Get all valid neighboring positions (4-directional: up, down, left, right).
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            List of valid neighboring (row, col) tuples
        """
        neighbors = []
        # Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position(new_row, new_col):
                neighbors.append((new_row, new_col))
        
        return neighbors
