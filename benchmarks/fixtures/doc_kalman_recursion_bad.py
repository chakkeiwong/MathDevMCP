def kalman_step(F, H, Q, R, x, P, y, solve, eye):
    x_pred = F @ x
    P_pred = F @ P @ F.T + Q
    innovation = y - H @ x_pred
    S = H @ P_pred @ H.T + R
    K = P_pred @ H.T @ solve(S, eye(S.shape[0]))
    x_filt = x_pred + K @ innovation
    return x_filt, P_pred
