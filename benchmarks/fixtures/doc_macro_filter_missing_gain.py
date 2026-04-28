import numpy as np


def macro_filter_step(F, H, Q, R, x, P, y):
    x_pred = F @ x
    P_pred = F @ P @ F.T + Q
    innovation = y - H @ x_pred
    S = H @ P_pred @ H.T + R
    sign, logdet = np.linalg.slogdet(S)
    alpha = np.linalg.solve(S, innovation)
    ll = -0.5 * (logdet + innovation @ alpha)
    return x_pred, P_pred, ll
