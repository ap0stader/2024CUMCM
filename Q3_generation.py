import os
import pickle

from shapely import Point, Polygon

import CONST
import PARA
import Q2
from SHAPE import ArchimedeanSpiral

# 创建结果保存目录
RESULT_DIR = CONST.RESULT_ROOT + "Q3_generation/"
os.makedirs(RESULT_DIR, exist_ok=True)

# 精细模拟，一秒钟均分成几份
SEC_DIVISION = 50
# 精细模拟，每一轮螺距减少多少厘米
STEP_SPIRAL_DISTANCE = 0.1

# 每一模拟步龙头前把手行进的弧长
HEAD_STEP_CURVE_LENGTH = CONST.DEFAULT_HEAD_SPEED / SEC_DIVISION

# 开始尝试的螺距
spiral_distance = 50

# 停止尝试的螺距
end_spiral_distance = 10

# 数据存储
data = list()

while spiral_distance >= end_spiral_distance:
    print("正在计算螺距为 " + "{:.2f}".format(spiral_distance) + " 厘米信息")
    # 创建螺线
    spiral = ArchimedeanSpiral(spiral_distance)
    # 确定起始的位置
    head_theta = spiral.theta(CONST.Q345_TURNAROUND_RADIUS) + PARA.Q3_START_THETA_REVERSE
    print("初始龙头前把手距离螺线中心 " + "{:.2f}".format(spiral.p(head_theta)) + " 厘米")
    # 龙头停止的位置
    end_head_theta = spiral.theta(CONST.Q345_TURNAROUND_RADIUS)
    # 模拟后是否发生碰撞
    collision_flag = False
    while head_theta >= end_head_theta:
        # 求解第一节龙身前把手的位置和速度
        first_body_theta = spiral.point_after_chord(head_theta, CONST.HEAD_BENCH_LEN)
        # 获取龙头的板凳的边框
        c_points, _ = Q2.get_four_corner_point(spiral, CONST.HEAD_BENCH_LEN, head_theta, first_body_theta)
        # 保存龙头前端尖锐点
        head_head_sharp_point = Point(c_points[0])
        # 保存龙头后端尖锐点
        head_tail_sharp_point = Point(c_points[3])

        # 第2节龙身前把手至第222节龙身前把手的位置和速度
        last_body_theta = first_body_theta
        for ben in range(2, CONST.BODY_TAIL_COUNT + 1):
            # 求解下一节龙身前把手的位置和速度
            next_body_theta = spiral.point_after_chord(last_body_theta, CONST.OTHER_BENCH_LEN)
            # 获取龙身的板凳的边框
            c_points, _ = Q2.get_four_corner_point(spiral, CONST.OTHER_BENCH_LEN, last_body_theta, next_body_theta)
            # 只判断有可能发生碰撞的板凳
            if ben <= PARA.Q3_JUDGE_BODY:
                judge_polygon = Polygon(c_points)
                if judge_polygon.contains(head_head_sharp_point):
                    print("在螺距为 " + "{:.2f}".format(spiral_distance) + " 厘米，龙头前把手距离螺距中心 " +
                          "{:.2f}".format(spiral.p(head_theta)) + " 厘米时龙头前方发生碰撞，" +
                          "发生碰撞的龙身是第 " + str(ben) + " 块")
                    collision_flag = True
                if judge_polygon.contains(head_tail_sharp_point):
                    print("在螺距为 " + "{:.2f}".format(spiral_distance) + " 厘米，龙头前把手距离螺距中心 " +
                          "{:.2f}".format(spiral.p(head_theta)) + " 厘米时龙头后方发生碰撞，" +
                          "发生碰撞的龙身是第 " + str(ben) + " 块")
                    collision_flag = True
            # 迭代
            last_body_theta = next_body_theta

        # 求解龙头前把手新的位置
        head_theta = spiral.point_before_curve(head_theta, HEAD_STEP_CURVE_LENGTH)

        # 发生了碰撞，终止本轮模拟
        if collision_flag:
            break

    # 输出并记录数据
    data_record = [spiral_distance, collision_flag, end_head_theta, head_theta, spiral.p(head_theta)]
    print("记录情况：" + str(data_record))
    data.append(data_record)
    # 清除螺线
    del spiral

    # 迭代
    spiral_distance -= STEP_SPIRAL_DISTANCE

# 数据解读方法
# 第一维为数据索引
# 第二维第一个数据是螺距，单位为厘米，第二个数据是是否发生碰撞
# 第三个数据是掉头区域边界与螺线的交点对应的theta
# 第四个数据和第五个数据分别时是结束模拟时龙头所在位置的theta和p

with open(RESULT_DIR + 'data.pkl', 'wb') as f:
    pickle.dump(data, f)
