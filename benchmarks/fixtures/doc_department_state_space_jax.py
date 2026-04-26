def kalman_filter_scan(jnp, lax, solve, eye, params, y):
    F, H, Q, R = params

    def step(carry, obs):
        x, P = carry
        assert F.shape[0] == F.shape[1]
        assert P.shape[0] == P.shape[1]
        assert is_symmetric(P) and is_positive_semidefinite(P)
        x_pred = F @ x
        P_pred = F @ P @ F.T + Q
        innovation = obs - H @ x_pred
        S = H @ P_pred @ H.T + R
        sign, logdet = jnp.linalg.slogdet(S)
        K = P_pred @ H.T @ solve(S, eye(S.shape[0]))
        x_filt = x_pred + K @ innovation
        P_filt = P_pred - K @ H @ P_pred
        ll_t = -0.5 * (logdet + innovation @ solve(S, innovation))
        return (x_filt, P_filt), ll_t

    return lax.scan(step, initial_state(params), y)
