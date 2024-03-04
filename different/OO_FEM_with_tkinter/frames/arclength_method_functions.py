import numpy as np


def compute_Du_lambda(K_inv, r_0):
    return np.matmul(K_inv, r_0)


def compute_Du_r(K_inv, r_int, lambda_, r_0):
    return np.matmul(K_inv, (lambda_ * r_0 - r_int))


def compute_radius_predictor(du_lambda):
    return np.sqrt(np.matmul(du_lambda, du_lambda) + 1)


def compute_Dlambda(f_n_k, s, du_r, du_lambda, lambda_n1_k, lambda_n, u_n1_k, u_n):
    return - (f_n_k * (f_n_k + s) + np.matmul((u_n1_k - u_n), du_r)) / (
            np.matmul((u_n1_k - u_n), du_lambda) + (lambda_n1_k - lambda_n))


def compute_ConstrainFunction_Sphere(u_n1_k, u_n, lambda_n1_k, lambda_n, s):
    # hint, use np.dot and np.sqrt
    return np.sqrt(np.matmul(u_n1_k - u_n, u_n1_k - u_n) + (lambda_n1_k - lambda_n) ** 2) - s


def compute_Error(du, u_n1_k1, u_n):
    # hint, use np.dot and np.sqrt
    return np.linalg.norm(du) / np.linalg.norm(u_n1_k1 - u_n)
    # return np.linalg.norm(u_n1_k1 - u_n)


def increment(det_k, u_n, delta_u, lambda_n, delta_lambda):
    if det_k > 0:
        return u_n + delta_u, lambda_n + delta_lambda
    elif det_k < 0:
        return u_n - delta_u, lambda_n - delta_lambda
