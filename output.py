from detect_blinks import *
from angle import *
import cv2
import numpy as np
from kuangshi_api import *

data_path = "./"

img_path = os.path.join(data_path, "Test", "new_crop")
landmark_path = os.path.join(data_path, "Test", "new_landmark")

img_paths = os.listdir(img_path)

left_eye_status_list = []
right_eye_status_list = []
yaw_angle_list = []
row_angle_list = []
roll_angle_list = []
# initialize the frame counters and the total number of blinks
COUNTER = [0 for i in range(3)]
TOTAL = 0
LEFT_EYE = 0
RIGHT_EYE = 0
ID_KEY = ["yaw_angle", "pitch_angle", "roll_angle"]
for idx in range(len(img_paths)):
    i = img_paths[idx]
    current_img_path = os.path.join(img_path, i)
    current_landmark_path = os.path.join(landmark_path, i) + ".txt"
    if not os.path.exists(current_img_path):
        continue

    if not os.path.exists(current_landmark_path):
        continue

    img = cv2.imread(current_img_path)

    landmark_idx = 0

    with open(current_landmark_path, 'r') as f:
        lines = f.readlines()
        shape = np.zeros((len(lines), 2))
        for poit in lines:
            x, y = poit.split(' ')
            shape[landmark_idx] = (float(x), float(y))
            landmark_idx += 1
    left_eye_status, right_eye_status = get_eye_status(shape)

    angle = get_angle(shape)
    yaw_angle, row_angle, roll_angle = angle[0], angle[1], angle[2]

    left_eye_status_list.append(left_eye_status)
    right_eye_status_list.append(right_eye_status)
    row_angle_list.append(row_angle)
    yaw_angle_list.append(yaw_angle)
    roll_angle_list.append(roll_angle)
    # api_angles,eye_open = get_api_angle(current_img_path)
    # if len(api_angles) > 0:
    #     TOTAL += 1
    #     for i in range(3):
    #         if abs(api_angles[0][ID_KEY[i]] - angle[i]) <= 5:
    #             COUNTER[i] += 1
    #     if left_eye_status == eye_open[0][0]:
    #         LEFT_EYE += 1
    #     if right_eye_status == eye_open[0][1]:
    #         RIGHT_EYE += 1
# print("yaw: {0}".format(COUNTER[0] / TOTAL))
# print("pitch: {0}".format(COUNTER[1] / TOTAL))
# print("roll: {0}".format(COUNTER[2] / TOTAL))
# print("left eye: {0}".format(LEFT_EYE / TOTAL))
# print("right eye: {0}".format(RIGHT_EYE / TOTAL))
print(left_eye_status_list)
print(right_eye_status_list)
print(row_angle_list)
print(roll_angle_list)
print(yaw_angle_list)
