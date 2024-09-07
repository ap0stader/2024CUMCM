import numpy as np
from matplotlib import pyplot as plt

import CONST
from SHAPE import ArchimedeanSpiral


# 获取螺线绘图背景
def get_spiral_background(spiral: ArchimedeanSpiral, loop: int, point_num: int):
    spiral_plot_theta = np.linspace(0, loop * 2 * np.pi, point_num)
    spiral_plot_r = spiral.p(spiral_plot_theta)

    figure, ax = plt.subplots(figsize=(20, 21), layout="constrained", subplot_kw={"projection": "polar"})
    ax.spines['polar'].set_visible(False)
    ax.plot(spiral_plot_theta, spiral_plot_r, color="green", linewidth=1)

    return figure, ax


def annotate_point(axis, spiral: ArchimedeanSpiral, number: int, theta):
    axis.annotate(str(number), (theta, spiral.p(theta)),
                  textcoords="offset fontsize", xytext=(0.1, 0.1), fontsize=18)


# 根据切线和板凳的夹角计算速度
def calc_speed(spiral: ArchimedeanSpiral, last_speed, last_theta, next_theta):
    bench_slope = (spiral.y(next_theta) - spiral.y(last_theta)) / (spiral.x(next_theta) - spiral.x(last_theta))
    last_theta_tangent_slope = spiral.tangent_slope(last_theta)
    next_theta_tangent_slope = spiral.tangent_slope(next_theta)
    last_bench_angle = np.arctan(np.abs((last_theta_tangent_slope - bench_slope)
                                        / (1 + last_theta_tangent_slope * bench_slope)))
    next_bench_angle = np.arctan(np.abs((next_theta_tangent_slope - bench_slope)
                                        / (1 + next_theta_tangent_slope * bench_slope)))
    next_speed = (last_speed * np.cos(last_bench_angle)) / np.cos(next_bench_angle)
    return next_speed


# 中心距离最近的板头的距离和宽度的对角线的长度的平方
PADDING_WIDTH_DIAGONAL_SQUARE = CONST.ALL_PADDING_HALF ** 2 + CONST.ALL_WIDTH_HALF ** 2


# 根据两个把手中心点的位置计算板凳四个角的坐标位置
def get_four_corner_point(spiral: ArchimedeanSpiral, bench_length, last_theta, next_theta):
    # 计算四个顶点
    last_x = spiral.x(last_theta)
    last_y = spiral.y(last_theta)
    next_x = spiral.x(next_theta)
    next_y = spiral.y(next_theta)
    # 上一节龙身前把手前方左侧点的配置
    vertical_x = (CONST.ALL_PADDING_HALF / bench_length) * (next_x - last_x)
    vertical_y = (CONST.ALL_PADDING_HALF / bench_length) * (next_y - last_y)
    horizontal_x = -(CONST.ALL_WIDTH_HALF / bench_length) * (next_y - last_y)
    horizontal_y = (CONST.ALL_WIDTH_HALF / bench_length) * (next_x - last_x)
    # 前方左侧点
    last_sharp_x = last_x - vertical_x - horizontal_x
    last_sharp_y = last_y - vertical_y - horizontal_y
    # 前方又侧点
    last_dull_x = last_x - vertical_x + horizontal_x
    last_dull_y = last_y - vertical_y + horizontal_y
    # 后方又侧点
    next_dull_x = next_x + vertical_x + horizontal_x
    next_dull_y = next_y + vertical_y + horizontal_y
    # 后方又侧点
    next_sharp_x = next_x + vertical_x - horizontal_x
    next_sharp_y = next_y + vertical_y - horizontal_y
    # 各点的极径
    last_sharp_p_square = last_sharp_x ** 2 + last_sharp_y ** 2
    last_dull_p_square = last_dull_x ** 2 + last_dull_y ** 2
    next_dull_p_square = next_dull_x ** 2 + next_dull_y ** 2
    next_sharp_p_square = next_sharp_x ** 2 + next_sharp_y ** 2

    def get_theta_delta(origin_theta, new_p_square):
        return np.arccos((spiral.p(origin_theta) ** 2 + new_p_square - PADDING_WIDTH_DIAGONAL_SQUARE)
                         / (2 * spiral.p(origin_theta) * np.sqrt(new_p_square)))

    last_sharp_theta = last_theta - get_theta_delta(last_theta, last_sharp_p_square)
    last_dull_theta = last_theta - get_theta_delta(last_theta, last_dull_p_square)
    next_dull_theta = next_theta + get_theta_delta(next_theta, next_dull_p_square)
    next_sharp_theta = next_theta + get_theta_delta(next_theta, next_sharp_p_square)

    c_point = [(last_sharp_x, last_sharp_y), (last_dull_x, last_dull_y),
               (next_dull_x, next_dull_y), (next_sharp_x, next_sharp_y)]

    p_point = [(last_sharp_theta, np.sqrt(last_sharp_p_square)), (last_dull_theta, np.sqrt(last_dull_p_square)),
               (next_dull_theta, np.sqrt(next_dull_p_square)), (next_sharp_theta, np.sqrt(next_sharp_p_square))]

    return c_point, p_point
