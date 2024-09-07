from enum import Enum, unique

import numpy as np
from matplotlib import pyplot as plt

import CONST
import PARA
from SHAPE import ArchimedeanSpiral, ArchimedeanSpiralReverse, Round, Shape
from UTIL import xy2polar

# 详见GeoGebra文件ggb
alpha = CONST.Q45_RADIUS_RATIO

theta_A = (CONST.Q345_TURNAROUND_RADIUS /
           (CONST.Q45_SPIRAL_DISTANCE / (2 * np.pi)))
theta_B = theta_A

x_A = CONST.Q345_TURNAROUND_RADIUS * np.cos(theta_A)
y_A = CONST.Q345_TURNAROUND_RADIUS * np.sin(theta_A)
A = [x_A, y_A]
x_B = -x_A
y_B = -y_A
B = [x_B, y_B]

k_A = ((np.sin(theta_A) + theta_A * np.cos(theta_A))
       / (np.cos(theta_A) - theta_A * np.sin(theta_A)))

delta_x = ((x_A ** 2 + y_A ** 2) /
           ((1 + alpha) * ((y_A / k_A) - x_A)))

x_C1 = x_A + delta_x
y_C1 = y_A - (delta_x / k_A)
C1 = [x_C1, y_C1]

x_C2 = -x_A - alpha * delta_x
y_C2 = -y_A + ((alpha * delta_x) / k_A)
C2 = [x_C2, y_C2]

x_T = (2 / 3) * x_C2 + (1 / 3) * x_C1
y_T = (2 / 3) * y_C2 + (1 / 3) * y_C1
T = [x_T, y_T]

r_C1 = np.sqrt(1 + (1 / k_A ** 2)) * delta_x
r_C2 = alpha * r_C1

theta_C1_start = np.pi + np.arctan((y_C1 - y_A) / (x_C1 - x_A))  # 约4.00，230度
theta_C1_end = np.arctan((y_C2 - y_C1) / (x_C2 - x_C1))  # 约0.98，56度
theta_C2_start = -(np.pi - theta_C1_end)  # 约-2.15，-123度
theta_C2_end = np.arctan((y_B - y_C2) / (x_B - x_C2))  # 约0.86，49度

# 创建螺线
spiral_in = ArchimedeanSpiral(CONST.Q45_SPIRAL_DISTANCE)
spiral_out = ArchimedeanSpiralReverse(CONST.Q45_SPIRAL_DISTANCE)

# 创建圆
round_in = Round(x_C1, y_C1, r_C1)
round_out = Round(x_C2, y_C2, r_C2)


# theta的类型
@unique
class ThetaType(Enum):
    SPIRAL_IN = 0
    ROUND_IN = 1
    ROUND_OUT = 2
    SPIRAL_OUT = 3


# 根据theta类型获取对应图形
def get_shape(theta: [ThetaType, any]) -> Shape:
    match theta[0]:
        case ThetaType.SPIRAL_IN:
            return spiral_in
        case ThetaType.ROUND_IN:
            return round_in
        case ThetaType.ROUND_OUT:
            return round_out
        case ThetaType.SPIRAL_OUT:
            return spiral_out


# 根据theta类型获取对应直角坐标系的坐标
# 可以批量计算
def theta2x(theta: [ThetaType, any]):
    return get_shape(theta).x(theta[1])


def theta2y(theta: [ThetaType, any]):
    return get_shape(theta).y(theta[1])


# 获取绘图背景
def get_figure_background():
    figure, ax = plt.subplots(figsize=(20, 21), layout="constrained", subplot_kw={"projection": "polar"})
    ax.spines['polar'].set_visible(False)

    spiral_plot_theta = np.linspace(theta_A, theta_A + PARA.Q4_SPIRAL_PLOT_LOOP * 2 * np.pi,
                                    PARA.Q4_SPIRAL_PLOT_POINT_NUM)
    spiral_in_plot_p = spiral_in.p(spiral_plot_theta)
    spiral_out_plot_p = np.abs(spiral_out.p(spiral_plot_theta))

    ax.plot(spiral_plot_theta, spiral_in_plot_p, color="orange", linewidth=1)
    ax.plot(spiral_plot_theta + np.pi, spiral_out_plot_p, color="purple", linewidth=1)

    round_in_theta = np.linspace(theta_C1_start, theta_C1_end, PARA.Q4_SPIRAL_PLOT_ROUND_IN_NUM)
    round_in_global_theta, round_in_global_p = xy2polar(round_in.x(round_in_theta), round_in.y(round_in_theta))
    round_out_theta = np.linspace(theta_C2_start, theta_C2_end, PARA.Q4_SPIRAL_PLOT_ROUND_OUT_NUM)
    round_out_global_theta, round_out_global_p = xy2polar(round_out.x(round_out_theta), round_out.y(round_out_theta))

    ax.plot(round_in_global_theta, round_in_global_p, color="green", linewidth=1)
    ax.plot(round_out_global_theta, round_out_global_p, color="blue", linewidth=1)

    return figure, ax


# 计算龙头的下一个位置
def calc_next_head_theta(last_head_theta: [ThetaType, any], head_step_curve_length):
    match last_head_theta[0]:
        case ThetaType.ROUND_IN:
            next_round_in = last_head_theta[1] - round_in.curve_theta(head_step_curve_length)
            # 判断是否仍然在round_in上
            if next_round_in >= theta_C1_end:
                return [ThetaType.ROUND_IN, next_round_in]
            else:
                # 在round_out上
                remain_curve_length = head_step_curve_length - round_in.curve_length(theta_C1_end, last_head_theta[1])
                next_round_out = theta_C2_start + round_out.curve_theta(remain_curve_length)
                # 认为速度不可能大到一下子跨越round_out
                assert next_round_out <= theta_C2_end
                return [ThetaType.ROUND_OUT, next_round_out]
        case ThetaType.ROUND_OUT:
            next_round_out = last_head_theta[1] + round_out.curve_theta(head_step_curve_length)
            # 判断是否仍然在round_out上
            if next_round_out <= theta_C2_end:
                return [ThetaType.ROUND_OUT, next_round_out]
            else:
                # 在round_in上
                remain_curve_length = head_step_curve_length - round_out.curve_length(theta_C2_end, last_head_theta[1])
                next_spiral_out = spiral_out.point_before_curve(theta_B, remain_curve_length)
                return [ThetaType.SPIRAL_OUT, next_spiral_out]
        case ThetaType.SPIRAL_OUT:
            next_spiral_out = spiral_out.point_before_curve(last_head_theta[1], head_step_curve_length)
            return [ThetaType.SPIRAL_OUT, next_spiral_out]
        case _:
            raise Exception("ThetaType " + str(last_head_theta[0]) + " not supported")
