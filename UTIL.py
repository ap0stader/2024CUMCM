import numpy as np

from SHAPE import ArchimedeanSpiral


# 将直角坐标系的坐标转换为全局极坐标
# 利用numpy的广播机制，可以进行批量的计算
def xy2polar(x, y):
    p = np.sqrt(x ** 2 + y ** 2)
    theta = np.arctan(y / x)
    return theta + np.pi + (x > 0) * np.pi, p


# 给点标记文字
def annotate_point(axis, number: int, theta, p):
    axis.annotate(str(number), (theta, p),
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
