import os

import matplotlib.pyplot as plt

import CONST
import Q4
from UTIL import xy2polar, annotate_point

# 创建结果保存目录
RESULT_DIR = CONST.RESULT_ROOT + "Q4_plot/"
os.makedirs(RESULT_DIR, exist_ok=True)

# 模拟精度：1秒
SIM_SECOND = 100

# 每一秒龙头前把手行进的弧长
HEAD_SECOND_CURVE_LENGTH = CONST.DEFAULT_HEAD_SPEED

# 确定起始的位置
head_theta = [Q4.ThetaType.ROUND_IN, Q4.theta_C1_start]

figure, ax = Q4.get_figure_background()

for sec in range(SIM_SECOND + 1):
    theta, p = xy2polar(Q4.theta2x(head_theta), Q4.theta2y(head_theta))
    ax.plot(theta, p, 'x', color="red", markersize=10, markeredgewidth=2)
    annotate_point(ax, sec, theta, p)

    head_theta = Q4.calc_next_head_theta(head_theta, HEAD_SECOND_CURVE_LENGTH)

figure.show()
plt.close(figure)
