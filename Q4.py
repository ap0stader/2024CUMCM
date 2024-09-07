import numpy as np

import CONST

# 详见GeoGebra文件Q4.ggb
alpha = CONST.Q45_RADIUS_RATIO

theta_A = (CONST.Q345_TURNAROUND_RADIUS /
           (CONST.Q45_SPIRAL_DISTANCE / (2 * np.pi)))

x_A = CONST.Q345_TURNAROUND_RADIUS * np.cos(theta_A)
y_A = CONST.Q345_TURNAROUND_RADIUS * np.sin(theta_A)
A = [x_A, y_A]
x_B = -x_A
y_B = -y_A
B = [x_B, y_B]

k_A = ((np.sin(theta_A) + theta_A * np.cos(theta_A))
       / (np.cos(theta_A) - theta_A * np.sin(theta_A)))

delta_x = ((x_A ** 2 + y_A ** 2) /
           ((1 + alpha) * ((y_A / k_A) - x_A)))

x_C1 = x_A + delta_x
y_C1 = y_A - (delta_x / k_A)
C1 = [x_C1, y_C1]

x_C2 = -x_A - alpha * delta_x
y_C2 = -y_A + ((alpha * delta_x) / k_A)
C2 = [x_C2, y_C2]

x_T = (2 / 3) * x_C2 + (1 / 3) * x_C1
y_T = (2 / 3) * y_C2 + (1 / 3) * y_C1
T = [x_T, y_T]

r_C1 = np.sqrt(1 + (1 / k_A ** 2)) * delta_x
r_C2 = alpha * r_C1

theta_C1_start = np.pi + np.arctan((y_C1 - y_A) / (x_C1 - x_A))  # 约4.00，230度
theta_C1_end = np.arctan((y_C2 - y_C1) / (x_C2 - x_C1))  # 约0.98，56度
theta_C2_start = -(np.pi - theta_C1_end)  # 约-2.15，-123度
theta_C2_end = np.arctan((y_B - y_C2) / (x_B - x_C2))  # 约0.86，49度
