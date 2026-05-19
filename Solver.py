"""
Solver.py — Search algorithms to solve Bloxorz automatically.

This module implements two algorithms:
  1. BFS  (Breadth-First Search)   — explores states level by level
  2. A*   (A-Star)                 — informed search using a heuristic

Both find the path from the start to the goal,
returning the list of moves to perform.
"""

from collections import deque   # Efficient queue for BFS
import heapq                    # Priority queue for A*


# ---------------------------------------------------------------------------
# Helper functions shared by both algorithms
# ---------------------------------------------------------------------------

def get_cells(row, col, orientation):
    """
    Returns the cells occupied by the block given its state.

    Args:
        row (int): reference row
        col (int): reference column
        orientation (str): "upright", "horizontal", or "vertical"

    Returns:
        list of tuple: list of (row, col) for each occupied cell
    """
    if orientation == "upright":
        return [(row, col), (row, col)]          # Standing: 1 cell
    elif orientation == "horizontal":
        return [(row, col), (row, col + 1)]      # Horizontal: 2 cells same row
    elif orientation == "vertical":
        return [(row, col), (row + 1, col)]      # Vertical: 2 cells same column


def apply_move(row, col, orientation, direction):
    """
    Computes the new block state after a move.

    Does not modify any object — purely calculates and returns the new state.
    This replicates the Block.move() logic as a pure function.

    Args:
        row (int): current row
        col (int): current column
        orientation (str): current orientation
        direction (str): "up", "down", "left", or "right"

    Returns:
        tuple: (new_row, new_col, new_orientation)
    """
    if orientation == "upright":
        if direction == "up":
            return (row - 2, col, "vertical")
        elif direction == "down":
            return (row + 1, col, "vertical")
        elif direction == "left":
            return (row, col - 2, "horizontal")
        elif direction == "right":
            return (row, col + 1, "horizontal")

    elif orientation == "horizontal":
        if direction == "up":
            return (row - 1, col, "horizontal")
        elif direction == "down":
            return (row + 1, col, "horizontal")
        elif direction == "left":
            return (row, col - 1, "upright")
        elif direction == "right":
            return (row, col + 2, "upright")

    elif orientation == "vertical":
        if direction == "up":
            return (row - 1, col, "upright")
        elif direction == "down":
            return (row + 2, col, "upright")
        elif direction == "left":
            return (row, col - 1, "vertical")
        elif direction == "right":
            return (row, col + 1, "vertical")


def is_valid_state(board, row, col, orientation):
    """
    Checks whether a state is valid on the given board.

    A state is valid if all cells the block occupies exist
    on the board and are not empty (value 0).

    Args:
        board (Board): the game board
        row, col, orientation: state to check

    Returns:
        bool: True if the state is valid
    """
    for (r, c) in get_cells(row, col, orientation):
        if not board.valid_cell(r, c):
            return False
    return True


def is_goal(row, col, orientation, goal):
    """
    Checks whether the current state is the winning state.

    The block must be upright exactly on the goal cell.

    Args:
        row, col, orientation: current state
        goal (tuple): (row, col) of the goal cell

    Returns:
        bool: True if the block has won
    """
    return orientation == "upright" and row == goal[0] and col == goal[1]


# ---------------------------------------------------------------------------
# Algorithm 1: BFS — Breadth-First Search
# ---------------------------------------------------------------------------

def bfs(board, start, goal):
    """
    Finds the shortest path using BFS (Breadth-First Search).

    BFS explores all states at distance 1, then distance 2, and so on.
    This guarantees that the first path found is the shortest.

    How it works:
      - Start from the initial state
      - Store all unexplored states in a queue
      - Take the first from the queue, test 4 possible moves
      - If the goal is found, return the path
      - If the state was already visited, skip it (avoids cycles)

    Args:
        board (Board): game board
        start (tuple): (row, col, orientation) of the initial state
        goal (tuple): (row, col) of the goal cell

    Returns:
        list or None: list of moves ["up", "right", ...] or None if no solution
    """
    start_row, start_col, start_orient = start

    # BFS queue: each element is (current_state, path_so_far)
    # deque is used because removing from the front is O(1)
    queue = deque()
    queue.append(((start_row, start_col, start_orient), []))

    # Set of already visited states (avoids revisiting the same state)
    visited = set()
    visited.add((start_row, start_col, start_orient))

    nodes_explored = 0  # Counter for statistics

    while queue:
        # Remove the first state from the queue
        (row, col, orient), path = queue.popleft()
        nodes_explored += 1

        # Test all 4 possible moves
        for direction in ["up", "down", "left", "right"]:
            new_row, new_col, new_orient = apply_move(row, col, orient, direction)

            # Skip invalid states (block out of bounds or on empty cell)
            if not is_valid_state(board, new_row, new_col, new_orient):
                continue

            new_path = path + [direction]

            # Check if we reached the goal
            if is_goal(new_row, new_col, new_orient, goal):
                print(f"[BFS] Solution found! "
                      f"Moves: {len(new_path)} | "
                      f"Nodes explored: {nodes_explored}")
                return new_path

            # Add to queue if not yet visited
            new_state = (new_row, new_col, new_orient)
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, new_path))

    print(f"[BFS] No solution found. Nodes explored: {nodes_explored}")
    return None  # No solution exists


# ---------------------------------------------------------------------------
# Algorithm 2: A* — Informed Search with Heuristic
# ---------------------------------------------------------------------------

def heuristic(row, col, orientation, goal):
    """
    Heuristic for A*: Manhattan distance to the goal.

    Manhattan distance is the sum of absolute differences
    between rows and columns — like moving on a grid without diagonals.

    For non-upright blocks, we use the average position of both cells
    to get a more accurate estimate.

    Args:
        row, col, orientation: current state
        goal (tuple): (row, col) of the goal cell

    Returns:
        float: estimated remaining cost
    """
    cells = get_cells(row, col, orientation)

    # Average position of the block
    avg_row = sum(r for r, c in cells) / len(cells)
    avg_col = sum(c for r, c in cells) / len(cells)

    # Manhattan distance
    return abs(avg_row - goal[0]) + abs(avg_col - goal[1])


def astar(board, start, goal):
    """
    Finds the optimal path using A* (A-Star).

    A* is smarter than BFS because it uses a heuristic to explore
    the most promising states first.

    How it works:
      - For each state, compute f = g + h where:
          g = number of moves already made (real cost)
          h = estimated distance to the goal (heuristic)
      - Always explore the state with the lowest f first
      - This guides the search in the right direction

    Args:
        board (Board): game board
        start (tuple): (row, col, orientation) of the initial state
        goal (tuple): (row, col) of the goal cell

    Returns:
        list or None: list of moves or None if no solution
    """
    start_row, start_col, start_orient = start

    # Initial cost values
    g_start = 0
    h_start = heuristic(start_row, start_col, start_orient, goal)
    f_start = g_start + h_start

    # Priority queue: (f, g, state, path)
    # Python's heapq sorts by the first element (f)
    queue = []
    heapq.heappush(queue, (f_start, g_start,
                           (start_row, start_col, start_orient), []))

    # Dictionary: state → best g known for that state
    best_g = {(start_row, start_col, start_orient): 0}

    nodes_explored = 0

    while queue:
        # Remove the state with the lowest f from the queue
        f, g, (row, col, orient), path = heapq.heappop(queue)
        nodes_explored += 1

        # If we already found a better path to this state, skip it
        if g > best_g.get((row, col, orient), float('inf')):
            continue

        # Test all 4 possible moves
        for direction in ["up", "down", "left", "right"]:
            new_row, new_col, new_orient = apply_move(row, col, orient, direction)

            if not is_valid_state(board, new_row, new_col, new_orient):
                continue

            new_g = g + 1  # Each move has cost 1
            new_path = path + [direction]

            # Check for win
            if is_goal(new_row, new_col, new_orient, goal):
                print(f"[A*]  Solution found! "
                      f"Moves: {len(new_path)} | "
                      f"Nodes explored: {nodes_explored}")
                return new_path

            # Only explore if this is the best known path to this state
            new_state = (new_row, new_col, new_orient)
            if new_g < best_g.get(new_state, float('inf')):
                best_g[new_state] = new_g
                h = heuristic(new_row, new_col, new_orient, goal)
                new_f = new_g + h
                heapq.heappush(queue, (new_f, new_g, new_state, new_path))

    print(f"[A*] No solution found. Nodes explored: {nodes_explored}")
    return None


# ---------------------------------------------------------------------------
# Solver class — main interface
# ---------------------------------------------------------------------------

class Solver:
    """
    Main interface to automatically solve a Bloxorz game.

    Uses BFS or A* to find the sequence of moves
    that takes the block from start to goal.
    """

    def __init__(self, game):
        """
        Initializes the solver with a configured game instance.

        Args:
            game (Game): the game instance to solve
        """
        self.game = game
        self.board = game.board
        self.start = (game.block.row, game.block.col, game.block.orientation)
        self.goal = game.goal

    def solve(self, algorithm="bfs"):
        """
        Solves the game using the chosen algorithm.

        Args:
            algorithm (str): "bfs" or "astar"

        Returns:
            list or None: sequence of moves, or None if no solution
        """
        print(f"\nSolving with {algorithm.upper()}...")
        print(f"Start: {self.start} | Goal: {self.goal}")

        if algorithm == "bfs":
            return bfs(self.board, self.start, self.goal)
        elif algorithm == "astar":
            return astar(self.board, self.start, self.goal)
        else:
            print(f"Unknown algorithm '{algorithm}'. Use 'bfs' or 'astar'.")
            return None

    def compare(self):
        """
        Runs both algorithms and compares their results.
        Useful for the report — shows the efficiency difference.
        """
        print("\n" + "="*50)
        print("ALGORITHM COMPARISON")
        print("="*50)

        solution_bfs = bfs(self.board, self.start, self.goal)
        solution_astar = astar(self.board, self.start, self.goal)

        if solution_bfs:
            print(f"\nBFS  → {solution_bfs}")
        if solution_astar:
            print(f"A*   → {solution_astar}")

        if solution_bfs and solution_astar:
            if len(solution_bfs) == len(solution_astar):
                print("\nBoth algorithms found the shortest path!")
            else:
                diff = abs(len(solution_bfs) - len(solution_astar))
                print(f"\nDifference: {diff} move(s)")

        return solution_bfs, solution_astar
    
    def replay(self, solution):
        """
        Replays the solution visually, step by step.

        Args:
            solution (list): list of move strings to execute
        """
        import time  
        print("\nReplaying solution...\n")
        self.game.display()
        for i, move in enumerate(solution):
            input(f"  Step {i+1}/{len(solution)} — Press Enter for '{move}'...")
            self.game.next_move(move)
            self.game.display()
        print("Replay complete!")   

# ---------------------------------------------------------------------------
# Quick test (only runs if this file is executed directly)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from Board import Board
    from Game import Game

    board = Board([
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 2, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 9, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    ])

    game = Game(board)
    solver = Solver(game)
    solver.compare()
