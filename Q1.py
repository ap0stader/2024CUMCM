import matplotlib.pyplot as plt
import numpy as np
import os

from scipy.optimize import brentq

# 模拟精度：1s

# 创建题目结果目录
RESULT_DIR = "./result/Q1/"
os.makedirs("./result/", exist_ok=True)
os.makedirs("./result/Q1/", exist_ok=True)

# 阿基米德螺线方程：r = b * θ
# 阿基米德螺线参数
SPIRAL_B = 55 / (2 * np.pi)

# 来自题目的数据单位为厘米
PADDING_LENGTH = 55  # 27.5cm x 2
FIRST_LENGTH = 341 - PADDING_LENGTH
OTHER_LENGTH = 220 - PADDING_LENGTH
HEAD_SPEED = 100  # 1m/s

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
def solve_next_head(last_theta):
    def equation(theta):
        return calc_curve_length(theta, last_theta) - STEP_HEAD_CURVE_LENGTH

    solution = brentq(equation, last_theta - np.pi, last_theta)
    return solution

# 求解龙头后第一1节前把手的位置
# def solve_first(head_theta):
#
# def solve_other(last_theta):

# 龙头位于螺线第16圈A点处
start_theta = 16 * 2 * np.pi

# 计算最多能走多少秒
all_curve_length = calc_curve_length(0, start_theta)
max_step = int(all_curve_length / STEP_HEAD_CURVE_LENGTH)
print("自开始点到坐标轴原点的弧长共 " + str(all_curve_length) + " cm")
print("仅考虑龙头前把手的运动，仅可运动 " + str(max_step) + " 秒")

# 确定起始的位置
now_theta = start_theta

spiral_plot_theta = np.linspace(0, 16 * 2 * np.pi, 4000)
spiral_plot_r = spiral(spiral_plot_theta)

# 实验结果是最多走
for step in range(3 + 1):
    assert step < max_step
    print("正在计算第 " + str(step) + " 秒信息")
    # 绘制底图
    figure, ax = plt.subplots(figsize=(20, 20), subplot_kw={"projection": "polar"})
    ax.spines['polar'].set_visible(False)
    ax.plot(spiral_plot_theta, spiral_plot_r, color="black", linewidth=0.5)
    # 龙头前把手的位置绘制
    print("当前龙头前把手的位置的θ=" + "{:.4f}".format(now_theta / (2 * np.pi)))
    ax.plot(now_theta, spiral(now_theta), 'x', color="red", markersize=20, markeredgewidth=2)
    # 解决第一个块板的问题

    # 显示图片并保存
    figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
    figure.show()
    figure.savefig(RESULT_DIR + str(step) + ".png")

    now_theta = solve_next_head(now_theta)
