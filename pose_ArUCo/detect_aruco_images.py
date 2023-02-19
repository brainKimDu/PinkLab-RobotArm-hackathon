import numpy as np
from pose_ArUCo.utils import ARUCO_DICT, aruco_display
import argparse
import cv2
import sys
import os

def detect_marker(image, marker_type):
	# ArUCo 마커 이미지 읽기

	# 이미지 전처리
	h,w,_ = image.shape
	width=600
	height = int(width*(h/w))
	image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)

	# verify that the supplied ArUCo tag exists and is supported by OpenCV
	if ARUCO_DICT.get(marker_type, None) is None:
		print(f"ArUCo tag type '{marker_type}' is not supported")
		sys.exit(0)

	# load the ArUCo dictionary, grab the ArUCo parameters, and detect
	# the markers
	print("Detecting '{}' tags....".format(marker_type))
	arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[marker_type])
	arucoParams = cv2.aruco.DetectorParameters_create()
	corners, ids, rejected = cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)

	# print(f"corners : {corners}")
	# print(f"ids : {ids}")

	# ArUCo 마커 검출 결과에 대한 시각화
	detected_markers = aruco_display(corners, ids, rejected, image)

	return detected_markers