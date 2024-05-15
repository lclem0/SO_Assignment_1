import numpy as np
import argparse
import matplotlib.pyplot as plt

def load_parameters(file_path):
    parameters = {}
    with open(file_path, 'r') as f:
        for line in f:
            key, value = line.strip().split()
            parameters[key] = float(value)
    return parameters

def model_rk4(s0, i0, r0, beta, k, dt, tfinal):
    num_steps = int(tfinal / dt) + 1

    s = np.zeros(num_steps)
    i = np.zeros(num_steps)
    r = np.zeros(num_steps)

    s[0] = s0
    i[0] = i0
    r[0] = r0

    for t in range(1, num_steps):
        k1s = -beta * s[t-1] * i[t-1]
        k1i = beta * s[t-1] * i[t-1] - k * i[t-1]
        k1r = k * i[t-1]

        k2s = -beta * (s[t-1] + 0.5 * dt * k1s) * (i[t-1] + 0.5 * dt * k1i)
        k2i = beta * (s[t-1] + 0.5 * dt * k1s) * (i[t-1] + 0.5 * dt * k1i) - k * (i[t-1] + 0.5 * dt * k1i)
        k2r = k * (i[t-1] + 0.5 * dt * k1i)

        k3s = -beta * (s[t-1] + 0.5 * dt * k2s) * (i[t-1] + 0.5 * dt * k2i)
        k3i = beta * (s[t-1] + 0.5 * dt * k2s) * (i[t-1] + 0.5 * dt * k2i) - k * (i[t-1] + 0.5 * dt * k2i)
        k3r = k * (i[t-1] + 0.5 * dt * k2i)

        k4s = -beta * (s[t-1] + dt * k3s) * (i[t-1] + dt * k3i)
        k4i = beta * (s[t-1] + dt * k3s) * (i[t-1] + dt * k3i) - k * (i[t-1] + dt * k3i)
        k4r = k * (i[t-1] + dt * k3i)

        s[t] = s[t-1] + (1/6) * dt * (k1s + 2*k2s + 2*k3s + k4s)
        i[t] = i[t-1] + (1/6) * dt * (k1i + 2*k2i + 2*k3i + k4i)
        r[t] = r[t-1] + (1/6) * dt * (k1r + 2*k2r + 2*k3r + k4r)

    return s, i, r

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Runge-Kutta 4th order method.')
    parser.add_argument('--s0', type=float, help='Initial fraction of susceptible population')
    parser.add_argument('--i0', type=float, help='Initial fraction of infected population')
    parser.add_argument('--r0', type=float, help='Initial fraction of recovered population')

    parser.add_argument('--beta', type=float, help='Transmission rate')
    parser.add_argument('--k', type=float, help='Recovery rate')
    parser.add_argument('--dt', type=float, help='Time step size')
    parser.add_argument('--tfinal', type=float, help='Final time')
    parser.add_argument('--parameter_file', type=str, help='File containing parameters')
    args = parser.parse_args()

    if args.parameter_file is None:
        # No parameter file specified, using command-line arguments
        s0 = args.s0
        i0 = args.i0
        r0 = args.r0
        beta = args.beta
        k = args.k
        dt = args.dt
        tfinal = args.tfinal
    else:
        # Load parameters from file
        parameters = load_parameters(args.parameter_file)
        s0 = parameters['s0']
        i0 = parameters['i0']
        r0 = parameters['r0']
        beta = parameters['beta']
        k = parameters['k']
        dt = parameters['dt']
        tfinal = parameters['tfinal']

    s, i, r = model_rk4(s0, i0, r0, beta, k, dt, tfinal)

    # Plotting the data
    plt.plot(np.arange(0, tfinal+dt, dt), s, label='Susceptible')
    plt.plot(np.arange(0, tfinal+dt, dt), i, label='Infected')
    plt.plot(np.arange(0, tfinal+dt, dt), r, label='Recovered')
    plt.xlabel('Time')
    plt.ylabel('Fraction of Population')
    plt.title('Runge-Kutta 4th Order Method')
    plt.legend()
    plt.grid(True)
    plt.show()
