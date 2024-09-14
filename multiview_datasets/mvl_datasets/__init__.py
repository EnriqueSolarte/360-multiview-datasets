from .hm3d_mvl import HM3D_MVL
from .hm3d_mvl import MP3D_FPE_MVL
from .zind_mvl import ZInD_mvl
from .mvl_dataset import MVL_dataset
import logging
import copy
from multiprocessing.pool import ThreadPool
from tqdm import tqdm
from multiview_datasets.utils.layout_utils import set_reference_at_room_center
from geometry_perception_utils.geometry_utils import extend_array_to_homogeneous, get_quaternion_from_matrix
import threading
import time
import json
import os


def load_mvl_dataset(cfg)->MVL_dataset:
    if cfg.dataset_name == "hm3d_mvl":
        return HM3D_MVL(cfg)
    elif cfg.dataset_name == "mp3d_fpe_mvl":
        return MP3D_FPE_MVL(cfg)
    elif cfg.dataset_name == "zind_mvl":
        return ZInD_mvl(cfg)
    else:
        raise NotImplementedError(f"Unknown MVL dataset: {cfg.name}")


def load_mvl_dataset_iterator(dt, model=None, target_scene=None):
    list_scenes = dt.list_scenes
    list_target = None
    if target_scene is not None:
        if target_scene.get("only") is not None:
            idx = dt.list_scenes.index(target_scene.get("only"))
            list_scenes = [dt.list_scenes[idx]]
            list_target = None

        if target_scene.get("from") is not None:
            idx = dt.list_scenes.index(target_scene.get("from"))
            list_scenes = dt.list_scenes[idx:]
            list_target = None

        if target_scene.get("scene_list") is not None:
            assert os.path.exists(target_scene.get(
                "scene_list")), f"{target_scene.get('scene_list')} does not exist"
            scenes = json.load(open(target_scene.get("scene_list"), "r"))
            list_scenes = list(scenes.keys())
            list_target = [sc for sc in scenes.values()]
            # flat list of list
            list_target = [item for sublist in list_target for item in sublist]

    for scene in list_scenes:
        idx = dt.list_scenes.index(scene)
        logging.info(
            f"Processing scene: {scene}: {idx/dt.list_scenes.__len__()*100:.2f}% - {idx}")

        list_ly = dt.get_list_ly(scene_name=scene)

        if model is not None:
            model.estimate_within_list_ly(list_ly)

        set_reference_at_room_center(list_ly)
        list_ly = sorted(list_ly, key=lambda ly: int(ly.idx.split('_')[-1]))
        if list_target is not None:
            list_ly = [ly for ly in list_ly if ly.idx in list_target]
        yield list_ly


def load_mvl_data_with_multithread(dataset: HM3D_MVL):
    """
    * Loads from a dataset instance the whole data using multi-threads
    """
    global_list_ly = dict()

    def load_mvl_data(scene):
        __list_ly = copy.deepcopy(dataset).get_list_ly(scene_name=scene)
        local_list = {f"{scene}": __list_ly}
        return local_list

    pool = ThreadPool(processes=10)
    list_threads = []
    for scene in tqdm(dataset.list_scenes, desc=f"Loading MVL data..."):
        list_threads.append(
            pool.apply_async(load_mvl_data, (scene,))
        )
    for thread in tqdm(list_threads, desc="Multithread..."):
        local_data = thread.get()
        global_list_ly = {**global_list_ly, **local_data}

    return global_list_ly
