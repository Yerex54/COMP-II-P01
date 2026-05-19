"""
Main.py — Entry point for the Bloxorz game.

Run this file to start the game:
    python Main.py

Available options:
  1. Play manually
  2. Watch automatic solution (BFS)
  3. Watch automatic solution (A*)
  4. Compare both algorithms
"""

from Board import Board
from Game import Game
from Solver import Solver


# ---------------------------------------------------------------------------
# Level definitions
# ---------------------------------------------------------------------------

LEVELS = {
    1: [
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 2, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 9, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    ],
    2: [
        [0, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 2, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 9, 1],
        [0, 0, 0, 0, 0, 0, 1, 0],
    ],
}


def show_menu():
    """Displays the main menu."""
    print("\n" + "="*45)
    print("        BLOXORZ — Main Menu")
    print("="*45)
    print("  1. Play manually")
    print("  2. Watch solution (BFS)")
    print("  3. Watch solution (A*)")
    print("  4. Compare BFS vs A*")
    print("  0. Exit")
    print("="*45)


def choose_level():
    """Asks the user to choose a level."""
    print(f"\nAvailable levels: {list(LEVELS.keys())}")
    while True:
        try:
            level = int(input("Choose a level: "))
            if level in LEVELS:
                return level
            print(f"Invalid level. Choose from {list(LEVELS.keys())}.")
        except ValueError:
            print("Please enter a valid number.")


def show_solution(solution, algorithm):
    """Displays the solution step by step in a readable format."""
    if not solution:
        print("No solution found.")
        return

    print(f"\n{'='*45}")
    print(f"  Solution found by {algorithm}")
    print(f"{'='*45}")
    print(f"  Total moves: {len(solution)}")
    print(f"  Sequence: {' -> '.join(solution)}")
    print(f"{'='*45}\n")


def main():
    """Main function — controls the program flow."""
    print("\nWelcome to BLOXORZ!")
    print("Goal: make the block fall into the hole (X) while standing upright.")

    while True:
        show_menu()

        try:
            option = int(input("\nChoose an option: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if option == 0:
            print("\nGoodbye!")
            break

        elif option == 1:
            # Manual play mode
            level = choose_level()
            board = Board(LEVELS[level])
            game = Game(board)
            game.start()

        elif option == 2:
            # Automatic solution with BFS
            level = choose_level()
            board = Board(LEVELS[level])
            game = Game(board)
            solver = Solver(game)
            solution = solver.solve(algorithm="bfs")
            show_solution(solution, "BFS")
            if solution:
                solver.replay(solution)
                
        elif option == 3:
            # Automatic solution with A*
            level = choose_level()
            board = Board(LEVELS[level])
            game = Game(board)
            solver = Solver(game)
            solution = solver.solve(algorithm="astar")
            show_solution(solution, "A*")
            if solution:
                solver.replay(solution)

        elif option == 4:
            # Compare both algorithms
            level = choose_level()
            board = Board(LEVELS[level])
            game = Game(board)
            solver = Solver(game)
            solver.compare()

        else:
            print("Invalid option. Choose between 0 and 4.")


# Only runs main() if this file is executed directly
if __name__ == "__main__":
    main()
