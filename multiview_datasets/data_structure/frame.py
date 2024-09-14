import os
import os

import numpy as np
from imageio import imread

from geometry_perception_utils.geometry_utils import extend_array_to_homogeneous
from geometry_perception_utils.image_utils import load_depth_map


class Frame:
    def __init__(self):
        self.camera = None
        self.rgb = None
        self.depth = None
        self.pose = None
        self.idx = None
        self.__reverse_color = False

    def get_rgb(self):
        if type(self.rgb) == str:
            if not os.path.exists(self.rgb):
                raise FileNotFoundError(self.rgb)
            if self.__reverse_color:
                self.rgb = np.array(imread(self.rgb))[:, :, ::-1]
            else:
                self.rgb = np.array(imread(self.rgb))
            return self.rgb
        if type(self.rgb) == np.ndarray:
            return self.rgb

    def get_depth(self):
        if type(self.depth) == str:
            if not os.path.exists(self.depth):
                raise FileNotFoundError(self.depth)
            self.depth = load_depth_map(self.depth)
            return self.depth
        if type(self.depth) == np.ndarray:
            return self.depth

    def get_color_pcl(self):
        color_map = self.get_rgb()
        depth_map = self.get_depth()
        if (depth_map is None) or (color_map is None):
            return None
        pcl, color = self.camera.get_color_pcl_from_depth_and_rgb_maps(
            color_map=color_map,
            depth_map=depth_map,
        )
        return np.vstack((pcl, color))
