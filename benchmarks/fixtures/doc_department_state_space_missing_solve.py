def kalman_filter_scan(jnp, lax, params, y):
    F, H, Q, R = params

    def step(carry, obs):
        x, P = carry
        x_pred = F @ x
        P_pred = F @ P @ F.T + Q
        innovation = obs - H @ x_pred
        S = H @ P_pred @ H.T + R
        sign, logdet = jnp.linalg.slogdet(S)
        K = P_pred @ H.T
        x_filt = x_pred + K @ innovation
        P_filt = P_pred - K @ H @ P_pred
        ll_t = -0.5 * (logdet + innovation @ innovation)
        return (x_filt, P_filt), ll_t

    return lax.scan(step, initial_state(params), y)
