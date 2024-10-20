import numpy as np


def f(x):
    return 0.5 * x**4 + x


def g(x):
    x1, x2 = x[0], x[1]
    term1 = np.exp(-x1**2 - (x2 + 1)**2)
    term2 = np.exp(-(x1 - 1.75)**2 - (x2 + 2)**2)
    return 1 - 0.6 * term1 - 0.4 * term2


def grad_f(x):
    return 2 * x**3 + 1


def grad_g(x):
    x1, x2 = x[0], x[1]

    term1_x1 = 1.2 * x1 * np.exp(-x1**2 - (x2 + 1)**2)
    term2_x1 = 0.8 * (x1 - 1.75) * np.exp(-(x1 - 1.75)**2 - (x2 + 2)**2)
    grad_x1 = term1_x1 + term2_x1

    term1_x2 = 1.2 * (x2 + 1) * np.exp(-x1**2 - (x2 + 1)**2)
    term2_x2 = 0.8 * (x2 + 2) * np.exp(-(x1 - 1.75)**2 - (x2 + 2)**2)
    grad_x2 = term1_x2 + term2_x2

    return np.array([grad_x1, grad_x2])


def gradient_descent(f, grad_f, x0, beta=0.1, epsilon=0.00001, max_iter=100000):
    x = x0
    path = [x0.copy()]
    for t in range(max_iter):
        grad = grad_f(x)
        if np.linalg.norm(grad) < epsilon:
            return x, path, t
        x = x - beta * grad
        path.append(x.copy())
    return x, path, max_iter
