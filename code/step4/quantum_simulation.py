# -*- coding: euc-kr -*-
import numpy as np
import csv
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

z_data = []

with open('../../output/csv/measured_terrain.csv', 'r', encoding='utf-8') as f:
    for row in csv.reader(f):
        if row: z_data.extend([float(val) for val in row])

heights = np.array(z_data)
N_actual = len(heights)
dx_dy_area = 2.0 * 2.0

num_qubits = 7
num_states = 2 ** num_qubits

padded_heights = np.pad(heights, (0, num_states - N_actual), 'constant')

norm = np.linalg.norm(padded_heights)
amplitudes = padded_heights / norm

qc = QuantumCircuit(num_qubits)
qc.initialize(amplitudes, range(num_qubits))
qc.measure_all()

simulator = AerSimulator()
shots_count = 10000
job = simulator.run(qc, shots=shots_count)
counts = job.result().get_counts()

estimated_volume = 0

for state, count in counts.items():
    prob = count / shots_count
    estimated_height = norm * np.sqrt(prob)
    estimated_volume += estimated_height * dx_dy_area

print("=== 양자 시뮬레이션을 통한 적분 계산 결과 ===")
print(f"사용 큐비트 수: {num_qubits} (총 {num_states}개 상태 중 {N_actual}개 데이터 매핑)")
print(f"양자 진폭 추정 기반 토공량(부피): {estimated_volume:.2f} cm³")