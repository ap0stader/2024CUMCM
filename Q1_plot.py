import matplotlib.pyplot as plt
import numpy as np
import os

import CONST
import Q1
from SHAPE import ArchimedeanSpiral
from UTIL import annotate_point

# 创建结果保存目录
RESULT_DIR = CONST.RESULT_ROOT + "Q1_plot/"
os.makedirs(RESULT_DIR, exist_ok=True)

# 创建螺线
spiral = ArchimedeanSpiral(CONST.Q12_SPIRAL_DISTANCE)

# 模拟精度：1秒
SIM_SECOND = 430
assert SIM_SECOND <= CONST.Q12_MAX_SIM_SECOND

# 每一秒龙头前把手行进的弧长
HEAD_SECOND_CURVE_LENGTH = CONST.DEFAULT_HEAD_SPEED

# 确定起始的位置
head_theta = CONST.Q12_HEAD_START_THETA

# 共需300秒数据
for sec in range(SIM_SECOND + 1):
    print("正在计算第 " + str(sec) + " 秒信息")
    print("当前龙头前把手的位置为θ=" + "{:.4f}".format(head_theta / (2 * np.pi)) + "x2π")
    # 获取极坐标系绘制底图
    figure, ax = Q1.get_spiral_background(spiral)
    # 设置图表标题
    figure.suptitle("Time: " + str(sec) + " s", fontsize=60, fontweight='bold')
    # 绘制龙头前把手的位置
    ax.plot(head_theta, spiral.p(head_theta), 'x', color="red", markersize=20, markeredgewidth=2)
    annotate_point(ax, 0, head_theta, spiral.p(head_theta))
    # 求解第一节龙身前把手的位置
    first_body_theta = spiral.point_after_chord(head_theta, CONST.HEAD_BENCH_LEN)
    # 绘制第一节龙身前把手的位置和龙头板凳
    head_bench_segment = np.array([head_theta, first_body_theta])
    ax.plot(head_bench_segment, spiral.p(head_bench_segment), '-', color="red", linewidth=5)
    annotate_point(ax, 1, first_body_theta, spiral.p(first_body_theta))

    # 第2节龙身前把手至第222节龙身前把手的位置
    last_body_theta = first_body_theta
    for ben in range(2, CONST.BODY_TAIL_COUNT + 1):
        # 求解下一节龙身前把手的位置
        next_body_theta = spiral.point_after_chord(last_body_theta, CONST.OTHER_BENCH_LEN)
        # 绘制这一节龙身前把手的位置和上一节板凳
        annotate_point(ax, ben, next_body_theta, spiral.p(next_body_theta))
        last_bench_segment = np.array([last_body_theta, next_body_theta])
        ax.plot(last_bench_segment, spiral.p(last_bench_segment), 'x-', color="blue", linewidth=5,
                markersize=20, markeredgewidth=2)
        # 迭代
        last_body_theta = next_body_theta

    # 减少图表更新
    if sec % 5 == 0:
        figure.show()
    # 保存图表
    figure.savefig(RESULT_DIR + str(sec) + ".png")
    # 关闭图表
    plt.close(figure)

    # 求解龙头前把手新的位置
    head_theta = spiral.point_before_curve(head_theta, HEAD_SECOND_CURVE_LENGTH)
