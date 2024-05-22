
# PAUSED-EV-CHARGING[![DOI](https://zenodo.org/badge/776002789.svg)](https://zenodo.org/doi/10.5281/zenodo.10932795)

![Static Badge](https://img.shields.io/badge/MADE_WITH-PYTHON_-orange?style=for-the-badge)

[![matplotlib](https://img.shields.io/badge/matplotlib-3.5.1-blue.svg)](https://pypi.org/project/matplotlib/3.5.1/)
[![numpy](https://img.shields.io/badge/numpy-1.22.3-blue.svg)](https://pypi.org/project/numpy/1.22.3/)
[![pandas](https://img.shields.io/badge/pandas-1.4.3-blue.svg)](https://pypi.org/project/pandas/1.4.3/)
[![tqdm](https://img.shields.io/badge/tqdm-4.62.3-blue.svg)](https://pypi.org/project/tqdm/4.62.3/)
[![Gurobi Version](https://img.shields.io/badge/Gurobi-10.0.2-blue.svg)](https://www.gurobi.com/)

This repository contains the codes and results which is published in the paper titled: **"Enhancing smart charging in electric vehicles by addressing paused and delayed charging problems"**.

The following repository is maintained by [Nico Brinkel](https://github.com/nicobrinkel) and [Nanda Kishor Panda](https://github.com/nkpanda97)

<inkline>
  <picture>
    <source srcset="https://fonts.gstatic.com/s/e/notoemoji/latest/1f31f/512.webp" type="image/webp">
    <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f31f/512.gif" alt="🌟" width="25" height="25">
  </picture>
</inkline> <span style="font-size:1.8em;font-style:italic">Highlights</span>

&#x2705; Many electric vehicle models lack the technical capabilities for effective smart charging, as they cannot handle charging pauses or delays. 🚗 🚙  <br>
&#x2705; Technical charging tests reveal that around one-third of tested car models suffer from these charging issues. <br>
&#x2705; Model simulations suggest that eliminating these problems would double the smart charging potential for all applications. <br>
&#x2705; Concrete legal and practical solutions are proposed to address these issues. ⚖️ <br>

## File organization

The repository is organized as follows:

- 📁 [data](data/): Contains the data used in the paper. This folder contains the following data:
    - [Day ahead prices for the Netherlands (2022) [CSV]](data/DA_prices_NL.csv) 
    - [Day ahead prices for the Netherlands (2022) [PKL]](data/DA_prices_NL.pkl)
    - [Sample of 100 EV charging sessions [CSV]](data/ev_sample_data.csv) 
    - [Example of non-EV load profiles [PKL]](data/NonEVload_example.pkl) 
    - [Excel containing source data for all figures [XLSX]](<data/Source Data.xlsx>)

- 📁 [helper_functions](matlab_functions/): Contains the required functions needed to run the [main](main.ipynb) python notebook. This folder contains the following functions:
    - <img src="python_logo.png" alt="python logo" width="15" height="15"> [cost_minimization_model.py](helper_functions/cost_minimization_model.py): Contains the functions to run the cost minimization model
    - <img src="python_logo.png" alt="python logo" width="15" height="15"> [flexibility_offering_model.py](helper_functions/flexibility_offering_model.py): Contains the functions to run the flexibility offering model
    - <img src="python_logo.png" alt="python logo" width="15" height="15"> [peak_minimization_model.py](helper_functions/peak_minimization_model.py): Contains the functions to run the peak minimization model
    - <img src="python_logo.png" alt="python logo" width="15" height="15"> [uncontrolled_charging_costs_model.py](helper_functions/uncontrolled_charging_costs_model.py): Contains the functions to run the uncontrolled charging cost model
    - <img src="python_logo.png" alt="python logo" width="15" height="15"> [uncontrolled_charging_model.py](helper_functions/uncontrolled_charging_model.py): Contains the functions to run the uncontrolled charging model
    - <img src="python_logo.png" alt="python logo" width="15" height="15"> [uncontrolled_charging_peak_model.py](helper_functions/uncontrolled_charging_peak_model.py): Contains the functions to run the uncontrolled charging peak model
    

- <img src="Jupyter_logo.png" alt="python logo" width="15" height="15"> [main.ipynb](main.py): Contains the main code to run the results of the paper and other functions.
- [.gitignore](.gitignore): Contains the files to be ignored by git
- [LICENSE](LICENSE): Contains the license information


## Installation

***Step 1:*** Clone the repository

```bash
git clone <repo-link>
```

***Step 2:*** Install the required packages
The code is tested on [![Python Version](https://img.shields.io/badge/Python-3.10.13-blue.svg)](https://www.python.org/downloads/release/python-3812/). The required packages are listed in the [requirements.txt](requirements.txt) file. To install the required packages, run the following command:

```bash
pip install -r requirements.txt
```

or

```bash
conda install --file requirements.txt
```

For the optimization solver, we used [![gurobipy](https://img.shields.io/badge/gurobipy-11.0.1-blue.svg)](https://www.gurobi.com/)
. You can install the Gurobi license by following the instructions in the [Gurobi Documentation](https://www.gurobi.com/documentation/10.0/quickstart_mac/installing_the_anaconda_py.html) for Mac and Linux and [Gurobi Documentation](https://www.gurobi.com/documentation/10.0/quickstart_windows/installing_the_anaconda_py.html) for Windows.

## Cite this work

If you re-use part of the code or some of the functions, please consider citing the repository:

```bibtex
@software{brinkel_2024_10932796,
  author       = {Brinkel, Nico and
                  Nanda Kishor Panda},
  title        = {{ROBUST-NL/paused\_ev\_charging: Publication ready 
                   code}},
  month        = apr,
  year         = 2024,
  publisher    = {Zenodo},
  version      = {v0.1.0},
  doi          = {10.5281/zenodo.10932796},
  url          = {https://doi.org/10.5281/zenodo.10932796}
}
```

## Funding

This study was supported by the Topsector Energy subsidy scheme of the Dutch Ministry of Economic Affairs and Climate Policy through the project "Slim laden met flexibele nettarieven in Utrecht ([FLEET](https://ssc-fleet.nl/))", by the Dutch Ministry of Economic Affairs and Climate Policy and the Dutch Ministry of the Interior and Kingdom Relations through the [ROBUST](https://tki-robust.nl/) project under grant agreement MOOI32014 and by the European Union’s Horizon Europe Research and Innovation program through the [SCALE](https://scale-horizon.eu/) project (Grant Agreement No. 101056874).

