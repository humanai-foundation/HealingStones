# Healing Stones – Contributor Onboarding Guide

> 📌 This document is intended for **new contributors** and readers who want to **run and understand the codebase** quickly.
> For detailed research context, experimental notes, and methodology, see `README.md` in this directory.

---

## 🧠 What Is This?

`Atif/Gsoc-HealingStones` contains the **core Python-based machine learning and geometry pipeline** for the *Healing Stones* project.

The goal is to **digitally reconstruct fragmented cultural heritage artifacts** (e.g. Mayan stelae) using:

* 3D mesh processing (`.ply` files)
* Geometric feature extraction
* Surface matching
* Fragment alignment (ICP-style)
* Quantitative evaluation and visualization

This is a **research-oriented codebase**, not a production system.

---

## 📁 Repository Structure (Simplified)

```
Atif/Gsoc-HealingStones/
├── README.md                    # Research overview & experiments (existing)
├── README_ONBOARDING.md         # ← You are here
├── configs/                     # JSON configs controlling pipeline behavior
│   └── high_selectivity_config.json
├── ply_loader.py                # Load .ply fragment meshes
├── feature_extractor.py         # Geometric / surface feature extraction
├── surface_matcher.py           # Fragment surface matching logic
├── fragment_aligner.py          # Fragment alignment (ICP / transforms)
├── reconstruction_evaluator.py  # Evaluation metrics
├── reconstruction_visualizer.py # Visualization utilities
├── main_pipeline.py             # Primary pipeline entry point
├── main_pipeline1.py            # Experimental variant
├── main_pipeline2.py            # Experimental variant
├── requirements.txt             # Python dependencies
└── setup_system.py              # Environment/system helpers
```

> ⚠️ Files like `main_pipeline1.py` and `main_pipeline2.py` are **experimental** and may change.

---

## ⚙️ Environment Setup

### Requirements

* Python **3.9 or newer** (recommended)
* macOS or Linux (Windows may require additional Open3D setup)

### Create a virtual environment

```bash
cd Atif/Gsoc-HealingStones
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Pipeline

### Basic run

```bash
python main_pipeline.py
```

This will:

1. Load fragment meshes
2. Extract geometric features
3. Identify candidate fragment matches
4. Align fragment pairs
5. Evaluate reconstruction quality
6. Visualize results (if enabled)

### Running experimental variants

```bash
python main_pipeline1.py
# or
python main_pipeline2.py
```

> Some scripts expect fragment paths and parameters to be defined in config files.

---

## 🔧 Configuration System

Pipeline behavior is controlled using JSON config files in the `configs/` directory.

Example (`high_selectivity_config.json`):

```json
{
  "selectivity_threshold": 0.85,
  "max_candidate_pairs": 50,
  "use_surface_normals": true
}
```

Configs allow experimentation with:

* Matching strictness (precision vs recall)
* Number of candidate fragment pairs
* Feature extraction parameters

Configs are loaded via `config_manager.py`.

---

## 📊 Outputs & Evaluation

Evaluation logic lives in:

* `reconstruction_evaluator.py`

Typical evaluation signals include:

* Match confidence scores
* Alignment quality indicators

Visualization utilities:

* `reconstruction_visualizer.py`

These help inspect whether fragment matches and alignments are plausible.

---

## 🧪 Research vs Stable Code

**Relatively stable components:**

* `ply_loader.py`
* `feature_extractor.py`
* `surface_matcher.py`
* `fragment_aligner.py`

**Experimental / evolving components:**

* `main_pipeline1.py`
* `main_pipeline2.py`
* ML-based approaches described in `README.md`

Contributors are encouraged to keep experiments isolated and well-documented.

---

## 🤝 How You Can Contribute

Good first contributions include:

* Improving documentation and onboarding
* Adding CLI flags for config selection
* Improving evaluation metrics
* Enhancing visualization clarity
* Refactoring duplicated pipeline logic

Please keep changes:

* Modular
* Well-documented
* Focused on clarity and reproducibility

---

## 📌 Notes for New Contributors

* This project prioritizes **research clarity over performance**
* Expect partial implementations and iterative experimentation
* Do not use `npm` — this is a **Python-only** project

---

For deeper background, methodology, and experimental notes, see `README.md` in this directory.
