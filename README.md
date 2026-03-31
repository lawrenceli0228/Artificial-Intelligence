# Artificial Intelligence — COMP SCI 3007

University of Adelaide, Semester 1 2022

Three assignments covering core AI techniques: search, machine learning, and probabilistic reasoning.

---

## Assignment 1 — Pathfinding

Finds the lowest-cost path on a 2D elevation map using three search algorithms.

| Algorithm | Description |
|-----------|-------------|
| BFS | Breadth-First Search |
| UCS | Uniform-Cost Search |
| A* | A* with Euclidean or Manhattan heuristic |

**Cost model:** moving uphill costs `1 + elevation difference`; level or downhill costs `1`.

```bash
python pathfinder.py <map> <algorithm> [heuristic]
# e.g. python pathfinder.py map.txt astar manhattan
```

→ [`AI_assignment1/`](AI_assignment1/)

---

## Assignment 2 — Decision Tree (Wine Quality)

Predicts white wine quality (5 / 6 / 7) from 11 physicochemical features using a decision tree built from scratch with information gain splitting.

```bash
python winequality.py <train> <test> <minleaf>
# e.g. python winequality.py train test-sample 30
```

→ [`AI_assignment2/`](AI_assignment2/)

---

## Assignment 3 — Robot Localisation (Viterbi)

Estimates the robot's position on a 2D grid from noisy NESW sensor readings using the **Viterbi forward algorithm** on a Hidden Markov Model.

```bash
python viterbi.py <input_file>
# outputs output.npz — one probability map per time step
```

→ [`AI_assignment3/`](AI_assignment3/)

---

## Requirements

- Python 3.6+
- NumPy
