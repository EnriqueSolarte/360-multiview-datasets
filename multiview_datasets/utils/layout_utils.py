import numpy as np
import logging
from geometry_perception_utils.geometry_utils import extend_array_to_homogeneous


def get_bev_ref_at_cc(list_ly, ly_ref):
    pose_wc = list_ly[0].pose()
    pose_cc = ly_ref.pose.get_inv() @ pose_wc

    xyz_boundary = np.hstack([ly.boundary_floor for ly in list_ly])
    bev = pose_cc[:3, :] @ extend_array_to_homogeneous(xyz_boundary)
    bev[1, :] = 0
    return bev


def set_reference_at_room_center(list_ly):
    # * Transform to the 1st frame
    center = np.hstack([ly.pose.t.reshape(3, 1) for ly in list_ly])
    center_idx = np.argmin(
        [np.linalg.norm(ly.pose.t - np.median(center, axis=1)) for ly in list_ly])
    pose_wc = list_ly[center_idx].pose.get_inv()

    [ly.set_boundaries_transformed_at(pose_wc)
        for ly in list_ly
     ]
    [ly.set_cam_pose(pose_wc @ ly.pose())
        for ly in list_ly
     ]
    return list_ly[center_idx]


def set_reference_at(list_ly, ly_ref):
    pose_wc = ly_ref.pose.get_inv()
    [ly.set_boundaries_transformed_at(pose_wc)
        for ly in list_ly
     ]
    [ly.set_cam_pose(pose_wc @ ly.pose())
        for ly in list_ly
     ]


def mask_by_dist_within_list_ly(list_ly, cam_dist_threshold=3):
    logging.info("Total number of frames: {}".format(len(list_ly)))
    sparse_bound_frs = 0
    for ly in list_ly:
        mask = ly.cam2boundary < cam_dist_threshold
        if np.sum(mask) < 10:
            # logging.warning(f"Sparse boundary for {ly.idx}")
            sparse_bound_frs += 1
        ly.boundary_floor = ly.boundary_floor[:, mask]
        ly.boundary_ceiling = ly.boundary_ceiling[:, mask]
    logging.info(f"Sparse boundary frames: {sparse_bound_frs}")
