def sgu_residual_fixed(beta, r_next, mu_cur, lam_next, lam_cur, tf):
    dlam = lam_next - lam_cur
    return beta * (1 + tf.exp(r_next)) * tf.exp(mu_cur + dlam) - 1
