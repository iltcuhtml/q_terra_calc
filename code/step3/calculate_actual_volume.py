# -*- coding: euc-kr -*-
import csv

def load_data_from_csv(filename):
    z_data = []

    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        for row in reader:
            if row:
                z_data.append([float(val) for val in row])

    return z_data

def calculate_measured_volume(z_grid, dx, dy, baseline_depth):
    rows, cols = len(z_grid), len(z_grid[0])
    total_volume = 0
    
    for i in range(rows - 1):
        for j in range(cols - 1):
            h1 = max(0, baseline_depth - z_grid[i][j])
            h2 = max(0, baseline_depth - z_grid[i + 1][j])
            h3 = max(0, baseline_depth - z_grid[i][j + 1])
            h4 = max(0, baseline_depth - z_grid[i + 1][j + 1])
            
            avg_height = (h1 + h2 + h3 + h4) / 4.0
            total_volume += avg_height * dx * dy
            
    return total_volume

measured_z_data = load_data_from_csv('../../output/csv/measured_terrain.csv')
dx_cm, dy_cm = 2.0, 2.0

user_input = input("평평한 바닥일 때의 기준 거리를 입력하세요 (단위: cm, 예: 4.00): ")
baseline_depth = float(user_input)

final_volume = calculate_measured_volume(measured_z_data, dx_cm, dy_cm, baseline_depth)

print("\n=== 구분구적법(사다리꼴법) 지형 부피 계산 결과 ===")
print(f"데이터 크기: {len(measured_z_data)} x {len(measured_z_data[0])} 격자")
print(f"측정된 모형의 실제 토공량(부피): {final_volume:.2f} cm^3")