## Cube Helper

![Tests](https://github.com/MetOffice/cube_helper/workflows/Tests/badge.svg) 
![PEP8](https://github.com/MetOffice/cube_helper/workflows/PEP8/badge.svg) 
[![Documentation Status](https://readthedocs.org/projects/cube-helper/badge/?version=latest)](https://cube-helper.readthedocs.io/en/latest/?badge=latest) 
![Licence](https://img.shields.io/github/license/MetOffice/cube_helper) 
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4073150.svg)](https://doi.org/10.5281/zenodo.4073150)



Cube Helper is a package to make equalisation, concatenation, and analysis of 
[Iris](https://scitools-iris.readthedocs.io/)
cubes easier. It is written with reasearchers in mind and provides a good degree of
abstraction from many Iris functions and methods.
 
The package is written entirely in Python and provides a number of reusable methods.

## Documentation

cube_helper's documentation is available from https://cube-helper.readthedocs.io/
 
## Requirements
Please ensure you have the following dependencies installed:  
`cf_units`  
`iris`  
`numpy`

## Installing

cube_helper is already installed at several sites. Please see their internal documentation for details of how to access it there. 

To install your own copy, then cube_helper is available via PyPI and conda-forge:

`pip install cube-helper`
`conda install -c conda-forge cube_helper`

Alternatively, make sure all the requirements are installed, then clone the repository
and set your Python environment to point to your copy, for example:  
`git clone https://github.com/MetOffice/cube_helper.git`  
`export PYTHONPATH=<path/to/cube_helper>`  

## Contributing  
If you want to contribute to Cube Helper be sure to review the 
[contribution guidelines](https://github.com/MetOffice/cube_helper/blob/master/CONTRIBUTING.md).

## License
[BSD-3 License](https://github.com/MetOffice/cube_helper/blob/master/LICENSE)
