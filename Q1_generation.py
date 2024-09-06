import matplotlib.pyplot as plt
import numpy as np
import os

from scipy.optimize import brentq, fsolve

# 阿基米德螺线方程：r = b * θ
# 阿基米德螺线参数
SPIRAL_B = 55 / (2 * np.pi)

# 来自题目的数据单位为厘米
PADDING_LENGTH = 55  # 27.5cm x 2
FIRST_LENGTH = 341 - PADDING_LENGTH
OTHER_LENGTH = 220 - PADDING_LENGTH
HEAD_SPEED = 100  # 1m/s

# 模拟精度：1s
SIMULATION_ALL_STEP = 430
# 每一模拟步骤龙头前把手行进的距离
STEP_HEAD_CURVE_LENGTH = HEAD_SPEED


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


def spiral_tangent_slope(theta):
    return (np.sin(theta) + theta * np.cos(theta)) / (np.cos(theta) - theta * np.sin(theta))


def calc_speed(last_speed, last_theta, new_theta):
    ben_slope = ((spiral(new_theta) * np.sin(new_theta) - spiral(last_theta) * np.sin(last_theta)) /
                 (spiral(new_theta) * np.cos(new_theta) - spiral(last_theta) * np.cos(last_theta)))
    last_theta_tangent_slope = spiral_tangent_slope(last_theta)
    new_theta_tangent_slope = spiral_tangent_slope(new_theta)
    last_ben_angle = np.arctan(np.abs((last_theta_tangent_slope - ben_slope)
                                      / (1 + last_theta_tangent_slope * ben_slope)))
    new_ben_angle = np.arctan(np.abs((new_theta_tangent_slope - ben_slope)
                                     / (1 + new_theta_tangent_slope * ben_slope)))
    new_speed = (last_speed * np.cos(last_ben_angle)) / np.cos(new_ben_angle)
    return new_speed


# 龙头位于螺线第16圈A点处
start_head_theta = 16 * 2 * np.pi

# 计算最多能走多少秒
all_curve_length = calc_curve_length(0, start_head_theta)
max_step = int(all_curve_length / STEP_HEAD_CURVE_LENGTH)
print("自开始点到坐标轴原点的弧长共 " + str(all_curve_length) + " cm")
print("仅考虑龙头前把手的运动，仅可运动 " + str(max_step) + " 秒")

# 确定起始的位置
now_head_theta = start_head_theta

# 存储数据，下标表示的第几节龙身，0表示龙头
data = list()

# 实验结果是最多走
for step in range(SIMULATION_ALL_STEP + 1):  # 共需300s数据
    assert step < max_step
    data.append(list())
    print("正在计算第 " + str(step) + " 秒信息")
    # 龙头前把手的位置绘制
    print("当前龙头前把手的位置的θ=" + "{:.4f}".format(now_head_theta / (2 * np.pi)) + "x2π")
    data[step].append((now_head_theta,
                       spiral(now_head_theta) * np.cos(now_head_theta),
                       spiral(now_head_theta) * np.sin(now_head_theta),
                       HEAD_SPEED))
    # 龙头后第一节前把手的位置
    second_ben_f_theta = solve_next_ben_f_theta(FIRST_LENGTH, now_head_theta)
    second_ben_f_speed = calc_speed(HEAD_SPEED, now_head_theta, second_ben_f_theta)
    data[step].append((second_ben_f_theta,
                       spiral(second_ben_f_theta) * np.cos(second_ben_f_theta),
                       spiral(second_ben_f_theta) * np.sin(second_ben_f_theta),
                       second_ben_f_speed))

    # 后222节前把手位置
    last_ben_f_theta = second_ben_f_theta
    last_ben_f_speed = second_ben_f_speed
    for ben in range(3, 225):  # 3 <= ben <= 224 第 224 号为最后一节的后把手
        new_ben_f_theta = solve_next_ben_f_theta(OTHER_LENGTH, last_ben_f_theta)
        new_ben_f_speed = calc_speed(last_ben_f_speed, last_ben_f_theta, new_ben_f_theta)
        data[step].append((new_ben_f_theta,
                           spiral(new_ben_f_theta) * np.cos(new_ben_f_theta),
                           spiral(new_ben_f_theta) * np.sin(new_ben_f_theta),
                           new_ben_f_speed))
        last_ben_f_theta = new_ben_f_theta

    now_head_theta = solve_next_now_head_theta(now_head_theta)
    print(np.shape(data[step]))
    print("第一个点的情况：" + str(data[step][0]))
    print("最后一个点的情况：" + str(data[step][223]))

# 数据解读方法
# 第一维时间
# 第二维第几个板凳把手，0表示龙头前把手，1-222表示221节龙身+1节龙尾前把手，223表示龙尾后把手
# 第三维，第一个数字是theta，第二个数字是x坐标，第三个数字是y坐标，第四个数字是速度
# theta的单位为弧度，其余数字的长度单位均为cm
