import hydra
from geometry_perception_utils.io_utils import get_abs_path
from geometry_perception_utils.config_utils import save_cfg
from multiview_datasets.mvl_datasets import load_mvl_dataset
from geometry_perception_utils.vispy_utils import plot_list_pcl
from geometry_perception_utils.image_utils import draw_boundaries_phi_coords
from imageio.v2 import imwrite
from tqdm import tqdm
import numpy as np


@hydra.main(version_base=None,
            config_path=get_abs_path(__file__),
            config_name="cfg")
def main(cfg):
    data = load_mvl_dataset(cfg.mvl_dataset)
    list_ly = data.get_list_ly()
    [ly.set_gt_phi_coords_as_default() for ly in list_ly]

    for ly in tqdm(list_ly):

        xyz = (ly.boundary_floor, ly.boundary_ceiling)
        canvas = plot_list_pcl(xyz, elevation=20, return_canvas=True)
        img = canvas.render()
        imwrite(f"{cfg.log_dir}/boundaries_3d.png", img)
        input("Press Enter to continue...")


if __name__ == '__main__':
    main()
