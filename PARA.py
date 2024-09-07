import numpy as np

# 螺线求解在某点前距离该点一定弧长的点搜索宽度
POINT_BEFORE_CURVE_SEARCH_WIDTH = np.pi
# 问题1-2绘图时螺线的圈数
Q12_SPIRAL_PLOT_LOOP = 22
# 问题1-2绘图时螺线的点数
Q12_SPIRAL_PLOT_POINT_NUM = 5000
# 问题2判断哪些龙身可能与龙头相碰
Q2_JUDGE_BODY = 30
# 问题3模拟倒退的距离
Q3_START_THETA_REVERSE = 2 * np.pi
# 问题2判断哪些龙身可能与龙头相碰
Q3_JUDGE_BODY = 50