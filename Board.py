class Board:
    def __init__(self, board):
        self.board = board

    def block(self):
        row = len(self.board)
        for i in range(row):
            col = len(self.board[i])
            for j in range(col):
                if self.board[i][j] == 2:
                    print(f"Block at position ({i},{j})")

    def goal(self):
        row = len(self.board)
        for i in range(row):
            col = len(self.board[i])
            for j in range(col):
                if self.board[i][j] == 9:
                    print(f"Goal at position ({i},{j})")

    def empty_cell(self, i, j):
        if 0 <= i < len(self.board) and 0 <= j < len(self.board[i]):
            return self.board[i][j] == 0
        return False
    def display(self):
        for row in self.board:
            print(*row)

b1 = Board([
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 2, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 1, 9, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
])

b1.block()
b1.goal()
print(b1.empty_cell(1,2))
b1.display()