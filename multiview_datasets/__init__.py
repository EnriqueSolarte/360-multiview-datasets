import os

DATASETS_ROOT = os.path.dirname(os.path.abspath(__file__))
DATASETS_ASSETS = os.path.join(DATASETS_ROOT, 'assets')
DATASETS_CFG = os.path.join(DATASETS_ROOT, 'config')
DATASETS_SCENE_LISTS = os.path.join(DATASETS_CFG, 'scene_lists')

os.environ['DATASETS_ASSETS'] = DATASETS_ASSETS
os.environ['DATASETS_SCENE_LISTS'] = DATASETS_SCENE_LISTS
os.environ['DATASETS_CFG'] = DATASETS_CFG

