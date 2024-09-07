import pickle

import numpy as np
import os

from shapely.geometry import Point, Polygon

import CONST

import PARA
import Q2
from SHAPE import ArchimedeanSpiral
from UTIL import calc_speed

# 创建结果保存目录
RESULT_DIR = CONST.RESULT_ROOT + "Q2_generation/"
os.makedirs(RESULT_DIR, exist_ok=True)

# 创建螺线
spiral = ArchimedeanSpiral(CONST.Q12_SPIRAL_DISTANCE)

# 精细模拟，一秒钟均分成几份
SEC_DIVISION = 50
# 模拟的秒数
SIM_SECOND = 430
# 模拟的轮数
SIM_STEP = SIM_SECOND * SEC_DIVISION
# 跳过的秒数
SKIP_SECOND = 400
# 跳过的轮数
SKIP_STEP = SKIP_SECOND * SEC_DIVISION
# 开始绘图的轮数
START_FIGURE_STEP = 410 * SEC_DIVISION

# 每一模拟步龙头前把手行进的弧长
HEAD_STEP_CURVE_LENGTH = CONST.DEFAULT_HEAD_SPEED / SEC_DIVISION

# 确定起始的位置
head_theta = CONST.Q12_HEAD_START_THETA
# 跳过轮数
for step in range(SKIP_STEP):
    head_theta = spiral.point_before_curve(head_theta, HEAD_STEP_CURVE_LENGTH)

# 数据存储
data = list()


def store_point(index, theta, speed):
    data[index].append([theta, spiral.x(theta), spiral.y(theta), speed])


# 如果已经发生了碰撞，则停止模拟
sim_finish_flag = False
# 记录数据为412.48秒出现碰撞
for step in range(SKIP_STEP, SIM_STEP + 1):
    # step不一定从0开始，step SKIP_STEP才是数组下标
    data.append(list())
    array_index = step - SKIP_STEP
    print("正在计算第 " + "{:.4f}".format(step / SEC_DIVISION) + " 秒信息")
    print("当前龙头前把手的位置为θ=" + "{:.4f}".format(head_theta / (2 * np.pi)) + "x2π")
    # 存储龙头前把手的信息
    store_point(array_index, head_theta, CONST.DEFAULT_HEAD_SPEED)
    # 求解第一节龙身前把手的位置和速度
    first_body_theta = spiral.point_after_chord(head_theta, CONST.HEAD_BENCH_LEN)
    first_body_speed = calc_speed(spiral, CONST.DEFAULT_HEAD_SPEED, head_theta, spiral, first_body_theta)
    # 存储第一节龙身前把手的信息
    store_point(array_index, first_body_theta, first_body_speed)
    # 获取龙头的板凳的边框
    c_points, _ = Q2.get_four_corner_point(spiral, CONST.HEAD_BENCH_LEN, head_theta, first_body_theta)
    # 保存龙头前端尖锐点
    head_head_sharp_point = Point(c_points[0])
    # 保存龙头后端尖锐点
    head_tail_sharp_point = Point(c_points[3])

    # 第2节龙身前把手至第222节龙身前把手的位置和速度
    last_body_theta = first_body_theta
    last_body_speed = first_body_speed
    for ben in range(2, CONST.BODY_TAIL_COUNT + 1):
        # 求解下一节龙身前把手的位置和速度
        next_body_theta = spiral.point_after_chord(last_body_theta, CONST.OTHER_BENCH_LEN)
        next_body_speed = calc_speed(spiral, last_body_speed, last_body_theta, spiral, next_body_theta)
        # 存储这一节龙身前把手的信息
        store_point(array_index, next_body_theta, next_body_speed)
        # 获取龙身的板凳的边框
        c_points, _ = Q2.get_four_corner_point(spiral, CONST.OTHER_BENCH_LEN, last_body_theta, next_body_theta)
        # 只判断有可能发生碰撞的板凳
        if ben <= PARA.Q2_JUDGE_BODY:
            judge_polygon = Polygon(c_points)
            if judge_polygon.contains(head_head_sharp_point):
                print("在第 " + str(step) + " 步（" + "{:.4f}".format(step / SEC_DIVISION) +
                      "秒）龙头前方发生碰撞，发生碰撞的龙身是第 " + str(ben) + " 块")
                sim_finish_flag = True
            if judge_polygon.contains(head_tail_sharp_point):
                print("在第 " + str(step) + " 步（" + "{:.4f}".format(step / SEC_DIVISION) +
                      "秒）龙头后方发生碰撞，发生碰撞的龙身是第 " + str(ben) + " 块")
                sim_finish_flag = True
        # 迭代
        last_body_theta = next_body_theta
        last_body_speed = next_body_speed

    # 求解龙头前把手新的位置
    head_theta = spiral.point_before_curve(head_theta, HEAD_STEP_CURVE_LENGTH)

    print(np.shape(data[array_index]))
    print("第一个点的情况：" + str(data[array_index][0]))
    print("最后一个点的情况：" + str(data[array_index][223]))

    # 发生了碰撞，终止模拟
    if sim_finish_flag:
        break

# 数据解读方法
# 第一维为模拟步数，SKIP_STEP那一步下标为0
# 第二维为把手，0表示龙头前把手，1-222表示221节龙身+1节龙尾前把手，223表示龙尾后把手
# 第三维，第一个数字是theta，第二个数字是x坐标，第三个数字是y坐标，第四个数字是速度
# theta的单位为弧度，其余数字的长度单位均为cm

with open(RESULT_DIR + 'data.pkl', 'wb') as f:
    pickle.dump(data, f)
