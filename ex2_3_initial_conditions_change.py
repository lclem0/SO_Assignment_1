import numpy as np
import matplotlib.pyplot as plt
from ex2_1 import model_euler
from ex2_2 import model_rk4

initial_conditions = [
    (0.99, 0.01, 0.0),  
    (0.9, 0.1, 0.0),    
    (0.8, 0.15, 0.05)   
]
beta, k = 0.3, 0.1
dt, tfinal = 0.1, 100

plt.figure(figsize=(18, 10))

for s0, i0, r0 in initial_conditions:
    s_euler, i_euler, r_euler = model_euler(s0, i0, r0, beta, k, dt, tfinal)
    s_rk4, i_rk4, r_rk4 = model_rk4(s0, i0, r0, beta, k, dt, tfinal)
    
    time = np.arange(0, tfinal + dt, dt)
    plt.plot(time, i_euler, '--', label=f'Infected (Euler) s0={s0}, i0={i0}, r0={r0}')
    plt.plot(time, i_rk4, label=f'Infected (RK4) s0={s0}, i0={i0}, r0={r0}')

plt.title('Impact of Initial Conditions on Infected Population')
plt.xlabel('Time')
plt.ylabel('Fraction of Infected Population')
plt.legend()
plt.grid(True)
plt.show()
