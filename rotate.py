# 0, 0, 0.43 m
# 303.364344,10.701535,-53.869747,149.572220,0.000000,0.000000

import numpy as np

def transform_cam_to_robot(cam_pose):
	# 로봇 베이스 좌표계
	# distance_cam_between_robot = [0.35, 0.02, 0.33]
	distance_cam_between_robot = [0.35, 0.015, 0.33]

	# 두봇 좌표 보정 (unit : m -> mm)
	dobot_scale = 1000
	gripper_height = [0, 0, 0.06] 	# unit : m

	# y축 회전 행렬 (180도)
	y_angle = np.pi
	rotate_y_matrix = [[np.cos(y_angle), 0, np.sin(y_angle)], 
						[0, 1, 0],
						[-np.sin(y_angle), 0, np.cos(y_angle)]]

	# z축 회전 행렬 (-90도)
	z_angle = -np.pi/2
	rotate_z_matrix = [[np.cos(z_angle), -np.sin(z_angle), 0],
						[np.sin(z_angle), np.cos(z_angle), 0],
						[0, 0, 1]]

	# list -> numpy array
	pose_np = np.array(cam_pose)
	rotate_y_matrix_np = np.array(rotate_y_matrix)
	rotate_z_matrix_np = np.array(rotate_z_matrix)

	# 내적 : y축 180도 회전 -> z축 -90도 회전
	pose_rotate_y = rotate_y_matrix_np.dot(pose_np)
	pose_rotate_y = pose_rotate_y.round(3)
	# print(f"cam rotate y : {pose_rotate_y}")

	pose_rotate_y_z = rotate_z_matrix_np.dot(pose_rotate_y)
	pose_rotate_y_z = pose_rotate_y_z.round(3)
	# print(f"cam rotate y->z : {pose_rotate_y_z}")

	# 최종 좌표
	pose_final = (pose_rotate_y_z + distance_cam_between_robot + gripper_height) * dobot_scale

	return pose_final