class Board:
    """
    Represents the Bloxorz game board.

    The board is a 2D matrix of integers where each value means:
      0 → empty cell (block falls if it lands here)
      1 → normal cell (block can stand here)
      2 → starting position of the block
      9 → goal cell (block must fall here while upright to win)

    Attributes:
        board (list[list[int]]): matrix representing the board layout
    """

    def __init__(self, board_matrix):
        """Initializes the board with the given matrix."""
        self.board = board_matrix

    def check_tile(self, value):
        """
        Finds the first cell with a specific value.

        Used to locate the start position (value 2) and the goal (value 9).

        Args:
            value (int): value to search for in the matrix

        Returns:
            tuple: (row, col) of the found cell, or None if not found
        """
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == value:
                    return (i, j)
        return None

    def valid_cell(self, i, j):
        """
        Checks if a cell is valid (within bounds and not empty).

        Args:
            i (int): row index
            j (int): column index

        Returns:
            bool: True if the cell exists and is not 0, False otherwise
        """
        if 0 <= i < len(self.board) and 0 <= j < len(self.board[i]):
            return self.board[i][j] != 0
        return False

    def get_cell(self, i, j):
        """
        Returns the value of a cell if it is valid.

        Args:
            i (int): row index
            j (int): column index

        Returns:
            int or None: cell value, or None if the position is invalid
        """
        if self.valid_cell(i, j):
            return self.board[i][j]
        return None

    def display(self):
        """
        Prints the board to the console in a readable format.
        Empty cells (0) are shown as dots for better visualization.
        """
        for row in self.board:
            print(" ".join(str(cell) if cell != 0 else "." for cell in row))


# --- Quick test (only runs if this file is executed directly) ---
if __name__ == "__main__":
    b1 = Board([
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 2, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 9, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    ])
    print("Start position:", b1.check_tile(2))   # → (1, 1)
    print("Goal position:", b1.check_tile(9))    # → (4, 7)
    print("Cell (1,2) valid?", b1.valid_cell(1, 2))  # → True
    print("\nBoard:")
    b1.display()
