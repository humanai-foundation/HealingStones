# mayan_stele_readme

# Mayan Stele Fragment Reconstruction System

## Requirements

- Python 3.8 or higher
- pip
- Virtual environment (recommended)
- OS: Windows / Linux / macOS


## Project Overview

The goal of this project is to digitally reconstruct a fragmented **Mayan stele** using advanced 3D computer vision and deep learning techniques. The central topic is automatic artifact reassembly, where broken stone fragments are scanned as 3D point clouds and then analyzed to detect break surfaces, extract geometric features, and identify possible matches. To tackle this challenge, I preprocess the fragments with multi-scale downsampling and clustering, represent them as graphs of potential connections, and train a graph neural network and Siamese-based models to predict which fragments belong together. These predictions are refined with alignment algorithms like Iterative Closest Point (ICP), while ground truth reconstructions provide assembly knowledge to guide the model. Ultimately, the system aims to move from scattered fragments to a coherent, near-complete digital reconstruction of the stele, reducing manual effort while preserving archaeological heritage.

## What I Built (use the config I created)

This project implements a complete **geometric-based reconstruction pipeline** as the foundation for future deep learning integration. The system consists of several interconnected modules:

### Experimental Machine Learning Approaches (links below)

1. **Machine Learning Approach** (Incomplete - Future Work)
    - Initial deep learning models for fragment relationship prediction
    - Graph neural network architectures for assembly planning
    - Abandoned due to dataset limitations and overfitting issues
    - Code structure exists for future development with larger datasets
2. **Cluster on Break Surface Method** (Incomplete - Future Work)
    - Alternative clustering-based approach for break surface detection
    - Potential for handling unmarked fragments in future applications
    - Preliminary implementation available for further exploration
    - Could be extremely useful for fully automated reconstruction pipelines

### Core Pipeline Components

1. **PLY Processing & Color Detection** (`ply_loader.py`, `direct_mesh_detector.py`)
    - Loads 3D mesh fragments from PLY files
    - Detects colored break surfaces (blue, green, red markers)
    - Direct mesh-based color extraction with configurable thresholds
    - Validation and preprocessing tools
2. **Geometric Feature Extraction** (`feature_extractor.py`)
    - Surface normal computation using PCA
    - Curvature analysis and distribution histograms
    - Boundary detection with convex hull approximation
    - Geometric moments and shape descriptors
    - Surface area and compactness metrics
3. **Surface Matching Engine** (`surface_matcher.py`)
    - Multi-criteria similarity scoring system
    - Weighted combination of normal, area, shape, curvature features
    - Hungarian algorithm for optimal one-to-one matching
    - Cross-color matching capability for realistic fragment scenarios
4. **Fragment Alignment System** (`fragment_aligner.py`)
    - Contact-based surface alignment
    - Origin-based progressive assembly strategy
    - Iterative Closest Point (ICP) refinement
    - Quality metrics and validation
5. **Advanced Visualization** (`reconstruction_visualizer.py`)
    - Step-by-step reconstruction visualization
    - 3D match visualization with connecting lines
    - Quality analysis reports and charts
    - Export capabilities for aligned fragments

### Supporting Infrastructure

1. **Interactive GUI Tools** (`interactive_tools.py`)
    - Real-time fragment manipulation
    - Manual alignment correction interface
    - Match validation and rejection tools
2. **Configuration Management** (`config_manager.py`)
    - Template-based configuration system
    - Multiple processing profiles (high-quality, fast, conservative)
    - YAML/JSON configuration support
3. **Comprehensive Pipeline** (`main_pipeline.py`)
    - End-to-end reconstruction orchestration
    - Progress tracking and quality reporting
    - Automatic component assembly

## Current State

### Completed Features

- **Full geometric processing pipeline** working end-to-end
- **Colored break surface detection** with high accuracy
- **Multi-criteria surface matching** with similarity scoring
- **Progressive fragment assembly** using contact-based alignment
- **3D visualization system** with quality reports
- **Interactive tools** for manual refinement
- **Comprehensive configuration system** with multiple profiles
- **Automated setup and validation** scripts

### Technical Achievements

- **Cross-color matching**: Handles realistic scenarios where break surfaces have different colors
- **Contact-based assembly**: Brings matching surfaces together with configurable precision (1mm default)
- **Quality evaluation**: Comprehensive metrics including contact distances and alignment errors
- **Scalable architecture**: Handles multiple fragments with efficient graph-based component detection
- **Robust preprocessing**: Validation, cleaning, and normalization of input meshes

### Performance Characteristics

- Processes fragments with 50K-900K vertices efficiently
- Achieves sub-millimeter contact precision in alignments
- Handles 3-10 fragment assemblies with good quality
- Supports various PLY mesh formats with colored vertices

![Screenshot from 2025-09-28 15-41-13.png](mayan_stele_readme%2027cedc65e15f80c1bb0be43dbed3117b/Screenshot_from_2025-09-28_15-41-13.png)

Previous reconstruction

![Screenshot from 2025-09-27 10-21-47.png](mayan_stele_readme%2027cedc65e15f80c1bb0be43dbed3117b/Screenshot_from_2025-09-27_10-21-47.png)

Latest reconstruction pipeline

## What’s Left to Do

### Immediate Priorities

1. **Deep Learning Integration**
    - Implement graph neural network for fragment relationship prediction
    - Develop Siamese network for break surface similarity learning
    - Create training data generation from geometric pipeline results
2. 2D Approach 
    - Add texture and surface roughness analysis
    - Implement 2D images of the textures
    - Develop fracture pattern recognition
3. **Assembly Optimization**
    - Global optimization for multi-fragment assemblies
    - Constraint-based assembly with archaeological knowledge
    - Uncertainty quantification and confidence scoring

### Research Extensions

1. **Robustness Improvements**
    - Handle partial and weathered fragments
    - Noise-resistant feature extraction
    - Multi-hypothesis assembly exploration
2. **Validation Framework**
    - Synthetic dataset generation for benchmarking
    - Ground truth comparison metrics
    - Cross-validation with archaeological expert assessments

## Key Challenges & Learnings

### Technical Challenges Overcome

1. **Limited Dataset and Deep Learning Overfitting**
    - Extremely small dataset (only a few Mayan stele fragments available) caused severe overfitting in initial deep learning approaches
    - Neural networks memorized training examples instead of learning generalizable patterns
    - **Solution**: Shifted to robust geometric methods that work with minimal data
    - **Future Direction**: Acquire larger datasets or develop data augmentation techniques for deep learning viability
2. **Color-based Break Surface Detection**
    - Initial clustering approaches were unreliable with real mesh data
    - **Solution**: Developed direct mesh vertex color thresholding with configurable ranges
    - **Learning**: Simple approaches often work better than complex ones for noisy archaeological data

![Screenshot from 2025-09-28 15-37-08.png](mayan_stele_readme%2027cedc65e15f80c1bb0be43dbed3117b/Screenshot_from_2025-09-28_15-37-08.png)

![Screenshot from 2025-09-28 15-36-52.png](mayan_stele_readme%2027cedc65e15f80c1bb0be43dbed3117b/Screenshot_from_2025-09-28_15-36-52.png)

1. **Surface Matching Complexity**
    - Naive geometric similarity led to many false matches
    - **Solution**: Multi-criteria scoring with domain-specific weights
    - **Learning**: Archaeological fragments require specialized similarity measures beyond standard geometric descriptors
2. **Fragment Assembly Strategy**
    - Random pairwise alignment created accumulating errors
    - **Solution**: Origin-based progressive assembly starting from best-connected fragment
    - **Learning**: Assembly order significantly impacts final reconstruction quality
3. **Real vs. Synthetic Data Gap**
    - Algorithms working on perfect synthetic data failed on real archaeological meshes
    - **Solution**: Robust preprocessing pipeline with mesh validation and repair
    - **Learning**: Archaeological data has unique characteristics (weathering, scanning artifacts) requiring specialized handling

### Archaeological Domain Insights

1. **Break Surface Characteristics**: Real fractures don’t always have perfectly matching geometry due to weathering and material loss
2. **Scale Considerations**: Fragment sizes vary dramatically, requiring scale-invariant features
3. **Assembly Ambiguity**: Multiple valid local arrangements may exist, requiring global optimization

### Software Engineering Learnings

1. **Modular Design Benefits**: Clean separation allowed rapid iteration on individual components
2. **Configuration Management**: Essential for managing complex algorithmic parameter spaces
3. **Visualization Importance**: 3D visualization was crucial for debugging and validation
4. **Quality Metrics**: Quantitative assembly quality measures enable systematic improvement

## Getting Started

This section explains how to set up the environment and run the reconstruction pipeline locally.


## Project Structure

```
├── main_pipeline.py           # End-to-end reconstruction orchestration
├── ply_loader.py             # PLY file processing and color detection
├── feature_extractor.py      # Geometric feature extraction
├── surface_matcher.py        # Break surface matching algorithms
├── fragment_aligner.py       # Fragment alignment and assembly
├── reconstruction_visualizer.py # 3D visualization and reporting
├── interactive_tools.py      # GUI tools for manual refinement
├── config_manager.py         # Configuration management system
├── setup_system.py          # Automated system setup
├── configs/                  # Configuration templates
├── data/examples/           # Example PLY files for testing
└── examples/                # Usage examples and tutorials
```

### Prerequisites

```bash
# Install dependencies
python setup_system.py
```

### Quick Start

```bash
# Test with example data
python examples/basic_test.py
# Reconstruct your fragments
python main_pipeline.py data/input data/output
# Interactive refinement
python interactive_tools.py
```

### Configuration

```bash
# Use predefined profiles
python main_pipeline.py data/input data/output --config configs/high_quality_config.json
# Create custom configuration
python config_manager.py create --template conservative --output my_config.json
```

## Project Summary

**The Challenge**: Ancient stone fragments are extremely difficult to reconstruct because weathered break surfaces look nearly identical and provide few clues about which pieces originally fit together.

**Our Solution**:

- Mark break surfaces with colored paint (red, blue, green) during 3D scanning
- Build software that detects these colored regions automatically
- Extract geometric features like surface shape, curvature, and size from each colored area
- Use intelligent matching algorithms to find which colored surfaces from different fragments could have once been connected
- Assemble fragments step-by-step, starting with the most confident matches and bringing break surfaces into physical contact

**What We Built**: A complete automated reconstruction system that takes scattered 3D fragment scans as input and outputs a digitally reconstructed artifact with millimeter-level precision.

**Key Innovation**: Instead of trying to match entire complex stone surfaces, we focus computational power only on the break regions - turning an impossible search problem into a solvable computer vision task.

**Impact**: Successfully reconstructs multi-fragment Mayan stele assemblies while providing quality metrics to validate the accuracy of each reconstruction.

## Useful Links

For more comprehensive details about the project and documentation, you can explore the following links:

- **Blog**: [Atif_Khan_HealingSrones_Blog](https://medium.com/@atif.4024120/gsoc-2025-with-humanai-healing-stones-8b9f50618030)
- **Blog for cluster approch**: [cluster approach](https://medium.com/@atif.4024120/gsoc-2024-with-humanai-healing-stones-811a9010cfa0)
- **Google Summer of Code (GSoC) 2025 Project**: [Gsoc 2025](https://summerofcode.withgoogle.com/programs/2025/projects/elgslkxD)
- **HumanAI Foundation**: [Human AI Projects](https://humanai.foundation/activities/gsoc2025.html)
- **Machine learning approach**: [Master Branch](https://github.com/K-Atif18/healing-stones/tree/master)
- **cluster on break surface method**: [Cluster Branch](https://github.com/K-Atif18/healing-stones/tree/cluster)

Contributions to this project are welcome. If you are interested in contributing, please fork the repository and submit a pull request. Ensure that your code follows the style and conventions used in this repository.




## Installation

### 1. Navigate to this directory
```bash
cd Atif/Gsoc-HealingStones

python -m venv venv

Win: venv\Scripts\activate

Linux/OS: source venv/bin/activate

pip install -r requirements.txt

Verify: python setup_system.py
