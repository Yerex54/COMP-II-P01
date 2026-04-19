class Board:
    def __init__(self, board):
        self.board = board

    def check_tile(self, value):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == value:
                    return (i, j)
        return None

    def valid_cell(self, i, j):
        if 0 <= i < len(self.board) and 0 <= j < len(self.board[i]):
            return self.board[i][j] != 0
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

if __name__ == "__main__":
    b1.check_tile(2)
    b1.check_tile(9)
    print(b1.valid_cell(1, 2))
    b1.display()