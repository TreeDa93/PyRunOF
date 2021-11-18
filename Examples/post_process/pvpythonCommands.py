import os
# trace generated using paraview version 5.9.0

#### import the simple module from the paraview
from paraview.simple import *

dataPath = 'C:\\Users\\Ivan\\science\\works\\2021_UIE\\results'
foamName = 'res.foam'
U = [0.3, 0.7, 1, 1.2]

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
for u in U:
    current_folder = f'MHD_LES_inlet_U_{u}\\res.foam'
    fullpath = os.path.join(dataPath, current_folder, foamName)
    resfoam = OpenFOAMReader(registrationName='res.foam',
                             FileName=f'C:\\Users\\Ivan\\science\\works\\2021_UIE\\results\\MHD_LES_inlet_U_{u}\\res.foam')
    resfoam.MeshRegions = ['internalMesh']
    # Properties modified on resfoam
    resfoam.CaseType = 'Decomposed Case'
    # get animation scene
    animationScene1 = GetAnimationScene()
    # get time steps
    tk = GetTimeKeeper()
    timesteps = tk.TimestepValues
    # go to the first step using one of them
    animationScene1.GoToFirst()
    animationScene1.AnimationTime = timesteps[0]
    """
    # last time step
    animationScene1.GoToLast()
    animationScene1.AnimationTime = timesteps[-1]
    # Properties modified on animationScene1
    animationScene1.AnimationTime = 0.116
    integrateVariables1 = IntegrateVariables(registrationName='IntegrateVariables1', Input=resfoam)
    integrated_filter = paraview.servermanager.Fetch(integrateVariables1)
    print(integrated_filter.GetPoint(0))
    # get the time-keeper
    timeKeeper1 = GetTimeKeeper()
    # save data
    SaveData(f'C:/Users/Ivan/science/works/2021_RMHD/data/PVdata_U_{u}.csv',
             proxy=resfoam, ChooseArraysToWrite=1,
        PointDataArrays=['JxB', 'U', 'p'])
    """
    integrateVariables1 = IntegrateVariables(registrationName='IntegrateVariables1', Input=resfoam)
    DataSliceFile = servermanager.Fetch(integrateVariables1)
    numCells = DataSliceFile.GetNumberOfCells()
    U1 = [ ]
    for x in range(numCells):
        U1.append(DataSliceFile.GetCellData().GetArray('p').GetValue(x))

    print(U1)
    Delete(integrateVariables1)
    Delete(resfoam)

print('Keys for points', programmableFilter1.CellData.keys())
    print('Keys for points', programmableFilter1.CellData.values())

import sys
sys.path.append('C:\\Users\\Ivan\\science\\works\\2021_PVpython\\')
exec(open("C:\\Users\\Ivan\\science\\works\\2021_PVpython\\ProgrammableScript.py").read())

from ProgrammableScript import *


print('Number of points is', dataInfo.GetNumberOfPoints())
    print('Number of cells is', dataInfo.GetNumberOfCells())
    print('Keys for points', resfoam.PointData[:])
    print('range is ', resfoam.PointData['p'].GetNumberOfTuples())


"""Programable filter
import csv
import pandas
FilePath = "C:\\Users\\Ivan\science\\works\\2021_PVpython\\data\\dataOutput.csv"
input0 = inputs[0]
rho = 1500
area = input0.CellData['Area']
Umag = mag(input0.CellData['U'])
p_kietic = input0.CellData['p']
p_static = rho *p_kietic
p_total = p_static + 0.5* rho * Umag**2
C_fric = p_static/(0.5*rho*Umag**2)
output.CellData.append(p_static, 'p_s')
output.CellData.append(Umag, 'Umag')
output.CellData.append(p_total, 'p_t')
output.CellData.append(p_kietic, 'p_k')
output.CellData.append(C_fric, 'C_fric')
input0 = inputs[0]
rho = 1500
Umag = mag(input0.CellData['U'])
p_kietic = input0.CellData['p']
p_static = rho *p_kietic
p_total = p_static + 0.5* rho * Umag**2
C_fric = p_static/(0.5*rho*Umag**2)
output.CellData.append(p_static, 'p_s')
output.CellData.append(Umag, 'Umag')
output.CellData.append(p_total, 'p_t')
output.CellData.append(p_kietic, 'p_k')
output.CellData.append(C_fric, 'C_fric')
output.CellData.append(area, 'area')

headers = ['C_fric', 'Umag', 'p_k', 'p_s', 'p_t']
FieldData = [C_fric, Umag, p_kietic, p_static, p_total]
test = output.GetCellData().GetArray('C_fric')

with open(FilePath, 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=';')
    filewriter.writerow(headers)
with open(FilePath, 'a') as csvfile:
    filewriter = csv.writer(csvfile,lineterminator='\n')
    filewriter.writerow(test)
"""

import csv

#Create an empty csv file with headers:
FilePath = "C:\\Users\\Ivan\science\\works\\2021_PVpython\\data\\dataOutput.csv"
Headers=["X","Y","Z","PRESSURE","VELOCITY"]
with open(FilePath, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerow(Headers)

# Get array data from input:
X = inputs[0].Points[:,0][0]
Y = inputs[0].Points[:,1][0]
Z = inputs[0].Points[:,2][0]
PRESSURE = inputs[0] .GetPointData().GetArray(" PRESSURE ")
VELOCITY  = inputs[0] .GetPointData().GetArray("  VELOCITY  ")


# Add this data to the file (you can use an interation here if you want to
do add info comming from several slices)
FieldData=[X,Y,Z, PRESSURE, VELOCITY ]
with open(FilePath, 'a') as csvfile:
           filewriter = csv.writer(csvfile,lineterminator='\n')
           filewriter.writerow(FieldData)


programmableFilter1.RequestInformationScript = """# Code for \'RequestInformation Script\'.
def setOutputTimesteps(algorithm, timesteps):
    "helper routine to set timestep information"
    executive = algorithm.GetExecutive()
    outInfo = executive.GetOutputInformation(0)

    outInfo.Remove(executive.TIME_STEPS())
    for timestep in timesteps:
        outInfo.Append(executive.TIME_STEPS(), timestep)

    outInfo.Remove(executive.TIME_RANGE())
    outInfo.Append(executive.TIME_RANGE(), timesteps[0])
    outInfo.Append(executive.TIME_RANGE(), timesteps[-1])"""
programmableFilter1.RequestUpdateExtentScript = """# Code for \'Script\'
def GetUpdateTimestep(algorithm):
    \"\"\"Returns the requested time value, or None if not present\"\"\"
    executive = algorithm.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    return outInfo.Get(executive.UPDATE_TIME_STEP()) \\
              if outInfo.Has(executive.UPDATE_TIME_STEP()) else None

# This is the requested time-step. This may not be exactly equal to the
# timesteps published in RequestInformation(). Your code must handle that
# correctly.
req_time = GetUpdateTimestep(self)

# Now, use req_time to determine which CSV file to read and read it as before.
# Remember req_time need not match the time values put out in
# \'RequestInformation Script\'. Your code need to pick an appropriate file to
# read, irrespective.

...
# TODO: Generate the data as you want.

# Now mark the timestep produced.
output.GetInformation().Set(output.DATA_TIME_STEP(), req_time)"""