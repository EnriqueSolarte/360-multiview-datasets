import os
import json
import numpy as np
from tqdm import tqdm
from multiprocessing.pool import ThreadPool
import logging
from abc import ABC, abstractmethod
from typing import List
from multiview_datasets.data_structure.layout import Layout


class MVL_dataset(ABC):
    def __init__(self, cfg):
        self.cfg = cfg
        self.set_paths()

    def set_paths(self):
        # * Set main lists of files
        #! List of scene names
        assert os.path.exists(self.cfg.scene_list)
        logging.info(f"Scene list: {self.cfg.scene_list}")
        self.data_scenes = json.load(
            open(self.cfg.scene_list, 'r'))

        self.DIR_GEOM_FILES = self.cfg.geometry_info_dir
        self.DIR_IMGS = self.cfg.img_dir
        self.LABELS_DIR = self.cfg.labels_dir

        assert os.path.exists(
            self.DIR_GEOM_FILES), f"Path to geometry info does not exist: {self.DIR_GEOM_FILES}"
        assert os.path.exists(
            self.DIR_IMGS), f"Path to images does not exist: {self.DIR_IMGS}"
        if not os.path.exists(self.LABELS_DIR):
            logging.warn(f"Path to labels does not exist: {self.LABELS_DIR}")

        if self.cfg.get("size", -1) > 0:
            if self.cfg.size > 1:
                self.list_scenes = list(self.data_scenes.keys())
                np.random.shuffle(self.list_scenes)
                self.list_scenes = self.list_scenes[:self.cfg.size]
            else:
                self.list_scenes = list(self.data_scenes.keys())
                np.random.shuffle(self.list_scenes)
                self.list_scenes = self.list_scenes[:int(
                    self.list_scenes.__len__() * self.cfg.size)]
            return
        self.list_scenes = list(self.data_scenes.keys())
        self.get_data_info()

    def get_data_info(self):
        a = [dt.__len__() for dt in self.data_scenes.values()]
        logging.info(f"Total number of frame scenes: {np.sum(a)}")
        logging.info(f"Total number of room scenes: {a.__len__()}")

    def check_data(self):
        data = {}
        pool = ThreadPool(10)

        def __check_data(_scene):
            list_frames = [sc for sc in self.data_scenes[_scene]]
            for frame in list_frames:
                geometry_fn = os.path.join(
                    self.DIR_GEOM_FILES, f"{frame}.json")
                img_fn = os.path.join(self.DIR_IMGS, f"{frame}.jpg")
                labels_fn = os.path.join(self.LABELS_DIR, f"{frame}.npy")
                for geometry_fn in [geometry_fn, img_fn, labels_fn]:
                    data[geometry_fn] = os.path.exists(geometry_fn)

        list_threads = []
        for scene in self.list_scenes:
            list_threads.append(pool.apply_async(__check_data, (scene,)))

        [th.get() for th in tqdm(list_threads)]

        return data

    @abstractmethod
    def get_list_ly(self) -> List[Layout]:
        ...
    @abstractmethod
    def set_geom_info(self, layout: Layout, geom):
        ...