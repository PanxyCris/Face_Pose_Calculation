from scipy.spatial import distance as dist
from imutils import face_utils
import os
import cv2

data_path = "./"

img_path = os.path.join(data_path, "Test", "new_crop")
landmark_path = os.path.join(data_path, "Test", "new_landmark")

img_paths = os.listdir(img_path)

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
        for poit in lines:
            x, y = poit.split(' ')
            landmark_idx += 1

            # show landmarks location
            cv2.circle(
                img,
                (int(float(x) * img.shape[1]), int(float(y) * img.shape[0])),
                1, (0, 0, 255))
            
            # show landmarks idx
            cv2.putText(
                img, str(landmark_idx),
                (int(float(x) * img.shape[1]), int(float(y) * img.shape[0])),
                cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255, 255, 0), 1)

    cv2.imshow(str(idx % 10), img)

    # press ESC to next 10 pictures
    while (idx % 10 == 0):
        if (cv2.waitKey(0) == 27):
            break
