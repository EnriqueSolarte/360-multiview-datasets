import os
import json
from tqdm import tqdm
import numpy as np
from pyquaternion import Quaternion
from PIL import Image, ImageFile
from multiview_datasets.data_structure.cam_pose import CamPose
from multiview_datasets.data_structure.layout import Layout
from multiview_datasets.mvl_datasets.mvl_dataset import MVL_dataset
from geometry_perception_utils.spherical_utils import SphericalCamera
from typing import List
import logging
ImageFile.LOAD_TRUNCATED_IMAGES = True


class HM3D_MVL(MVL_dataset):
    def __init__(self, cfg):
        logging.info("Initializing HM3D_MVL dataloader...")
        super().__init__(cfg)
        logging.info("HM3D_MVL dataloader successfully initialized")

    def get_list_ly(self, idx=0, scene_name="") -> List[Layout]:
        """
        Returns a list of layout described by scene_name or scene idx
        """
        if scene_name == "":
            scene_data = self.data_scenes[self.list_scenes[idx]]
        else:
            scene_data = self.data_scenes[scene_name]

        self.list_ly = []
        cam = SphericalCamera(self.cfg.resolution)

        for frame in tqdm(scene_data, desc=f"Loading data scene {scene_name}..."):

            ly = Layout(self.cfg)
            ly.camera = cam
            ly.idx = os.path.splitext(frame)[0]

            ly.img_fn = os.path.join(self.DIR_IMGS, f"{ly.idx}.jpg")
            assert os.path.exists(ly.img_fn), f"Not found {ly.img_fn}"

            # phi_coords = np.load(os.path.join(self.cfg.labels_dir, f"{ly.idx}.npz"))['phi_coords']
            phi_coords_gt_fn = os.path.join(
                self.cfg.labels_dir, f"{ly.idx}")
            if os.path.exists(phi_coords_gt_fn + '.npy'):
                phi_coords = np.load(phi_coords_gt_fn + '.npy')
                ly.set_gt_phi_coords(phi_coords=phi_coords)

            elif os.path.exists(phi_coords_gt_fn + '.npz'):
                phi_coords = np.load(phi_coords_gt_fn + '.npz')["phi_coords"]
                ly.set_gt_phi_coords(phi_coords=phi_coords)

            # ! Loading geometry
            geom = json.load(
                open(os.path.join(self.DIR_GEOM_FILES, f"{ly.idx}.json")))

            self.set_geom_info(layout=ly, geom=geom)

            # ! Setting in WC
            ly.cam_ref = 'WC'

            self.list_ly.append(ly)

        return self.list_ly

    def set_geom_info(self, layout: Layout, geom):

        layout.pose = CamPose(layout.cfg)
        layout.pose.t = np.array(geom['translation'])  # * geom['scale']
        qx, qy, qz, qw = geom['quaternion']
        q = Quaternion(qx=qx, qy=qy, qz=qz, qw=qw)
        layout.pose.rot = q.rotation_matrix
        layout.pose.idx = layout.idx
        layout.camera_height = geom.get('cam_h', 1)


class MP3D_FPE_MVL(HM3D_MVL):
    def __init__(self, cfg):
        logging.info("Initializing MP3D_FPE_MVL dataloader...")
        super().__init__(cfg)
        logging.info("MP3D_FPE_MVL dataloader successfully initialized")
