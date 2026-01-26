# Mayan Stele Reconstruction Pipeline - Onboarding

## Running via CLI

### Data Validation
Before running expensive processing steps, you can quickly validate your dataset structure:
```bash
python main_pipeline.py check-data <input_dir>
```
> [!TIP]
> **check-data** is a fast, read-only check that ensures the directory is accessible and contains `.ply` files. Use it to verify your paths.
> 
> **validate** (in `batch_processor.py`) is a heavy-duty check that analyzes the actual mesh quality (vertex counts, colors, etc.).

### Reconstruction Pipeline
To run the main reconstruction pipeline:
```bash
python main_pipeline.py <input_dir> <output_dir>
```

### Batch Processor
The batch processor supports validation, preprocessing, and data checking:
```bash
# Check dataset structure
python batch_processor.py check-data <input_dir>

# Validate PLY files (heavy processing)
python batch_processor.py validate <input_dir_or_file>

# Preprocess PLY files
python batch_processor.py preprocess <input_dir> <output_dir>
```
