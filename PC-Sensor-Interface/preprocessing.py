import numpy as np
import matplotlib.pyplot as plt
import pickle
import struct


def check_data(data):
    for sample in data:
        if len(sample) != 13 or (sum(sample[:12]) & 0x7f) != (sample[12] & 0x7f) or sample[12] & 128:
            raise RuntimeError("Invalid Sample")
        pass
    pass


def load(name):
    with open(name+'.pickle', 'rb') as f:
        calib, data, t = pickle.load(f)
        pass

    del data[0]
    check_data(data)
    return calib, data, t


def calibration_matrix(calib):
    cm = [struct.unpack('>f', int.to_bytes(calib[32+2*i], 2, 'big')
                        + int.to_bytes(calib[33+2*i], 2, 'big'))[0] for i in range(36)]
    return np.array(cm).reshape(6, 6)


def force_torque_scaling_factors(calib):
    counts_per_torque = struct.unpack('>i', int.to_bytes(calib[119], 2, 'big') + int.to_bytes(calib[120], 2, 'big'))[0]
    counts_per_force = struct.unpack('>i', int.to_bytes(calib[117], 2, 'big') + int.to_bytes(calib[118], 2, 'big'))[0]

    if counts_per_force != counts_per_torque:
        raise RuntimeError("Unequal Scaling Factors")

    return counts_per_force


def max_rating(calib):
    max_f_t = []
    for i in range(6):
        max_f_t.append(struct.unpack('>f', int.to_bytes(calib[105 + 2*i], 2, 'big')
                                     + int.to_bytes(calib[106 + 2*i], 2, 'big'))[0])
        pass
    return max_f_t


def get_values(data, calib):
    n = len(data)

    values = np.zeros((n, 6))
    for i in range(n):
        gage_vector = np.array([struct.unpack('>h', data[i][j:j + 2])[0] for j in (0, 6, 2, 8, 4, 10)])
        values[i] = calibration_matrix(calib) @ gage_vector
        pass
    values /= force_torque_scaling_factors(calib)

    return values


def save_preprocessed_data(values, t, name):
    with open(name + '_preprocessed.pickle', 'wb') as f:
        pickle.dump((values, t), f)
        pass
    pass


def plot_initial_data(values, t, calib, name):  # plots data after basic taring and computes measured average frequency
    n = len(values)
    # Basic Taring
    values -= np.average(values[:n//10], 0)

    # Maximum rated force/torque
    max_f_t = max_rating(calib)
    print(f"{np.int_(100 * np.max(np.abs(values), axis=0) / np.array(max_f_t))} % of max rated force/torque")

    plt.figure()
    plt.plot(np.linspace(0, t, n), values, lw=0.5)
    plt.title(f"{round(n / t)} Hz")
    plt.legend(["Fx", "Fy", "Fz", "Tx", "Ty", "Tz"])
    plt.savefig(name + "-initial_plot.png")
    pass
