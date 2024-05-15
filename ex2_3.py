import numpy as np
import matplotlib.pyplot as plt
from ex2_1 import model_euler
from ex2_2 import model_rk4


# Common parameters
s0, i0, r0 = 0.99, 0.01, 0.0
beta, k = 0.5, 0.1
dt, tfinal = 0.1, 100

# Simulate both methods
s_euler, i_euler, r_euler = model_euler(s0, i0, r0, beta, k, dt, tfinal)
s_rk4, i_rk4, r_rk4 = model_rk4(s0, i0, r0, beta, k, dt, tfinal)

# Compute absolute errors
a_error_s = np.abs(s_rk4 - s_euler)
a_error_i = np.abs(i_rk4 - i_euler)
a_error_r = np.abs(r_rk4 - r_euler)

# Small constant to prevent division by zero
epsilon = 1e-10

r_error_s = a_error_s / (s_rk4 + epsilon) * 100
r_error_i = a_error_i / (i_rk4 + epsilon) * 100
r_error_r = a_error_r / (r_rk4 + epsilon) * 100

time = np.arange(0, tfinal + dt, dt)

plt.figure(figsize=(18, 10))

plt.subplot(1, 2, 1)
plt.plot(time, s_euler, 'b--', label='Susceptible (Euler)')
plt.plot(time, i_euler, 'r--', label='Infected (Euler)')
plt.plot(time, r_euler, 'g--', label='Recovered (Euler)')
plt.plot(time, s_rk4, 'b', label='Susceptible (RK4)')
plt.plot(time, i_rk4, 'r', label='Infected (RK4)')
plt.plot(time, r_rk4, 'g', label='Recovered (RK4)')
plt.title('Comparison of Euler and RK4 Methods')
plt.xlabel('Time')
plt.ylabel('Fraction of Population')
plt.legend()
plt.grid(True)

# Plot errors
plt.subplot(1, 2, 2)
plt.plot(time, r_error_s, 'b', label='Relative Error in Susceptible')
plt.plot(time, r_error_i, 'r', label='Relative Error in Infected')
plt.plot(time, r_error_r, 'g', label='Relative Error in Recovered')
plt.title('Relative Errors of Euler Method Relative to RK4')
plt.xlabel('Time')
plt.ylabel('Relative Error')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
