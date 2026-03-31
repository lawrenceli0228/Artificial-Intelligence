# AI Assignment 3 — Robot Localisation (Viterbi Algorithm)

University of Adelaide — COMP SCI 3007 Artificial Intelligence, Semester 1 2022

## Overview

Robot localisation using the **Viterbi forward algorithm** on a Hidden Markov Model (HMM). Given a 2D grid map and a sequence of noisy sensor readings, the program estimates the probability of the robot being at each position at each time step.

## Problem Setup

- The map is a 2D grid where `0` = traversable, `X` = obstacle.
- The robot moves with equal probability to any adjacent traversable cell.
- Sensors report whether obstacles exist to the **N, E, S, W** — with an error rate `ε`.
- The emission probability for a state given an observation is: `P(e|x) = (1-ε)^(4-d) * ε^d`, where `d` is the number of sensor directions reporting incorrectly.

## Algorithm

Implements **Algorithm 1: Viterbi forward** to compute a trellis matrix:

1. Initialise each state with `π_i * Em[i][y_1]` (uniform prior × emission).
2. For each subsequent observation, propagate: `trellis[i][j] = max_k(trellis[k][j-1] * Tm[k→i] * Em[i][y_j])`.
3. Map each column of the trellis back onto the grid (obstacles remain 0).

## Usage

```bash
python viterbi.py <input_file>
```

Output is written to `output.npz` in the current directory.

## Input Format

```
<rows> <cols>
<map row 1>        # space-separated 0 or X
...
<map row n>
<num_observations>
<obs_1>            # 4-bit NESW string, e.g. 1011
...
<obs_t>
<error_rate>       # float, e.g. 0.2
```

**Example (`testcase.txt`):**
```
4 10
0 0 0 0 X 0 0 0 0 X
X X 0 0 X 0 X X 0 X
X 0 0 0 X 0 X X 0 0
0 0 X 0 0 0 X 0 0 0
4
1011
1010
1000
1100
0.2
```

## Output

`output.npz` — a NumPy archive containing `t` arrays (one per time step), each of shape `(rows, cols)`. Obstacle cells are `0.0`; traversable cells hold their Viterbi probability.

Load with:
```python
import numpy as np
data = np.load("output.npz")
maps = [data[k] for k in data]  # list of (rows x cols) arrays
```

## Files

| File | Description |
|------|-------------|
| `viterbi.py` | Main submission — Viterbi forward algorithm |
| `testcase.txt` | Sample input (4×10 map, 4 observations, ε=0.2) |
| `case1.txt` | Larger test input (14×18 map, 16 observations, ε=0.4) |
| `output.npz` | Generated output from last run |
| `test.py` | Development scratch file (not for submission) |

## Dependencies

- Python 3.6.9+
- NumPy
