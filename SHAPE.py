from abc import ABC, abstractmethod

import numpy as np
from scipy.optimize import brentq, fsolve

import CONST
import PARA


class Shape(ABC):
    @abstractmethod
    def x(self, theta):
        pass

    def y(self, theta):
        pass


# 盘入螺线
class ArchimedeanSpiral(Shape):
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


# 盘出螺线
class ArchimedeanSpiralReverse(ArchimedeanSpiral):
    # p < 0 时，表示的点在极角为θ的射线的反向延长线上
    # 极径：p = -bθ
    def p(self, theta):
        return -(self.b * theta)

    # 极角：θ = -p/b
    def theta(self, p):
        return -(p / self.b)

    # 求解在某点前距离该点一定弧长的点
    def point_before_curve(self, known_theta, curve_length, search_width=PARA.POINT_BEFORE_CURVE_SEARCH_WIDTH):
        def equation(theta):
            return self.curve_length(theta, known_theta) - curve_length

        return brentq(equation, known_theta, known_theta + search_width)

    # 求解在某点后距离该点一定弦长的点
    # 用于已知板凳前把手求解板凳后把手（下一个板凳前把手）的θ
    def point_after_chord(self, known_theta, chord_length):
        def equation(theta):
            return ((theta * np.cos(theta) - known_theta * np.cos(known_theta)) ** 2
                    + (theta * np.sin(theta) - known_theta * np.sin(known_theta)) ** 2
                    - ((chord_length ** 2) / (self.b ** 2)))

        guess = np.arccos((2 * self.p(known_theta) ** 2 - chord_length ** 2) / (2 * self.p(known_theta) ** 2))
        solution = fsolve(equation, x0=(known_theta - guess))
        return float(solution[0])


# 掉头路径圆
class Round(Shape):
    x_C = 0.0
    y_C = 0.0
    r = 0.0

    def __init__(self, x_C, y_C, r):
        self.x_C = x_C
        self.y_C = y_C
        self.r = r

    # x坐标：x = x_C + rcosθ
    def x(self, theta):
        return self.x_C + self.r * np.cos(theta)

    # y坐标：y = y_C + ycosθ
    def y(self, theta):
        return self.y_C + self.r * np.sin(theta)

    # 弧长：θ1到θ2的弧长
    def curve_length(self, theta1, theta2):
        return self.r * np.abs(theta2 - theta1)

    # 弦长：θ1到θ2的弧长
    def chord_length(self, theta1, theta2):
        return np.sqrt(2 * self.r ** 2 * (1 - np.cos(np.abs(theta2 - theta1))))

    # 弧长对应的圆心角
    def curve_theta(self, curve_length):
        return curve_length / self.r

    # 计算螺线上某一点的切线的斜率
    def tangent_slope(self, theta):
        return -(1 / np.tan(theta))
