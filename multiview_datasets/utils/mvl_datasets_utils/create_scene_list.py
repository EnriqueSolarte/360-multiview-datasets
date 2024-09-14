
import argparse
from geometry_perception_utils.io_utils import save_json_dict
import json
from multiview_datasets.utils.scene_version_idx_utils import get_all_scenes_from_scene_list, get_scene_list_from_list_scenes
import os
from pathlib import Path


path = '/media/public_dataset/ZInD/360_layout_challenge'


def main(args):
    scene_list = get_all_scenes_from_scene_list(args.file)
    reg_scene_files = [Path(f).stem for f in os.listdir(args.dir)]

    verified_scenes = [f for f in scene_list if f in reg_scene_files]

    new_scene_list = get_scene_list_from_list_scenes(verified_scenes)

    fn = os.path.join(Path(args.file).parent, Path(
        args.file).stem + "__v.231005.json")
    save_json_dict(fn, new_scene_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='validate all scenes existed in the directory')
    parser.add_argument('-d', '--dir', type=str,
                        default=f"{path}/labels/layout_visible", help='Dir scenes ')
    parser.add_argument('-f', '--file', type=str,
                        default=f"{path}/scene_lists/scene_list__testing_set.json",  help='scene list file')

    args = parser.parse_args()
    main(args)
