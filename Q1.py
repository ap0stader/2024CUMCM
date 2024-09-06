import matplotlib.pyplot as plt
import numpy as np
import os

from scipy.optimize import brentq, fsolve

# 模拟精度：1s
SIMULATION_ALL_STEP = 430

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
def solve_next_now_head_theta(last_theta):
    def equation(theta):
        return calc_curve_length(theta, last_theta) - STEP_HEAD_CURVE_LENGTH

    solution = brentq(equation, last_theta - np.pi, last_theta)
    return solution


# 求解龙头后第一节前把手的位置
def solve_next_bench_forehead_theta(bench_length, last_theta):
    last_theta_cos = last_theta * np.cos(last_theta)
    last_theta_sin = last_theta * np.sin(last_theta)
    right_constant = (bench_length ** 2) / (SPIRAL_B ** 2)

    def equation(theta):
        return ((theta * np.cos(theta) - last_theta_cos) ** 2
                + (theta * np.sin(theta) - last_theta_sin) ** 2
                - right_constant)

    guess = np.arccos((2 * spiral(last_theta) ** 2 - bench_length ** 2) / (2 * spiral(last_theta) ** 2))
    solution = fsolve(equation, x0=(last_theta + guess))
    return float(solution[0])


# 龙头位于螺线第16圈A点处
start_head_theta = 16 * 2 * np.pi

# 计算最多能走多少秒
all_curve_length = calc_curve_length(0, start_head_theta)
max_step = int(all_curve_length / STEP_HEAD_CURVE_LENGTH)
print("自开始点到坐标轴原点的弧长共 " + str(all_curve_length) + " cm")
print("仅考虑龙头前把手的运动，仅可运动 " + str(max_step) + " 秒")

# 确定起始的位置
now_head_theta = start_head_theta

spiral_plot_theta = np.linspace(0, 22 * 2 * np.pi, 5000)
spiral_plot_r = spiral(spiral_plot_theta)

# 实验结果是最多走
for step in range(SIMULATION_ALL_STEP + 1):  # 共需300s数据
    assert step < max_step
    print("正在计算第 " + str(step) + " 秒信息")
    # 绘制底图
    figure, ax = plt.subplots(figsize=(20, 20), layout="constrained", subplot_kw={"projection": "polar"})
    ax.spines['polar'].set_visible(False)
    ax.plot(spiral_plot_theta, spiral_plot_r, color="green", linewidth=1)
    # 龙头前把手的位置绘制
    print("当前龙头前把手的位置的θ=" + "{:.4f}".format(now_head_theta / (2 * np.pi)))
    ax.plot(now_head_theta, spiral(now_head_theta), 'x', color="red", markersize=20, markeredgewidth=2)
    ax.annotate("1", (now_head_theta, spiral(now_head_theta)),
                textcoords="offset fontsize", xytext=(1, 0), fontsize=18)
    # 龙头后第一节前把手的位置
    second_bench_forehead_theta = solve_next_bench_forehead_theta(FIRST_LENGTH, now_head_theta)
    ax.annotate("2", (second_bench_forehead_theta, spiral(second_bench_forehead_theta)),
                textcoords="offset fontsize", xytext=(1, 0), fontsize=18)
    first_segment = np.array([now_head_theta, second_bench_forehead_theta])
    ax.plot(first_segment, spiral(first_segment), '-', color="red", linewidth=5)

    # 后222节前把手位置
    last_bench_forehead_theta = second_bench_forehead_theta
    for bench in range(3, 225):  # 3 <= bench <= 224 第 224 号为最后一节的后把手
        new_bench_forehead_theta = solve_next_bench_forehead_theta(OTHER_LENGTH, last_bench_forehead_theta)
        ax.annotate(str(bench), (new_bench_forehead_theta, spiral(new_bench_forehead_theta)),
                    textcoords="offset fontsize", xytext=(1, 0), fontsize=18)
        new_segment = np.array([last_bench_forehead_theta, new_bench_forehead_theta])
        ax.plot(new_segment, spiral(new_segment), 'x-', color="blue", linewidth=5, markersize=20, markeredgewidth=2)
        last_bench_forehead_theta = new_bench_forehead_theta

    # 显示图片并保存
    figure.suptitle("Time " + str(step) + " second", fontsize=60, fontweight='bold')

    # figure.show()
    if step > 300:
        figure.savefig(RESULT_DIR + str(step) + ".png")
    plt.close(figure)

    now_head_theta = solve_next_now_head_theta(now_head_theta)
