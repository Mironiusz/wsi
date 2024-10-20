import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from functions import g, f


def plot_g_function(paths, steps, output_file="wykres_funkcji_g_2d.png"):
    x1_vals = np.linspace(-3, 3, 300)
    x2_vals = np.linspace(-3, 3, 300)
    X1, X2 = np.meshgrid(x1_vals, x2_vals)
    Z = np.array([[g([x1, x2]) for x1 in x1_vals] for x2 in x2_vals])

    plt.figure(figsize=(10, 8))
    contour = plt.contourf(X1, X2, Z, levels=50, cmap='viridis')
    plt.colorbar(contour, label="Wartość funkcji g(x1, x2)")

    # rysowanie trajektorii dla różnych kroków
    for i, path in enumerate(paths):
        path = np.array(path)
        plt.plot(path[:, 0], path[:, 1], '-o', label=f"Ścieżka beta={steps[i]}", markersize=5, linewidth=2)

    plt.title("Wykres konturowy funkcji g(x1, x2) z trajektoriami")
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file, dpi=300)
    plt.show()


def plot_f_function(paths, steps, output_file="wykres_funkcji_f_2d.png"):
    x_vals = np.linspace(-3, 3, 300)
    y_vals = np.array([f(x) for x in x_vals])

    plt.figure(figsize=(8, 6))
    plt.plot(x_vals, y_vals, label="f(x) = 0.5 * x^4 + x", color='b')

    # rysowanie trajektorii dla różnych kroków
    for i, path in enumerate(paths):
        path = np.array(path)
        plt.plot(path, f(path), '-o', label=f"Ścieżka beta={steps[i]}", markersize=5, linewidth=2)

    plt.xlim(-5, 5)
    plt.ylim(-2, 8)
    plt.title("Wykres funkcji f(x) z trajektoriami")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.savefig(output_file, dpi=300)
    plt.show()



def plot_g_function_3d(output_file="wykres_funkcji_g_3d.png"):
    x1_vals = np.linspace(-3, 3, 300)
    x2_vals = np.linspace(-3, 3, 300)
    X1, X2 = np.meshgrid(x1_vals, x2_vals)
    Z = np.array([[g([x1, x2]) for x1 in x1_vals] for x2 in x2_vals])

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X1, X2, Z, cmap='viridis', edgecolor='none')
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    ax.set_title("Render 3D funkcji g(x1, x2)")
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_zlabel("g(x1, x2)")
    plt.savefig(output_file, dpi=300)
    plt.show()
