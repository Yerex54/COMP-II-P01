class Block:
    """
    Represents the block in the Bloxorz game.

    The block can be in three orientations:
      - "upright"    : standing up, occupies 1 cell
      - "horizontal" : lying flat horizontally, occupies 2 cells (same row)
      - "vertical"   : lying flat vertically, occupies 2 cells (same column)

    Attributes:
        row (int): row of the reference cell (top-left cell)
        col (int): column of the reference cell
        orientation (str): current orientation of the block
    """

    def __init__(self, row, col, orientation):
        """Initializes the block with position and orientation."""
        self.row = row
        self.col = col
        self.orientation = orientation

    def status(self):
        """
        Returns the two cells the block currently occupies.

        Returns:
            tuple: pair of (row, col) for each occupied cell.
                   If upright, both cells are the same.
        """
        if self.orientation == "upright":
            # Standing: occupies only 1 cell (returned twice for consistency)
            return ((self.row, self.col), (self.row, self.col))
        if self.orientation == "horizontal":
            # Flat horizontal: left cell and right cell
            return ((self.row, self.col), (self.row, self.col + 1))
        if self.orientation == "vertical":
            # Flat vertical: top cell and bottom cell
            return ((self.row, self.col), (self.row + 1, self.col))

    def move(self, direction):
        """
        Moves the block in a given direction, updating position and orientation.

        Movement rules:
          - Upright block: tips over → becomes flat
          - Horizontal block: left/right slides; up/down stands upright
          - Vertical block: up/down slides; left/right stands upright

        Args:
            direction (str): "up", "down", "left", or "right"
        """
        if self.orientation == "upright":
            if direction == "up":
                # Tips backward → vertical covering (row-2) and (row-1)
                self.orientation = "vertical"
                self.row -= 2
            elif direction == "down":
                # Tips forward → vertical covering (row+1) and (row+2)
                self.orientation = "vertical"
                self.row += 1
            elif direction == "left":
                # Tips left → horizontal covering (col-2) and (col-1)
                self.orientation = "horizontal"
                self.col -= 2
            elif direction == "right":
                # Tips right → horizontal covering (col+1) and (col+2)
                self.orientation = "horizontal"
                self.col += 1


        elif self.orientation == "horizontal":
            # Block lying flat horizontally (occupies col and col+1)
            if direction == "up":
                # roll upward →  stays horizontal (row-1)
                self.orientation = "horizontal"
                self.row -= 1
            elif direction == "down":
                # roll downward →  stays horizontal (row+1)
                self.orientation = "horizontal"
                self.row += 1
            elif direction == "left":
                # Tips left → becomes upright (row, col-1)
                self.orientation = "upright"
                self.col -= 1
            elif direction == "right":
                # Tips right → becomes upright (row, col+2)
                self.orientation = "upright"
                self.col += 2

        elif self.orientation == "vertical":
            # Block lying flat vertically (occupies row and row+1)
            if direction == "up":
                # Tips upward → becomes upright (row-1, col)
                self.orientation = "upright"
                self.row -= 1
            elif direction == "down":
                # Tips downward → becomes upright (row+1, col)
                self.orientation = "upright"
                self.row += 2
            elif direction == "left":
                # slide left → stays vertical (row, col-1)
                self.orientation = "vertical"
                self.col -= 1
            elif direction == "right":
                # slide right → stays vertical (row, col+1)
                self.orientation = "vertical"
                self.col += 1
