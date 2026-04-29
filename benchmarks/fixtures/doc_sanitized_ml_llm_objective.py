def objective_and_gradient(grad, log_prob, theta, batch):
    loss = -sum(log_prob(theta, x, y) for x, y in batch)
    gradient_value = grad(lambda value: -sum(log_prob(value, x, y) for x, y in batch))(theta)
    posterior_or_likelihood = loss
    return loss, gradient_value, posterior_or_likelihood
