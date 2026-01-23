# Healing Stones Reconstruction Pipeline: Data Format Specification

## 1. Overview
The Healing Stones reconstruction pipeline operates on digitized 3D meshes of stone fragments. Each fragment is processed individually to extract geometric and color features, which are subsequently used for surface matching and alignment to reconstruct the original artifact.

## 2. Supported File Format
The pipeline currently operates on **.ply** mesh files (Polygon File Format). The system expects mesh-based PLY files; point-cloud-only representations without face connectivity may not be compatible with current geometric analysis algorithms.

## 3. Mesh Structure Expectations
- **Vertices**: Files must contain vertices with defined 3D coordinates (x, y, z).
- **Faces**: Surface geometry is assumed to be defined by faces (typically triangles) that establish connectivity.
- **Fragment Representation**: Each PLY file is expected to correspond to one physical fragment.

## 4. Color Information
- **Per-vertex RGB**: Per-vertex RGB color information is expected within the PLY files.
- **Detection Heuristics**: Color channels are used as primary indicators for detecting "break" surfaces versus original artifact surfaces.
- **Semantics**: The exact color semantics are heuristic-based (e.g., matching specific ranges for blue, green, or red) and are not strictly enforced by a formal schema. The mapping of RGB values to semantic meaning is dataset-specific and heuristically inferred.

## 5. Coordinate System and Scale
- **Common Coordinate System**: Individual fragments are assumed to share a common coordinate system prior to processing.
- **Scale Consistency**: The pipeline assumes scale consistency across all input fragments. No automatic scale validation or normalization between fragments is performed by the system.

## 6. Directory Layout
Inputs should be organized as a set of PLY files within a single directory. A minimal example layout is provided below:

```text
data/
  fragment_001.ply
  fragment_002.ply
```

## 7. Batch Processing Assumptions
- Batch processing tools are designed to iterate over directories of .ply files.
- Each fragment is processed independently during the feature extraction phase prior to the multi-fragment matching phase.

## 8. Known Limitations
- **No Formal Schema Validation**: Input files are assumed to be valid meshes; degenerate geometry or missing attributes may cause silent failures or crashes.
- **Implicit Color Conventions**: Color-based surface detection relies on hardcoded heuristics rather than a configurable schema or automatic learning.
- **Dataset Assumptions**: Most dataset requirements (such as scale and orientation) are implicit in the geometric algorithms and are not explicitly validated at the input stage.

## 9. Code References
The following scripts in the `Gsoc-HealingStones` directory provide the source for the assumptions documented here:
- `ply_loader.py`: Implementation of PLY ingestion and initial data structure creation.
- `feature_extractor.py`: Geometric and color analysis logic for individual fragments.
- `surface_matcher.py`: Logic for cross-fragment matching based on shared coordinate space and scale.
- `batch_processor.py`: Implementation of directory-level iteration and independent fragment processing.

This document reflects current implicit assumptions and may evolve as validation processes are formalized.
