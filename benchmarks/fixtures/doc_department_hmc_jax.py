def hmc_kernel(jnp, grad, log_prob, theta, momentum, step_size, mass_inv):
    grad_logp = grad(log_prob)
    p_half = momentum + 0.5 * step_size * grad_logp(theta)
    theta_next = theta + step_size * (mass_inv @ p_half)
    p_next = p_half + 0.5 * step_size * grad_logp(theta_next)
    potential_energy = -log_prob(theta_next)
    kinetic_energy = 0.5 * p_next @ mass_inv @ p_next
    hamiltonian = potential_energy + kinetic_energy
    return theta_next, p_next, hamiltonian
