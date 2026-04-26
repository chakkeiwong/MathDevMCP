def particle_filter_update(jnp, logsumexp, particles, log_weights, observation, transition, log_likelihood):
    predicted = transition(particles)
    log_weight_next = log_weights + log_likelihood(observation, predicted)
    log_normalizer = logsumexp(log_weight_next)
    normalized_log_weights = log_weight_next - log_normalizer
    ess = 1.0 / jnp.sum(jnp.exp(normalized_log_weights) ** 2)
    return predicted, normalized_log_weights, ess
