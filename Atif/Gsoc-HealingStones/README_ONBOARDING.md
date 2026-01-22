# Mayan Stele Fragment Reconstruction Pipeline - Onboarding Guide

This document provides instructions for getting started with the fragment reconstruction pipeline.

## Quick Start

```bash
cd HealingStones/Atif/Gsoc-HealingStones
python main_pipeline.py input_dir output_dir
```

## Running via CLI

### Basic CLI Usage Examples

```bash
# Show help
python main_pipeline.py --help

# Basic run
python main_pipeline.py input_fragments/ output_results/

# With visualizations
python main_pipeline.py input/ output/ --visualize-steps

# With custom config
python main_pipeline.py input/ output/ --config configs/high_selectivity_config.json
```

## Batch Processing via CLI

The `batch_processor.py` script provides validation and preprocessing utilities.

### Basic Batch Processing Examples

```bash
# Show help
python batch_processor.py --help

# Validate PLY files in a directory
python batch_processor.py validate input_dir/

# Preprocess PLY files
python batch_processor.py preprocess input_dir/ output_dir/

# Preprocess with options
python batch_processor.py preprocess input/ output/ --no-normalize
```

### Available Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--input-dir` | string | None | Input directory (optional) |
| `--output-dir` | string | None | Output directory (optional) |
| `--config` | string | `configs/high_selectivity_config.json` | Config file path |

> **Note:** `--config` is parsed but not yet wired into batch processing logic.

## Configuration

The pipeline uses JSON config files in `configs/`. Default: `high_selectivity_config.json`.

## Output

Results saved to output directory:
- Reconstructed fragment meshes
- `quality_metrics.json`
- `surface_matches.json`
- `transformations.json`
