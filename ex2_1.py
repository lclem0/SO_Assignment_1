#from class 3 exercise 4 - euler method - adapted to the logistic growth model
import argparse
import matplotlib.pyplot as plt
import numpy as np


def model_euler(s0, i0, r0, beta, k, dt, tfinal):
    num_steps = int(tfinal / dt) + 1

    s = np.zeros(num_steps)
    i = np.zeros(num_steps)
    r = np.zeros(num_steps)

    s[0] = s0
    i[0] = i0
    r[0] = r0

    for t in range(1, num_steps):
        ds_dt = -beta * s[t-1] * i[t-1]
        di_dt = beta * s[t-1] * i[t-1] - k * i[t-1]
        dr_dt = k * i[t-1]

        s[t] = s[t-1] + ds_dt * dt
        i[t] = i[t-1] + di_dt * dt
        r[t] = r[t-1] + dr_dt * dt

    return s, i, r
           

def load_parameters(file_path):
    parameters = {}
    with open(file_path, 'r') as f:
        for line in f:
            key, value = line.strip().split()
            parameters[key] = float(value)
    return parameters
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Forward Euler method.')
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

    s, i, r = model_euler(s0, i0, r0, beta, k, dt, tfinal)
    # Plotting the data
    plt.plot(np.arange(0, tfinal+dt, dt), s, label='Susceptible')
    plt.plot(np.arange(0, tfinal+dt, dt), i, label='Infected')
    plt.plot(np.arange(0, tfinal+dt, dt), r, label='Recovered')
    plt.xlabel('Time')
    plt.ylabel('Fraction of Population')
    plt.title('Euler Method')
    plt.legend()
    plt.grid(True)
    plt.show()

