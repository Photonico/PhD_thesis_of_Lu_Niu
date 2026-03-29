#### single frame
# pylint: disable = C0103, C0114, C0116, C0301, C0321, R0913, R0914

# import numpy as np
import matplotlib.pyplot as plt

# from pathlib import Path
from mpl_toolkits.axisartist.axislines import AxesZero

## personal settings
label = 14
params = {"text.usetex": False,
          "font.family": "serif",
          "mathtext.fontset": "cm",
          "axes.titlesize": 16,
          "axes.labelsize": label,
          "figure.facecolor": "w"}
plt.rcParams.update(params)
fig = plt.figure(figsize=(4.0, 4.0), dpi=1024)
# fig.suptitle("Kohn--Sham construction", fontsize=16)

## one AxesZero
ax = fig.add_subplot(1, 1, 1, axes_class=AxesZero)
for d in ("xzero", "yzero"):
    ax.axis[d].set_axisline_style("-|>")
    ax.axis[d].set_visible(True)
for d in ("left", "right", "bottom", "top"):
    ax.axis[d].set_visible(False)
ax.set(xlim=(-1, 1), ylim=(-1, 1), xticks=[], yticks=[])

## schematic curves
