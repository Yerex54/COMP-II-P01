"""
Test.py — Unit tests for the Bloxorz project.

Verifies the correct behaviour of each component:
  - Block: moves and orientations
  - Board: cell validation and value lookup
  - Game: win, loss and move execution
  - Solver: BFS and A* find correct solutions
"""

from Block import Block
from Board import Board
from Game import Game
from Solver import Solver, bfs, astar

# Standard test board
TEST_BOARD = [
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 2, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 1, 9, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
]

passed = 0
failed = 0


def test(name, condition):
    """Records the result of a test."""
    global passed, failed
    if condition:
        print(f"  PASS  {name}")
        passed += 1
    else:
        print(f"  FAIL  {name}")
        failed += 1


# ---------------------------------------------------------------------------
# Block tests
# ---------------------------------------------------------------------------
print("\n-- Block tests --")

b = Block(3, 3, "upright")
test("Initial state: upright at (3,3)",
     b.status() == ((3, 3), (3, 3)))

b.move("right")
test("Upright + right → horizontal at (3,4)-(3,5)",
     b.orientation == "horizontal" and b.status() == ((3, 4), (3, 5)))

b2 = Block(3, 3, "upright")
b2.move("down")
test("Upright + down → vertical at (4,3)-(5,3)",
     b2.orientation == "vertical" and b2.status() == ((4, 3), (5, 3)))

b3 = Block(3, 3, "horizontal")
b3.move("right")
test("Horizontal + right → upright at (3,5)-(3,5)",
     b3.orientation == "upright" and b3.status() == ((3, 5), (3, 5)))

b4 = Block(3, 3, "horizontal")
b4.move("up")
test("Horizontal + up → horizontal at (2,3)-(2,4)",
     b4.orientation == "horizontal" and b4.status() == ((2, 3), (2, 4)))

b5 = Block(3, 3, "vertical")
b5.move("down")
test("Vertical + down → upright at (5,3)",
     b5.orientation == "upright" and b5.status() == ((5, 3), (5, 3)))

b6 = Block(3, 3, "vertical")
b6.move("right")
test("Vertical + right → vertical at (3,4)-(4,4)",
     b6.orientation == "vertical" and b6.status() == ((3, 4), (4, 4)))

# ---------------------------------------------------------------------------
# Board tests
# ---------------------------------------------------------------------------
print("\n-- Board tests --")

board = Board(TEST_BOARD)

test("check_tile(2) finds start position (1,1)",
     board.check_tile(2) == (1, 1))

test("check_tile(9) finds goal (4,7)",
     board.check_tile(9) == (4, 7))

test("valid_cell(1,1) → True (normal cell)",
     board.valid_cell(1, 1) == True)

test("valid_cell(0,3) → False (empty cell)",
     board.valid_cell(0, 3) == False)

test("valid_cell(-1,0) → False (out of bounds)",
     board.valid_cell(-1, 0) == False)

test("get_cell(1,1) → 2 (correct value)",
     board.get_cell(1, 1) == 2)

test("get_cell(0,3) → None (invalid cell)",
     board.get_cell(0, 3) is None)

# ---------------------------------------------------------------------------
# Game tests
# ---------------------------------------------------------------------------
print("\n-- Game tests --")

board = Board(TEST_BOARD)
game = Game(board)

test("Block starts upright at (1,1)",
     game.block.orientation == "upright" and
     game.block.row == 1 and game.block.col == 1)

test("Goal is at (4,7)",
     game.goal == (4, 7))

test("Initial position is valid",
     game.is_valid_position() == True)

test("Game not won at start",
     game.check_win() == False)

# Move to invalid position
board2 = Board(TEST_BOARD)
game2 = Game(board2)
game2.block.row = 0
game2.block.col = 3  # Empty cell
test("Invalid position correctly detected",
     game2.is_valid_position() == False)

# Simulate win
board3 = Board(TEST_BOARD)
game3 = Game(board3)
game3.block.row = 4
game3.block.col = 7
game3.block.orientation = "upright"
test("Win detected when block is upright on goal",
     game3.check_win() == True)

# ---------------------------------------------------------------------------
# Solver tests
# ---------------------------------------------------------------------------
print("\n-- Solver tests --")

board = Board(TEST_BOARD)
game = Game(board)
solver = Solver(game)

solution_bfs = solver.solve(algorithm="bfs")
test("BFS finds a solution",
     solution_bfs is not None)


board2 = Board(TEST_BOARD)
game2 = Game(board2)
solver2 = Solver(game2)
solution_astar = solver2.solve(algorithm="astar")
test("A* finds a solution",
     solution_astar is not None)

test("A* and BFS find equally short paths",
     solution_bfs is not None and solution_astar is not None and
     len(solution_bfs) == len(solution_astar))

# Verify that executing the BFS solution actually wins the game
board3 = Board(TEST_BOARD)
game3 = Game(board3)
if solution_bfs:
    for move in solution_bfs:
        game3.next_move(move)
test("Executing BFS solution results in a win",
     game3.check_win())

# ---------------------------------------------------------------------------
# Final result
# ---------------------------------------------------------------------------
print(f"\n{'='*40}")
print(f"  Result: {passed} passed | {failed} failed")
print(f"{'='*40}\n")
