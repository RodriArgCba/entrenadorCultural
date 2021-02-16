import numpy as np


def distanciaentrelineas(a0, a1, b0, b1):
    a0 = np.array(a0)
    a1 = np.array(a1)
    p1 = a0 + 0.5 * (a1 - a0)
    b0 = np.array(b0)
    b1 = np.array(b1)
    p2 = b0 + 0.5 * (b1 - b0)
    return np.sqrt((p2 - p1).dot(p2 - p1))



