import numpy as np
import matplotlib.pyplot as plt
from ex2_1 import model_euler
from ex2_2 import model_rk4

beta_values = [0.1, 0.3, 0.5]  
k = 0.1  
s0, i0, r0 = 0.99, 0.01, 0.0
dt, tfinal = 0.1, 100

plt.figure(figsize=(18, 10))

for beta in beta_values:
    s_euler, i_euler, r_euler = model_euler(s0, i0, r0, beta, k, dt, tfinal)
    s_rk4, i_rk4, r_rk4 = model_rk4(s0, i0, r0, beta, k, dt, tfinal)
    
    time = np.arange(0, tfinal + dt, dt)
    plt.plot(time, i_euler, '--', label=f'Infected (Euler) Beta={beta}')
    plt.plot(time, i_rk4, label=f'Infected (RK4) Beta={beta}')

plt.title('Impact of Transmission Rate (Beta) on Infected Population')
plt.xlabel('Time')
plt.ylabel('Fraction of Infected Population')
plt.legend()
plt.grid(True)
plt.show()
