
from multiview_datasets import HM3D_MVL
from multiview_datasets import ZInD_mvl
from multiview_datasets import MP3D_FPE_MVL
from multiview_datasets import VSLAB_DATASETS_FN_DEFAULT_CFG
from geometry_perception_utils.config_utils import read_omega_cfg
import json
import os
from pathlib import Path
import numpy as np
import shutil
from tqdm import tqdm
from multiprocessing.pool import ThreadPool


# SRC_DIR = "/media/public_dataset/mvl_challenge/mp3d_fpe/merged_data/geometry_info"
SRC_DIR = "/media/public_dataset/mvl_challenge/mvl_challenge_dataset/geometry_info"


def main(cfg):

    dt = MP3D_FPE_MVL(cfg.mp3d_fpe_mvl)
    # dt =  HM3D_MVL(cfg.hm3d_mvl)

    list_geometry_info_src = os.listdir(SRC_DIR)
    list_frames = list(dt.data_scenes.values())
    list_frames = [item for sublist in list_frames for item in sublist]

    check = [f"{f}.json" in list_geometry_info_src for f in list_frames]
    print(f"Total frames found: {len(check)}")
    print(f"Total frames: {len(list_frames)}")
    print(f"Total frames not found: {len(check) - np.sum(check)}")

    assert np.sum(check) == len(check)

    pool = ThreadPool(10)

    def __copy(_frame):
        shutil.copy(
            dst=os.path.join(dt.DIR_GEOM_FILES, f"{_frame}.json"),
            src=os.path.join(SRC_DIR, f"{_frame}.json")
        )

    list_threads = []
    for frame in list_frames:
        list_threads.append(pool.apply_async(__copy, (frame,)))

    [th.get() for th in tqdm(list_threads)]


if __name__ == '__main__':
    cfg = read_omega_cfg(VSLAB_DATASETS_FN_DEFAULT_CFG)
    main(cfg)
