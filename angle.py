import cv2
import numpy as np
import math

FACE_POINTS = [57, 6, 13, 34, 58, 117]  # NOSE_TIP, CHIN, LEFT_EYE, RIGHT_EYE, LEFT_MOUTH, RIGHT_MOUTH

# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6


# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def get_euler_angle_byMatrix(rvec):
    # theta = np.linalg.norm(rvec)
    # r = rvec / theta
    # R_ = np.array([[0, -r[2][0], r[1][0]],
    #                [r[2][0], 0, -r[0][0]],
    #                [-r[1][0], r[0][0], 0]])
    # R = np.cos(theta) * np.eye(3) + (1 - np.cos(theta)) * r * r.T + np.sin(theta) * R_
    R = cv2.Rodrigues(rvec)[0]
    assert (isRotationMatrix(R))

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    x = x * 180.0 / np.pi
    y = y * 180.0 / np.pi
    z = z * 180.0 / np.pi

    if x > 0:
        x -= 180
    else:
        x += 180

    return np.array([y, x, z])


# 从旋转向量转换为欧拉角
def get_euler_angle_byRvec(rotation_vector):
    # calculate rotation angles
    theta = cv2.norm(rotation_vector, cv2.NORM_L2)

    # transformed to quaterniond
    w = math.cos(theta / 2)
    x = math.sin(theta / 2) * rotation_vector[0][0] / theta
    y = math.sin(theta / 2) * rotation_vector[1][0] / theta
    z = math.sin(theta / 2) * rotation_vector[2][0] / theta

    ysqr = y * y
    # pitch (x-axis rotation)
    t0 = 2.0 * (w * x + y * z)
    t1 = 1.0 - 2.0 * (x * x + ysqr)
    # print('t0:{}, t1:{}'.format(t0, t1))
    pitch = math.atan2(t0, t1)

    # yaw (y-axis rotation)
    t2 = 2.0 * (w * y - z * x)
    if t2 > 1.0:
        t2 = 1.0
    if t2 < -1.0:
        t2 = -1.0
    yaw = math.asin(t2)

    # roll (z-axis rotation)
    t3 = 2.0 * (w * z + x * y)
    t4 = 1.0 - 2.0 * (ysqr + z * z)
    roll = math.atan2(t3, t4)

    # print('yaw:{}, pitch:{}, roll:{}'.format(yaw, pitch, roll))

    # 单位转换：将弧度转换为度
    Y = (pitch / math.pi) * 180
    X = (yaw / math.pi) * 180
    Z = (roll / math.pi) * 180

    if Y > 0:
        Y -= 180
    else:
        Y += 180

    return X, Y, Z


def get_angle(shape):
    image_points = shape[FACE_POINTS]
    model_points = np.array([
        (0.0, 0.0, 0.0),  # Nose tip
        (0.0, -330.0, -65.0),  # Chin
        (-225.0, 170.0, -135.0),  # Left eye left corner
        (225.0, 170.0, -135.0),  # Right eye right corner
        (-150.0, -150.0, -125.0),  # Left Mouth corner
        (150.0, -150.0, -125.0)  # Right mouth corner

    ])
    focal_length = 1
    center = (1 / 2, 1 / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype="double"
    )
    dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix,
                                                                  dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

    euler_angles = get_euler_angle_byRvec(rotation_vector)
    return euler_angles
