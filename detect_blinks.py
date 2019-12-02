from scipy.spatial import distance as dist
import numpy as np
import requests
import os
import base64
import sys
import json

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = (13, 20)  # face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = (30, 37)  # face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold
EYE_AR_THRESH = 0.3


def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[-1])
    B = dist.euclidean(eye[3], eye[5])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[4])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear


def is_open(eyeEAR):
    status = False if eyeEAR < EYE_AR_THRESH else True
    return status

# 显示左右眼是否睁开
def get_eye_status(shape):
    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]
    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)
    leftStatus = is_open(leftEAR)
    rightStatus = is_open(rightEAR)
    return leftStatus, rightStatus


def get_eye(filepath):
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=HsVmphL7K3y5QY0ubsElQIDA&client_secret=DBdLgzh5VsPVGIPfBqI5arA3QXZR1HwE'
    response = requests.get(host).json()
    access_token = response['access_token']
    http_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    http_url += "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    for img_path in os.listdir(filepath):
        with open(os.path.join(filepath, img_path), "rb") as f:
            sFile = f.read()
            encodeStr = base64.b64encode(sFile)
            data = {"image": encodeStr, "image_type": "BASE64",
                    "face_field": "eye_status"}
            response = requests.post(http_url, data=data, headers=headers)
            req_dict = response.json()
            print(req_dict)
    return ""
