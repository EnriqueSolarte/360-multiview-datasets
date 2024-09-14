import os
import json
from tqdm import tqdm
from geometry_perception_utils.geometry_utils import eulerAnglesToRotationMatrix
import numpy as np
from PIL import Image, ImageFile
from multiview_datasets.data_structure.cam_pose import CamPose
from multiview_datasets.data_structure.layout import Layout
from multiview_datasets.mvl_datasets.mvl_dataset import MVL_dataset
from geometry_perception_utils.spherical_utils import SphericalCamera
ImageFile.LOAD_TRUNCATED_IMAGES = True


class ZInD_mvl(MVL_dataset):
    def __init__(self, cfg):
        print("Initializing ZinD-MVL dataloader...")
        super().__init__(cfg)
        print("ZinD-MVL dataloader successfully initialized")

    def get_list_ly(self, idx=0, scene_name=""):
        """
        Returns a list of layout described by scene_name or scene idx
        """
        if scene_name == "":
            # When no scene_name has been passed
            scene_data = self.data_scenes[self.list_scenes[idx]]
        else:
            scene_data = self.data_scenes[scene_name]

        self.list_ly = []
        cam = SphericalCamera(self.cfg.resolution)
        for frame in tqdm(scene_data, desc=f"Loading data scene {scene_name}..."):

            ly = Layout(self.cfg)
            ly.camera = cam
            ly.idx = os.path.splitext(frame)[0]

            # ! Loading img
            ly.img_fn = os.path.join(self.DIR_IMGS, f"{ly.idx}.jpg")

            try:
                phi_coords = np.load(os.path.join(
                    self.cfg.labels_dir, f"{ly.idx}.npy"))
                ly.set_gt_phi_coords(phi_coords=phi_coords)
            except:
                if "testing" in self.cfg.scene_list:
                    raise FileNotFoundError(
                        f"Phi coords not found for {ly.idx}")
                else:
                    print(f"Phi coords not found for {ly.idx}")

            # ! Loading geometry
            geom = json.load(
                open(os.path.join(self.DIR_GEOM_FILES, f"{ly.idx}.json")))

            self.set_geom_info(layout=ly, geom=geom)

            # ! Setting in WC
            ly.cam_ref = 'WC'

            self.list_ly.append(ly)
        return self.list_ly

    def set_geom_info(self, layout, geom):
        layout.pose = CamPose(layout.cfg)
        x, z = geom['translation']
        layout.pose.t = np.array((-x, 0, z))
        layout.pose.rot = eulerAnglesToRotationMatrix(
            [0, np.radians(geom['rotation']), 0])[:3, :3]
        layout.pose.idx = layout.idx
        layout.ceiling_height = geom['ceiling_height'] * geom['scale']
        layout.camera_height = geom['camera_height'] * geom['scale']
        layout.scale = geom['scale']
        layout.primary = geom['primary']


if __name__ == '__main__':
    from multiview_datasets import VSLAB_DATASETS_FN_DEFAULT_CFG
    from geometry_perception_utils.config_utils import read_omega_cfg
    from geometry_perception_utils.vispy_utils import plot_color_plc
    from imageio import imwrite

    cfg = read_omega_cfg(VSLAB_DATASETS_FN_DEFAULT_CFG)
    dt = ZInD_mvl(cfg.zind_mvl)

    for scene in dt.list_scenes:
        list_ly = dt.get_list_ly(scene_name=scene)
        [ly.set_gt_phi_coords_as_default() for ly in list_ly]
        pcl = [ly.boundary_floor for ly in list_ly]
        plot_color_plc(np.hstack(pcl).T)
        # for ly in list_ly:
        #     plot_color_plc(ly.boundary_floor.T)

        print("done")
