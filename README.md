# Multiview Datasets

This repository contains the code for handling several multiview datasets. 
In particular, it contains the following datasets:

- [MP3D-VO Dataset](https://github.com/EnriqueSolarte/robust_360_8PA): A dataset of sequence of 360-images for visual odometry task.
- [MP3D-FPE Dataset](https://github.com/EnriqueSolarte/direct_360_FPE): A dataset for floor plan estimation using multiple 360-images.
- [MP3D-FPE-MLV Dataset](https://github.com/EnriqueSolarte/360-mlc): A dataset for multiview layout estimation. Particularly, for self-training 360-layout models.
- [360-HM3D-MLV Dataset](https://github.com/EnriqueSolarte/360-mlc): A dataset for multiview layout estimation using HM3D dataset.

## Installation

### Create a virtual environment
```sh 
conda create -n mv_datasets python=3.9
conda activate mv_datasets
```

### Install the package from the repository
```sh
pip install git+https://github.com/EnriqueSolarte/multiview-datasets.git
```

### For installing this package in dev mode (for development)
```sh 
git clone git@github.com:EnriqueSolarte/multiview-datasets.git
cd multiview-datasets
pip install -e .
```
