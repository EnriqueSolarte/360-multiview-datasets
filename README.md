# Multiview Datasets

This repository contains the code for handling several multiview datasets. 
In particular, it contains the following datasets:

- [ ] [MP3D-VO Dataset](https://github.com/EnriqueSolarte/robust_360_8PA): A dataset of sequence of 360-images for visual odometry task.
- [ ] [MP3D-FPE Dataset](https://github.com/EnriqueSolarte/direct_360_FPE): A dataset for floor plan estimation using multiple 360-images.
- [x] [MP3D-FPE-MLV Dataset](https://github.com/EnriqueSolarte/360-mlc): A dataset for multiview layout estimation. Particularly, for self-training 360-layout models.
- [x] [360-HM3D-MLV Dataset](https://github.com/EnriqueSolarte/360-mlc): A dataset for multiview layout estimation using HM3D dataset.

## Installation

### Create a virtual environment
```sh 
conda create -n mv_datasets python=3.9
conda activate mv_datasets
```

### Install the package from the repository
```sh

# Installing version v1.0.24.11.24
pip install git+https://github.com/EnriqueSolarte/multiview-datasets.git@v1.0.24.11.24
```

### For installing this package in dev mode (for development)
```sh 
git clone git@github.com:EnriqueSolarte/multiview-datasets.git
cd multiview-datasets
pip install -e .
```

## Download MLV-Datasets
The mvl-datasets is host in [huggingface/EnriqueSolarte/mvl_datasets](https://huggingface.co/datasets/EnriqueSolarte/mvl_datasets) 🤗. 

> [!WARNING]  
> To access to the mvl-datasets (i.e., hm3d-mvl, mp3d-mvl, and zind-mvl), you need to create an account and login on HuggingFace and accept the terms and conditions described [HERE](https://huggingface.co/datasets/EnriqueSolarte/mvl_datasets). 

After you get access to the datasets, you have to login your account in your system by following the next commands:

```bash
# Install huggingface CLI 
pip install -U "huggingface_hub[cli]"

# Login to your account
huggingface-cli login

# Login to your account
huggingface-cli whoami
```

Ideally, after login you can download the mvl-dataset by executing the next commands: 
```bash

# To download and save the dataset in DIR_DATASET
python examples/download_mvl_data/mvl_datasets.py dir_mvl_dataset=${DIR_DATASET}

# To download mp3d_fpe_mvl, hm3d_mvl, or zind_mvl 
python examples/download_mvl_data/mvl_datasets.py dir_mvl_dataset=${DIR_DATASET} dataset=${DATASET_NAME}

# To use the default OmegaConfig in the examples/download_mvl_data/cfg.yaml 
python examples/download_mvl_data/mvl_datasets.py
```

> [!NOTE]
> These datasets were officially proposed in [360-MLC - NeuriPS'22](https://github.com/EnriqueSolarte/360-mlc) and [Ray-casting MLC - ECCV'24](https://github.com/EnriqueSolarte/ray_casting_mlc?tab=readme-ov-file). If you use them, please cite them accordingly. 


For the `hm3d_mvl` dataset please cite the following paper:

```bibtex
@article{solarte2024_ray_casting_mlc,
    title   ={Self-training Room Layout Estimation via Geometry-aware Ray-casting}, 
    author  ={Bolivar Solarte and Chin-Hsuan Wu and Jin-Cheng Jhang and Jonathan Lee and Yi-Hsuan Tsai and Min Sun},
    journal ={European Conference on Computer Vision (ECCV)},
    year    ={2024},
    url     ={https://arxiv.org/abs/2407.15041}, 
}
```

For the `mp3d_fpe_mvl` dataset please cite the following paper:
```bibtex
@article{Solarte2022_360_MLC,
    title   ={360-mlc: Multi-view layout consistency for self-training and hyper-parameter tuning},
    author  ={Solarte, Bolivar and Wu, Chin-Hsuan and Liu, Yueh-Cheng and Tsai, Yi-Hsuan and Sun, Min},
    journal ={Advances in Neural Information Processing Systems (NeurIPS)},
    volume  ={35},
    pages   ={6133--6146},
    year    ={2022}
}
```

For the `zind-mvl` dataset please cite the following paper:
```bibtex
@inproceedings{ZInD,
  title     = {Zillow Indoor Dataset: Annotated Floor Plans With 360º Panoramas and 3D Room Layouts},
  author    = {Cruz, Steve and Hutchcroft, Will and Li, Yuguang and Khosravan, Naji and Boyadzhiev, Ivaylo and Kang, Sing Bing},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  month     = {June},
  year      = {2021},
  pages     = {2133--2143}
}
```

