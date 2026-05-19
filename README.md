# Bloxorz — Computação II Project

**Nova IMS — Information Management School**  
Information Systems and Technology | 2025/2026

---

## Project Description

Implementation of the **Bloxorz** puzzle game in Python. The player controls a rectangular block on a suspended board and must make it fall upright into a specific hole, without going out of bounds.

The project also includes an **automatic solver** with two search algorithms: BFS and A*.

---

## How to Run

```bash
python Main.py
```

On startup, choose one of the following options:

| Option | Description |
|--------|-------------|
| 1 | Play manually |
| 2 | Watch automatic solution (BFS) — replays solution step by step (press Enter to advance) |
| 3 | Watch automatic solution (A*) — replays solution step by step (press Enter to advance) |
| 4 | Compare both algorithms |
| 0 | Exit |

**Valid moves:** `up`, `down`, `left`, `right`

---

## Board Representation

| Symbol | Meaning |
|--------|---------|
| `1` | Normal cell |
| `.` | Empty cell (block falls) |
| `S` | Block start position |
| `X` | Goal cell |
| `B` | Current block position |

---

## Project Structure

```
├── Main.py      # Entry point — main menu and level definitions
├── Block.py     # Block class: position, orientation, movement logic
├── Board.py     # Board class: cell validation and value lookup
├── Game.py      # Game logic: win/loss detection, display, interaction
├── Solver.py    # BFS and A* algorithms for automatic solving
├── Test.py      # Unit tests (25 tests, all passing)
└── README.md    # This file
```

---

## Search Algorithms

### BFS — Breadth-First Search

Explores states in order of increasing distance from the start.  
**Guarantees** finding the path with the fewest moves.  
Each state is represented as `(row, col, orientation)`.

### A* — A-Star (Informed Search)

Uses the evaluation function `f = g + h`:
- `g` = number of moves already made (actual cost)
- `h` = Manhattan distance to the goal (admissible heuristic)

Guides the search towards the most promising states, generally more efficient than BFS on larger boards.

---

## Test Results

```
-- Block tests --   7 tests  PASS
-- Board tests --   7 tests  PASS
-- Game tests  --   6 tests  PASS
-- Solver tests--   4 tests  PASS

Result: 24 passed | 0 failed
```

---

## Sample Output

```
Level 1 — 6x10 board:

[BFS]  Moves: 7 | Nodes explored: 48
[A*]   Moves: 7 | Nodes explored: 10

BFS sequence: right -> down -> down -> right -> right -> down -> right
A* : right -> right -> down -> right -> right -> right -> down
```

---

## Requirements

- Python 3.8 or higher
- No external libraries (uses only `collections` and `heapq` from the standard library)

---

## Author

Project developed for the Computação II course  
Nova IMS — Information Management School — 2025/2026
