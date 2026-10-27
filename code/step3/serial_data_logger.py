# -*- coding: euc-kr -*-
import serial
import csv
import numpy as np

arduino_port = 'COM8'
baud_rate = 9600
grid_size = 10

z_grid = np.zeros((grid_size, grid_size))

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout = 1)

    print("아두이노 통신 대기 중... (0,0 데이터가 들어오면 시작합니다)")
    
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            
            if "," in line:
                parts = line.split(',')

                if len(parts) == 3:
                    x = int(parts[0])
                    y = int(parts[1])
                    distance = float(parts[2])
                    
                    if x == 0 and y == 0:
                        print("\n=== 새로운 스캔 시작 ===")

                        z_grid = np.zeros((grid_size, grid_size))
                        
                    z_grid[x][y] = distance

                    print(f"좌표 ({x}, {y}) 거리: {distance} cm 기록됨")
                    
                    if x == 9 and y == 9:
                        print("\n=== 스캔 완료 ===")
                        print("데이터를 파일로 저장합니다.")

                        break

    with open('measured_terrain.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(z_grid)

    print("성공적으로 'measured_terrain.csv' 파일이 저장되었습니다.")

except Exception as e:
    print(f"오류 발생: {e}")