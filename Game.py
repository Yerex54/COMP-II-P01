class Game:
    def __init__(self, board):
        self.board = board
        start = board.check_tile(2)
        self.block = Block(start[0], start[1], "upright")
        self.moves = 0
        self.goal = board.check_tile(9)

    def display(self):
        self.board.display()

    def is_valid_position(self):
        for (r, c) in self.block.status():
            if not self.board.valid_cell(r, c):
                return False
        return True
    
    def next_move(self, direction):
        self.block.move(direction)
        self.moves += 1
        return self.is_valid_position()
    
    def check_win(self):
        if self.block.orientation == "upright":
            return self.block.row == self.goal[0] and self.block.col == self.goal[1]
        return False
    
    def check_loss(self):
        return not self.is_valid_position()
    
    def start(self):
        while True:
            self.display()
            move = input("Enter move (up, down, left, right): ")
            self.next_move(move)
            if self.check_win():
                print(f"Congratulations! You won in {self.moves} moves!")
                choice = input("Restart (r), Next level (n), or Quit (q)? ")
                if choice.upper() == "R":
                    self.restart()
                elif choice.upper() == "N":
                    pass
                else:
                    self.quit()
                break
            if self.check_loss():
                print("Game over! You lost.")
                choice = input("Restart (r), Next level (n), or Quit (q)? ")
                if choice.upper() == "R":
                    self.restart()
                else:
                    self.quit()
                break

    def restart(self):
        start = self.board.check_tile(2)
        self.block = Block(start[0], start[1], "upright")
        self.moves = 0
        self.start()
    
    def level(self, new_board):
        self.board = new_board
        start = self.board.check_tile(2)
        self.block = Block(start[0], start[1], "upright")
        self.moves = 0
        self.start()
        
    def quit(self):
        if input("Are you sure you want to quit? (y/n): ").lower() == "y":
            print("Thanks for playing!")
            exit()