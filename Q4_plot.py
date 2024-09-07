import os

import CONST
from SHAPE import ArchimedeanSpiral, ArchimedeanSpiralReverse

# 创建结果保存目录
RESULT_DIR = CONST.RESULT_ROOT + "Q4_plot/"
os.makedirs(RESULT_DIR, exist_ok=True)

# 创建螺线
spiral_in = ArchimedeanSpiral(CONST.Q45_SPIRAL_DISTANCE)
spiral_out = ArchimedeanSpiralReverse(CONST.Q45_SPIRAL_DISTANCE)

