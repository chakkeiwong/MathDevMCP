def sgu_residual_bad(beta, r_next, mu_next, lam_next, lam_cur, tf):
    dlam = lam_next - lam_cur
    return beta * (1 + tf.exp(r_next)) * tf.exp(mu_next + dlam) - 1
