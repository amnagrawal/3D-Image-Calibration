import cv2
import numpy as np
import pandas as pd


def main():
    points_2d = pd.read_csv("./ncc-noise-1-imagePt.txt", delimiter=" ", skiprows=1, skipinitialspace=True, header=None)
    points_3d = pd.read_csv("./ncc-worldPt.txt", delimiter=" ", skiprows=1, skipinitialspace=True, header=None)

    m = points_3d.shape[0]

    M = []

    for i in range(0, m):
        X, Y, Z = points_3d.iloc[i]
        x, y = points_2d.iloc[i]

        row_1 = [X, Y, Z, 1, 0, 0, 0, 0, -1 * X * x, -1 * Y * x, -1 * Z * x, -1 * x]
        row_2 = [0, 0, 0, 0, X, Y, Z, 1, -1 * X * y, -1 * Y * y, -1 * Z * y, -1 * y]
        M.append(row_1)
        M.append(row_2)

    u, D, v_t = np.linalg.svd(M)
    M_solved = v_t[np.argmin(D)]
    M_solved = M_solved.reshape(3, 4)
    epsilon = 0

    get_camera_params(M_solved, verbose=True)

    points_3dh = cv2.convertPointsToHomogeneous(np.array(points_3d))
    points_3dh = points_3dh.reshape(points_3dh.shape[0], points_3dh.shape[2])

    total_projection_error = 0

    for i in range(m):
        pred_x = np.dot(M_solved[0], points_3dh[i]) / (np.dot(M_solved[2], points_3dh[i]) + epsilon)
        pred_y = np.dot(M_solved[1], points_3dh[i]) / (np.dot(M_solved[2], points_3dh[i]) + epsilon)
        pe = ((points_2d.iloc[i][0] - pred_x) ** 2) + ((points_2d.iloc[i][1] - pred_y) ** 2)
        if np.isnan(pe):
            print(pred_x, pred_y)
        total_projection_error += pe

    error_rate = np.sqrt(total_projection_error / m)

    print(f"Projection Error = {error_rate}")


def get_camera_params(projection_matrix, verbose=0):
    # global M_solved, rho, u0, v0, alpha_v, epsilon, s, alpha_u, K_star, T_star, R_star
    a1 = projection_matrix[0, 0:3]
    a2 = projection_matrix[1, 0:3]
    a3 = projection_matrix[2, 0:3]
    b = projection_matrix[0:3, 3]
    sign = 1
    if b[-1] < 0:
        sign = -1
    rho = sign * (1 / np.linalg.norm(a3))
    u0 = (rho ** 2) * np.dot(a1, a3)
    v0 = (rho ** 2) * np.dot(a2, a3)
    alpha_v = np.sqrt(((rho ** 2) * np.dot(a2, a2)) - (v0 ** 2))
    # epsilon = 0.0000001
    epsilon = 0
    s = ((rho ** 4) * np.dot(np.cross(a1, a3), np.cross(a2, a3))) / (alpha_v + epsilon)
    alpha_u = np.sqrt(((rho ** 2) * np.dot(a1, a1)) - (s ** 2) - (u0 ** 2))
    K_star = [[alpha_u, s, u0],
              [0, alpha_v, v0],
              [0, 0, 1]]
    K_star = np.array(K_star)
    T_star = rho * np.matmul(np.linalg.pinv(K_star), b)
    r3 = rho * a3
    r1 = ((rho ** 2) * np.cross(a2, a3)) / (alpha_v + epsilon)
    r2 = np.cross(r3, r1)
    R_star = [r1, r2, r3]
    R_star = np.array(R_star)

    if verbose:
        print("The computed camera parameters are: ")
        print(f"rho = {rho}")
        print(f"u0 = {u0}")
        print(f"v0 = {v0}")
        print(f"alpha_v = {alpha_v}")
        print(f"s = {s}")
        print(f"alpha_u = {alpha_u}")
        print(f"T* = {T_star}")
        print(f"R* = {R_star}")
        print(f"K* = {K_star}")


if __name__ == "__main__":
    main()
