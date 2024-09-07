import pickle

import numpy as np
import os

import CONST
from SPIRAL import ArchimedeanSpiral
from UTIL import calc_speed

# 创建结果保存目录
RESULT_DIR = CONST.RESULT_ROOT + "Q1_generation/"
os.makedirs(RESULT_DIR, exist_ok=True)

# 创建螺线
spiral = ArchimedeanSpiral(CONST.Q12_SPIRAL_DISTANCE)

# 模拟精度：1秒
SIM_SECOND = 300
assert SIM_SECOND <= CONST.Q12_MAX_SIM_SECOND

# 每一秒龙头前把手行进的弧长
HEAD_SECOND_CURVE_LENGTH = CONST.DEFAULT_HEAD_SPEED

# 确定起始的位置
head_theta = CONST.Q12_HEAD_START_THETA

# 数据存储
data = list()


def store_point(index, theta, speed):
    data[index].append([theta, spiral.x(theta), spiral.y(theta), speed])


# 共需300秒数据
for sec in range(SIM_SECOND + 1):
    # 因为从0秒开始模拟，故second就是数组下标
    data.append(list())
    print("正在计算第 " + str(sec) + " 秒信息")
    print("当前龙头前把手的位置为θ=" + "{:.4f}".format(head_theta / (2 * np.pi)) + "x2π")
    # 存储龙头前把手的信息
    store_point(sec, head_theta, CONST.DEFAULT_HEAD_SPEED)
    # 求解第一节龙身前把手的位置和速度
    first_body_theta = spiral.point_after_chord(head_theta, CONST.HEAD_BENCH_LEN)
    first_body_speed = calc_speed(spiral, CONST.DEFAULT_HEAD_SPEED, head_theta, first_body_theta)
    # 存储第一节龙身前把手的信息
    store_point(sec, first_body_theta, first_body_speed)

    # 第2节龙身前把手至第222节龙身前把手的位置和速度
    last_body_theta = first_body_theta
    last_body_speed = first_body_speed
    for ben in range(2, CONST.BODY_TAIL_COUNT + 1):
        # 求解下一节龙身前把手的位置和速度
        next_body_theta = spiral.point_after_chord(last_body_theta, CONST.OTHER_BENCH_LEN)
        next_body_speed = calc_speed(spiral, last_body_speed, last_body_theta, next_body_theta)
        # 存储这一节龙身前把手的信息
        store_point(sec, next_body_theta, next_body_speed)
        # 迭代
        last_body_theta = next_body_theta
        last_body_speed = next_body_speed

    # 求解龙头前把手新的位置
    head_theta = spiral.point_before_curve(head_theta, HEAD_SECOND_CURVE_LENGTH)

    print(np.shape(data[sec]))
    print("第一个点的情况：" + str(data[sec][0]))
    print("最后一个点的情况：" + str(data[sec][223]))

# 数据解读方法
# 第一维为模拟时间
# 第二维为把手，0表示龙头前把手，1-222表示221节龙身+1节龙尾前把手，223表示龙尾后把手
# 第三维，第一个数字是theta，第二个数字是x坐标，第三个数字是y坐标，第四个数字是速度
# theta的单位为弧度，其余数字的长度单位均为cm

with open(RESULT_DIR + 'data.pkl', 'wb') as f:
    pickle.dump(data, f)
