import numpy as np
from matplotlib import pyplot as plt

from SPIRAL import ArchimedeanSpiral


# 获取螺线绘图背景
def get_spiral_background(spiral: ArchimedeanSpiral, loop: int, point_num):
    spiral_plot_theta = np.linspace(0, loop * 2 * np.pi, point_num)
    spiral_plot_r = spiral.p(spiral_plot_theta)

    figure, ax = plt.subplots(figsize=(20, 21), layout="constrained", subplot_kw={"projection": "polar"})
    ax.spines['polar'].set_visible(False)
    ax.plot(spiral_plot_theta, spiral_plot_r, color="green", linewidth=1)

    return figure, ax


# 根据切线和板凳的夹角计算速度
def calc_speed(spiral, last_speed, last_theta, next_theta):
    bench_slope = (spiral.y(next_theta) - spiral.y(last_theta)) / (spiral.x(next_theta) - spiral.x(last_theta))
    last_theta_tangent_slope = spiral.tangent_slope(last_theta)
    next_theta_tangent_slope = spiral.tangent_slope(next_theta)
    last_bench_angle = np.arctan(np.abs((last_theta_tangent_slope - bench_slope)
                                        / (1 + last_theta_tangent_slope * bench_slope)))
    next_bench_angle = np.arctan(np.abs((next_theta_tangent_slope - bench_slope)
                                        / (1 + next_theta_tangent_slope * bench_slope)))
    next_speed = (last_speed * np.cos(last_bench_angle)) / np.cos(next_bench_angle)
    return next_speed
