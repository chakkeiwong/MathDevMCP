def hamiltonian_mcmc_acceptance(jnp, potential_energy, grad, q, p, q_next, p_next, mass_inv):
    gradient = grad(potential_energy)(q)
    kinetic_energy = 0.5 * p @ mass_inv @ p
    kinetic_energy_next = 0.5 * p_next @ mass_inv @ p_next
    hamiltonian = potential_energy(q) + kinetic_energy
    hamiltonian_next = potential_energy(q_next) + kinetic_energy_next
    log_acceptance_ratio = -hamiltonian_next + hamiltonian
    accept_prob = jnp.minimum(1.0, jnp.exp(log_acceptance_ratio))
    return gradient, accept_prob
