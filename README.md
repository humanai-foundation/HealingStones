# Healing Stones

<div align="center">
   <img src="Puzzle2.jpg.jpeg" width=15% />
    Reconstructing Digitized Cultural Heritage Artifacts with Artificial Intelligence.
</div>

<br>


## Installation

The end-to-end geometric reconstruction pipeline is in
`Atif/GSoC_deep_learning_pipeline`. It uses Python 3.10 or newer and expects
the fragment data already included in that directory.


```bash

git clone <repository-or-fork-url>
cd <cloned-repository>/Atif/GSoC_deep_learning_pipeline

python3 -m venv .venv
source .venv/bin/activate             # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```


On Windows Command Prompt, activate the environment with
`.venv\Scripts\activate.bat`. If PowerShell blocks script activation, run
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and activate the
environment again.


## Usage

Run the phases from `Atif/GSoC_deep_learning_pipeline` in order. Each phase
reads the output of the previous phase and writes its results to the
corresponding output directory.


```bash
# Phase 1: align, normalize, estimate normals, and validate the fragments
PYTHONPATH=src python -m dataset_foundation.pipeline --config config/default.yaml

# Phase 2: sample and extract local geometric patches
PYTHONPATH=src python -m patch_generation.pipeline --config config/patch_generation.yaml

# Phase 3: generate fragment-pair ground truth and contact regions
PYTHONPATH=src python scripts/phase3_pipeline.py --config config/ground_truth.yaml

# Phase 4: compute descriptors, retrieve candidate matches, and register pairs
PYTHONPATH=src python -m baseline_geometry.pipeline --config config/baseline_geometry.yaml
```

The commands above create aligned point clouds and metadata in `dataset/`,
patch archives in `patches/`, labelled pairs in `pairs/`, and descriptor,
retrieval, registration, and visualization results in `baseline_results/`.
The original model is used to create training ground truth; it is not required
at inference time.


### Windows `PYTHONPATH`

The `PYTHONPATH=src` prefix is the POSIX shell syntax. Use the equivalent
command for your Windows shell:


```powershell

# PowerShell
$env:PYTHONPATH = "src"
python -m dataset_foundation.pipeline --config config/default.yaml
```


```bat

:: Command Prompt
set PYTHONPATH=src
python -m dataset_foundation.pipeline --config config\default.yaml
```


### Visualize results

Use the interactive viewer when a graphical display is available:

```bash
PYTHONPATH=src python scripts/visualize.py --interactive
PYTHONPATH=src python scripts/visualize_patches.py \
  --fragment fragment_caesar_fragment_1 --mode heatmap
PYTHONPATH=src python scripts/explore_fragment.py --fragment 1
```

For headless environments, generate an image instead of opening a window:

```bash
PYTHONPATH=src python scripts/visualize.py --save
```

The saved Phase 1 visualization is written to
`dataset/visualization.png`.


### Run tests

```bash

python -m pytest tests/ -q
```

Run a focused test group when iterating on one phase:


```bash
python -m pytest tests/baseline_geometry/ -q
python -m pytest tests/patch_generation/ -q
```


## Pipeline layout

```text
Atif/GSoC_deep_learning_pipeline/
├── data/                  # Full Caesar model and seven fragment PLY files
├── config/                # YAML configuration for each pipeline phase
├── src/                   # Dataset, patch, ground-truth, and geometry modules
├── scripts/               # Visualization, alignment, and phase utilities
├── dataset/               # Phase 1 generated outputs
├── patches/               # Phase 2 generated patch archives
├── pairs/                 # Phase 3 generated pair labels and contacts
├── baseline_results/      # Phase 4 descriptors and registration results
└── tests/                 # Unit, property, and integration tests
```

For detailed phase-specific commands and configuration options, see
[`Atif/GSoC_deep_learning_pipeline/QUICKSTART.md`](Atif/GSoC_deep_learning_pipeline/QUICKSTART.md)
and
[`Atif/GSoC_deep_learning_pipeline/COMMANDS.md`](Atif/GSoC_deep_learning_pipeline/COMMANDS.md).


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

