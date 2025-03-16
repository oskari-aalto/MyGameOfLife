import random
import sys
import pygame


class LifeGame:

    def __init__(self, screen_width=800, screen_height=600, cell_size=10, alive_color=(0, 255, 255),
                 dead_color=(0, 0, 0), max_fps=10):
        """
        Initialize grid, set default game state, initialize screen.

        :param screen_width: Game window width
        :param screen_height: Game window height
        :param cell_size: Radius of circles
        :param alive_color: RGB tuple e.g. (255, 255, 255) for cells
        :param dead_color: RGB tuple e.g. (255, 255, 255)
        :param max_fps: Frame rate cap to limit game speed
        """
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size  # Radius
        self.alive_color = alive_color
        self.dead_color = dead_color
        self.font_size = 25

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clear_screen()
        pygame.display.flip()

        self.last_update_completed = 0.0
        self.desired_milliseconds_between_updates = (1.0 / max_fps) * 1000.0

        self.grids = []
        self.active_grid = 0
        self.num_cols = int(self.screen_width / self.cell_size)
        self.num_rows = int(self.screen_height / self.cell_size)
        print(f"Columns: {self.num_cols}\nRows: {self.num_rows}")
        self.init_grids()
        self.set_grid()

        self.paused = False
        self.game_over = False

        # set the pygame window name
        pygame.display.set_caption('LifeGame - mrWawe')

        # create a font object. (Font file (None=default), font size)
        self.font = pygame.font.Font(None, self.font_size)
        # create a text surface object, on which text is drawn on it.
        self.text = self.font.render('"s" to Pause - "r" to Randomize - "q" to Quit', True, alive_color, dead_color)
        # create a text surface object, on which text is drawn on it.
        self.text_rect = self.text.get_rect()
        # set the center of the rectangular object.
        self.text_rect.center = (self.screen_width - self.screen_width + self.text_rect.width / 2,
                                 self.screen_height - self.screen_height + self.text_rect.height / 2)

    def init_grids(self):
        """
        Create the default active and inactive grid
        Two grids with columns and rows represented with three level list:
        first level is grid states (0, 1),
        second level is columns (num_columns),
        third layer is rows (num_rows)

        :return: None
        """
        # Not a perfect way of creating list. Editing single value ended up changing multiple values
        # self.grids = [[[0] * self.num_rows] * self.num_cols, [[0] * self.num_rows] * self.num_cols]
        def create_grid():
            """
            Generate two(2) empty grids
            :return:
            """
            rows = []
            for row_num in range(self.num_rows):
                list_of_columns = [0] * self.num_cols
                rows.append(list_of_columns)
            return rows
        # Two grids are need for current generation and next generation
        self.grids.append(create_grid())
        self.grids.append(create_grid())

    def set_grid(self, value=None, grid=0):
        """
        Set an entire grid at once. Set to a single value or random 0/1.

        Examples:
        # set_grid(0) # all dead
        # set_grid(1) # all alive
        # set_grid() # random
        # set_grid(None) # random

        :param grid: Index of grid, for active/inactive (0 or 1)
        :param value: Value to set the cell to (0 or 1)
        :return:
       """
        # iterates the lists (amount: num_rows) that are inside grids[active_grid]
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if value is None:
                    cell_value = random.randint(0, 1)
                else:
                    cell_value = value
                self.grids[grid][r][c] = cell_value

    def draw_grid(self):
        """
        Given the grid and cell states, draw the cells on the screen

        :return:
        """
        self.clear_screen()
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.grids[self.active_grid][r][c] == 1:
                    color = self.alive_color
                else:
                    color = self.dead_color
                # circle_rect = pygame.draw.circle(self.screen, ALIVE_COLOR, (50, 50), 5, 0)
                pygame.draw.circle(self.screen,  # surface
                                   color,  # rgb color
                                   # center point to draw the circle, tuple (x, y)
                                   (int(c * self.cell_size + (self.cell_size / 2)),
                                    int(r * self.cell_size + (self.cell_size / 2))),
                                   int(self.cell_size / 2),  # radius
                                   0  # width used for line thickness or to indicate that the circle is to be filled
                                   )
        self.screen.blit(self.text, self.text_rect)
        pygame.display.flip()

    def clear_screen(self):
        """
        Fill the whole screen with dead color
        :return:
        """
        self.screen.fill(self.dead_color)

    def get_cell(self, row_num, col_num):
        """
        Get the alive/dead (0/1) state of a specific cell in active grid
        Function to handle the case where neighbor doesn't exist
        :param row_num:
        :param col_num:
        :return: 0 or 1 depending on state of cell. Defaults to 0 (dead)
        """
        try:
            cell_value = self.grids[self.active_grid][row_num][col_num]
        except IndexError:
            cell_value = 0
        return cell_value

    def check_cell_neighbors(self, row_index, col_index):
        """
        Get the number of alive neighbor cells, and determine teh state of the cell
        for the next generation. Determine whether if lives, dies, or is born.
        :param row_index: Row number of cell to check
        :param col_index: Column number of cell to check
        :return: The state the cell should be in next generation 0 or 1
        """
        # Check all 8 neighbors, add up alive count
        num_alive_neighbors = 0
        num_alive_neighbors += self.get_cell(row_index - 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index + 1)

        # Rules for life and death
        if self.grids[self.active_grid][row_index][col_index] == 1:  # Alive
            if num_alive_neighbors > 3:  # Overpopulation
                return 0
            if num_alive_neighbors < 2:  # Underpopulation
                return 0
            if num_alive_neighbors == 2 or num_alive_neighbors == 3:  # Survive
                return 1
        elif self.grids[self.active_grid][row_index][col_index] == 0:  # Dead
            if num_alive_neighbors == 3:
                return 1  # Come to life
        return self.grids[self.active_grid][row_index][col_index]  # Return as is

    def update_generation(self):
        """
        Inspect current generation state, prepare next generation
        For each cell in active grid, check its neighbors, update state, swap out grids

        :return:
        """
        # clear grid for preparing next generation
        self.set_grid(0, self.inactive_grid())
        # prepare next generation
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                next_gen_state = self.check_cell_neighbors(r, c)
                # Set inactive grid future cell state
                self.grids[self.inactive_grid()][r][c] = next_gen_state
        # swap out the active grid
        self.active_grid = self.inactive_grid()

    def inactive_grid(self):
        """
        Helper function to get the index of the inactive grid
        If active frid is 0 will return 1 and vice-versa.

        :return:
        """
        # ((0 + 1) % 2 = 1) or ((1 + 1) % 2 = 0)
        return (self.active_grid + 1) % 2

    def handle_events(self):
        """
        Handle any key presses
        s - start/stop (pause) the game
        r - randomize the grid
        q - quit

        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print("key pressed")
                if event.unicode == 's':
                    print("Toggling pause.")
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True
                elif event.unicode == 'r':
                    print("Randomizing grid.")
                    self.active_grid = 0
                    self.set_grid(None, self.active_grid)  # Randomize
                    self.set_grid(0, self.inactive_grid())  # set to 0
                    self.draw_grid()
                elif event.unicode == 'q':
                    print("Exiting.")
                    self.game_over = True
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        """
        Kick-off the game and loop forever until quit state

        :return:
        """
        while True:
            if self.game_over:
                return

            self.handle_events()
            if self.paused:
                continue

            self.update_generation()
            self.draw_grid()
            self.cap_frame_rate()
        sys.exit()

    def cap_frame_rate(self):
        """
        If game is running too fast and updating frames too frequently,
        wait to maintain stable frame rate

        :return:
        """
        # cap frame rate. If time since last frame draw < 1/MAX_FPS of milliseconds, sleep for remaining time
        now = pygame.time.get_ticks()
        milliseconds_since_last_update = now - self.last_update_completed
        time_to_sleep = self.desired_milliseconds_between_updates - milliseconds_since_last_update
        if time_to_sleep > 0:
            pygame.time.wait(int(time_to_sleep))
        self.last_update_completed = now
