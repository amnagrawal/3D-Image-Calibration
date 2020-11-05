import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

img = cv2.imread("test.png")
img = cv2.resize(img, (500, 500))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
pattern_size = (7, 7)

cornersFound, corners = cv2.findChessboardCorners(gray, pattern_size, None)

objp = np.zeros((7 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:7].T.reshape(-1, 2)

points_3d = []
points_2d = []

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
if cornersFound:
    corner_coords = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

    points_3d.append(objp)
    points_2d.append(corner_coords)

    cv2.drawChessboardCorners(img, pattern_size, corner_coords, cornersFound)
    cv2.imshow('Image', img)
    cv2.waitKey()
    cv2.destroyAllWindows()

with open("img_pts.txt", "w") as f:
    for point in points_2d[0]:
        f.write(str(point[0][0]) + "\t" + str(point[0][1]) + "\n");
f.close()

with open("world_pts.txt", "w") as f:
    for point in points_3d[0]:
        f.write(str(point[0]) + "\t" + str(point[1]) + "\t" + str(point[2]) + "\n");
f.close()