def transformed_density(log_pi, logdet, temperature):
    return log_pi + logdet + temperature
