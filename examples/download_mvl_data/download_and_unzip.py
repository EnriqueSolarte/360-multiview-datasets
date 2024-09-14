import os
from pathlib import Path
import json
import multiview_datasets
import hydra
from geometry_perception_utils.io_utils import get_abs_path, create_directory
from geometry_perception_utils.config_utils import save_cfg
import json
import logging
from tqdm import tqdm


def download_gdrive_file(file_id, output_file):
    cmd = f"wget --no-check-certificate 'https://docs.google.com/uc?export=download&id={file_id}' -O {output_file}"
    ret = os.system(cmd)
    if ret != 0:
        logging.error(f"Error downloading {output_file} ID: {file_id}")
        exit(1)


def unzip_file(file_path, output_dir):
    cmd = f'unzip {file_path} -d {output_dir}'
    ret = os.system(cmd)
    if ret != 0:
        logging.error(f"Error unzipping {file_path}")
        exit(1)


@hydra.main(version_base=None,
            config_path=get_abs_path(__file__),
            config_name="cfg")
def main(cfg):
    save_cfg(cfg, [__file__], resolve=True)
    for fn in cfg.download:
        zip_dir = create_directory(
            f'{cfg.output_dir}/{Path(fn).stem}', delete_prev=False)

        unzip_dir = create_directory(
            f'{cfg.output_dir}/data', delete_prev=False)

        logging.info(f"Downloading... {fn}")
        gdrive_metadata = json.load(open(fn, "r"))
        for md in tqdm(gdrive_metadata, desc="Downloading files..."):
            id = md["ID"]
            output_file = md["Name"]

            download_gdrive_file(id, f"{zip_dir}/{output_file}")
            logging.info(f"Downloaded {output_file} ID: {id}")

            unzip_file(f"{zip_dir}/{output_file}", unzip_dir)
            logging.info(f"Unzipped {output_file}")


if __name__ == "__main__":
    main()
