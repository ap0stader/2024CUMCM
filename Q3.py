import matplotlib.pyplot as plt
import numpy as np
import os

from matplotlib import patches
from scipy.optimize import brentq, fsolve
from shapely.geometry import Point, Polygon

# 阿基米德螺线方程：r = b * θ
# 阿基米德螺线参数
SPIRAL_B = 55 / (2 * np.pi)

# 来自题目的数据单位为厘米
ALL_PADDING_HALF = 27.5
ALL_PADDING_LENGTH = 55  # 27.5cm x 2
FIRST_LENGTH = 341 - ALL_PADDING_LENGTH
OTHER_LENGTH = 220 - ALL_PADDING_LENGTH
ALL_WIDTH_HALF = 15  # 30cm / 2
PADDING_WIDTH_DIAGONAL_SQUARE = ALL_PADDING_HALF ** 2 + ALL_WIDTH_HALF ** 2
HEAD_SPEED = 100  # 1m/s

# 精细模拟，一秒钟均分成几份
PRECISE_DIVISION = 100
# 模拟精度：1s
SIMULATION_ALL_STEP = 400 * PRECISE_DIVISION
# 每一模拟步骤龙头前把手行进的距离
STEP_HEAD_CURVE_LENGTH = HEAD_SPEED / PRECISE_DIVISION
# 跳过的轮数
SKIP_STEP = 0 * PRECISE_DIVISION


# 阿基米德螺线公式
def spiral(theta):
    return SPIRAL_B * theta


# 计算θ1到θ2的弧长（要求θ1<=02）
def calc_curve_length(theta1, theta2):
    def summa(theta):
        return (SPIRAL_B / 2) * (theta * np.sqrt(1 + theta * theta) + np.log(theta + np.sqrt(1 + theta * theta)))

    assert theta1 <= theta2
    return summa(theta2) - summa(theta1)


# 求解龙头的位置在当前位置前进一秒后的θ
def solve_next_now_head_theta(last_theta):
    def equation(theta):
        return calc_curve_length(theta, last_theta) - STEP_HEAD_CURVE_LENGTH

    solution = brentq(equation, last_theta - np.pi, last_theta)
    return solution


# 求解龙头后第一节前把手的位置
def solve_next_ben_f_theta(ben_length, last_theta):
    last_theta_cos = last_theta * np.cos(last_theta)
    last_theta_sin = last_theta * np.sin(last_theta)
    right_constant = (ben_length ** 2) / (SPIRAL_B ** 2)

    def equation(theta):
        return ((theta * np.cos(theta) - last_theta_cos) ** 2
                + (theta * np.sin(theta) - last_theta_sin) ** 2
                - right_constant)

    guess = np.arccos((2 * spiral(last_theta) ** 2 - ben_length ** 2) / (2 * spiral(last_theta) ** 2))
    solution = fsolve(equation, x0=(last_theta + guess))
    return float(solution[0])


# 根据两个把手中心点的位置计算板凳四个角的坐标位置
def get_four_corner_point(bench_length, last_theta, new_theta):
    # 计算四个顶点
    last_bench_f_x = spiral(last_theta) * np.cos(last_theta)
    last_bench_f_y = spiral(last_theta) * np.sin(last_theta)
    new_ben_f_x = spiral(new_theta) * np.cos(new_theta)
    new_ben_f_y = spiral(new_theta) * np.sin(new_theta)
    # 前一板凳左侧点的配置
    vertical_x = (ALL_PADDING_HALF / bench_length) * (new_ben_f_x - last_bench_f_x)
    vertical_y = (ALL_PADDING_HALF / bench_length) * (new_ben_f_y - last_bench_f_y)
    horizontal_x = -(ALL_WIDTH_HALF / bench_length) * (new_ben_f_y - last_bench_f_y)
    horizontal_y = (ALL_WIDTH_HALF / bench_length) * (new_ben_f_x - last_bench_f_x)
    # 前方左侧点
    last_sharp_x = last_bench_f_x - vertical_x - horizontal_x
    last_sharp_y = last_bench_f_y - vertical_y - horizontal_y
    last_dull_x = last_bench_f_x - vertical_x + horizontal_x
    last_dull_y = last_bench_f_y - vertical_y + horizontal_y
    new_dull_x = new_ben_f_x + vertical_x + horizontal_x
    new_dull_y = new_ben_f_y + vertical_y + horizontal_y
    new_sharp_x = new_ben_f_x + vertical_x - horizontal_x
    new_sharp_y = new_ben_f_y + vertical_y - horizontal_y

    last_sharp_r_square = last_sharp_x ** 2 + last_sharp_y ** 2
    last_dull_r_square = last_dull_x ** 2 + last_dull_y ** 2
    new_dull_r_square = new_dull_x ** 2 + new_dull_y ** 2
    new_sharp_r_square = new_sharp_x ** 2 + new_sharp_y ** 2

    def get_theta_delta(origin_theta, new_r_square):
        return np.arccos((spiral(origin_theta) ** 2 + new_r_square - PADDING_WIDTH_DIAGONAL_SQUARE)
                         / (2 * spiral(origin_theta) * np.sqrt(new_r_square)))

    last_sharp_theta = last_theta - get_theta_delta(last_theta, last_sharp_r_square)
    last_dull_theta = last_theta - get_theta_delta(last_theta, last_dull_r_square)
    new_dull_theta = new_theta + get_theta_delta(new_theta, new_dull_r_square)
    new_sharp_theta = new_theta + get_theta_delta(new_theta, new_sharp_r_square)

    c_point = [(last_sharp_x, last_sharp_y), (last_dull_x, last_dull_y),
               (new_dull_x, new_dull_y), (new_sharp_x, new_sharp_y)]

    p_point = [(last_sharp_theta, np.sqrt(last_sharp_r_square)), (last_dull_theta, np.sqrt(last_dull_r_square)),
               (new_dull_theta, np.sqrt(new_dull_r_square)), (new_sharp_theta, np.sqrt(new_sharp_r_square))]

    return c_point, p_point


gap = 55

while gap >= 10:
    SPIRAL_B = gap / (2 * np.pi)
    start_head_theta = 450 / SPIRAL_B + 4 * np.pi
    # 确定起始的位置
    now_head_theta = start_head_theta

    for step in range(SKIP_STEP, SIMULATION_ALL_STEP + 1):
        print("正在计算第 " + str(step) + " 轮信息")
        print("当前龙头前把手的位置的θ=" + "{:.4f}".format(now_head_theta / (2 * np.pi)) + "x2π")
        # 龙头后第一节前把手的位置
        second_ben_f_theta = solve_next_ben_f_theta(FIRST_LENGTH, now_head_theta)
        # 绘制龙头的板凳
        c_four_corner_point, _ = get_four_corner_point(FIRST_LENGTH, now_head_theta, second_ben_f_theta)
        # 保存龙头前端尖锐点
        head_head_sharp_point = Point(c_four_corner_point[0])
        # 保存龙头后端尖锐点
        head_tail_sharp_point = Point(c_four_corner_point[3])

        # 后222节前把手位置
        last_ben_f_theta = second_ben_f_theta
        for ben in range(3, 225):  # 3 <= ben <= 224 第 224 号为最后一节的后把手
            new_ben_f_theta = solve_next_ben_f_theta(OTHER_LENGTH, last_ben_f_theta)

            c_four_corner_point, _ = get_four_corner_point(OTHER_LENGTH, last_ben_f_theta,
                                                           new_ben_f_theta)

            # 判断，在300步之后才开始判断
            if ben <= 30:
                judge_polygon = Polygon(c_four_corner_point)
                if judge_polygon.contains(head_head_sharp_point):
                    print("在第 " + str(step) + " 龙头前方发生碰撞，发生碰撞的板凳是第 " + str(ben - 1) + " 条")
                if judge_polygon.contains(head_tail_sharp_point):
                    print("在第 " + str(step) + " 龙头前方发生碰撞，发生碰撞的板凳是第 " + str(ben - 1) + " 条")

            last_ben_f_theta = new_ben_f_theta

        now_head_theta = solve_next_now_head_theta(now_head_theta)
