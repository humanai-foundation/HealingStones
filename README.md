# Healing Stones

<div align="center">
   <img src="Puzzle2.jpg.jpeg" width=15% />
    Reconstructing Digitized Cultural Heritage Artifacts with Artificial Intelligence.
</div>

<br>


## Background
Historically works of art and architecture have been subjected to fragmentation: ancient Maya stelae were cut away from monuments by collectors; medieval sculptures from Notre-Dame in Paris were broken into multiple parts and dispersed in acts of political iconoclasm. Art historians and archaeologists seek to reconstruct these works to more fully understand their cultural meaning and value, however the traditional method of physical refitting is labor intensive and not always possible when fragments are dispersed throughout the world. We use AI in combination with existing digital scan models of fragments to develop a means for reconstructing fragmented cultural heritage artifacts in a virtual space. The project dataset used are the remaining and reconstructed stone fragments of Stela #43 from the archaeological site of Naranjo, in the Petén region of Guatemala. This stela, adorned with carved, high-relief images and hieroglyphs, holds immense historical significance in studying ancient Maya iconography and dating. Its reconstruction becomes particularly crucial in advancing new initiatives in the preservation of historical art and architecture.     

## Tasks
- Search for direct fit matches between surfaces (e.g. two parts of something broken).
- Identify continuity of carved topography (e.g. parts of the same carved feature, but with gaps).
- Identify continuity of surface designs (e.g. parts of the same carved feature, but with gaps).
- Identify broader dimensional resemblance (e.g. the shape of the stone blocks used to make that sculptural facade).


## Expected results
- Develop machine learning models that can reconstruct digitized fragments with at least 80% accuracy.
- Train AI model to search for matches between digitized fragments for which is original orientation is certain.
- Test and train AI model using fragments for which original orientation is uncertain.

## Links
[University of Alabama](https://www.ua.edu)

[Human AI Foundation](https://humanai.foundation/gsoc/organizations/2025/alabama.html)
 
[Notre Dame in Color](https://adhc1.ua.edu/notre_dame_in_color/)
  
[Visual Documentation Lab](https://sites.ua.edu/atokovinine/3d-lab/)



Clarification: `atif/` vs. `satvik/` Implementations

### Overview
This repository contains two distinct implementation directories — **`atif/`** and **`satvik/`** — which were developed in parallel by different contributors.  
Their purposes and maintenance status differ, and this section clarifies their roles.

| Directory | Purpose | Status | Recommended for New Contributors? |
|------------|----------|---------|----------------------------------|
| `atif/` | Early **experimental** pipeline used for initial prototyping and exploration of the HealingStones framework. Retained for reference and reproducibility of older experiments. | **Experimental / Legacy** | ❌ No |
| `satvik/` | **Current, actively maintained implementation** that reflects the latest design decisions, updated dependencies, and stable architecture. Intended for new development and general use. | **Active / Maintained** | ✅ Yes |

---

### Setup Guidance

1. **For new contributors**, use the `satvik/` implementation.  
2. **Install dependencies** from `satvik/requirements.txt`:
   ```bash
   cd satvik
   pip install -r requirements.txt

1. Follow the setup and usage instructions provided in satvik/README.md.
2. Only use the atif/ directory if you need to reproduce older results or review legacy experiments.
bashDownloadCopy codecd atif
pip install -r requirements.txt     # Only required for legacy reproduction



Why This Matters
Without clear distinction between these directories, contributors may:

* Install conflicting or outdated dependencies.
* Work within an unmaintained experimental branch.
* Duplicate efforts by following outdated pipelines.

Clarifying these details helps ensure smooth onboarding, consistent environment setup, and proper focus on the active (satvik/) pipeline.

Suggested Improvement Summary

* Add this clarification section to the main README.md.
* Indicate that satvik/ is the recommended starting point for all new contributors.
* Optionally include the maintenance status table above to guide future contributors.


## Mentors
|||| 
|-----------------|-----------------|-----------------
| Jennifer Feltman  | University of Alabama  | [About Link](https://art.ua.edu/people/jennifer-m-feltman/)
| Alexandre Tokovinine  | University of Alabama  | [About Link](https://anthropology.ua.edu/people/alexandre-tokovinine/)  
| Emanuele Usai|University of Alabama|[About Link](https://physics.ua.edu/people/emanuele-usai/)
| Sergei Gleyzer | University of Alabama|[About Link](https://physics.ua.edu/people/sergei-gleyzer/)
| Lizzette Soto| University of Alabama|[About Link](https://anthropology.ua.edu/graduate-student/lizzette-soto/)

