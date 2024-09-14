import zipfile
import os
from tqdm import tqdm
from pathlib import Path
from geometry_perception_utils.io_utils import create_directory, process_arcname, get_abs_path
from multiview_datasets.utils.scene_version_idx_utils import get_scene_list_from_list_scenes
from geometry_perception_utils.config_utils import save_cfg
import hydra


def zip_data(root_dir, zf, list_fn):
    list_arc_fn = process_arcname(list_fn, root_dir)
    [
        (
            print(f"zipping {fn}"),
            zf.write(
                os.path.join(root_dir, fn),
                compress_type=zipfile.ZIP_DEFLATED,
                arcname=fn,
            ),
        )
        for fn in tqdm(list_arc_fn)
    ]


def zip_mvl_data(src_dir, dst_dir, root):
    assert os.path.exists(
        src_dir), f"Source directory {src_dir} does not exist"

    create_directory(dst_dir, delete_prev=False)
    list_all_fn = os.listdir(src_dir)
    list_mvl_fn = [Path(fn).stem for fn in list_all_fn]

    mvl_data = get_scene_list_from_list_scenes(list_mvl_fn)

    ext = os.path.splitext(list_all_fn[0])[1]
    for room, scene_list in tqdm(mvl_data.items(), desc="Zipping Data"):
        zip_filename = os.path.join(dst_dir, f"{room}.zip")
        with zipfile.ZipFile(file=zip_filename, mode="w") as zf:
            list_fn = [
                os.path.join(src_dir, f"{sc}{ext}")
                for sc in scene_list
            ]
            zip_data(root, zf, list_fn)


@hydra.main(version_base=None,
            config_path=get_abs_path(__file__),
            config_name="cfg")
def main(cfg):
    save_cfg(cfg, resolve=True)

    # Labels
    src_dir = f'{cfg.mvl_dataset.labels_dir}'
    if os.path.exists(f'{src_dir}'):
        dst_dir = f'{cfg.output_dir}/labels'
        zip_mvl_data(src_dir, dst_dir, root=cfg.mvl_dataset.dir)

    # Geometry Info
    src_dir = f'{cfg.mvl_dataset.geometry_info_dir}'
    dst_dir = f'{cfg.output_dir}/geometry_info'
    zip_mvl_data(src_dir, dst_dir, root=cfg.mvl_dataset.dir)

    # images
    src_dir = f'{cfg.mvl_dataset.img_dir}'
    dst_dir = f'{cfg.output_dir}/img'
    zip_mvl_data(src_dir, dst_dir, root=cfg.mvl_dataset.dir)


if __name__ == "__main__":
    main()
