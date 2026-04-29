def elbo_reparameterization_gradient(expectation, grad, log_joint, log_q, transform, lam):
    eps = "epsilon"
    z_sample = transform(lam, eps)
    elbo_value = expectation(log_joint(z_sample) - log_q(lam, z_sample))
    reparameterization_gradient = grad(lambda value: expectation(log_joint(transform(value, eps)) - log_q(value, transform(value, eps))))(lam)
    return elbo_value, reparameterization_gradient
