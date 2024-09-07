import matplotlib.pyplot as plt
import numpy as np
import os

from matplotlib import patches
from shapely.geometry import Point, Polygon

import CONST
import ENV
import PARA
from SPIRAL import ArchimedeanSpiral
from UTIL import get_spiral_background, annotate_point, get_four_corner_point

# 创建结果保存目录
RESULT_DIR = CONST.RESULT_ROOT + "Q2_plot/"
os.makedirs(RESULT_DIR, exist_ok=True)

# 创建螺线
spiral = ArchimedeanSpiral(CONST.Q12_SPIRAL_DISTANCE)

# 精细模拟，一秒钟均分成几份
SEC_DIVISION = 1
# 模拟的秒数
SIM_SECOND = 430
# 模拟的轮数
SIM_STEP = SIM_SECOND * SEC_DIVISION
# 跳过的秒数
SKIP_SECOND = 400
# 跳过的轮数
SKIP_STEP = SKIP_SECOND * SEC_DIVISION
# 开始绘图的轮数
START_FIGURE_STEP = 410 * SEC_DIVISION

# 每一模拟步龙头前把手行进的弧长
HEAD_STEP_CURVE_LENGTH = CONST.DEFAULT_HEAD_SPEED / SEC_DIVISION

# 确定起始的位置
head_theta = CONST.Q12_HEAD_START_THETA
# 跳过轮数
for step in range(SKIP_STEP):
    head_theta = spiral.point_before_curve(head_theta, HEAD_STEP_CURVE_LENGTH)

# 记录数据为412.48秒出现碰撞
for step in range(SKIP_STEP, SIM_STEP + 1):
    print("正在计算第 " + "{:.4f}".format(step / SEC_DIVISION) + " 秒信息")
    print("当前龙头前把手的位置为θ=" + "{:.4f}".format(head_theta / (2 * np.pi)) + "x2π")
    # 获取极坐标系绘制底图
    figure, ax = get_spiral_background(spiral, PARA.Q12_SPIRAL_PLOT_LOOP, PARA.Q12_SPIRAL_PLOT_POINT_NUM)
    # 设置图表标题
    figure.suptitle("Time: " + "{:.4f}".format(step / SEC_DIVISION) + " s", fontsize=60, fontweight='bold')
    # 绘制龙头前把手的位置
    ax.plot(head_theta, spiral.p(head_theta), 'x', color="red", markersize=10, markeredgewidth=2)
    annotate_point(ax, spiral, 0, head_theta)
    # 求解第一节龙身前把手的位置
    first_body_theta = spiral.point_after_chord(head_theta, CONST.HEAD_BENCH_LEN)
    # 绘制第一节龙身前把手的位置和龙头板凳
    head_bench_segment = np.array([head_theta, first_body_theta])
    ax.plot(head_bench_segment, spiral.p(head_bench_segment), '--', color="red", linewidth=2)
    annotate_point(ax, spiral, 1, first_body_theta)
    # 绘制龙头的板凳的边框
    c_points, p_points = get_four_corner_point(spiral, CONST.HEAD_BENCH_LEN, head_theta, first_body_theta)
    bond = patches.Polygon(p_points, closed=True, facecolor=(1, 0, 0, 0.2), edgecolor="red", linewidth=0.5)
    ax.add_patch(bond)
    # 保存龙头前端尖锐点
    head_head_sharp_point = Point(c_points[0])
    # 保存龙头后端尖锐点
    head_tail_sharp_point = Point(c_points[3])

    # 第2节龙身前把手至第222节龙身前把手的位置
    last_body_theta = first_body_theta
    for ben in range(2, CONST.BODY_TAIL_COUNT + 1):
        # 求解下一节龙身前把手的位置
        next_body_theta = spiral.point_after_chord(last_body_theta, CONST.OTHER_BENCH_LEN)
        # 绘制这一节龙身前把手的位置和上一节板凳
        annotate_point(ax, spiral, ben, next_body_theta)
        last_bench_segment = np.array([last_body_theta, next_body_theta])
        ax.plot(last_bench_segment, spiral.p(last_bench_segment), 'x--', color="blue", linewidth=2,
                markersize=10, markeredgewidth=2)
        # 绘制龙身的板凳的边框
        c_points, p_points = get_four_corner_point(spiral, CONST.OTHER_BENCH_LEN, last_body_theta, next_body_theta)
        bond = patches.Polygon(p_points, closed=True, facecolor=(0, 0, 1, 0.2), edgecolor="blue",
                               linewidth=0.5)
        ax.add_patch(bond)
        # 只判断有可能发生碰撞的板凳
        if ben <= PARA.Q2_JUDGE_BODY:
            judge_polygon = Polygon(c_points)
            if judge_polygon.contains(head_head_sharp_point):
                print("在第 " + str(step) + " 龙头前方发生碰撞，发生碰撞的龙身是第 " + str(ben - 1) + " 块")
            if judge_polygon.contains(head_tail_sharp_point):
                print("在第 " + str(step) + " 龙头后方发生碰撞，发生碰撞的龙身是第 " + str(ben - 1) + " 块")
        # 迭代
        last_body_theta = next_body_theta

    if step >= START_FIGURE_STEP:
        # 减少图表更新
        if ENV.SHOW_PLOT and step % 5 == 0:
            figure.show()
        # 保存图表
        figure.savefig(RESULT_DIR + str(step) + ".png")
    # 关闭图表
    plt.close(figure)

    head_theta = spiral.point_before_curve(head_theta, HEAD_STEP_CURVE_LENGTH)
