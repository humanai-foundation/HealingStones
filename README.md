# 🧱 Healing Stones  
**Reconstructing Digitized Cultural Heritage Artifacts with Artificial Intelligence**

<div align="center">
  <img src="Puzzle2.jpg.jpeg" width="15%" />
  <br/>
  <em>Preserving cultural heritage through AI-driven digital reconstruction</em>
</div>

---

## Background

Historically, works of art and architecture have been subjected to fragmentation due to natural decay, conflict, and human intervention. Ancient Maya stelae were cut away from monuments by collectors, while medieval sculptures from sites such as Notre-Dame in Paris were broken into multiple parts during periods of political iconoclasm.

Art historians and archaeologists seek to reconstruct these artifacts to better understand their cultural meaning and historical context. However, traditional physical refitting is labor-intensive and often infeasible when fragments are dispersed across different locations.

**Healing Stones** explores the use of **artificial intelligence and 3D computer vision** to virtually reconstruct fragmented cultural heritage artifacts. By leveraging digitized 3D scan models, the project aims to assist researchers in assembling fragmented objects in a virtual space. The primary dataset focuses on stone fragments from **Stela #43** at the archaeological site of **Naranjo** in the Petén region of Guatemala—an artifact of immense significance for the study of ancient Maya iconography and chronology.

---

## Project Objectives

The project investigates machine learning and geometric approaches to:

- Search for direct surface matches between fragmented pieces  
- Identify continuity in carved topography across fragments  
- Detect continuity in surface designs, even with missing regions  
- Analyze broader dimensional resemblance between stone blocks  

---

## Expected Outcomes

- Development of models capable of reconstructing digitized fragments with high accuracy  
- Identification of fragment matches when original orientation is known  
- Robust handling of fragments with unknown or uncertain orientation  
- A reusable framework for virtual reconstruction of cultural heritage artifacts  

---

## Project Structure

The repository is organized as follows:

```text

├── data/                  # Input 3D fragment files (.PLY)
├── scripts/               # Core reconstruction, alignment, and analysis scripts
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── (additional files and folders)

```

---

## Getting Started

These instructions help you set up the project locally and understand the overall workflow.  
Basic familiarity with **Python** and **3D point cloud data** is recommended.

---

## Installation

It is strongly recommended to use a virtual environment.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate    # Linux / macOS
venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

```

## Dataset and Input Format

The reconstruction pipeline operates on fragmented 3D point cloud files in .PLY format.


- Each .PLY file should represent a single artifact fragment

- Fragment files should be placed inside the data/ directory

- Colored fragments (if available) can improve surface detection and matching quality

#### Note: Example datasets are not included due to cultural heritage access restrictions and data ownership policies.

## Typical Workflow

**1.** Place fragment .PLY files into the data/ directory

**2.** Run surface detection and pairwise matching scripts

**3.** Analyze similarity and alignment scores

**4.** Perform global fragment assembly

**5.** Visualize and evaluate the reconstructed artifact

Refer to the scripts in the scripts/ directory for specific execution details

## Contributing

### Contributions are welcome!

#### If you are new to the project:

- Start by running the existing pipeline locally

- Improve documentation, usability, or visualizations

- Open issues for bugs or enhancement ideas


#### To contribute:

**1.** Fork the repository  
**2.** Create a new branch  
**3.** Submit a pull request with a clear description of your changes  
  


## Links

- **University of Alabama**: https://www.ua.edu
- **HumanAI Foundation**: https://humanai.foundation/gsoc/organizations/2025/alabama.html
- **Notre Dame in Color**: https://adhc1.ua.edu/notre_dame_in_color/
- **Visual Documentation Lab**: https://sites.ua.edu/atokovinine/3d-lab/

## Mentors



| Name                 | Affiliation           | Profile                                                              |
| -------------------- | --------------------- | -------------------------------------------------------------------- |
| Jennifer Feltman     | University of Alabama | [About](https://art.ua.edu/people/jennifer-m-feltman/)               |
| Alexandre Tokovinine | University of Alabama | [About](https://anthropology.ua.edu/people/alexandre-tokovinine/)    |
| Emanuele Usai        | University of Alabama | [About](https://physics.ua.edu/people/emanuele-usai/)                |
| Sergei Gleyzer       | University of Alabama | [About](https://physics.ua.edu/people/sergei-gleyzer/)               |
| Lizzette Soto        | University of Alabama | [About](https://anthropology.ua.edu/graduate-student/lizzette-soto/) |








