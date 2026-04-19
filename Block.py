class Block:
    def __init__(self, row, col, orientation):
        self.orientation = orientation
        self.row = row
        self.col = col

    def status(self):
        if self.orientation == "upright":
            return ((self.row, self.col), (self.row, self.col))
        if self.orientation == "horizontal":
            return ((self.row, self.col), (self.row, self.col+1))
        if self.orientation == "vertical":
            return ((self.row, self.col), (self.row+1, self.col))
        
    def move(self, direction):
        if self.orientation == "upright":
            if direction == "up":
                self.orientation = "vertical"
                self.row -= 2
            elif direction == "down":
                self.orientation = "vertical"
                self.row += 2
            elif direction == "left":
                self.orientation = "horizontal"
                self.col -= 2
            elif direction == "right":
                self.orientation = "horizontal"
                self.col += 2
        elif self.orientation == "horizontal":
            if direction == "up":
                self.orientation = "horizontal"
                self.row -= 1
            elif direction == "down":
                self.orientation = "horizontal"
                self.row += 1
            elif direction == "left":
                self.orientation = "upright"
                self.col -= 1
            elif direction == "right":
                self.orientation = "upright"
                self.col += 1
        elif self.orientation == "vertical":
            if direction == "up":
                self.orientation = "upright"
                self.row -= 1
            elif direction == "down":
                self.orientation = "upright"
                self.row += 1
            elif direction == "left":
                self.orientation = "vertical"
                self.col -= 1
            elif direction == "right":
                self.orientation = "vertical"
                self.col += 1