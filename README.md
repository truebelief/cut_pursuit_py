# Cut Pursuit Segmentation

## Overview

Cut Pursuit is an efficient algorithm for segmenting point clouds by minimizing a functional over a graph. This package provides a Python interface to the C++ implementation of the Cut Pursuit algorithm.

## Installation (Easy way - Recommended)

```bash
pip install cut-pursuit-py
```


## Installation from the source
### 1. Clone the Repository

Open a terminal and clone the repo:

```bash
git clone https://github.com/truebelief/cut_pursuit_py.git
```

Then change into the project directory:

```bash
cd cut_pursuit_py
```

---

### 2. (Optional) Create and Activate a Virtual Environment

It’s a good idea to isolate your installation:

```bash
python -m venv venv
source venv/bin/activate      # On Linux/macOS
venv\Scripts\activate         # On Windows
```

---

### 3. Install Dependencies

Ensure you have a C++11–compatible compiler installed (needed to compile the C++ extension). Also install Python dependencies like NumPy (and SciPy if you plan to run the example):

```bash
pip install numpy scipy
```

---

### 4. Install the Package

You have two main options:

- **Editable Installation (for development):**

  This lets you modify the source code and see changes immediately.

  ```bash
  pip install -e .
  ```

- **Standard Installation:**

  This builds and installs the package without linking directly to the source.

  ```bash
  pip install .
  ```

Both commands use the build configuration specified in `pyproject.toml` and `setup.py` to compile the C++ extension and install the Python binder.

---

### 5. Verify the Installation

Open a Python shell and try importing the package:

```python
import cut_pursuit
```

If there’s no error, your installation was successful.

---



## Usage Example

```python
import numpy as np
import cut_pursuit_py

# Assume pcd is a numpy array of 3D points (N x 3)
def segment_point_cloud(pcd, k=7, reg_strength=1.0):
    # Preprocess point cloud 
    pcd = pcd - np.mean(pcd, axis=0)
    
    # Compute k-nearest neighbors
    from scipy.spatial import cKDTree
    kdtree = cKDTree(pcd)
    _, nn_idx = kdtree.query(pcd, k=k)
    
    # Prepare graph structure
    indices = nn_idx[:, 1:]  # exclude self
    n_nodes = len(pcd)
    
    # Create edge lists
    eu = np.repeat(np.arange(n_nodes), k-1)
    ev = indices.ravel()
    
    # Edge weights 
    edge_weights = np.ones_like(eu, dtype=np.float32)
    
    # Perform cut pursuit
    segments = cut_pursuit_py.perform_cut_pursuit(
        K=k,              # Number of neighbors
        reg_strength=reg_strength,  # Regularization strength
        D=3,              # Dimension of points
        pc_vec=pcd,        # Point cloud 
        edge_weights=edge_weights,
        first_edge=np.cumsum(np.repeat(k-1, n_nodes+1))[:-1],
        adj_vertices=ev
    )
    
    return segments

# Example usage
point_cloud = np.random.rand(1000, 3)
segmentation = segment_point_cloud(point_cloud)
print(f"Number of segments: {len(np.unique(segmentation))}")
```

## Dependencies

- NumPy
- C++11 compatible compiler (Not required if you choose to download prebuilt wheels via pip)

## Citation

If you use this implementation, please cite the original paper:

Landrieu, L., & Obozinski, G. (2017). Cut Pursuit: Fast Algorithms to Learn Piecewise Constant Functions on General Weighted Graphs. SIAM Journal on Imaging Sciences, 10(4), 1724-1766.
