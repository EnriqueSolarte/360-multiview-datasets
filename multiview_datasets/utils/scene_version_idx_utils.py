import numpy as np
import os
import json
from pathlib import Path
from tqdm import tqdm


def get_room_idx_from_scene_idx(scene_idx):
    rooms = "_".join(scene_idx.split("_")[:-1])
    return rooms


def get_scene_list_from_list_scenes(list_scenes):
    rooms = set(["_".join(f.split("_")[:-1]) for f in list_scenes])
    # if all(["_pano" in s for s in rooms]):
    #     rooms = set(["_".join(f.split("_pano")[:-1]) for f in rooms])

    data_dict = {}
    for r in rooms:
        data_dict[r] = [f for f in list_scenes if r in f]

    return data_dict


def get_scene_version_idx_from_fn_name(fn_name):
    return ["_".join(fn.split("/")[-2:]) for fn in fn_name]


def get_idx_from_scene_version_idx(fr_name):
    return int(fr_name.split("_")[-1].split(".")[0])


def get_all_scenes_from_scene_list(scene_list_fn):
    data = json.load(open(scene_list_fn, "r"))
    list_geom_info = [f for f in data.values()]
    list_geom_info = set(
        [item for sublist in list_geom_info for item in sublist])
    return list(list_geom_info)


def get_rgbd_scenes_list(args):
    dir_data = args.scene_dir
    scene_list = get_all_scenes_from_scene_list(args.scene_list)
    return np.unique(
        [os.path.join(dir_data, f.split("_")[0], f.split("_")[1])
         for f in scene_list]
    ).tolist()
