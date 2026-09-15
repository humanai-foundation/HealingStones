# Healing Stones

<div align="center">
   <img src="Puzzle2.jpg.jpeg" width=15% />
    Reconstructing Digitized Cultural Heritage Artifacts with Artificial Intelligence.
</div>

<br>

## Implementations and setup

This repository contains two independent implementations. They explore related
fragment-reconstruction ideas, but they do **not** share a virtual environment
or a `requirements.txt` file.

### Recommended implementation: `Atif/GSoC_deep_learning_pipeline`

Use this implementation if you are a new contributor or want to work on the
main research pipeline. It is the current, phase-based workflow for the
Caesar statue dataset:

1. dataset foundation and fragment alignment
2. local patch generation
3. ground-truth and contact-pair generation
4. geometric descriptors, retrieval, and registration
5. diagnostics and the planned learned encoder

It includes the most complete documentation, configuration files, source
modules, generated phase outputs, and automated tests in this repository.
Install its dependencies from its own directory:

```bash
cd Atif/GSoC_deep_learning_pipeline
python -m pip install -r requirements.txt
```

Continue with [`Atif/GSoC_deep_learning_pipeline/README.md`](Atif/GSoC_deep_learning_pipeline/README.md)
or [`Atif/GSoC_deep_learning_pipeline/QUICKSTART.md`](Atif/GSoC_deep_learning_pipeline/QUICKSTART.md)
for the pipeline commands. The commands in those documents, including
`PYTHONPATH=src`, must be run from that directory.

### Alternative implementation: `Satvik/gsoc-2025-Healing-Stones-main`

This is an earlier, standalone geometric baseline. It uses pairwise
point-to-plane Iterative Closest Point (ICP), ranks fragment pairs, and builds
a global assembly before cleaning and colorizing the result. It is useful for
reproducing or extending the ICP baseline, but it is not a second setup step
for the recommended pipeline and its dependencies must not be installed
instead of Atif's.

To work on it independently:

```bash
cd Satvik/gsoc-2025-Healing-Stones-main
python -m pip install -r requirements.txt
```

Run the scripts described in
[`Satvik/gsoc-2025-Healing-Stones-main/README.md`](Satvik/gsoc-2025-Healing-Stones-main/README.md)
from that directory.

The `Atif/` and `Satvik/` directories are retained as separate research
implementations; choosing one does not require setting up the other.


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

## Mentors
|||| 
|-----------------|-----------------|-----------------
| Jennifer Feltman  | University of Alabama  | [About Link](https://art.ua.edu/people/jennifer-m-feltman/)
| Alexandre Tokovinine  | University of Alabama  | [About Link](https://anthropology.ua.edu/people/alexandre-tokovinine/)  
| Emanuele Usai|University of Alabama|[About Link](https://physics.ua.edu/people/emanuele-usai/)
| Sergei Gleyzer | University of Alabama|[About Link](https://physics.ua.edu/people/sergei-gleyzer/)
| Lizzette Soto| University of Alabama|[About Link](https://anthropology.ua.edu/graduate-student/lizzette-soto/)
