import pandas as pd
import os, sys
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

surfaceIntegral = {}
for xi in xnew:
    surfaceIntegral[xi] = integrate.simps(integrate.simps(dataNew[xi], znew[xi]), ynew[xi])
integrate.simps(integrate.simps(dataNew[xnew[-1]], znew[xnew[-1]]), ynew[xnew[-1]])