# Wine Quality Prediction with Decision Tree

A decision tree learning program that predicts white wine quality ratings based on physicochemical features.

## Usage

```bash
python winequality.py [train] [test] [minleaf]
```

| Argument | Description |
|----------|-------------|
| `train` | Path to the training data file |
| `test` | Path to the testing data file |
| `minleaf` | Minimum number of samples required to split a node (integer ≥ 1) |

### Example

```bash
python winequality.py train test-sample 30
```

## Data Format

**Training file** — 11 feature columns + 1 label column (`quality`):

```
f_acid  v_acid  c_acid  res_sugar  chlorides  fs_dioxide  ts_dioxide  density  pH  sulphates  alcohol  quality
8.10    0.270   0.41    1.45       0.033      11.0        63.0        0.99080  2.99  0.56     12.0     5
```

**Test file** — same 11 feature columns, no `quality` column.

## Features

| Feature | Description |
|---------|-------------|
| `f_acid` | Fixed acidity |
| `v_acid` | Volatile acidity |
| `c_acid` | Citric acid |
| `res_sugar` | Residual sugar |
| `chlorides` | Chlorides |
| `fs_dioxide` | Free sulfur dioxide |
| `ts_dioxide` | Total sulfur dioxide |
| `density` | Density |
| `pH` | pH |
| `sulphates` | Sulphates |
| `alcohol` | Alcohol |

Quality ratings in the dataset: **5**, **6**, **7**.

## Output

Predicted quality ratings printed to stdout, one per line, in the order the test samples appear:

```
5
6
7
5
```

If a leaf node has no unique majority label (tie), `unknown` is printed for that sample.

## Algorithm

The program implements three algorithms:

- **DTL** — builds a decision tree recursively. Stops when the number of samples is below `minleaf`, all labels are identical, or all feature values are identical.
- **ChooseSplit** — selects the best (attribute, split value) pair by maximising information gain over all candidate midpoints.
- **Predict** — traverses the tree from root to leaf to classify a new sample.

## Dependencies

- Python 3.6+
- NumPy
