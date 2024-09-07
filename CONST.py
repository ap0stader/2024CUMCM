import os

import numpy as np

# 结果保存根目录
RESULT_ROOT = "./result/"
os.makedirs(RESULT_ROOT, exist_ok=True)

# 板凳龙由223节板凳组成，其中第1节为龙头，后面221节为龙身，最后1节为龙尾
# 因为龙尾使用的板凳与龙身相同，称龙尾为第222节龙身
# 称龙尾后把手为第223节龙身前把手
BODY_TAIL_COUNT = 221 + 1 + 1

# 以下数据的长度单位为厘米
# 孔的中心距离最近的板头 27.5 cm
ALL_PADDING_HALF = 27.5
# 两孔的中心距离最近的板头的距离之和
ALL_PADDING_LEN = ALL_PADDING_HALF * 2
# 板凳宽度的一半
ALL_WIDTH_HALF = 15  # 30cm / 2
# 龙头板凳两孔之间的距离（有效长度）
HEAD_BENCH_LEN = 341 - ALL_PADDING_LEN
# 其他板凳两孔之间的距离（有效长度）
OTHER_BENCH_LEN = 220 - ALL_PADDING_LEN
# 问题1-2的螺距、问题3的初始螺距
Q12_SPIRAL_DISTANCE = 55
# 问题3-5掉头范围的半径
Q345_TURNAROUND_RADIUS = 450  # 9m / 2
# 问题4-5的螺距
Q45_SPIRAL_DISTANCE = 170  # 1.7 m
# 默认的龙头前把手速度
DEFAULT_HEAD_SPEED = 100  # 1 m/s

# 以下数据的时间单位为秒
# 问题1-2的最大模拟描述，超过430秒，求解器可能出现问题
# from SPIRAL import ArchimedeanSpiral
# spiral = ArchimedeanSpiral(Q12_SPIRAL_DISTANCE)
# all_curve_length = spiral.curve_length(0, Q1_HEAD_START_THETA)
# Q12_MAX_SIM_SECOND = int(all_curve_length / DEFAULT_HEAD_SPEED)
Q12_MAX_SIM_SECOND = 430

# 以下数据的角单位为弧度
# 问题1开始时龙头前把手位于螺线第16圈A点处
Q12_HEAD_START_THETA = 16 * 2 * np.pi

# 问题4-5前一段弧和后一段弧的半径的比例
Q45_RADIUS_RATIO = 0.5
