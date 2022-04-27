import pandas as pd
import scipy.integrate as integrate


name = 'data/test.csv'
dataEOF = pd.read_csv(name)
dataEOF = pd.pivot_table(dataEOF, values=['U:0'], columns=['Points:2'], index=['Points:0', 'Points:1']).dropna()

xnew= dataEOF.index.levels[0].values
ynew = {}
znew = {}
dataNew = {}
surfaceIntegral = {}
for xi in xnew:
    dataNew[xi] = dataEOF['U:0'].xs(xi, level="Points:0").values
    ynew[xi] = dataEOF['U:0'].xs(xi, level="Points:0").axes[0].values
    znew[xi] = dataEOF['U:0'].xs(xi, level="Points:0").axes[1].values

for xi in xnew:
    surfaceIntegral[xi] = integrate.simps(integrate.simps(dataNew[xi], znew[xi]), ynew[xi])

lineData = integrate.simps(integrate.simps(dataNew[xnew[-1]], znew[xnew[-1]]), ynew[xnew[-1]])
