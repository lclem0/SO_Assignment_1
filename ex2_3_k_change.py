import numpy as np
import matplotlib.pyplot as plt
from ex2_1 import model_euler
from ex2_2 import model_rk4

k_values = [0.05, 0.1, 0.2]  
beta = 0.3  
s0, i0, r0 = 0.99, 0.01, 0.0
dt, tfinal = 0.1, 100

plt.figure(figsize=(18, 10))

for k in k_values:
    s_euler, i_euler, r_euler = model_euler(s0, i0, r0, beta, k, dt, tfinal)
    s_rk4, i_rk4, r_rk4 = model_rk4(s0, i0, r0, beta, k, dt, tfinal)
    
    time = np.arange(0, tfinal + dt, dt)
    plt.plot(time, r_euler, '--', label=f'Recovered (Euler) K={k}')
    plt.plot(time, r_rk4, label=f'Recovered (RK4) K={k}')

plt.title('Impact of Recovery Rate (K) on Recovered Population')
plt.xlabel('Time')
plt.ylabel('Fraction of Recovered Population')
plt.legend()
plt.grid(True)
plt.show()
