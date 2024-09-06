import numpy as np
from matplotlib import pyplot as plt

from SPIRAL import ArchimedeanSpiral


def get_spiral_background(spiral: ArchimedeanSpiral, loop: int, point_num):
    spiral_plot_theta = np.linspace(0, loop * 2 * np.pi, point_num)
    spiral_plot_r = spiral.p(spiral_plot_theta)

    figure, ax = plt.subplots(figsize=(20, 21), layout="constrained", subplot_kw={"projection": "polar"})
    ax.spines['polar'].set_visible(False)
    ax.plot(spiral_plot_theta, spiral_plot_r, color="green", linewidth=1)

    return figure, ax
