import os

import matplotlib.pyplot as plt
import numpy as np

import CONST
import Q4
from UTIL import xy2polar, annotate_point

# 创建结果保存目录
RESULT_DIR = CONST.RESULT_ROOT + "Q4_plot_forward/"
os.makedirs(RESULT_DIR, exist_ok=True)

# 模拟精度：1秒
SIM_SECOND = 100

# 每一秒龙头前把手行进的弧长
HEAD_SECOND_CURVE_LENGTH = CONST.DEFAULT_HEAD_SPEED

# 确定起始的位置
head_theta = [Q4.ThetaType.ROUND_IN, Q4.theta_C1_start]

for sec in range(SIM_SECOND + 1):
    print("正在计算第 " + str(sec) + " 秒信息")
    # 获取极坐标系绘制底图
    figure, ax = Q4.get_figure_background()
    # 设置图表标题
    figure.suptitle("Time: " + str(sec) + " s", fontsize=60, fontweight='bold')
    # 绘制龙头前把手的位置
    head_global_theta, head_global_p = xy2polar(Q4.theta2x(head_theta), Q4.theta2y(head_theta))
    ax.plot(head_global_theta, head_global_p, 'x', color="red", markersize=10, markeredgewidth=2)
    annotate_point(ax, 0, head_global_theta, head_global_p)
    # 求解第一节龙身前把手的位置
    first_body_theta = Q4.calc_next_handle_theta(head_theta, CONST.HEAD_BENCH_LEN)
    # 绘制第一节龙身前把手的位置和龙头板凳
    last_global_theta, last_global_p = xy2polar(Q4.theta2x(first_body_theta), Q4.theta2y(first_body_theta))
    head_bench_segment_theta = np.array([head_global_theta, last_global_theta])
    head_bench_segment_p = np.array([head_global_p, last_global_p])
    ax.plot(head_bench_segment_theta, head_bench_segment_p, '-', color="red", linewidth=5)
    annotate_point(ax, 1, last_global_theta, last_global_p)

    # 第2节龙身前把手至第222节龙身前把手的位置
    last_body_theta = first_body_theta
    for ben in range(2, CONST.BODY_TAIL_COUNT + 1):
        # 求解下一节龙身前把手的位置
        next_body_theta = Q4.calc_next_handle_theta(last_body_theta, CONST.OTHER_BENCH_LEN)
        # 绘制这一节龙身前把手的位置和上一节板凳
        next_global_theta, next_global_p = xy2polar(Q4.theta2x(next_body_theta), Q4.theta2y(next_body_theta))
        annotate_point(ax, ben, next_global_theta, next_global_p)
        last_bench_segment_theta = np.array([last_global_theta, next_global_theta])
        last_bench_segment_p = np.array([last_global_p, next_global_p])
        ax.plot(last_bench_segment_theta, last_bench_segment_p, 'x-', color="blue", linewidth=5,
                markersize=20, markeredgewidth=2)
        # 迭代
        last_body_theta = next_body_theta
        last_global_theta = next_global_theta
        last_global_p = next_global_p

    # 减少图表更新
    if sec % 5 == 0:
        figure.show()
    # 保存图表
    figure.savefig(RESULT_DIR + str(sec) + ".png")
    # 关闭图表
    plt.close(figure)

    # 求解龙头前把手新的位置
    head_theta = Q4.calc_next_head_theta(head_theta, HEAD_SECOND_CURVE_LENGTH)
