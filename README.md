# Healing Stones

![Puzzle](Puzzle2.jpg.jpeg)

Reconstructing Digitized Cultural Heritage Artifacts with Artificial Intelligence.

---

## Background

Historically works of art and architecture have been subjected to fragmentation: ancient Maya stelae were cut away from monuments by collectors; medieval sculptures from Notre-Dame in Paris were broken into multiple parts and dispersed in acts of political iconoclasm. Art historians and archaeologists seek to reconstruct these works to more fully understand their cultural meaning and value, however the traditional method of physical refitting is labor intensive and not always possible when fragments are dispersed throughout the world. We use AI in combination with existing digital scan models of fragments to develop a means for reconstructing fragmented cultural heritage artifacts in a virtual space. The project dataset used are the remaining and reconstructed stone fragments of Stela #43 from the archaeological site of Naranjo, in the Petén region of Guatemala. This stela, adorned with carved, high-relief images and hieroglyphs, holds immense historical significance in studying ancient Maya iconography and dating. Its reconstruction becomes particularly crucial in advancing new initiatives in the preservation of historical art and architecture.

---

## Repository Structure

This repository contains two independent implementation folders, each developed by a different contributor during the GSoC program. They are **parallel experimental pipelines** — not sequential stages — and explore different approaches to the same artifact reconstruction problem.

### `Atif/` — Deep Learning-Based Fragment Matching

| Property | Details |
|---|---|
| **Author** | Atif (GSoC contributor) |
| **Approach** | Deep learning for fragment surface matching and feature extraction |
| **Status** | Active / Reference implementation |
| **Best for** | New contributors getting started |

**What it does:** Implements a neural network–based pipeline for identifying direct-fit matches and surface continuities between digitized stone fragments. Focuses on learned feature representations of 3D mesh data.

**Quick setup:**
```bash
cd Atif
pip install -r requirements.txt
```

---

### `Satvik/` — Geometric & Classical CV Approach

| Property | Details |
|---|---|
| **Author** | Satvik (GSoC contributor) |
| **Approach** | Geometric analysis and classical computer vision techniques |
| **Status** | 🔬 Experimental / Research exploration |
| **Best for** | Contributors exploring alternative methodologies |

**What it does:** Explores geometric shape descriptors, classical computer vision, and traditional curve/surface matching algorithms as alternatives to deep learning for fragment reconstruction.

**Quick setup:**
```bash
cd Satvik
pip install -r requirements.txt
```

---

### For New Contributors

**Start with the `Atif/` folder.** It is the more stable and documented implementation and provides a solid baseline for understanding the problem and the codebase.

Once you're comfortable, you're encouraged to explore `Satvik/` to understand the alternative approach and consider how both implementations might be unified or improved.

> **Note:** Both folders have their own `requirements.txt`. You do **not** need to install both at the same time. Use a separate virtual environment for each if you wish to test both.

---

## Tasks

- Search for direct fit matches between surfaces (e.g. two parts of something broken).
- Identify continuity of carved topography (e.g. parts of the same carved feature, but with gaps).
- Identify continuity of surface designs (e.g. parts of the same carved feature, but with gaps).
- Identify broader dimensional resemblance (e.g. the shape of the stone blocks used to make that sculptural facade).

## Expected Results

- Develop machine learning models that can reconstruct digitized fragments with at least 80% accuracy.
- Train AI model to search for matches between digitized fragments for which original orientation is certain.
- Test and train AI model using fragments for which original orientation is uncertain.

---

## Links

- [University of Alabama](https://www.ua.edu)
- [Human AI Foundation](https://humanai.foundation/gsoc/organizations/2025/alabama.html)
- [Notre Dame in Color](https://adhc1.ua.edu/notre_dame_in_color/)
- [Visual Documentation Lab](https://sites.ua.edu/atokovinine/3d-lab/)

---

## Mentors

| Name | Institution | Profile |
|---|---|---|
| Jennifer Feltman | University of Alabama | [About](https://art.ua.edu/people/jennifer-m-feltman/) |
| Alexandre Tokovinine | University of Alabama | [About](https://anthropology.ua.edu/people/alexandre-tokovinine/) |
| Emanuele Usai | University of Alabama | [About](https://physics.ua.edu/people/emanuele-usai/) |
| Sergei Gleyzer | University of Alabama | [About](https://physics.ua.edu/people/sergei-gleyzer/) |
| Lizzette Soto | University of Alabama | [About](https://anthropology.ua.edu/graduate-student/lizzette-soto/) |