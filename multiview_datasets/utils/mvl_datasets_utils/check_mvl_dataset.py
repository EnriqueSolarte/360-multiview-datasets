
from multiview_datasets import HM3D_MVL
from multiview_datasets import ZInD_mvl
from multiview_datasets import MP3D_FPE_MVL
from multiview_datasets import VSLAB_DATASETS_FN_DEFAULT_CFG
from geometry_perception_utils.config_utils import read_omega_cfg


def check(data, endswith="", verbose=False):
    print(f"Total number of scenes: {len(data)}")
    not_found = 0
    for file, state in data.items():
        if file.endswith(endswith):
            if not state:
                if verbose:
                    print(f"SCENE: {file}  not found")
                not_found += 1
    print(f"Total number of files not found: {not_found}")
    return not_found == 0


def main(cfg):
    # dt = HM3D_MVL(cfg.hm3d_mvl)
    # dt = MP3D_FPE_MVL(cfg.mp3d_fpe_mvl)
    dt = ZInD_mvl(cfg.zind_mvl)
    data = dt.check_data()
    print("Checking images files")
    check(data, endswith=".jpg")
    print("Checking geometry info files")
    check(data, endswith=".json")
    print("Checking labels files")
    check(data, endswith=".npy", verbose=True)


if __name__ == '__main__':
    cfg = read_omega_cfg(VSLAB_DATASETS_FN_DEFAULT_CFG)
    main(cfg)
