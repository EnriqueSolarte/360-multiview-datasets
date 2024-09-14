from typing import Any
import numpy as np
from geometry_perception_utils.geometry_utils import isRotationMatrix

# TODO:
# 1. Add method to get the inverse pose -> get_inv()
# 2. Eval and Add faster method to cam pose transformation R + t -> SE3
# 3. If we know that some Transf are in 2D (e.g. BEV),  we can use a faster method


class CAM_REF:
    WC = "WC"  # ! World Coordinates
    CC = "CC"  # ! Cameras Coordinates
    WC_SO3 = "WC_SO3"  # ! World Coordinates only Rot applied
    ROOM = "ROOM_REF"  # ! Room Coordinates (primary frame)


class CamPose:
    def __init__(self, cfg):
        self.cfg = cfg
        self.SE3 = np.eye(4)
        self.vo_scale = 1
        self.gt_scale = 1
        self.idx = None
        self.camera_height = 1

    def __call__(self):
        return self.SE3_scaled()

    @property
    def vo_scale(self):
        return self.__vo_scale

    @vo_scale.setter
    def vo_scale(self, value):
        assert value > 0
        self.__vo_scale = value

    @property
    def SE3(self):
        return self.__pose

    @SE3.setter
    def SE3(self, value):
        assert value.shape == (4, 4)
        self.__pose = value
        self.rot = value[0:3, 0:3]
        self.t = value[0:3, 3]

    @property
    def rot(self):
        return self.__rot

    @rot.setter
    def rot(self, value):
        assert isRotationMatrix(value)
        self.__rot = value
        self.__pose[:3, :3] = value

    @property
    def t(self):
        return self.__t * self.vo_scale * self.gt_scale

    @t.setter
    def t(self, value):
        assert value.reshape(3, ).shape == (3, )
        self.__t = value.reshape(3, )
        self.__pose[:3, 3] = value

    def SE3_scaled(self):
        m = np.eye(4)
        m[0:3, 0:3] = self.rot
        m[0:3, 3] = self.t
        return m

    def get_inv(self):
        m = np.eye(4)
        m[0:3, 0:3] = self.rot.T
        m[0:3, 3] = - (self.rot.T @ self.t.reshape((3, 1))).ravel()
        return m

    def set_vo_scale(self, vo_scale):
        self.vo_scale = vo_scale
