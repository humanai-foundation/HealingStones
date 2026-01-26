# Healing Stones: Reconstructing Cultural Heritage with AI

This directory contains an **experimental ICP-based reconstruction pipeline**
developed as part of a Google Summer of Code (GSoC) exploration under the
HumanAI Foundation.


This project focuses on digitally reconstructing fragmented cultural artifacts (Mayan stele) using **3D point cloud data** and **AI-powered point cloud alignment techniques**.

---

## Project Overview

Over centuries, cultural heritage artifacts have been fragmented and scattered globally. Traditional physical reconstruction is time-intensive and limited.  
This project proposes an **AI-powered approach** to:
- Analyze fragmented 3D models
- Automatically align and reconstruct the artifact
- Visualize and export the final unified digital model

---

## Scope and Status

This implementation represents a **baseline, geometry-driven approach**
to fragment reconstruction using ICP alignment.

- Focuses on pairwise and global ICP-based assembly
- Does not include machine learning or learned feature extraction
- Intended for experimentation, benchmarking, and comparison
- Not the primary recommended pipeline for extension

For the main modular reconstruction pipeline, see:
➡️ `Atif/Gsoc-HealingStones`


## Features

- Pairwise ICP alignment (Point-to-Plane method)
- Automated pair ranking (Fitness, RMSE)
- Global multi-fragment assembly
- Cleaning and optimization (outlier removal, downsampling)
- Visualized and color-coded final assembly
- Fully automated pipeline, reproducible for any `.PLY` dataset

---

## Project Structure

```
.
├── data/
│   └── fragments/               # 3D fragment files (.PLY)
├── scripts/
│   ├── icp_align2.py            # ICP functions
│   ├── pairwise_icp_log.py      # Pairwise ICP execution
│   ├── analyze_icp_results.py   # Analyze ICP scores
│   ├── global_assembly.py       # Global assembly chaining script
│   └── clean_and_colorize_assembly.py  # Final cleaning and coloring
├── icp_results.csv              # Raw ICP scores
├── sorted_icp_results.csv       # Sorted ICP scores
├── global_assembly.ply          # Raw global assembly
├── global_assembly_cleaned.ply  # Final optimized model
├── progress_log.md              # Daily progress log
├── requirements.txt             # Dependencies
└── README.md                    # Project description
```

---

## Requirements

- Python 3.8+
- Open3D
- NumPy
- pandas

Install all dependencies using:
```bash
pip install -r requirements.txt


## How to Run

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Run pairwise ICP alignment**

```bash
python scripts/pairwise_icp_log.py
```

3. **Analyze ICP results**

```bash
python scripts/analyze_icp_results.py
```

4. **Build global assembly**

```bash
python scripts/global_assembly.py
```

5. **Clean and colorize final model**

```bash
python scripts/clean_and_colorize_assembly.py
```

6. **Visualize the result**

```bash
python -c "import open3d as o3d; pcd = o3d.io.read_point_cloud('global_assembly_cleaned.ply'); o3d.visualization.draw_geometries([pcd])"
```

---

## Results

- Successful global reconstruction of the Mayan Stele from fragmented `.PLY` files
- Visualized final assembly with distinct color-coded fragments
- Clean and optimized final point cloud saved as `global_assembly_cleaned.ply`
- Ready-to-use pipeline for any new `.PLY` dataset

---

## Metrics

| Metric | Description |
|--------|-------------|
| **Fitness** | Indicates how well fragments aligned (higher is better) |
| **RMSE** | Root Mean Square Error for alignment (lower is better) |

**Example (Top Fragment Pairs):**

```
Source, Target, Fitness, RMSE
FR_07 → FR_13: 1.0, 0.0
FR_07 → FR_14: 0.522584, 1.092644
...
```

---

## Deliverables

- End-to-end Python scripts (fully automated)
- Clean final reconstructed `.PLY`
- Test results (`icp_results.csv` and `sorted_icp_results.csv`)
- Progress log (`progress_log.md`)
- CV: https://drive.google.com/file/d/1h21K_vzx0T6zZiQzFOjGz82Xv2LwOg8Q/view?usp=sharing

---

