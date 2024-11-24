import hydra
from geometry_perception_utils.io_utils import get_abs_path
from geometry_perception_utils.config_utils import save_cfg
from multiview_datasets.mvl_datasets import load_mvl_dataset
from geometry_perception_utils.vispy_utils import plot_list_pcl
from geometry_perception_utils.image_utils import draw_boundaries_phi_coords
from imageio.v2 import imwrite
from tqdm import tqdm


@hydra.main(version_base=None,
            config_path=get_abs_path(__file__),
            config_name="cfg")
def main(cfg):
    data = load_mvl_dataset(cfg.mvl_dataset)
    list_ly = data.get_list_ly(idx=3)
    [ly.set_gt_phi_coords_as_default() for ly in list_ly]

    for ly in tqdm(list_ly):
        img = ly.get_rgb()
        img = draw_boundaries_phi_coords(img, ly.gt_phi_coord)
        fn = f"{cfg.log_dir}/boundaries.jpg"
        imwrite(fn, img)
        print(f"Image Visualization save at {fn}")
        input("Press Enter to continue...")


if __name__ == '__main__':
    main()
