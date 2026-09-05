# Healing Stones
<div align="center">
   <img src="Puzzle2.jpg.jpeg" width=15% />
   <p><i>Reconstructing Digitized Cultural Heritage Artifacts with Artificial Intelligence</i></p>
</div>

## 📋 Table of Contents
- [Background](#background)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Available Scripts](#available-scripts)
- [Configuration](#configuration)
- [Examples](#examples)
- [Contributing](#contributing)
- [Links](#links)
- [Mentors](#mentors)

---

## 🏛️ Background

Historically works of art and architecture have been subjected to fragmentation: ancient Maya stelae were cut away from monuments by collectors; medieval sculptures from Notre-Dame in Paris were broken into multiple parts and dispersed in acts of political iconoclasm. 

Art historians and archaeologists seek to reconstruct these works to more fully understand their cultural meaning and value. However, the traditional method of physical refitting is labor-intensive and not always possible when fragments are dispersed throughout the world. 

**Our Solution:** We use AI in combination with existing digital scan models of fragments to develop a means for reconstructing fragmented cultural heritage artifacts in a virtual space. 

The project dataset consists of the remaining and reconstructed stone fragments of **Stela #43** from the archaeological site of Naranjo, in the Petén region of Guatemala. This stela, adorned with carved, high-relief images and hieroglyphs, holds immense historical significance in studying ancient Maya iconography and dating.

---

## ✨ Features

- 🔍 **Direct Mesh Detection**: Automatic detection of matching mesh surfaces
- 🧩 **Fragment Alignment**: ICP-based alignment of 3D fragments  
- 🎯 **Surface Matching**: Advanced algorithms for surface correspondence
- 📊 **Reconstruction Evaluation**: Quantitative metrics for match quality
- 🎨 **Interactive Visualization**: Real-time 3D visualization tools
- 📈 **Diagnostic Tools**: Comprehensive matching diagnostics
- ⚙️ **Configurable Pipelines**: Multiple configuration presets
- 🔄 **Batch Processing**: Process multiple fragments simultaneously

---

## 🛠️ Installation

### Prerequisites

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **pip** (Python package manager)
- **Git** ([Download](https://git-scm.com/downloads))

### System Requirements
- **OS**: Linux, macOS, or Windows 10/11
- **RAM**: 8GB minimum (16GB recommended for batch processing)
- **GPU**: Optional but recommended for faster processing
- **Storage**: 2GB+ for project and dependencies

### Step-by-Step Installation

1. **Clone the repository**
```bash
   git clone https://github.com/humanai-foundation/HealingStones.git
   cd HealingStones
```

2. **Navigate to the main working directory**
```bash
   cd Atif/gsoc-HealingStones
```

3. **Create a virtual environment** (recommended)
```bash
   # On Linux/macOS
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
```

4. **Install dependencies**
```bash
   pip install -r requirements.txt
```

5. **Run system setup**
```bash
   python setup_system.py
```

6. **Verify installation**
```bash
   python example.py
```

---

## 🚀 Quick Start

### Run Example Demo
```bash
python example.py
```

This will:
- Load sample fragment data
- Extract features
- Match fragments
- Visualize results

### Process Your Own Data
```bash
# 1. Place your .ply files in data/fragments/
# 2. Run the main pipeline
python main_pipeline.py --config configs/high_selectivity_config.json
```

---

## 📖 Usage

### Basic Workflow

#### 1. **Prepare Your Data**
Organize 3D scan files in the data directory:
```
data/
├── fragments/
│   ├── fragment_001.ply
│   ├── fragment_002.ply
│   ├── fragment_003.ply
│   └── ...
└── labels/              # Optional: ground truth data
    └── matches.json
```

#### 2. **Run Feature Extraction**
```bash
python feature_extractor.py --input data/fragments --output results/features
```

#### 3. **Train the Model** (if needed)
```bash
python train_model.py --config configs/default_config.yaml
```

#### 4. **Match Fragments**
```bash
python match_fragments.py --input results/features --output results/matches
```

#### 5. **Align Fragments**
```bash
python fragment_aligner.py --matches results/matches --output results/aligned
```

#### 6. **Visualize Results**
```bash
python visualize.py --matches results/matches --fragments data/fragments
```

### Advanced Usage

#### Complete Pipeline (Automated)
```bash
# Main pipeline with default config
python main_pipeline.py

# With custom configuration
python main_pipeline.py --config configs/high_selectivity_config.json

# Alternative pipeline versions
python main_pipeline1.py  # Version 1: Basic approach
python main_pipeline2.py  # Version 2: Advanced features
```

#### Batch Processing
Process multiple fragment sets:
```bash
python batch_processor.py --input data/batch_fragments/ --output results/batch_results/
```

#### Interactive Mode
Launch GUI for manual adjustment:
```bash
python interactive_tools.py
```

#### Diagnostics & Evaluation
```bash
# Generate diagnostic reports
python matching_diagnostics.py --matches results/matches --output reports/

# Evaluate reconstruction accuracy
python reconstruction_evaluator.py \
    --ground_truth data/labels/matches.json \
    --predictions results/matches/ \
    --output reports/evaluation.json
```

#### Custom Configuration
```bash
# Use configuration manager
python config_manager.py --create my_custom_config.json

# Edit and use custom config
python main_pipeline.py --config configs/my_custom_config.json
```

---

## 📁 Project Structure
```
HealingStones/
├── Atif/
│   └── gsoc-HealingStones/
│       ├── configs/                        # Configuration files
│       │   ├── high_selectivity_config.json   # High precision config
│       │   ├── default_config.yaml           # Default settings
│       │   └── mayan_stele_readme_*.md      # Maya-specific docs
│       ├── data/                           # Dataset directory
│       │   ├── fragments/                 # Input 3D scans (.ply, .obj, .stl)
│       │   └── labels/                    # Ground truth matches
│       ├── results/                       # Output directory
│       │   ├── features/                 # Extracted feature vectors
│       │   ├── matches/                  # Predicted matches
│       │   ├── aligned/                  # Aligned 3D models
│       │   └── reports/                  # Diagnostic reports
│       │
│       ├── batch_processor.py            # Batch processing script
│       ├── config_manager.py             # Configuration management
│       ├── direct_mesh_detector.py       # Direct mesh detection
│       ├── example.py                    # Quick start demo
│       ├── feature_extractor.py          # Geometric feature extraction
│       ├── fragment_aligner.py           # Fragment alignment (ICP)
│       ├── interactive_tools.py          # Interactive GUI tools
│       ├── main_pipeline.py             # Main execution pipeline
│       ├── main_pipeline1.py            # Pipeline variant 1
│       ├── main_pipeline2.py            # Pipeline variant 2
│       ├── matching_diagnostics.py      # Diagnostics & analysis
│       ├── ply_loader.py                # PLY file loader utility
│       ├── reconstruction_evaluator.py   # Accuracy evaluation
│       ├── reconstruction_visualizer.py  # 3D visualization
│       ├── surface_matcher.py           # Surface matching algorithm
│       ├── setup_system.py              # Project initialization
│       ├── requirements.txt             # Python dependencies
│       └── README.md                    # This file
│
├── Satvik/                              # Alternative implementation
│   └── gsoc-2025-Healing-Stones-main/
│       ├── images/                      # Image data
│       ├── new/                         # Experimental code
│       ├── progress_log.md             # Development progress
│       └── README.md                   # Alternative documentation
│
└── Puzzle2.jpg.jpeg                    # Project logo
```

---

## 📜 Available Scripts

### Core Pipeline Scripts

| Script | Description | Command Example |
|--------|-------------|-----------------|
| **example.py** | Quick start demonstration | `python example.py` |
| **main_pipeline.py** | Complete automated pipeline | `python main_pipeline.py --config <config>` |
| **main_pipeline1.py** | Pipeline variant 1 (basic) | `python main_pipeline1.py` |
| **main_pipeline2.py** | Pipeline variant 2 (advanced) | `python main_pipeline2.py` |

### Feature & Matching Scripts

| Script | Description | Command Example |
|--------|-------------|-----------------|
| **feature_extractor.py** | Extract geometric features | `python feature_extractor.py --input data/fragments` |
| **surface_matcher.py** | Find matching surfaces | `python surface_matcher.py --features results/features` |
| **fragment_aligner.py** | Align matched fragments | `python fragment_aligner.py --matches results/matches` |
| **direct_mesh_detector.py** | Direct mesh detection | Used internally by pipeline |

### Utility Scripts

| Script | Description | Command Example |
|--------|-------------|-----------------|
| **batch_processor.py** | Process multiple fragments | `python batch_processor.py --input data/batch/` |
| **config_manager.py** | Manage configurations | `python config_manager.py --create new_config.json` |
| **ply_loader.py** | Load PLY/OBJ/STL files | Used as library import |
| **setup_system.py** | Initialize project structure | `python setup_system.py` |

### Visualization & Analysis

| Script | Description | Command Example |
|--------|-------------|-----------------|
| **interactive_tools.py** | Interactive GUI for manual review | `python interactive_tools.py` |
| **reconstruction_visualizer.py** | 3D visualization of results | `python reconstruction_visualizer.py --input results/aligned` |
| **matching_diagnostics.py** | Generate diagnostic reports | `python matching_diagnostics.py --matches results/` |
| **reconstruction_evaluator.py** | Evaluate accuracy metrics | `python reconstruction_evaluator.py --gt data/labels/` |

---

## ⚙️ Configuration

### Available Configurations

1. **`configs/high_selectivity_config.json`**
   - High precision matching
   - Strict thresholds
   - Best for high-quality scans

2. **`configs/default_config.yaml`**
   - Balanced settings
   - Good for most use cases

### Configuration Example

**high_selectivity_config.json:**
```json
{
  "feature_extraction": {
    "descriptor_type": "FPFH",
    "voxel_size": 0.05,
    "normal_radius": 0.1,
    "feature_radius": 0.25
  },
  "matching": {
    "method": "RANSAC",
    "distance_threshold": 0.02,
    "max_iterations": 100000,
    "confidence": 0.999
  },
  "alignment": {
    "icp_threshold": 0.02,
    "max_icp_iterations": 50
  },
  "visualization": {
    "point_size": 2,
    "background_color": [1.0, 1.0, 1.0],
    "show_normals": false,
    "show_correspondences": true
  }
}
```

### Create Custom Configuration
```bash
# Interactive configuration creation
python config_manager.py --create my_config.json

# Use your custom config
python main_pipeline.py --config configs/my_config.json
```

### Command-line Override
```bash
# Override specific parameters
python main_pipeline.py \
    --config configs/high_selectivity_config.json \
    --voxel_size 0.03 \
    --distance_threshold 0.01
```

---

## 💡 Examples

### Example 1: Process Single Fragment Pair
```bash
python example.py
```

### Example 2: Batch Process Multiple Fragments
```bash
# Prepare batch data
mkdir data/batch_fragments
cp data/fragments/*.ply data/batch_fragments/

# Run batch processor
python batch_processor.py \
    --input data/batch_fragments/ \
    --output results/batch_results/ \
    --config configs/high_selectivity_config.json
```

### Example 3: Custom Pipeline with Visualization
```bash
# Step 1: Extract features
python feature_extractor.py --input data/fragments --output results/features

# Step 2: Match with diagnostics
python surface_matcher.py --input results/features --output results/matches --verbose

# Step 3: Visualize matches
python interactive_tools.py --matches results/matches
```

### Example 4: Evaluate Against Ground Truth
```bash
python reconstruction_evaluator.py \
    --ground_truth data/labels/gt_matches.json \
    --predictions results/matches/ \
    --output reports/evaluation_report.json \
    --visualize
```

---

## 🎯 Tasks & Algorithms

### 1. Direct Fit Matching
- **Files**: `direct_mesh_detector.py`, `surface_matcher.py`
- **Method**: ICP (Iterative Closest Point) + RANSAC
- **Purpose**: Find exact surface matches between broken fragments

### 2. Carved Topography Analysis  
- **Files**: `feature_extractor.py`
- **Method**: FPFH/SHOT geometric descriptors
- **Purpose**: Identify continuity of carved features across gaps

### 3. Surface Design Recognition
- **Files**: `surface_matcher.py`, `matching_diagnostics.py`
- **Method**: Local feature matching + global consistency
- **Purpose**: Match hieroglyphs and decorative patterns

### 4. Dimensional Analysis
- **Files**: `fragment_aligner.py`, `reconstruction_evaluator.py`
- **Method**: Hausdorff distance, volume overlap
- **Purpose**: Compare overall block shapes and dimensions

---

## 📊 Expected Results

- ✅ **80%+ accuracy** in fragment reconstruction
- ✅ Automated matching for fragments with **known orientation**
- ✅ Robust testing on fragments with **uncertain orientation**
- ✅ Scalable pipeline for diverse cultural heritage artifacts
- ✅ Interactive tools for expert review and refinement

---

## 🤝 Contributing

We welcome contributions from the community!

### Current Contributors

- **Atif** - Main pipeline development (`Atif/gsoc-HealingStones/`)
- **Satvik** - Alternative approaches (`Satvik/gsoc-2025-Healing-Stones-main/`)

### How to Contribute

1. **Fork the repository**
2. **Create your workspace**
```bash
   mkdir YourName/
   cd YourName/
```
3. **Track your progress**
```bash
   echo "## Development Log" > progress_log.md
```
4. **Make changes and commit**
```bash
   git add .
   git commit -m "Feature: implemented X algorithm"
   git push origin your-branch
```
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Include unit tests for new features
- Update documentation
- Test with sample data before PR

### Areas for Contribution

- 🧠 Improve ML model architectures
- 📊 Add new matching algorithms
- 🔧 Optimize performance
- 📝 Enhance documentation
- 🐛 Fix bugs
- 🎨 Improve visualizations

---

## 🔗 Links

- [University of Alabama](https://www.ua.edu)
- [Human AI Foundation - GSoC 2025](https://humanai.foundation/gsoc/organizations/2025/alabama.html)
- [Notre Dame in Color Project](https://adhc1.ua.edu/notre_dame_in_color/)
- [Visual Documentation Lab](https://sites.ua.edu/atokovinine/3d-lab/)

---

## 👥 Mentors

| Name | Affiliation | Profile |
|------|-------------|---------|
| Jennifer Feltman | University of Alabama | [Link](https://art.ua.edu/people/jennifer-m-feltman/) |
| Alexandre Tokovinine | University of Alabama | [Link](https://anthropology.ua.edu/people/alexandre-tokovinine/) |
| Emanuele Usai | University of Alabama | [Link](https://physics.ua.edu/people/emanuele-usai/) |
| Sergei Gleyzer | University of Alabama | [Link](https://physics.ua.edu/people/sergei-gleyzer/) |
| Lizzette Soto | University of Alabama | [Link](https://anthropology.ua.edu/graduate-student/lizzette-soto/) |

---

## 🆘 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --upgrade
```

#### Memory Issues
```bash
# Solution: Reduce voxel size in config
# Edit configs/high_selectivity_config.json
# Change "voxel_size": 0.05 → 0.1
```

#### PLY Loading Errors
```bash
# Solution: Check file format
python ply_loader.py --validate data/fragments/fragment_001.ply
```

#### Visualization Not Working
```bash
# Solution: Install visualization dependencies
pip install open3d vtk matplotlib
```

#### Configuration Errors
```bash
# Solution: Validate config file
python config_manager.py --validate configs/your_config.json
```

### Getting Help

1. Check [GitHub Issues](https://github.com/humanai-foundation/HealingStones/issues)
2. Review contributor `progress_log.md` files
3. Contact mentors via university emails
4. Join GSoC 2025 community forums

---

## 📄 License

This project is part of **Google Summer of Code 2025** under the Human AI Foundation.

---

## 🙏 Acknowledgments

- **University of Alabama** for academic support and resources
- **Google Summer of Code 2025** program
- **Archaeological site of Naranjo** for dataset access
- **Open-source community** for tools and libraries
- **Contributors** Atif and Satvik for their development work

---

## 📚 Citation

If you use this work in your research, please cite:
```bibtex
@software{healingstones2025,
  title={Healing Stones: AI-Powered Reconstruction of Cultural Heritage Artifacts},
  author={Human AI Foundation},
  year={2025},
  publisher={GitHub},
  url={https://github.com/humanai-foundation/HealingStones}
}
```

---

<div align="center">
  <p>Made with ❤️ for Cultural Heritage Preservation</p>
  <p><i>Reconstructing the past, one fragment at a time</i></p>
  
  [![Stars](https://img.shields.io/github/stars/humanai-foundation/HealingStones?style=social)](https://github.com/humanai-foundation/HealingStones/stargazers)
  [![Forks](https://img.shields.io/github/forks/humanai-foundation/HealingStones?style=social)](https://github.com/humanai-foundation/HealingStones/network/members)
  [![Issues](https://img.shields.io/github/issues/humanai-foundation/HealingStones)](https://github.com/humanai-foundation/HealingStones/issues)
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![License](https://img.shields.io/badge/License-GSoC_2025-green.svg)](https://summerofcode.withgoogle.com/)
</div>