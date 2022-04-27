import pandas as pd
import os, sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp2d
import scipy.integrate as integrate
import matplotlib.gridspec as gridspec
from matplotlib import cm

dataFrame = pd.DataFrame({"Points:0": [0, 0, 0, 0, 0, 0, 0, 0, 0,
                                       1, 1, 1, 1, 1, 1, 1, 1, 1,
                                       2, 2, 2, 2, 2, 2, 2, 2, 2],
                           "Points:1": [3, 4, 5, 3, 4, 5, 3, 4, 5,
                                        3, 4, 5, 3, 4, 5, 3, 4, 5,
                                        3, 4, 5, 3, 4, 5, 3, 4, 5],
                           "Points:2": [6, 6, 6, 7, 7, 7, 8, 8, 8,
                                        6, 6, 6, 7, 7, 7, 8, 8, 8,
                                        6, 6, 6, 7, 7, 7, 8, 8, 8],
                   "U:0": [12, 12, 12, 12, 12, 12, 12, 12, 12,
                                       15, 15, 15, 15, 15, 15, 15, 15, 15,
                                        14, 14, 14, 14, 14, 14, 14, 14, 14]})

test5 = pd.pivot_table(dataFrame, values=['U:0'], columns=['Points:2'], index=['Points:0', 'Points:1'])
test5.columns.levels # Вывести уровни коллонок
test5.index.levels[0].values

x = test5.index.levels[0].values
y = test5.index.levels[1].values
z = test5['U:0'].columns.values
data = {}

for xi in x:
    data[xi] = test5['U:0'].xs(xi, level="Points:0").values

name = 'data/test.csv'
dataEOF = pd.read_csv(name)
dataEOF = pd.pivot_table(dataEOF, values=['U:0'], columns=['Points:2'], index=['Points:0', 'Points:1']).dropna()

xnew= dataEOF.index.levels[0].values
ynew = {}
znew = {}
dataNew = {}
for xi in xnew:
    dataNew[xi] = dataEOF['U:0'].xs(xi, level="Points:0").values
    ynew[xi] = dataEOF['U:0'].xs(xi, level="Points:0").axes[0].values
    znew[xi] = dataEOF['U:0'].xs(xi, level="Points:0").axes[1].values


figsurfcase1 = plt.figure(constrained_layout=True, figsize=(8, 4))
spec1 = gridspec.GridSpec(ncols=2, nrows=1, figure=figsurfcase1)

f1_ax1 = figsurfcase1.add_subplot(spec1[0, 0])
c1 = f1_ax1.contourf(znew[xnew[0]], ynew[xnew[0]], dataNew[xnew[0]], 15)
cs1 = f1_ax1.contour(znew[xnew[0]], ynew[xnew[0]], dataNew[xnew[0]], 5, colors='black')
f1_ax1.clabel(cs1, inline=True, fontsize=14)

f1_ax2 = figsurfcase1.add_subplot(spec1[0, 1])
c2 = f1_ax2.contourf(znew[xnew[-1]], ynew[xnew[-1]], dataNew[xnew[-1]], 15)
cs2 = f1_ax2.contour(znew[xnew[-1]], ynew[xnew[-1]], dataNew[xnew[-1]], 5, colors='black')
f1_ax2.clabel(cs2, inline=True, fontsize=14)

fig3Dsurfcase1 = plt.figure(constrained_layout=True, figsize=(16, 10))
spec2 = gridspec.GridSpec(ncols=2, nrows=1, figure=figsurfcase1)
ax1 = fig3Dsurfcase1.add_subplot(spec2[0, 0], projection="3d")
ZZ1, YY1 = np.meshgrid(znew[xnew[0]], ynew[xnew[0]])
surf = ax1.plot_surface(ZZ1, YY1, dataNew[xnew[0]], cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

ax2 = fig3Dsurfcase1.add_subplot(spec2[0, 1], projection="3d")
ZZ2, YY2 = np.meshgrid(znew[xnew[-1]], ynew[xnew[-1]])
surf = ax2.plot_surface(ZZ2, YY2, dataNew[xnew[-1]], cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

surfaceIntegral = {}
for xi in xnew:
    surfaceIntegral[xi] = integrate.simps(integrate.simps(dataNew[xi], znew[xi]), ynew[xi])
integrate.simps(integrate.simps(dataNew[xnew[-1]], znew[xnew[-1]]), ynew[xnew[-1]])