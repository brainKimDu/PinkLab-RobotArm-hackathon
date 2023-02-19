import numpy as np
import cv2
import sys
from pose_ArUCo.utils import ARUCO_DICT
import time


def pose_esitmation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients):
    rvec = []
    tvec = []
    points = []

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.aruco_dict = cv2.aruco.Dictionary_get(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters_create()
    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict, parameters=parameters)
    print(f"ids : {ids}")
    if len(corners) > 0:
        for i in range(0, len(ids)):
            # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
            tmp_rvec, tmp_tvec, tmp_markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, matrix_coefficients,
                                                                       distortion_coefficients)
            rvec.append(tmp_rvec)
            tvec.append(tmp_tvec)
            points.append(tmp_markerPoints)
            
    return rvec, tvec, corners

def run_aruco(image, marker_type):

    if ARUCO_DICT.get(marker_type, None) is None:
        print(f"ArUCo tag type is not supported")
        sys.exit(0)

    aruco_dict_type = ARUCO_DICT[marker_type]
    calibration_matrix_path = "./pose_ArUCo/calibration_matrix.npy"
    distortion_coefficients_path = "./pose_ArUCo/distortion_coefficients.npy"
    
    k = np.load(calibration_matrix_path)
    d = np.load(distortion_coefficients_path)
        
    rvec, tvec, corners = pose_esitmation(image, aruco_dict_type, k, d)

    return rvec, tvec, corners