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

## Repository Structure and Implementations

This repository currently contains multiple experimental and research implementations developed as part of different GSoC efforts. Each directory serves a distinct purpose.

### Atif/Gsoc-HealingStones
This directory contains a Python-based reconstruction pipeline with modular components for fragment processing, feature extraction, alignment, matching, and visualization.

Key characteristics:
- Script-based pipeline (`main_pipeline.py`, `batch_processor.py`)
- Modular architecture (feature extraction, surface matching, alignment)
- Uses `requirements.txt` for dependencies
- Intended for running end-to-end reconstruction experiments

This implementation is suitable for users who want to run or extend the reconstruction pipeline.

### Satvik/gsoc-2025-Healing-Stones-main
This directory contains exploratory work, documentation, and experimental artifacts produced during a separate GSoC effort.

Key characteristics:
- Contains progress logs and documentation
- Includes images and experimental resources
- May not represent a complete runnable pipeline

This implementation is useful for understanding research progress and exploratory approaches.

### Which should I use?
- If you want to **run or modify code**, start with `Atif/Gsoc-HealingStones`
- If you want to **review research progress or documentation**, explore `Satvik/gsoc-2025-Healing-Stones-main`



## Expected results
- Develop machine learning models that can reconstruct digitized fragments with at least 80% accuracy.
- Train AI model to search for matches between digitized fragments for which is original orientation is certain.
- Test and train AI model using fragments for which original orientation is uncertain.

## Links
[University of Alabama](https://www.ua.edu)

[Human AI Foundation](https://humanai.foundation/gsoc/organizations/2025/alabama.html)
 
[Notre Dame in Color](https://adhc1.ua.edu/notre_dame_in_color/)
  
[Visual Documentation Lab](https://sites.ua.edu/atokovinine/3d-lab/)

## Mentors
|||| 
|-----------------|-----------------|-----------------
| Jennifer Feltman  | University of Alabama  | [About Link](https://art.ua.edu/people/jennifer-m-feltman/)
| Alexandre Tokovinine  | University of Alabama  | [About Link](https://anthropology.ua.edu/people/alexandre-tokovinine/)  
| Emanuele Usai|University of Alabama|[About Link](https://physics.ua.edu/people/emanuele-usai/)
| Sergei Gleyzer | University of Alabama|[About Link](https://physics.ua.edu/people/sergei-gleyzer/)
| Lizzette Soto| University of Alabama|[About Link](https://anthropology.ua.edu/graduate-student/lizzette-soto/)

