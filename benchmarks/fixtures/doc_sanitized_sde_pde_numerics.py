def euler_maruyama_step(drift, diffusion, x_t, dt, noise):
    x_next = x_t + drift(x_t) * dt + diffusion(x_t) * (dt ** 0.5) * noise
    stable_step = dt <= 0.5
    stability_condition = stable_step
    return x_next, stability_condition
