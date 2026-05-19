# Required imports — without these, Python cannot find the other classes
from Block import Block
from Board import Board


class Game:
    """
    Controls the main logic of the Bloxorz game.

    Connects the board (Board) with the block (Block) and manages:
      - player moves
      - win and loss detection
      - restart and level switching
    """

    def __init__(self, board):
        """
        Initializes the game with a given board.

        Automatically finds the start position (cell with value 2)
        and the goal position (cell with value 9).

        Args:
            board (Board): the game board
        """
        self.board = board
        start = board.check_tile(2)       # Find where the block starts
        self.block = Block(start[0], start[1], "upright")  # Block starts upright
        self.moves = 0                    # Move counter
        self.goal = board.check_tile(9)   # Position the block must reach

    def display(self):
        """
        Prints the board with the current block position.

        The block is shown as 'B', the goal as 'X', empty cells as '.'.
        """
        # Create a visual copy of the board without modifying the original
        visual = [row[:] for row in self.board.board]

        # Mark the cells occupied by the block with value 8 (displayed as 'B')
        for (r, c) in self.block.status():
            if 0 <= r < len(visual) and 0 <= c < len(visual[r]):
                visual[r][c] = 8

        # Print the board row by row
        print()
        for row in visual:
            line = ""
            for cell in row:
                if cell == 0:
                    line += ".  "   # Empty cell
                elif cell == 8:
                    line += "B  "   # Block position
                elif cell == 9:
                    line += "X  "   # Goal
                elif cell == 2:
                    line += "S  "   # Start position
                else:
                    line += "1  "   # Normal cell
            print(line)
        print(f"Moves: {self.moves} | Orientation: {self.block.orientation}")
        print(f"Position: {self.block.status()[0]} | Goal: {self.goal}")
        print()

    def is_valid_position(self):
        """
        Checks whether the current block position is valid on the board.

        Returns:
            bool: True if all cells occupied by the block are valid
        """
        for (r, c) in self.block.status():
            if not self.board.valid_cell(r, c):
                return False
        return True

    def next_move(self, direction):
        """
        Executes a move and checks whether the new position is valid.

        Args:
            direction (str): move direction ("up", "down", "left", "right")

        Returns:
            bool: True if the new position is valid, False if the block fell
        """
        self.block.move(direction)
        self.moves += 1
        return self.is_valid_position()

    def check_win(self):
        """
        Checks whether the player has won.

        The player wins when the block is upright exactly on the goal cell.

        Returns:
            bool: True if the game is won
        """
        if self.block.orientation == "upright":
            return (self.block.row == self.goal[0] and
                    self.block.col == self.goal[1])
        return False

    def check_loss(self):
        """
        Checks whether the player has lost (block fell off the board).

        Returns:
            bool: True if the block is in an invalid position
        """
        return not self.is_valid_position()

    def restart(self):
        """Restarts the game on the same board, returning to the start."""
        start = self.board.check_tile(2)
        self.block = Block(start[0], start[1], "upright")
        self.moves = 0

    def level(self, new_board):
        """
        Loads a new level with a different board.

        Args:
            new_board (Board): the new board to use
        """
        self.board = new_board
        start = self.board.check_tile(2)
        self.block = Block(start[0], start[1], "upright")
        self.moves = 0
        self.goal = self.board.check_tile(9)

    def quit(self):
        """Ends the game after player confirmation."""
        answer = input("Are you sure you want to quit? (y/n): ").lower()
        if answer == "y":
            print("Thanks for playing Bloxorz!")
            exit()

    def start(self):
        """
        Starts the main game loop.

        Displays the board, asks the player for a move,
        and checks for win or loss after each turn.
        """
        print("\n=== BLOXORZ ===")
        print("Moves: up, down, left, right | Quit: quit")
        print("B = block | X = goal | S = start | . = empty")

        while True:
            self.display()

            # Ask for the next move
            move = input("Move: ").strip().lower()

            if move == "quit" or move == "q":
                self.quit()
                break
            if move == "restart" or move == "r":
                self.restart()
                continue
            # Validate the move before executing
            if move not in ["up", "down", "left", "right"]:
                print("Invalid move! Use: up, down, left, right")
                continue

            # Execute the move
            valid = self.next_move(move)

            # Check for win
            if self.check_win():
                self.display()
                print(f"Congratulations! You won in {self.moves} moves!")
                choice = input("Restart (r) or Quit (q)? ").lower()
                if choice == "r":
                    self.restart()
                    continue
                else:
                    self.quit()
                

            # Check for loss (block fell off)
            if not valid:
                self.display()
                print("The block fell! You lost.")
                choice = input("Restart (r) or Quit (q)? ").lower()
                if choice == "r":
                    self.restart()
                    continue
                else:
                    self.quit()
                
