# Mayan Stele CLI Usage Guide

This guide covers the new structured output capabilities for automation and CI/CD integration.

## Machine-Readable Output (--json / --report)

Use the `--json` flag (alias `--report`) to get a machine-readable JSON object on `stdout`. When enabled, all other logging is suppressed.

### Example: Validation
```bash
python main_pipeline.py check-data data/input --json
```

**JSON Schema:**
```json
{
  "command": "check-data",
  "status": "PASS",
  "input_metadata": {
    "input_path": "data/input",
    "ply_count": 5
  },
  "errors": [],
  "warnings": [],
  "timestamp": "2026-01-27T10:00:00Z"
}
```

### Example: Dry Run (Simulation)
```bash
python batch_processor.py dry-run data/input data/output --report
```

---

## Command Reference

### main_pipeline.py
- `reconstruct <input> <output>`: Run full reconstruction.
- `check-data <input>`: Check input availability.
- `validate <input>`: Verify data integrity.
- `dry-run <input> <output>`: Simulate pipeline initialization.

### batch_processor.py
- `validate <input>`: Comprehensive PLY mesh validation.
- `preprocess <input> <output>`: Clean, center, and normalize meshes.
- `dry-run <input> [output]`: Validate paths without processing.

> [!NOTE]
> **Exit Codes**: Every command returns `0` on `PASS` and `1` on `FAIL`, regardless of whether `--json` is used.
