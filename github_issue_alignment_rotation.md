# Bug: Fragment alignment only applies translation — rotation is never computed

## Summary

`ReconstructionPipeline.compute_contact_transform()` in `Atif/Gsoc-HealingStones/main_pipeline.py`
constructs a 4×4 homogeneous transform using **only a translation vector**, leaving the 3×3 rotation
block as the identity matrix. Fragments are shifted near each other but are **never rotated** to
orient their break surfaces face-to-face, making accurate reconstruction impossible.

## Affected Code

**File:** `Atif/Gsoc-HealingStones/main_pipeline.py` — `compute_contact_transform()`

```python
# Current behavior (lines ~455-495):
transform = np.eye(4)          # rotation = identity (never changed)
transform[:3, 3] = translation # only translation is set
return transform
```

`FragmentAligner.compute_surface_alignment()` in `fragment_aligner.py` **does** compute a proper
rotation via ICP alignment, but it is never called by the main pipeline's matching loop.

## Impact

- **Reconstruction accuracy drops severely** — fragments are placed near each other but with
  arbitrary orientation, making the 80% accuracy target effectively unreachable.
- **Downstream evaluation is invalid** — overlap, coverage, and quality metrics are computed on
  misaligned geometry, giving misleading results.
- **Visual output is nonsensical** — the reconstruction visualizer renders fragments that are
  clumped together but not properly oriented.

## Steps to Reproduce

1. Load any two fragments with known matching break surfaces.
2. Run the pipeline: `pipeline.find_all_matches(fragments)`.
3. Inspect the returned `transform` matrix for any match — the upper-left 3×3 block is always
   identity.
4. Visualize the reconstruction — fragments overlap or gap incorrectly because they were never
   rotated.

## Expected Behavior

The alignment transform should include a rotation component that orients the two break surfaces
to face each other (anti-parallel normals) before translating them into contact. The existing
`FragmentAligner.compute_surface_alignment()` method should be integrated into the pipeline.

## Proposed Fix

```python
# In ReconstructionPipeline — replace compute_contact_transform() body:

aligner = FragmentAligner()

# Use ICP-based alignment from fragment_aligner.py
alignment_result = aligner.compute_surface_alignment(
    source_points=surface1_points,
    target_points=surface2_points,
    source_normals=surface1_normals,
    target_normals=surface2_normals,
)

if alignment_result is not None:
    transform = alignment_result['transform']  # full 4×4 with rotation + translation
else:
    # Fallback: at minimum, rotate normals to be anti-parallel
    rotation = compute_rotation_between_normals(normal1, -normal2)
    transform = np.eye(4)
    transform[:3, :3] = rotation
    transform[:3, 3] = centroid2 - rotation @ centroid1
```

## Additional Context

- `FragmentAligner` is already imported and instantiated elsewhere but unused for this purpose.
- The `ICP` threshold in `FragmentAligner` is hardcoded to `0.02` and should be made configurable
  via `AlignmentConfig.icp_threshold` as part of this fix.

## Labels

`bug`, `critical`, `alignment`, `pipeline`
