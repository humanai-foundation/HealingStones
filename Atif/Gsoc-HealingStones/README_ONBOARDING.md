# Mayan Stele Fragment Reconstruction Pipeline - Onboarding Guide

This document provides instructions for getting started with the fragment reconstruction pipeline.

## Quick Start

```bash
# Navigate to the project directory
cd HealingStones/Atif/Gsoc-HealingStones

# Run with input and output directories
python main_pipeline.py --input-dir <input_dir> --output-dir <output_dir>
```

## Running via CLI

The pipeline supports command-line arguments for flexible configuration.

### Basic CLI Usage Examples

```bash
# Show help
python main_pipeline.py --help

# Run with no arguments (displays usage info)
python main_pipeline.py

# Basic run with input/output directories
python main_pipeline.py --input-dir input_fragments/ --output-dir output_results/

# Run with visualizations enabled
python main_pipeline.py --input-dir input/ --output-dir output/ --visualize

# Run with custom config file
python main_pipeline.py --input-dir input/ --output-dir output/ --config configs/high_selectivity_config.json
```

### Available Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--input-dir` | string | None | Directory containing PLY files |
| `--output-dir` | string | None | Directory for output results |
| `--config` | string | `configs/high_selectivity_config.json` | Path to config file |
| `--data-path` | string | None | Additional data path (not yet used) |
| `--visualize` | flag | False | Enable step-by-step visualizations |
| `--min-similarity` | float | 0.6 | Similarity threshold for matching |
| `--color-tolerance` | float | 0.3 | Color matching tolerance |
| `--no-reports` | flag | False | Skip generating reports |
| `--contact-distance` | float | 0.001 | Contact distance in meters |

> **Note:** `--data-path` is parsed but not yet wired into the pipeline. This is reserved for future use.

## Configuration

The pipeline uses JSON configuration files located in `configs/`. The default configuration (`high_selectivity_config.json`) provides optimized settings for high-quality matching.

## Output

Results are saved to the specified output directory, including:
- Reconstructed fragment meshes
- Quality metrics (`quality_metrics.json`)
- Surface match data (`surface_matches.json`)
- Transformation matrices (`transformations.json`)
- Visualization reports (if enabled)
