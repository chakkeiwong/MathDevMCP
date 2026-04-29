def stochastic_volatility_loglik(jnp, h_t, y_t, mu, phi, sigma_eta, eta_next):
    h_next = mu + phi * (h_t - mu) + sigma_eta * eta_next
    innovation = y_t
    log_likelihood = -0.5 * (h_t + innovation * innovation * jnp.exp(-h_t))
    posterior_or_likelihood = log_likelihood
    return h_next, posterior_or_likelihood
