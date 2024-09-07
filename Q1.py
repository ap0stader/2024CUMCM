import numpy as np
from matplotlib import pyplot as plt

import PARA
from SHAPE import ArchimedeanSpiral


# 获取螺线绘图背景
def get_spiral_background(spiral: ArchimedeanSpiral):
    figure, ax = plt.subplots(figsize=(20, 21), layout="constrained", subplot_kw={"projection": "polar"})
    ax.spines['polar'].set_visible(False)

    spiral_plot_theta = np.linspace(0, PARA.Q12_SPIRAL_PLOT_LOOP * 2 * np.pi, PARA.Q12_SPIRAL_PLOT_POINT_NUM)
    spiral_plot_p = spiral.p(spiral_plot_theta)

    ax.plot(spiral_plot_theta, spiral_plot_p, color="green", linewidth=1)

    return figure, ax
