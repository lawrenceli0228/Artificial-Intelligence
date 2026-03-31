# AI Assignment 1 - Pathfinding

University of Adelaide — Artificial Intelligence (Semester 1, 2022)

## Overview

This program solves a pathfinding problem on a 2D map using three search algorithms:

- **BFS** — Breadth-First Search
- **UCS** — Uniform-Cost Search
- **A\*** — A* Search (with Euclidean or Manhattan heuristic)

The map consists of elevation values (0–9) and obstacles marked as `X`. The goal is to find a path from a start position to an end position using 4-connectedness (up, down, left, right only).

## Path Cost

The cost between two adjacent positions is defined as:

- `1 + (destination elevation - source elevation)` — if moving **uphill**
- `1` — if moving **level** or **downhill**

Shorter paths that avoid climbing cost less.

## Usage

```bash
python pathfinder.py [map] [algorithm] [heuristic]
```

| Argument | Description |
|---|---|
| `[map]` | Path to the map text file |
| `[algorithm]` | `bfs`, `ucs`, or `astar` |
| `[heuristic]` | `euclidean` or `manhattan` (only required for `astar`) |

### Examples

```bash
# Breadth-First Search
python pathfinder.py map.txt bfs

# Uniform-Cost Search
python pathfinder.py map.txt ucs

# A* with Manhattan distance heuristic
python pathfinder.py map.txt astar manhattan

# A* with Euclidean distance heuristic
python pathfinder.py map.txt astar euclidean
```

## Map File Format

```
10 10        <- rows cols
1 1          <- start position (row col), 1-indexed
10 10        <- end position (row col), 1-indexed
1 1 1 1 1 1 4 7 8 X
1 1 1 1 1 1 1 5 8 8
...
```

- Elevation values are integers from `0` to `9`
- `X` represents an obstacle that cannot be traversed

## Output

The program prints the map to standard output with the path marked by `*`:

```
* 1 1 1 1 1 4 7 8 X
* 1 1 1 1 1 1 5 8 8
* 1 1 1 1 1 1 4 6 7
...
```

If no path exists, the program prints:

```
null
```

## Requirements

- Python 3
- NumPy

## File Structure

```
AI_assignment1/
├── pathfinder.py   # Main program
├── map.txt         # Test map 1 (10x10)
├── map2.txt        # Test map 2 (12x13)
└── README.md
```
