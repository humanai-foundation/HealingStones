# Steps to raise the PR for Issue #33

## 1. Fork & clone
Go to https://github.com/humanai-foundation/HealingStones and click **Fork**.

Then clone your fork:
```bash
git clone https://github.com/<YOUR_USERNAME>/HealingStones.git
cd HealingStones
```

## 2. Create a branch
```bash
git checkout -b fix/issue-33-fragment-alignment-rotation
```

## 3. Apply the changes

### fragment_aligner.py — 3 changes

**Change 1 · Lines 7–14** — add class constant + update constructor:
```python
# BEFORE
    def __init__(self):
        self.aligned_fragments = {}
        self.transformation_history = {}

# AFTER
    DEFAULT_ICP_THRESHOLD = 0.02

    def __init__(self, icp_threshold: float = DEFAULT_ICP_THRESHOLD):
        self.aligned_fragments = {}
        self.transformation_history = {}
        self.icp_threshold = icp_threshold
```

**Change 2 · Lines 31 and 64–65** — fix translation formula:
```python
# Line 31 — DELETE this line:
        translation = centroid1 - centroid2

# Between lines 64 and 65 — ADD this line before "transform = np.eye(4)":
        translation = centroid1 - rotation_matrix @ centroid2
```

**Change 3 · Line 98** — use instance variable instead of hardcoded value:
```python
# BEFORE
        threshold = 0.02  # Distance threshold

# AFTER
        threshold = self.icp_threshold  # Distance threshold
```

---

### main_pipeline.py — 3 changes

**Change 4 · Line 45** — add comma + new config key:
```python
# BEFORE
            'assembly_contact_distance': 0.001  # 1mm contact distance for assembly

# AFTER
            'assembly_contact_distance': 0.001,  # 1mm contact distance for assembly
            'icp_threshold': 0.02               # ICP correspondence distance (metres)
```

**Change 5 · Line 55** — pass icp_threshold to FragmentAligner:
```python
# BEFORE
        self.fragment_aligner = FragmentAligner()

# AFTER
        self.fragment_aligner = FragmentAligner(
            icp_threshold=self.config.get('icp_threshold', FragmentAligner.DEFAULT_ICP_THRESHOLD)
        )
```

**Change 6 · Lines 458–477** — replace translation-only block with full rigid alignment:
```python
# BEFORE (lines 458–477)
                # For break surfaces, we want them to face each other
                # Move target surface close to assembled surface along normal direction
                contact_distance = self.config['assembly_contact_distance']
                contact_offset = normal1 * contact_distance
                target_position = centroid1 + contact_offset
                translation = target_position - centroid2
            else:
                ...

            # Build transformation matrix
            transform = np.eye(4)
            transform[:3, 3] = translation

# AFTER
                # For break surfaces, we want them to face each other
                # Use full rigid alignment (rotation + translation) via FragmentAligner
                contact_distance = self.config['assembly_contact_distance']
                transform = self.fragment_aligner.compute_surface_alignment(
                    points1, points2, normal1, normal2
                )
                # Apply contact offset along assembled surface normal
                transform[:3, 3] += normal1 * contact_distance
            else:
                ...

                # Build transformation matrix
                transform = np.eye(4)
                transform[:3, 3] = translation
```

## 4. Commit
```bash
git add Atif/Gsoc-HealingStones/fragment_aligner.py
git add Atif/Gsoc-HealingStones/main_pipeline.py
git commit -m "fix: compute full rigid transform (R+t) in fragment alignment (#33)

- fragment_aligner.py: Fix translation formula in compute_surface_alignment
  to use t = centroid1 - R @ centroid2 instead of centroid1 - centroid2,
  which was incorrect whenever rotation != identity.
- fragment_aligner.py: Replace hardcoded ICP threshold (0.02) with
  configurable self.icp_threshold set via constructor.
- main_pipeline.py: Call FragmentAligner.compute_surface_alignment() in
  compute_contact_transform() to produce a full 4x4 rigid transform
  (rotation + translation) instead of translation-only.
- main_pipeline.py: Add icp_threshold to pipeline config and wire it
  through to FragmentAligner constructor.

Fixes #33"
```

## 5. Push & open PR
```bash
git push origin fix/issue-33-fragment-alignment-rotation
```

Then go to https://github.com/humanai-foundation/HealingStones/pulls  
and click **New pull request**.

**PR title:**
```
fix: compute full rigid transform (R+t) in fragment alignment (#33)
```

**PR description:**
```
## Problem
`compute_contact_transform()` in `main_pipeline.py` built a 4×4 transform
using only a translation vector, leaving the 3×3 rotation block as identity.
Fragments were shifted near each other but never rotated to orient their
break surfaces face-to-face.

Additionally, `compute_surface_alignment()` in `fragment_aligner.py` computed
`translation = centroid1 - centroid2`, which is incorrect when rotation ≠ I.
The correct formula is `t = centroid1 - R @ centroid2`.

## Fix
- `compute_contact_transform()` now calls `FragmentAligner.compute_surface_alignment()`
  which returns a full rigid transform (R + t), then applies the contact offset.
- `compute_surface_alignment()` now computes translation after the rotation is
  known: `t = centroid1 - R @ centroid2`.
- ICP threshold moved from hardcoded `0.02` to `self.icp_threshold`, configurable
  via `FragmentAligner(icp_threshold=...)` and `pipeline config['icp_threshold']`.

Closes #33
```