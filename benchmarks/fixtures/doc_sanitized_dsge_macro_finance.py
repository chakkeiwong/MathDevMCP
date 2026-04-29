def euler_residual(expectation, beta, marginal_utility_next, marginal_utility_now, gross_return):
    stochastic_discount_factor = beta * marginal_utility_next / marginal_utility_now
    expected_return = expectation(stochastic_discount_factor * gross_return)
    euler_residual_value = expected_return - 1.0
    return euler_residual_value
