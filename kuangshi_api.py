import requests
import json
import base64
import os

key = "R2lu-O5WfmRyKiG5ORtPu0JSK_b9su6L"
secret = "-mRwmQ-cUDZBnR2E7SGw4fDssLSKImpl"
attributes_yes = "headpose,eyestatus"

# set_path = "./Test/new_crop/"  # dir path


# testjpg  = "000065.jpg" # file path
def getStatus(value):
    return True if value > 0.5 else False

def get_api_angle(filepath):
    # filepath = os.path.join(set_path, img_path)
    http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
    files = {"image_file": open(filepath, "rb")}
    data = {"api_key": key, "api_secret": secret, "return_landmark": 0, "return_attributes": attributes_yes}
    response = requests.post(http_url, data=data, files=files)
    req_dict = response.json()

    if (req_dict['face_num'] != 1):
        print("Not 1 face in {}".format(filepath))

    headpose = []
    eyeopen = []
    for i in range(req_dict['face_num']):
        headpose.append(req_dict['faces'][i]['attributes']['headpose'])
        eyeopen.append([getStatus(req_dict['faces'][i]['attributes']['eyestatus']['left_eye_status']['no_glass_eye_open']),
                        getStatus(req_dict['faces'][i]['attributes']['eyestatus']['right_eye_status']['no_glass_eye_open'])])

    return headpose,eyeopen

# if __name__ == "__main__":
#     print(get_angle(testjpg))
