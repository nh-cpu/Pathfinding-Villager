"""
Visual Grid Pathfinding Game using Pygame
Displays the game with Minecraft-style textures.
"""

import pygame
import sys
import random
from typing import List, Tuple, Optional
from grid_map import GridMap
from pathfinding import PathFinder


class VisualGame:
    """
    Visual representation of the villager pathfinding game using Pygame.
    """
    
    def __init__(self, columns: int, rows: int, tile_size: int = 32):
        """
        Initialize the visual game.
        
        Args:
            columns: Number of columns in the grid
            rows: Number of rows in the grid
            tile_size: Size of each tile in pixels
        """
        pygame.init()
        
        self.columns = columns
        self.rows = rows
        self.tile_size = tile_size
        
        # Calculate window size with right panel
        self.grid_width = columns * tile_size
        self.grid_height = rows * tile_size
        self.panel_width = 250  # Width of right info panel
        self.min_height = 720  # Minimum height to show full right panel with all controls
        self.width = self.grid_width + self.panel_width
        self.height = max(self.grid_height, self.min_height)  # Use larger of grid height or min height
        
        # Create window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Villager Pathfinding Game")
        
        # Game components
        self.grid_map = GridMap(columns, rows)
        self.pathfinder = PathFinder(self.grid_map)
        self.villager_position = None
        self.current_path = None
        self.path_index = 0
        self.animating = False
        
        # Load textures
        self.load_textures()
        
        # Colors
        self.PATH_COLOR = (255, 255, 0, 128)  # Yellow with transparency
        self.INFO_BG_COLOR = (50, 50, 50)
        self.TEXT_COLOR = (255, 255, 255)
        
        # Font
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        # Animation
        self.animation_speed = 5  # Frames per move
        self.animation_counter = 0
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        self.fps = 30
        
        # Stats tracking
        self.visited_nodes_count = 0
        self.route_length = 0
        self.pathfinding_time = 0.0
        self.barrier_count = 0
        
        # Calculate panel position
        panel_x = self.grid_width + 10
        
        # Slider for barrier density
        self.fence_density = 0.15
        self.slider_rect = pygame.Rect(panel_x, 480, 220, 10)
        self.slider_handle_rect = pygame.Rect(panel_x, 475, 15, 20)
        self.dragging_slider = False
        self.initial_villager_pos = None
        self.initial_tilled_positions = []
        
        # Tile editing mode
        self.editing_mode = False
        
        # Algorithm selection
        self.algorithm = "astar"  # Default: astar, dijkstra, greedy, bfs
        self.algorithm_buttons = {
            "astar": pygame.Rect(panel_x, 250, 55, 35),
            "dijkstra": pygame.Rect(panel_x + 60, 250, 55, 35),
            "greedy": pygame.Rect(panel_x + 120, 250, 55, 35),
            "bfs": pygame.Rect(panel_x, 295, 55, 35),
        }
        
        # Heuristic selection
        self.heuristic_type = "manhattan"  # Default: manhattan, euclidean, chebyshev
        self.heuristic_buttons = {
            "manhattan": pygame.Rect(panel_x, 360, 70, 35),
            "euclidean": pygame.Rect(panel_x + 75, 360, 70, 35),
            "chebyshev": pygame.Rect(panel_x, 405, 70, 35),
        }
    
    def load_textures(self):
        """Load and scale texture images."""
        try:
            self.texture_land = pygame.image.load("land.png")
            self.texture_tilled = pygame.image.load("tilled.png")
            self.texture_fence = pygame.image.load("fence.png")
            self.texture_villager = pygame.image.load("villager.png")
            
            # Scale textures to tile size
            self.texture_land = pygame.transform.scale(
                self.texture_land, (self.tile_size, self.tile_size)
            )
            self.texture_tilled = pygame.transform.scale(
                self.texture_tilled, (self.tile_size, self.tile_size)
            )
            self.texture_fence = pygame.transform.scale(
                self.texture_fence, (self.tile_size, self.tile_size)
            )
            self.texture_villager = pygame.transform.scale(
                self.texture_villager, (self.tile_size, self.tile_size)
            )
            
            print("âœ“ All textures loaded successfully!")
            
        except pygame.error as e:
            print(f"Error loading textures: {e}")
            print("Make sure land.png, tilled.png, fence.png, and villager.png are in the same directory.")
            sys.exit(1)
    
    def setup_game(self, villager_pos: Tuple[int, int],
                   tilled_positions: List[Tuple[int, int]] = None,
                   fence_density: float = 0.15,
                   num_random_tilled: int = 3):
        """
        Set up the game with initial positions.
        
        Args:
            villager_pos: Starting position of the villager (row, col)
            tilled_positions: List of positions for tilled dirt tiles (None for random)
            fence_density: Density of fence obstacles (0.0 to 1.0)
            num_random_tilled: Number of random tilled tiles if tilled_positions is None
        """
        self.villager_position = villager_pos
        self.initial_villager_pos = villager_pos
        self.fence_density = fence_density
        
        # Generate random tilled positions if not provided
        if tilled_positions is None:
            tilled_positions = self.generate_random_tilled_positions(num_random_tilled)
        
        self.initial_tilled_positions = tilled_positions
        
        # Place tilled dirt tiles
        for pos in tilled_positions:
            self.grid_map.place_tilled_dirt(pos[0], pos[1])
        
        # Generate random fences
        self.grid_map.generate_random_obstacles(fence_density)
        
        # Make sure villager position and tilled positions are walkable
        if self.grid_map.get_tile(villager_pos[0], villager_pos[1]) == "F":
            self.grid_map.set_tile(villager_pos[0], villager_pos[1], "")
        
        # Count barriers
        self.count_barriers()
        
        # Update slider position
        self.update_slider_from_density()
    
    def find_path_to_nearest(self):
        """Find path to the nearest tilled dirt."""
        if self.villager_position is None:
            return
        
        result = self.pathfinder.find_nearest_tilled(self.villager_position, self.heuristic_type, self.algorithm)
        if result:
            goal, path = result
            self.current_path = path
            self.path_index = 0
            self.animating = False
            
            # Update stats
            self.visited_nodes_count = self.pathfinder.visited_nodes
            self.route_length = len(path) - 1
            self.pathfinding_time = self.pathfinder.pathfinding_time * 1000  # Convert to ms
            
            print(f"Path found to {goal}! Length: {len(path)-1} steps")
            print(f"Visited nodes: {self.visited_nodes_count}")
            print(f"Time: {self.pathfinding_time:.2f}ms")
        else:
            print("No path found!")
            self.current_path = None
            self.visited_nodes_count = self.pathfinder.visited_nodes
            self.route_length = 0
            self.pathfinding_time = self.pathfinder.pathfinding_time * 1000
    
    def start_animation(self):
        """Start animating the villager along the path."""
        if self.current_path and len(self.current_path) > 1:
            self.animating = True
            self.path_index = 0
            self.animation_counter = 0
    
    def update_animation(self):
        """Update the villager animation."""
        if not self.animating or not self.current_path:
            return
        
        self.animation_counter += 1
        
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.path_index += 1
            
            if self.path_index < len(self.current_path):
                self.villager_position = self.current_path[self.path_index]
            else:
                self.animating = False
                print("Villager reached the destination!")
    
    def draw_grid(self):
        """Draw the game grid with textures."""
        for row in range(self.rows):
            for col in range(self.columns):
                x = col * self.tile_size
                y = row * self.tile_size
                
                tile = self.grid_map.get_tile(row, col)
                
                # Draw base tile
                if tile == "F":
                    self.screen.blit(self.texture_fence, (x, y))
                elif tile == "T":
                    self.screen.blit(self.texture_tilled, (x, y))
                else:
                    self.screen.blit(self.texture_land, (x, y))
                
                # Draw grid lines (optional, can comment out for cleaner look)
                pygame.draw.rect(self.screen, (100, 100, 100), 
                               (x, y, self.tile_size, self.tile_size), 1)
    
    def draw_path(self):
        """Draw the current path overlay."""
        if not self.current_path:
            return
        
        # Create a transparent surface for the path
        path_surface = pygame.Surface((self.tile_size, self.tile_size))
        path_surface.set_alpha(128)
        path_surface.fill((255, 255, 0))  # Yellow
        
        for i, (row, col) in enumerate(self.current_path):
            if (row, col) != self.villager_position:
                x = col * self.tile_size
                y = row * self.tile_size
                self.screen.blit(path_surface, (x, y))
                
                # Draw path number for all steps (except the last one which is the goal)
                if i < len(self.current_path) - 1:
                    num_text = self.small_font.render(str(i), True, (0, 0, 0))
                    text_rect = num_text.get_rect(center=(x + self.tile_size // 2, 
                                                           y + self.tile_size // 2))
                    self.screen.blit(num_text, text_rect)
    
    def draw_villager(self):
        """Draw the villager."""
        if self.villager_position:
            row, col = self.villager_position
            x = col * self.tile_size
            y = row * self.tile_size
            self.screen.blit(self.texture_villager, (x, y))
    
    def draw_info_panel(self):
        """Draw the information panel on the right side."""
        panel_x = self.grid_width
        panel_width = self.panel_width
        
        # Background
        pygame.draw.rect(self.screen, self.INFO_BG_COLOR, 
                        (panel_x, 0, panel_width, self.height))
        
        # Stats text
        text_x = panel_x + 10
        text_y = 10
        
        # Title
        title_text = self.font.render("STATS", True, (255, 255, 100))
        self.screen.blit(title_text, (text_x + 80, text_y))
        
        # Stats display
        barriers_text = self.small_font.render(f"Barriers: {self.barrier_count}", True, self.TEXT_COLOR)
        self.screen.blit(barriers_text, (text_x, text_y + 35))
        
        route_text = self.small_font.render(f"Route: {self.route_length} steps", True, self.TEXT_COLOR)
        self.screen.blit(route_text, (text_x, text_y + 60))
        
        visited_text = self.small_font.render(f"Visited: {self.visited_nodes_count}", True, self.TEXT_COLOR)
        self.screen.blit(visited_text, (text_x, text_y + 85))
        
        time_text = self.small_font.render(f"Time: {self.pathfinding_time * 1000:.2f}ms", True, self.TEXT_COLOR)
        self.screen.blit(time_text, (text_x, text_y + 110))
        
        # Status message
        if self.editing_mode:
            status_text = "EDIT MODE"
            status_color = (255, 200, 100)
        elif self.animating:
            status_text = "Animating..."
            status_color = (150, 255, 150)
        elif self.current_path:
            status_text = "Path Found"
            status_color = (150, 255, 150)
        else:
            status_text = "Ready"
            status_color = (150, 255, 150)
        
        status = self.small_font.render(f"Status: {status_text}", True, status_color)
        self.screen.blit(status, (text_x, text_y + 135))
        
        # Slider for barrier density
        slider_label = self.font.render("DENSITY", True, (255, 255, 100))
        self.screen.blit(slider_label, (text_x + 60, 445))
        
        density_text = self.small_font.render(f"{int(self.fence_density * 100)}%", True, self.TEXT_COLOR)
        self.screen.blit(density_text, (text_x + 100, 510))
        
        # Draw slider track
        pygame.draw.rect(self.screen, (100, 100, 100), self.slider_rect)
        
        # Draw slider handle
        handle_x = self.slider_rect.x + int(self.fence_density * self.slider_rect.width)
        self.slider_handle_rect.centerx = handle_x
        self.slider_handle_rect.y = self.slider_rect.y - 5
        pygame.draw.rect(self.screen, (200, 200, 200), self.slider_handle_rect)
        
        # Algorithm selection buttons
        algo_label = self.font.render("ALGORITHM", True, (255, 255, 100))
        self.screen.blit(algo_label, (text_x + 50, 210))
        
        for algo_name, button_rect in self.algorithm_buttons.items():
            # Button background
            if algo_name == self.algorithm:
                button_color = (0, 100, 200)  # Blue for selected
            else:
                button_color = (80, 80, 80)  # Dark gray for unselected
            
            pygame.draw.rect(self.screen, button_color, button_rect)
            pygame.draw.rect(self.screen, (200, 200, 200), button_rect, 2)  # Border
            
            # Button text
            if algo_name == "astar":
                display_text = "A*"
            elif algo_name == "dijkstra":
                display_text = "DIJ"
            elif algo_name == "greedy":
                display_text = "GRE"
            else:  # bfs
                display_text = "BFS"
            
            button_text = self.small_font.render(display_text, True, self.TEXT_COLOR)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)
        
        # Heuristic selection buttons
        heuristic_label = self.font.render("HEURISTIC", True, (255, 255, 100))
        self.screen.blit(heuristic_label, (text_x + 50, 320))
        
        for heuristic_name, button_rect in self.heuristic_buttons.items():
            # Button background
            if heuristic_name == self.heuristic_type:
                button_color = (0, 150, 0)  # Green for selected
            else:
                button_color = (80, 80, 80)  # Dark gray for unselected
            
            pygame.draw.rect(self.screen, button_color, button_rect)
            pygame.draw.rect(self.screen, (200, 200, 200), button_rect, 2)  # Border
            
            # Button text
            button_text = self.small_font.render(heuristic_name[:3].upper(), True, self.TEXT_COLOR)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)
        
        # Controls section
        controls_label = self.font.render("CONTROLS", True, (255, 255, 100))
        self.screen.blit(controls_label, (text_x + 55, 540))
        
        controls = [
            "F: Find path",
            "E: Edit goals",
            "SPACE: Animate",
            "R: Reset",
            "G: Regenerate",
            "Q: Quit"
        ]
        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, (200, 200, 200))
            self.screen.blit(control_text, (text_x, 575 + i * 20))
    
    def count_barriers(self):
        """Count the number of barriers in the grid."""
        count = 0
        for row in range(self.rows):
            for col in range(self.columns):
                if self.grid_map.get_tile(row, col) == "F":
                    count += 1
        self.barrier_count = count
    
    def generate_random_tilled_positions(self, num_tiles: int = 3) -> List[Tuple[int, int]]:
        """Generate random positions for tilled dirt tiles."""
        positions = []
        max_attempts = num_tiles * 10  # Prevent infinite loop
        attempts = 0
        
        while len(positions) < num_tiles and attempts < max_attempts:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.columns - 1)
            
            # Make sure it's not the villager position and not already in list
            if (row, col) != self.initial_villager_pos and (row, col) not in positions:
                positions.append((row, col))
            
            attempts += 1
        
        return positions
    
    def handle_tile_click(self, pos):
        """Handle clicking on a tile to add/remove tilled dirt."""
        # Convert screen position to grid coordinates
        grid_y = pos[1] // self.tile_size
        grid_x = pos[0] // self.tile_size
        
        # Check if click is within the grid
        if grid_y >= self.rows or grid_x >= self.columns:
            return
        
        row, col = grid_y, grid_x
        current_tile = self.grid_map.get_tile(row, col)
        
        # Toggle tilled dirt (can't place on fences or villager position)
        if (row, col) == self.villager_position:
            print("Cannot place tilled dirt on villager position!")
            return
        
        if current_tile == "F":
            print("Cannot place tilled dirt on fence!")
            return
        
        if current_tile == "T":
            # Remove tilled dirt
            self.grid_map.set_tile(row, col, "")
            if (row, col) in self.initial_tilled_positions:
                self.initial_tilled_positions.remove((row, col))
            print(f"Removed tilled dirt at ({row}, {col})")
        else:
            # Add tilled dirt
            self.grid_map.set_tile(row, col, "T")
            if (row, col) not in self.initial_tilled_positions:
                self.initial_tilled_positions.append((row, col))
            print(f"Added tilled dirt at ({row}, {col})")
    
    def update_slider_from_density(self):
        """Update slider handle position based on current density."""
        handle_x = self.slider_rect.x + int(self.fence_density * self.slider_rect.width)
        self.slider_handle_rect.centerx = handle_x
    
    def regenerate_grid(self):
        """Regenerate the grid with current density setting."""
        if self.initial_villager_pos is None:
            return
        
        # Clear the grid
        self.grid_map.clear()
        
        # Reset villager position
        self.villager_position = self.initial_villager_pos
        
        # Generate new random tilled positions
        num_tilled = len(self.initial_tilled_positions) if self.initial_tilled_positions else 3
        self.initial_tilled_positions = self.generate_random_tilled_positions(num_tilled)
        
        # Replace tilled dirt
        for pos in self.initial_tilled_positions:
            self.grid_map.place_tilled_dirt(pos[0], pos[1])
        
        # Generate new random fences
        self.grid_map.generate_random_obstacles(self.fence_density)
        
        # Make sure villager position is walkable
        if self.grid_map.get_tile(self.villager_position[0], self.villager_position[1]) == "F":
            self.grid_map.set_tile(self.villager_position[0], self.villager_position[1], "")
        
        # Count barriers
        self.count_barriers()
        
        # Reset path
        self.current_path = None
        self.path_index = 0
        self.animating = False
        self.visited_nodes_count = 0
        self.route_length = 0
        self.pathfinding_time = 0.0
        
        print(f"Grid regenerated with {self.barrier_count} barriers ({int(self.fence_density * 100)}% density)")
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.current_path = None
        self.path_index = 0
        self.animating = False
        self.visited_nodes_count = 0
        self.route_length = 0
        self.pathfinding_time = 0.0
        
        # Reset villager to initial position
        if self.initial_villager_pos is not None:
            self.villager_position = self.initial_villager_pos
        
        print("Game reset!")
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_f:
                    if not self.editing_mode:
                        self.find_path_to_nearest()
                elif event.key == pygame.K_SPACE:
                    if not self.editing_mode:
                        self.start_animation()
                elif event.key == pygame.K_r:
                    if not self.editing_mode:
                        self.reset_game()
                elif event.key == pygame.K_g:
                    if not self.editing_mode:
                        self.regenerate_grid()
                elif event.key == pygame.K_e:
                    self.editing_mode = not self.editing_mode
                    if self.editing_mode:
                        print("\n--- EDIT MODE ENABLED ---")
                        print("Click on tiles to add/remove tilled dirt (goals)")
                        print("Press E again to exit edit mode\n")
                    else:
                        print("Edit mode disabled")
                        # Count tilled tiles
                        tilled_count = len(self.grid_map.find_tilled_tiles())
                        print(f"Current tilled dirt tiles: {tilled_count}")
            
            # Mouse events for slider, tile editing, and heuristic buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = event.pos
                    
                    # Check algorithm button clicks
                    clicked_algo = False
                    for algo_name, button_rect in self.algorithm_buttons.items():
                        if button_rect.collidepoint(mouse_pos):
                            self.algorithm = algo_name
                            print(f"Algorithm changed to: {algo_name}")
                            # Recalculate path if one exists
                            if self.current_path and not self.editing_mode:
                                self.find_path_to_nearest()
                            clicked_algo = True
                            break
                    
                    # Check heuristic button clicks
                    clicked_heuristic = False
                    if not clicked_algo:
                        for heuristic_name, button_rect in self.heuristic_buttons.items():
                            if button_rect.collidepoint(mouse_pos):
                                self.heuristic_type = heuristic_name
                                print(f"Heuristic changed to: {heuristic_name}")
                                # Recalculate path if one exists
                                if self.current_path and not self.editing_mode:
                                    self.find_path_to_nearest()
                                clicked_heuristic = True
                                break
                    
                    if not clicked_algo and not clicked_heuristic:
                        if self.editing_mode:
                            # Handle tile click for editing
                            self.handle_tile_click(event.pos)
                        elif self.slider_handle_rect.collidepoint(event.pos):
                            self.dragging_slider = True
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.dragging_slider:
                        self.dragging_slider = False
                        self.regenerate_grid()
            
            if event.type == pygame.MOUSEMOTION:
                if self.dragging_slider:
                    # Update slider position
                    mouse_x = event.pos[0]
                    relative_x = max(0, min(mouse_x - self.slider_rect.x, self.slider_rect.width))
                    self.fence_density = relative_x / self.slider_rect.width
                    self.update_slider_from_density()
        
        return True
    
    def run(self):
        """Main game loop."""
        running = True
        
        print("\n" + "="*60)
        print("VISUAL GAME CONTROLS:")
        print("="*60)
        print("F     - Find path to nearest tilled dirt")
        print("E     - Toggle edit mode (add/remove tilled dirt goals)")
        print("CLICK - In edit mode: add/remove tilled dirt on clicked tile")
        print("SPACE - Start/Continue animation")
        print("R     - Reset path and stats")
        print("G     - Regenerate grid with current barrier density")
        print("MOUSE - Drag slider to adjust barrier density")
        print("Q     - Quit game")
        print("="*60)
        print("\nSTATS DISPLAYED:")
        print("- Barriers: Number of fence obstacles")
        print("- Route Length: Steps in the calculated path")
        print("- Visited Nodes: Nodes explored by pathfinding algorithm")
        print("- Time: Pathfinding computation time in milliseconds")
        print("="*60 + "\n")
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update animation
            self.update_animation()
            
            # Draw everything
            self.screen.fill((0, 0, 0))  # Clear screen with dark background
            
            # Fill bottom-left area below grid (if any) with dark gray
            if self.grid_height < self.height:
                pygame.draw.rect(self.screen, (40, 40, 40), 
                               (0, self.grid_height, self.grid_width, self.height - self.grid_height))
            
            self.draw_grid()
            self.draw_path()
            self.draw_villager()
            self.draw_info_panel()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        pygame.quit()


def run_visual_game_10x10():
    """Run a 10x10 visual game."""
    game = VisualGame(10, 10, tile_size=48)
    
    villager_start = (5, 5)  # Center of 10x10 grid
    tilled_positions = [(8, 8), (0, 0), (2, 7)]
    
    game.setup_game(villager_start, tilled_positions, fence_density=0.15)
    game.run()


def run_visual_game_20x20():
    """Run a 20x20 visual game."""
    game = VisualGame(20, 20, tile_size=32)
    
    villager_start = (10, 10)  # Center of 20x20 grid
    tilled_positions = [(18, 18), (0, 0), (5, 15)]
    
    game.setup_game(villager_start, tilled_positions, fence_density=0.12)
    game.run()


def run_visual_game_15x15():
    """Run a 15x15 visual game (custom)."""
    game = VisualGame(15, 15, tile_size=40)
    
    villager_start = (7, 7)
    tilled_positions = [
        (0, 7), (14, 7),
        (7, 0), (7, 14)
    ]
    
    game.setup_game(villager_start, tilled_positions, fence_density=0.2)
    game.run()


if __name__ == "__main__":
    print("Select game size:")
    print("1. 10x10 Grid")
    print("2. 20x20 Grid")
    print("3. 15x15 Grid (Custom)")
    
    try:
        choice = input("Enter choice (1-3): ").strip()
        
        # Get barrier density from user
        while True:
            density_input = input("Enter barrier density percentage (0-100, default 15): ").strip()
            if density_input == "":
                fence_density = 0.15
                break
            try:
                density_value = float(density_input)
                if 0 <= density_value <= 100:
                    fence_density = density_value / 100
                    break
                else:
                    print("Please enter a value between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        if choice == "1":
            game = VisualGame(10, 10, tile_size=48)
            villager_start = (5, 5)  # Center of 10x10 grid
            game.setup_game(villager_start, None, fence_density=fence_density, num_random_tilled=3)
            game.run()
        elif choice == "2":
            game = VisualGame(20, 20, tile_size=32)
            villager_start = (10, 10)  # Center of 20x20 grid
            game.setup_game(villager_start, None, fence_density=fence_density, num_random_tilled=3)
            game.run()
        elif choice == "3":
            game = VisualGame(15, 15, tile_size=40)
            villager_start = (7, 7)
            game.setup_game(villager_start, None, fence_density=fence_density, num_random_tilled=4)
            game.run()
        else:
            print("Invalid choice. Running 10x10 game...")
            game = VisualGame(10, 10, tile_size=48)
            villager_start = (5, 5)  # Center of 10x10 grid
            game.setup_game(villager_start, None, fence_density=fence_density, num_random_tilled=3)
            game.run()
    except KeyboardInterrupt:
        print("\nGame cancelled.")

