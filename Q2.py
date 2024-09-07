import CONST
from SHAPE import ArchimedeanSpiral
from UTIL import xy2polar

# 中心距离最近的板头的距离和宽度的对角线的长度的平方
PADDING_WIDTH_DIAGONAL_SQUARE = CONST.ALL_PADDING_HALF ** 2 + CONST.ALL_WIDTH_HALF ** 2


# 根据两个把手中心点的位置计算板凳四个角的坐标位置
def get_four_corner_point(spiral: ArchimedeanSpiral, bench_length, last_theta, next_theta):
    # 计算四个顶点
    last_x = spiral.x(last_theta)
    last_y = spiral.y(last_theta)
    next_x = spiral.x(next_theta)
    next_y = spiral.y(next_theta)
    # 上一节龙身前把手前方左侧点的配置
    vertical_x = (CONST.ALL_PADDING_HALF / bench_length) * (next_x - last_x)
    vertical_y = (CONST.ALL_PADDING_HALF / bench_length) * (next_y - last_y)
    horizontal_x = -(CONST.ALL_WIDTH_HALF / bench_length) * (next_y - last_y)
    horizontal_y = (CONST.ALL_WIDTH_HALF / bench_length) * (next_x - last_x)
    # 前方左侧点
    last_sharp_x = last_x - vertical_x - horizontal_x
    last_sharp_y = last_y - vertical_y - horizontal_y
    # 前方又侧点
    last_dull_x = last_x - vertical_x + horizontal_x
    last_dull_y = last_y - vertical_y + horizontal_y
    # 后方又侧点
    next_dull_x = next_x + vertical_x + horizontal_x
    next_dull_y = next_y + vertical_y + horizontal_y
    # 后方又侧点
    next_sharp_x = next_x + vertical_x - horizontal_x
    next_sharp_y = next_y + vertical_y - horizontal_y

    c_point = [(last_sharp_x, last_sharp_y), (last_dull_x, last_dull_y),
               (next_dull_x, next_dull_y), (next_sharp_x, next_sharp_y)]

    p_point = [xy2polar(x, y) for x, y in c_point]

    return c_point, p_point
