import os
import pickle

import CONST
import Q4
from UTIL import calc_speed

# 创建结果保存目录
RESULT_DIR = CONST.RESULT_ROOT + "Q5_generation_forward/"
os.makedirs(RESULT_DIR, exist_ok=True)

# 精细模拟，一秒钟均分成几份
SEC_DIVISION = 100
# 模拟的秒数
SIM_SECOND = 30
# 模拟的轮数
SIM_STEP = SIM_SECOND * SEC_DIVISION
# 精细模拟，每一轮速度增加多少厘米
STEP_SPEED_INCREASE = 1

# 开始尝试的速度
head_speed = CONST.DEFAULT_HEAD_SPEED

# 结束尝试的速度
end_head_speed = CONST.Q5_MAX_HEAD_SPEED

# 数据存储
data = list()

while head_speed <= end_head_speed:
    print("正在计算龙头速度为 " + str(head_speed) + " 厘米每秒信息")
    # 每一秒龙头前把手行进的弧长
    head_step_curve_length = head_speed / SEC_DIVISION
    # 确定起始的位置
    head_theta = [Q4.ThetaType.ROUND_IN, Q4.theta_C1_start]
    # 初始化本轮最大速度
    max_speed = head_speed
    max_speed_bench = 0
    max_speed_step = 0
    for step in range(SIM_STEP + 1):
        if step % SEC_DIVISION == 0:
            print(str(step / SEC_DIVISION), end=" ", flush=True)
        # 求解第一节龙身前把手的位置
        first_body_theta = Q4.calc_next_handle_theta(head_theta, CONST.HEAD_BENCH_LEN)
        first_body_speed = calc_speed(Q4.get_shape(head_theta), CONST.DEFAULT_HEAD_SPEED, head_theta[1],
                                      Q4.get_shape(first_body_theta), first_body_theta[1])
        if first_body_speed > max_speed:
            max_speed = first_body_speed
            max_speed_bench = 1
            max_speed_step = step

        # 第2节龙身前把手至第222节龙身前把手的位置和速度
        last_body_theta = first_body_theta
        last_body_speed = first_body_speed
        for ben in range(2, CONST.BODY_TAIL_COUNT + 1):
            # 求解下一节龙身前把手的位置和速度
            next_body_theta = Q4.calc_next_handle_theta(last_body_theta, CONST.OTHER_BENCH_LEN)
            next_body_speed = calc_speed(Q4.get_shape(last_body_theta), last_body_speed, last_body_theta[1],
                                         Q4.get_shape(next_body_theta), next_body_theta[1])
            if next_body_speed > max_speed:
                max_speed = next_body_speed
                max_speed_bench = ben
                max_speed_step = step
            # 迭代
            last_body_theta = next_body_theta
            last_body_speed = next_body_speed

        # 求解龙头前把手新的位置
        head_theta = Q4.calc_next_head_theta(head_theta, head_step_curve_length)

    data_record = [head_speed, max_speed <= CONST.Q5_MAX_HEAD_SPEED, max_speed, max_speed_bench, max_speed_step]
    print("记录情况：" + str(data_record))
    data.append(data_record)

    if max_speed > CONST.Q5_MAX_HEAD_SPEED:
        print("已尝试到第一个不满足的龙头速度")
        break
    else:
        # 迭代
        head_speed += STEP_SPEED_INCREASE

# 数据解读方法
# 第一维为数据索引
# 第二维第一个数据是龙头的速度，单位为厘米每秒，第二个数据是是否满足各把手的速度均不超过2 m/s
# 第三个数据至第五个数据分别是各把手中的最大速度，把手编号（即绘制的图像上的编号），最大速度发生的模拟步骤

with open(RESULT_DIR + 'data.pkl', 'wb') as f:
    pickle.dump(data, f)
