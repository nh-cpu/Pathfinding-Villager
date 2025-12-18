"""
Pathfinding algorithms for the Villager Grid Game.
Implements A* and BFS algorithms for finding optimal paths.
"""

from typing import List, Tuple, Optional, Dict, Set
from collections import deque
import heapq
import time


class PathFinder:
    """
    Pathfinding implementation for navigating a villager through a grid.
    Supports multiple algorithms: A* and BFS.
    """
    
    def __init__(self, grid_map):
        """
        Initialize the pathfinder with a grid map.
        
        Args:
            grid_map: GridMap instance representing the game world
        """
        self.grid_map = grid_map
        self.visited_nodes = 0
        self.pathfinding_time = 0.0
    
    def find_path_astar(self, start: Tuple[int, int], goal: Tuple[int, int], heuristic_type: str = "manhattan") -> Optional[List[Tuple[int, int]]]:
        """
        Find the shortest path using A* algorithm.
        
        Args:
            start: Starting position (row, col)
            goal: Goal position (row, col)
            heuristic_type: Type of heuristic to use ("manhattan", "euclidean", "chebyshev")
            
        Returns:
            List of (row, col) tuples representing the path, or None if no path exists
        """
        start_time = time.time()
        self.visited_nodes = 0
        
        if not self.grid_map.is_valid_position(start[0], start[1]):
            return None
        if not self.grid_map.is_valid_position(goal[0], goal[1]):
            return None
        if not self.grid_map.is_walkable(start[0], start[1]):
            return None
        if not self.grid_map.is_walkable(goal[0], goal[1]):
            return None
        
        # Priority queue: (f_score, counter, position)
        counter = 0
        open_set = [(0, counter, start)]
        counter += 1
        
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        
        # g_score: cost from start to node
        g_score: Dict[Tuple[int, int], float] = {start: 0}
        
        # f_score: estimated total cost (g_score + heuristic)
        f_score: Dict[Tuple[int, int], float] = {start: self._get_heuristic(start, goal, heuristic_type)}
        
        # Set of positions in the open set for fast lookup
        open_set_hash: Set[Tuple[int, int]] = {start}
        
        while open_set:
            _, _, current = heapq.heappop(open_set)
            
            if current in open_set_hash:
                open_set_hash.remove(current)
            
            self.visited_nodes += 1
            
            if current == goal:
                self.pathfinding_time = time.time() - start_time
                return self._reconstruct_path(came_from, current)
            
            for neighbor in self.grid_map.get_neighbors(current[0], current[1]):
                if not self.grid_map.is_walkable(neighbor[0], neighbor[1]):
                    continue
                
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self._get_heuristic(neighbor, goal, heuristic_type)
                    
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], counter, neighbor))
                        counter += 1
                        open_set_hash.add(neighbor)
        
        self.pathfinding_time = time.time() - start_time
        return None  # No path found
    
    def find_path_bfs(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Find a path using Breadth-First Search (BFS) algorithm.
        
        Args:
            start: Starting position (row, col)
            goal: Goal position (row, col)
            
        Returns:
            List of (row, col) tuples representing the path, or None if no path exists
        """
        if not self.grid_map.is_valid_position(start[0], start[1]):
            return None
        if not self.grid_map.is_valid_position(goal[0], goal[1]):
            return None
        if not self.grid_map.is_walkable(start[0], start[1]):
            return None
        if not self.grid_map.is_walkable(goal[0], goal[1]):
            return None
        
        queue = deque([start])
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        visited: Set[Tuple[int, int]] = {start}
        
        while queue:
            current = queue.popleft()
            
            if current == goal:
                return self._reconstruct_path(came_from, current)
            
            for neighbor in self.grid_map.get_neighbors(current[0], current[1]):
                if not self.grid_map.is_walkable(neighbor[0], neighbor[1]):
                    continue
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)
        
        return None  # No path found
    
    def find_path_dijkstra(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Find the shortest path using Dijkstra's algorithm.
        
        Args:
            start: Starting position (row, col)
            goal: Goal position (row, col)
            
        Returns:
            List of (row, col) tuples representing the path, or None if no path exists
        """
        start_time = time.time()
        self.visited_nodes = 0
        
        if not self.grid_map.is_valid_position(start[0], start[1]):
            return None
        if not self.grid_map.is_valid_position(goal[0], goal[1]):
            return None
        if not self.grid_map.is_walkable(start[0], start[1]):
            return None
        if not self.grid_map.is_walkable(goal[0], goal[1]):
            return None
        
        # Priority queue: (cost, counter, position)
        counter = 0
        open_set = [(0, counter, start)]
        counter += 1
        
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        cost: Dict[Tuple[int, int], float] = {start: 0}
        open_set_hash: Set[Tuple[int, int]] = {start}
        
        while open_set:
            current_cost, _, current = heapq.heappop(open_set)
            
            if current in open_set_hash:
                open_set_hash.remove(current)
            
            self.visited_nodes += 1
            
            if current == goal:
                self.pathfinding_time = time.time() - start_time
                return self._reconstruct_path(came_from, current)
            
            for neighbor in self.grid_map.get_neighbors(current[0], current[1]):
                if not self.grid_map.is_walkable(neighbor[0], neighbor[1]):
                    continue
                
                tentative_cost = cost[current] + 1
                
                if neighbor not in cost or tentative_cost < cost[neighbor]:
                    came_from[neighbor] = current
                    cost[neighbor] = tentative_cost
                    
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (tentative_cost, counter, neighbor))
                        counter += 1
                        open_set_hash.add(neighbor)
        
        self.pathfinding_time = time.time() - start_time
        return None  # No path found
    
    def find_path_greedy_best_first(self, start: Tuple[int, int], goal: Tuple[int, int], heuristic_type: str = "manhattan") -> Optional[List[Tuple[int, int]]]:
        """
        Find a path using Greedy Best-First Search algorithm.
        Uses only heuristic (no actual cost), may not find optimal path.
        
        Args:
            start: Starting position (row, col)
            goal: Goal position (row, col)
            heuristic_type: Type of heuristic to use ("manhattan", "euclidean", "chebyshev")
            
        Returns:
            List of (row, col) tuples representing the path, or None if no path exists
        """
        start_time = time.time()
        self.visited_nodes = 0
        
        if not self.grid_map.is_valid_position(start[0], start[1]):
            return None
        if not self.grid_map.is_valid_position(goal[0], goal[1]):
            return None
        if not self.grid_map.is_walkable(start[0], start[1]):
            return None
        if not self.grid_map.is_walkable(goal[0], goal[1]):
            return None
        
        # Priority queue: (heuristic, counter, position)
        counter = 0
        open_set = [(self._get_heuristic(start, goal, heuristic_type), counter, start)]
        counter += 1
        
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        visited: Set[Tuple[int, int]] = {start}
        
        while open_set:
            _, _, current = heapq.heappop(open_set)
            
            self.visited_nodes += 1
            
            if current == goal:
                self.pathfinding_time = time.time() - start_time
                return self._reconstruct_path(came_from, current)
            
            for neighbor in self.grid_map.get_neighbors(current[0], current[1]):
                if not self.grid_map.is_walkable(neighbor[0], neighbor[1]):
                    continue
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    h = self._get_heuristic(neighbor, goal, heuristic_type)
                    heapq.heappush(open_set, (h, counter, neighbor))
                    counter += 1
        
        self.pathfinding_time = time.time() - start_time
        return None  # No path found
    
    def find_nearest_tilled(self, start: Tuple[int, int], heuristic_type: str = "manhattan", algorithm: str = "astar") -> Optional[Tuple[Tuple[int, int], List[Tuple[int, int]]]]:
        """
        Find the nearest tilled dirt tile and the path to it.
        
        Args:
            start: Starting position (row, col)
            heuristic_type: Type of heuristic to use ("manhattan", "euclidean", "chebyshev")
            algorithm: Algorithm to use ("astar", "dijkstra", "greedy", "bfs")
            
        Returns:
            Tuple of (goal_position, path) or None if no tilled tile is reachable
        """
        tilled_tiles = self.grid_map.find_tilled_tiles()
        
        if not tilled_tiles:
            return None
        
        shortest_path = None
        shortest_distance = float('inf')
        nearest_goal = None
        
        for tilled_pos in tilled_tiles:
            # Choose algorithm
            if algorithm == "dijkstra":
                path = self.find_path_dijkstra(start, tilled_pos)
            elif algorithm == "greedy":
                path = self.find_path_greedy_best_first(start, tilled_pos, heuristic_type)
            elif algorithm == "bfs":
                path = self.find_path_bfs(start, tilled_pos)
            else:  # astar (default)
                path = self.find_path_astar(start, tilled_pos, heuristic_type)
            
            if path and len(path) < shortest_distance:
                shortest_path = path
                shortest_distance = len(path)
                nearest_goal = tilled_pos
        
        if shortest_path:
            return (nearest_goal, shortest_path)
        
        return None
    
    def _get_heuristic(self, pos1: Tuple[int, int], pos2: Tuple[int, int], heuristic_type: str) -> float:
        """
        Get the appropriate heuristic based on type.
        
        Args:
            pos1: First position (row, col)
            pos2: Second position (row, col)
            heuristic_type: Type of heuristic ("manhattan", "euclidean", "chebyshev")
            
        Returns:
            Distance between positions using specified metric
        """
        if heuristic_type == "euclidean":
            return self._heuristic_euclidean(pos1, pos2)
        elif heuristic_type == "chebyshev":
            return self._heuristic_chebyshev(pos1, pos2)
        else:  # manhattan (default)
            return self._heuristic_manhattan(pos1, pos2)
    
    def _heuristic_manhattan(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Calculate Manhattan distance heuristic between two positions.
        4-directional movement (up, down, left, right).
        
        Args:
            pos1: First position (row, col)
            pos2: Second position (row, col)
            
        Returns:
            Manhattan distance between positions
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def _heuristic_euclidean(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Calculate Euclidean distance heuristic between two positions.
        Straight-line distance.
        
        Args:
            pos1: First position (row, col)
            pos2: Second position (row, col)
            
        Returns:
            Euclidean distance between positions
        """
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
    
    def _heuristic_chebyshev(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Calculate Chebyshev distance heuristic between two positions.
        8-directional movement (includes diagonals).
        
        Args:
            pos1: First position (row, col)
            pos2: Second position (row, col)
            
        Returns:
            Chebyshev distance between positions
        """
        return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))
    
    def _reconstruct_path(self, came_from: Dict[Tuple[int, int], Tuple[int, int]], 
                         current: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Reconstruct the path from start to goal using the came_from dictionary.
        
        Args:
            came_from: Dictionary mapping each position to its predecessor
            current: The goal position
            
        Returns:
            List of positions from start to goal
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def get_path_length(self, path: List[Tuple[int, int]]) -> int:
        """
        Get the length of a path.
        
        Args:
            path: List of positions
            
        Returns:
            Number of steps in the path (excluding start position)
        """
        return len(path) - 1 if path else 0
    
    def run_pathfinding_with_stats(self, start: Tuple[int, int], goal: Tuple[int, int], algorithm: str = "astar", heuristic_type: str = "manhattan") -> Dict:
        """
        Run pathfinding algorithm and return path plus stats.
        
        Args:
            start: Starting position (row, col)
            goal: Goal position (row, col)
            algorithm: Algorithm to use ("astar", "dijkstra", "greedy", "bfs")
            heuristic_type: Type of heuristic to use ("manhattan", "euclidean", "chebyshev")
            
        Returns:
            Dictionary containing path, route_length, visited_nodes, and time
        """
        # Choose algorithm
        if algorithm == "dijkstra":
            path = self.find_path_dijkstra(start, goal)
        elif algorithm == "greedy":
            path = self.find_path_greedy_best_first(start, goal, heuristic_type)
        elif algorithm == "bfs":
            path = self.find_path_bfs(start, goal)
        else:  # astar (default)
            path = self.find_path_astar(start, goal, heuristic_type)
        
        return {
            "path": path,
            "route_length": self.get_path_length(path) if path else None,
            "visited_nodes": self.visited_nodes,
            "time": self.pathfinding_time,
        }
    
    def run_astar_with_stats(self, start: Tuple[int, int], goal: Tuple[int, int], heuristic_type: str = "manhattan") -> Dict:
        """Legacy method for backward compatibility."""
        return self.run_pathfinding_with_stats(start, goal, "astar", heuristic_type)
    
    def visualize_path(self, path: Optional[List[Tuple[int, int]]], 
                      start: Tuple[int, int], goal: Tuple[int, int]):
        """
        Visualize the path on the grid.
        
        Args:
            path: List of positions in the path
            start: Starting position
            goal: Goal position
        """
        if path is None:
            print("\nNo path found!")
            return
        
        print(f"\nPath found! Length: {self.get_path_length(path)} steps")
        print(f"Start: {start}, Goal: {goal}")
        print("\nPath visualization:")
        
        # Create a copy of the grid for visualization
        rows, cols = self.grid_map.rows, self.grid_map.columns
        
        print("  ", end="")
        for col in range(cols):
            print(f"{col:2}", end=" ")
        print()
        
        for row in range(rows):
            print(f"{row:2} ", end="")
            for col in range(cols):
                pos = (row, col)
                tile = self.grid_map.get_tile(row, col)
                
                if pos == start:
                    print(" S", end=" ")
                elif pos == goal:
                    print(" G", end=" ")
                elif pos in path:
                    print(" *", end=" ")
                elif tile == "F":
                    print(" #", end=" ")
                elif tile == "T":
                    print(" T", end=" ")
                else:
                    print(" .", end=" ")
            print()
        
        print("\nLegend:")
        print("  S = Start position")
        print("  G = Goal position")
        print("  * = Path")
        print("  # = Fence (obstacle)")
        print("  T = Tilled dirt")
        print("  . = Empty land")


