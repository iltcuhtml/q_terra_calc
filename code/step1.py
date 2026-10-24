# -*- coding: euc-kr -*-
import numpy as np

def f(x, y):
    return x ** 2 + y **2

def calculate_volume_rectangular(x_max, y_max, nx, ny):
    dx = x_max / nx
    dy = y_max / ny
    volume = 0
    
    for i in range(nx):
        for j in range(ny):
            x = i * dx
            y = j * dy
            volume += f(x, y) * dx * dy
            
    return volume

def calculate_volume_trapezoidal(x_max, y_max, nx, ny):
    dx = x_max / nx
    dy = y_max / ny
    volume = 0
    
    for i in range(nx):
        for j in range(ny):
            x1, x2 = i * dx, (i + 1) * dx
            y1, y2 = j * dy, (j + 1) * dy
            
            h_avg = (f(x1, y1) + f(x2, y1) + f(x1, y2) + f(x2, y2)) / 4.0
            volume += h_avg * dx * dy
            
    return volume

x_bound, y_bound = 1.0, 1.0
grid_steps = [10, 50, 100, 500]

print("=== 이론 곡면 z = x^2 + y^2 (구간 0~1) 부피 계산 검증 ===")
print("이론적 정적분 값: 0.66666...\n")

for n in grid_steps:
    vol_rect = calculate_volume_rectangular(x_bound, y_bound, n, n)
    vol_trap = calculate_volume_trapezoidal(x_bound, y_bound, n, n)
    
    print(f"[격자 {n}x{n}]")
    print(f" - 직사각형법 계산값: {vol_rect:.6f} (오차: {abs(2/3 - vol_rect):.6f})")
    print(f" - 사다리꼴법 계산값: {vol_trap:.6f} (오차: {abs(2/3 - vol_trap):.6f})\n")