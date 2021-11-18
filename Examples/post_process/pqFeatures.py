import os
from PostProcessClass import PostProcess
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import cm

name_file2 = 'pressureData.csv'
dataDir = os.path.join(os.getcwd(), 'data')

pp = PostProcess()
pp.load_scv_file(name_file2, dir=dataDir,  key='pressureData')
pp.load_scv_file(name_file2, dir=dataDir,  key='pressureData2')
varNames = list(pp.data['pressureData'].columns)
pp.rebuildDataRun2('pressureData', data=None, values=['p'], generalAxis='Points:0',
                        surfaceAxis=['Points:2', 'Points:1'], methodFill='interpolate')
pp.rebuildDataRun2('pressureData2', data=None, values=['p'], generalAxis='Points:2',
                        surfaceAxis=['Points:1', 'Points:0'], methodFill='interpolate')

i = pp.gFindIndexByNearestValue('pressureData', 0.300)

pp.surfaceIntegral('pressureData2', variable='p', generalNumber=0)
pp.lineIntegral('pressureData2', variable='p', integAxis='sAxis2', valueAxis=0.1, gVal=0)

gAxis = pp.newData['pressureData2']['gAxis'][0]
sAxis1 = pp.newData['pressureData2']['sAxis1'][gAxis]
sAxis2 = pp.newData['pressureData2']['sAxis2'][gAxis]
data = pp.newData['pressureData2']['p'][gAxis]

figSurface1 = plt.figure(constrained_layout=True, figsize=(12, 4))
spec1 = gridspec.GridSpec(ncols=1, nrows=3, figure=figSurface1)
figSurface1_ax1 = figSurface1.add_subplot(spec1[0, 0])
c1 = figSurface1_ax1.contourf(sAxis1, sAxis2, data, 100)
cs1 = figSurface1_ax1.contour(sAxis1, sAxis2, data, 5, colors='black', linewidths=0.3)
figSurface1_ax1.clabel(cs1, inline=True, fontsize=8)
figSurface1.colorbar(c1)