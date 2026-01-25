# Mayan Stele Reconstruction Pipeline - Onboarding

## Running via CLI

### Reconstruction Pipeline
To run the main reconstruction pipeline:
```bash
python main_pipeline.py <input_dir> <output_dir>
```

### Batch Processor
The batch processor supports validation and preprocessing:
```bash
# Validate PLY files
python batch_processor.py validate <input_dir_or_file>

# Preprocess PLY files
python batch_processor.py preprocess <input_dir> <output_dir>
```

### Dry Run Mode
Validate inputs and see planned actions without modifying any files:
```bash
python main_pipeline.py <input_dir> <output_dir> --dry-run
```
> [!NOTE]
> Works for both `main_pipeline.py` and `batch_processor.py`. No files are written or modified.
