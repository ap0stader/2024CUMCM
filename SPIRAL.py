# 阿基米德螺线类
import numpy as np
from scipy.optimize import brentq, fsolve

import CONST
import PARA


class ArchimedeanSpiral:
    b = CONST.Q12_SPIRAL_DISTANCE / (2 * np.pi)

    def __init__(self, spiral_distance):
        self.b = spiral_distance / (2 * np.pi)

    # 极径：p = bθ
    def p(self, theta):
        return self.b * theta

    # 极角：θ = p/b
    def theta(self, p):
        return p / self.b

    # 转换为x坐标：x = pcosθ
    def x(self, theta):
        return self.p(theta) * np.cos(theta)

    # 转换为y坐标：y = psinθ
    def y(self, theta):
        return self.p(theta) * np.sin(theta)

    # 弧长：θ1到θ2的弧长
    def curve_length(self, theta1, theta2):
        def curve_summa(theta):
            return (self.b / 2) * (theta * np.sqrt(1 + theta ** 2) + np.log(theta + np.sqrt(1 + theta ** 2)))

        return np.abs(curve_summa(theta2) - curve_summa(theta1))

    # 求解在某点前距离该点一定弧长的点
    # 用于求解龙头前把手的位置在当前位置前进一秒后的θ
    def point_before_curve(self, known_theta, curve_length, search_width=PARA.POINT_BEFORE_CURVE_SEARCH_WIDTH):
        def equation(theta):
            return self.curve_length(theta, known_theta) - curve_length

        return brentq(equation, known_theta - search_width, known_theta)

    # 求解在某点后距离该点一定弦长的点
    # 用于已知板凳前把手求解板凳后把手（下一个板凳前把手）的θ
    def point_after_chord(self, known_theta, chord_length):
        def equation(theta):
            return ((theta * np.cos(theta) - known_theta * np.cos(known_theta)) ** 2
                    + (theta * np.sin(theta) - known_theta * np.sin(known_theta)) ** 2
                    - ((chord_length ** 2) / (self.b ** 2)))

        guess = np.arccos((2 * self.p(known_theta) ** 2 - chord_length ** 2) / (2 * self.p(known_theta) ** 2))
        solution = fsolve(equation, x0=(known_theta + guess))
        return float(solution[0])

    # 计算螺线上某一点的切线的斜率
    def tangent_slope(self, theta):
        return (np.sin(theta) + theta * np.cos(theta)) / (np.cos(theta) - theta * np.sin(theta))
