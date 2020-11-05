import cv2
import numpy as np
import sys
import random
import math
from configparser import ConfigParser
import pandas as pd
from q2 import get_camera_params

configFile = "./RANSAC.config"
config = ConfigParser()
config.read(configFile)
prob = float(config.get('config', 'prob'))
kmax = int(config.get('config', 'kmax'))
nmin = int(config.get('config', 'nmin'))
nmax = int(config.get('config', 'nmax'))
w = float(config.get('config', 'w'))
# print(config.get('config', 'prob'))
# sys.exit(-1)

# file_name = sys.argv[1]
points_2d = pd.read_csv("./ncc-noise-1-imagePt.txt", delimiter=" ", skiprows=1, skipinitialspace=True, header=None)
points_3d = pd.read_csv("./ncc-worldPt.txt", delimiter=" ", skiprows=1, skipinitialspace=True, header=None)
points_3dh = cv2.convertPointsToHomogeneous(np.array(points_3d))
points_3dh = points_3dh.reshape(points_3dh.shape[0], points_3dh.shape[2])

object_point = np.array(points_3d)
image_point = np.array(points_2d)

k = kmax
np.random.seed(0)
inlierNum = 0
M = None


def get_distances(points3D, points2D):
    # global i, X, Y, Z, x, y, row_1, row_2, u, D, v_t, distance, epsilon, pred_x, pred_y, pe

    points3DH = cv2.convertPointsToHomogeneous(np.array(points3D))
    points3DH = points3DH.reshape(points3DH.shape[0], points3DH.shape[2])
    M = get_projection_matrix(points3D, points2D)
    distance = []
    epsilon = 0
    m = len(points2D)
    for i in range(m):
        pred_x = np.dot(M[0], points3DH[i]) / (np.dot(M[2], points3DH[i]) + epsilon)
        pred_y = np.dot(M[1], points3DH[i]) / (np.dot(M[2], points3DH[i]) + epsilon)
        pe = ((points2D.iloc[i][0] - pred_x) ** 2) + ((points2D.iloc[i][1] - pred_y) ** 2)
        distance.append(np.sqrt(pe))

    return distance


def get_projection_matrix(points_3d, points_2d):
    a = []
    m = len(points_3d)
    for i in range(m):
        X, Y, Z = points_3d.iloc[i]
        x, y = points_2d.iloc[i]

        row_1 = [X, Y, Z, 1, 0, 0, 0, 0, -1 * X * x, -1 * Y * x, -1 * Z * x, -1 * x]
        row_2 = [0, 0, 0, 0, X, Y, Z, 1, -1 * X * y, -1 * Y * y, -1 * Z * y, -1 * y]
        a.append(row_1)
        a.append(row_2)

    u, D, v_t = np.linalg.svd(a, full_matrices=True)
    M = v_t[np.argmin(D)]
    M = M.reshape(3, 4)
    return M


distance = get_distances(points_3d, points_2d)

medianDistance = np.median(distance)
t = 1.5 * medianDistance
m = points_3d.shape[0]
n = random.randint(nmin, nmax)
M = []
for count in range(kmax):

    indices = np.random.choice(m, n)
    random_3d, random_2d = points_3d.iloc[indices], points_2d.iloc[indices]

    d_i = get_distances(random_3d, random_2d)
    inliers = []
    for i, d_i in enumerate(d_i):
        if d_i < t:
            inliers.append(i)

    if len(inliers) >= inlierNum:
        inliersNum = len(inliers)
        inliers_2d, inliers_3d = points_2d.iloc[inliers], points_3d.iloc[inliers]
        M = get_projection_matrix(random_3d, random_2d)

    if not (w == 0):
        w = float(len(inliers)) / float(len(image_point))
        k = float(math.log(1 - prob)) / np.absolute(math.log(1 - (w ** n)))


get_camera_params(M, verbose=True)