import os

from PostProcessClass import PostProcess
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

import scipy.ndimage
from matplotlib import cm
import pandas as pd
import math as ma

name_file1 = '2dCasetest.csv'
name_file2 = '2dCasetest2.csv'
name_file3 = '2dCasetest3.csv'

dataDir = os.path.join(os.getcwd(), 'data')

pp = PostProcess()
pp.load_scv_file(name_file1, dir=dataDir,  key='testData1')
pp.load_scv_file(name_file2, dir=dataDir,  key='testData2')
pp.load_scv_file(name_file2, dir=dataDir,  key='testData3')

pp.rebuildDataRun2('testData1', data=None, values=['U:0', 'U:1'], generalAxis='Points:2',
                        surfaceAxis=['Points:1', 'Points:0'])
pp.rebuildDataRun2('testData2', data=None, values=['U:0', 'U:1'], generalAxis='Points:2',
                        surfaceAxis=['Points:1', 'Points:0'])
pp.rebuildDataRun2('testData3', data=None, values=['U:0', 'U:1'], generalAxis='Points:2',
                        surfaceAxis=['Points:1', 'Points:0'], methodFill='interpolate')

gAxis = pp.newData['testData1']['gAxis'][0]
sAxis1 = pp.newData['testData1']['sAxis1'][gAxis]
sAxis2 = pp.newData['testData1']['sAxis2'][gAxis]
magU = (pp.newData['testData1']['U:0'][gAxis]**2+pp.newData['testData1']['U:1'][gAxis]**2)**0.5
u_x = pp.newData['testData1']['U:0'][gAxis]
u_y = pp.newData['testData1']['U:1'][gAxis]

gAxis_2 = pp.newData['testData2']['gAxis'][0]
sAxis1_2 = pp.newData['testData2']['sAxis1'][gAxis]
sAxis2_2 = pp.newData['testData2']['sAxis2'][gAxis]
magU_2 = (pp.newData['testData2']['U:0'][gAxis]**2+pp.newData['testData1']['U:1'][gAxis]**2)**0.5
u_x_2 = pp.newData['testData2']['U:0'][gAxis]
u_y_2 = pp.newData['testData2']['U:1'][gAxis]

gAxis_3 = pp.newData['testData3']['gAxis'][0]
sAxis1_3 = pp.newData['testData3']['sAxis1'][gAxis]
sAxis2_3 = pp.newData['testData3']['sAxis2'][gAxis]
magU_3 = (pp.newData['testData3']['U:0'][gAxis]**2+pp.newData['testData1']['U:1'][gAxis]**2)**0.5
u_x_3 = pp.newData['testData3']['U:0'][gAxis]
u_y_3 = pp.newData['testData3']['U:1'][gAxis]


figSurface1 = plt.figure(constrained_layout=True, figsize=(12, 4))
spec1 = gridspec.GridSpec(ncols=1, nrows=3, figure=figSurface1)
figSurface1_ax1 = figSurface1.add_subplot(spec1[0, 0])
c1 = figSurface1_ax1.contourf(sAxis1, sAxis2, magU, 100)
cs1 = figSurface1_ax1.contour(sAxis1, sAxis2, magU, 5, colors='black', linewidths=0.3)
figSurface1_ax1.clabel(cs1, inline=True, fontsize=8)

figSurface1_ax2 = figSurface1.add_subplot(spec1[2, 0])
c2 = figSurface1_ax2.contourf(sAxis1_2, sAxis2_2, magU_2, 100)
cs2 = figSurface1_ax2.contour(sAxis1_2, sAxis2_2, magU_2, 5, colors='black', linewidths=0.3)
figSurface1_ax2.clabel(cs2, inline=True, fontsize=8, colors='red')

figSurface1_ax3 = figSurface1.add_subplot(spec1[1, 0])
c3 = figSurface1_ax3.contourf(sAxis1_2, sAxis2_2, magU_2, 100)
cs3 = figSurface1_ax3.contour(sAxis1_2, sAxis2_2, magU_2, 5, colors='black', linewidths=0.3)
figSurface1_ax3.clabel(cs3, inline=True, fontsize=8)

print(pp.surfaceIntegral('testData3', variable='U:0', generalNumber=1))

#pp.findIndexByNearestValue('testData3', 0, where='gAxis')

