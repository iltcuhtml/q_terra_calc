# -*- coding: euc-kr -*-
import numpy as np
import matplotlib.pyplot as plt

def f(x, y):
    return x ** 2 + y ** 2

def monte_carlo_volume(x_max, y_max, num_samples):
    x_rand = np.random.uniform(0, x_max, num_samples)
    y_rand = np.random.uniform(0, y_max, num_samples)
    z_rand = f(x_rand, y_rand)

    area = x_max * y_max

    return area * np.mean(z_rand)

def get_errors():
    true_volume = 2 / 3
    N_values = [10 ** 2, 50 ** 2, 100 ** 2, 200 ** 2, 500 ** 2]
    
    err_rect = []
    err_trap = []
    err_mc = []

    for N in N_values:
        n = int(np.sqrt(N))
        dx, dy = 1.0 / n, 1.0 / n
        
        vol_rect = sum(f(i * dx, j * dy) * dx * dy for i in range(n) for j in range(n))
        err_rect.append(abs(true_volume - vol_rect))
        
        vol_trap = sum(((f(i * dx, j * dy) + f((i + 1) * dx, j * dy) + f(i * dx, (j + 1) * dy) + f((i + 1) * dx, (j + 1) * dy)) / 4) * dx * dy for i in range(n) for j in range(n))
        err_trap.append(abs(true_volume - vol_trap))
        
        vol_mc = monte_carlo_volume(1.0, 1.0, N)
        err_mc.append(abs(true_volume - vol_mc))

    return N_values, err_rect, err_trap, err_mc

N_vals, e_rect, e_trap, e_mc = get_errors()

plt.figure(figsize=(8, 6))

plt.loglog(N_vals, e_rect, marker = 'o', label = 'Rectangular', color = 'blue')
plt.loglog(N_vals, e_trap, marker = 's', label = 'Trapezoidal', color = 'green')
plt.loglog(N_vals, e_mc, marker = '^', label = 'Monte Carlo', color = 'orange')

theory_1_sqrt_N = [e_rect[0] * (N_vals[0] / n) ** 0.5 for n in N_vals]
theory_1_N = [e_trap[0] * (N_vals[0] / n) ** 1.0 for n in N_vals]
theory_mc_sqrt_N = [e_mc[0] * (N_vals[0] / n) ** 0.5 for n in N_vals]

plt.loglog(N_vals, theory_1_sqrt_N, 'k--', linewidth = 2, label = r'Theoretical: $1/\sqrt{N}$')
plt.loglog(N_vals, theory_1_N, 'r--', linewidth = 2, label = r'Theoretical: $1/N$')
plt.loglog(N_vals, theory_mc_sqrt_N, 'm--', linewidth = 2, label = r'Theoretical (MC): $1/\sqrt{N}$')

plt.xlabel('Total Grid Points (N)')
plt.ylabel('Absolute Error')
plt.title('Error Convergence: Actual vs Theoretical')

plt.legend()
plt.grid(True, which = "major", ls = "-", alpha = 0.5)

plt.show()