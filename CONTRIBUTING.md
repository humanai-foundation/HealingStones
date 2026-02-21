# HealingStones

HealingStones is a Python project for reconstructing Mayan stele fragments from 3D scans (PLY files).  
It features enhanced surface matching, contact-based alignment, and visualization of reconstructed fragments.

---

## Features

- Load and process PLY fragments with colored break surfaces
- Extract geometric features from fragment surfaces
- Find matching surfaces with cross-color analysis
- Align fragments using origin-based progressive assembly
- Visualize step-by-step matches and final reconstruction
- Save results, transformations, and quality metrics

---

## Installation

1. Clone your fork of the repository:

```bash
git clone https://github.com/<your-username>/HealingStones.git
cd HealingStones
```

2. Install required dependencies (Python 3.8+ recommended):

```bash
pip install -r requirements.txt
```

---

## Getting Started

### 1. Create a New Branch for Your Contribution

Before making changes, create a new branch. This keeps your work organized and makes it easy to submit a PR.

```bash
git checkout -b my-feature-branch
```

Replace `my-feature-branch` with a meaningful name, e.g., `fix-readme` or `add-usage-section`.

### 2. Running the Pipeline Locally

You can test the Mayan Stele Fragment Reconstruction Pipeline locally before contributing code:

```bash
python3 main_pipeline.py path/to/input_dir path/to/output_dir --visualize-steps
```

- `path/to/input_dir`: Directory containing your PLY fragment files
- `path/to/output_dir`: Directory where reconstruction results will be saved
- `--visualize-steps` (optional): Shows step-by-step visualizations of fragment matches and assembly

**Example:**

```bash
python3 main_pipeline.py data/fragments output/results --visualize-steps
```

This command processes all fragments in `data/fragments` and saves the results to `output/results`.

### 3. Optional Flags

- `--min-similarity`: Minimum surface similarity for matching (default: 0.6)
- `--color-tolerance`: Color matching tolerance (default: 0.3)
- `--visualize-steps`: Show step-by-step visualizations
- `--no-reports`: Skip generating detailed reports
- `--contact-distance`: Target contact distance between surfaces in meters (default: 0.001)

---

## Contributing

Thank you for your interest in contributing to HealingStones! 🪨

Follow these steps to make your first contribution:

### Step 1: Fork and Clone

```bash
git clone https://github.com/<your-username>/HealingStones.git
cd HealingStones
```

### Step 2: Create a Branch

```bash
git checkout -b my-feature-branch
```

Use a descriptive branch name like `fix-readme` or `add-usage-section`.

### Step 3: Make Changes

- Update README, documentation, or code
- Ensure your changes are small and focused

### Step 4: Commit Changes

```bash
git add .
git commit -m "type: short description of change"
```

**Commit types:**
- `fix`: bug fixes
- `docs`: documentation changes
- `feat`: new features
- `style`: formatting or style changes

### Step 5: Push Branch

```bash
git push origin my-feature-branch
```

### Step 6: Open a Pull Request

1. Go to your fork on GitHub
2. Click **Compare & Pull Request**
3. Make sure the base repository is the original HealingStones repo and base branch is `main`
4. Fill in a clear title and description
5. Submit the PR

### Step 7: Code Review

- Be polite and responsive to feedback
- Update your branch as requested; GitHub will update your PR automatically
- Celebrate your first merged PR! 🎉

---

## License

Distributed under the MIT License.
