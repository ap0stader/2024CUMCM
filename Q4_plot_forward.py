import os

import CONST
import Q4

# 创建结果保存目录
RESULT_DIR = CONST.RESULT_ROOT + "Q4_plot/"
os.makedirs(RESULT_DIR, exist_ok=True)

# 模拟精度：1秒
SIM_SECOND = 100

# 每一秒龙头前把手行进的弧长
HEAD_SECOND_CURVE_LENGTH = CONST.DEFAULT_HEAD_SPEED

# 确定起始的位置
head_theta = [Q4.ThetaType.ROUND_IN, Q4.theta_C1_start]

for sec in range(SIM_SECOND + 1):
    print("正在计算第 " + str(sec) + " 秒信息")

    head_theta = Q4.calc_next_head_theta(head_theta, HEAD_SECOND_CURVE_LENGTH)
