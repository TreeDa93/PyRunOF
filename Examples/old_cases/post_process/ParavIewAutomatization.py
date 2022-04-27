import os
# trace generated using paraview version 5.9.0

#### import the simple module from the paraview
from paraview.simple import *

dataPath = 'C:\\Users\\Ivan\\science\\works\\2021_UIE\\results'
foamName = 'res.foam'
U = [0.3, 0.7, 1, 1.2]

ResetSession()
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()
U = [1.2]
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
    # go to the first step using one of them
    animationScene1.GoToLast()
    UpdatePipeline()
    dataInfo = resfoam.GetDataInformation()
    print('Number of points is', dataInfo.GetNumberOfPoints())
    print('Number of cells is', dataInfo.GetNumberOfCells())
    print('Keys for points', resfoam.PointData[:])
    print('range is ', resfoam.PointData['p'].GetNumberOfTuples())
    resfoamPointData = resfoam.PointData
    resfoamPointData['p'].GetNumberOfComponents()

    integrateVariables1 = IntegrateVariables(registrationName='IntegrateVariables1', Input=resfoam)
    UpdatePipeline()
    integrateVariables1.PointData[:]
    DataSliceFile = servermanager.Fetch(integrateVariables1)
    print(DataSliceFile.GetNumberOfPoints())
    numCells = DataSliceFile.GetNumberOfCells()
    keys = DataSliceFile.GetCellData().keys()
    U1 = []
    U2 = []
    for x in range(numCells):
        U1.append(DataSliceFile.GetCellData().GetArray('p').GetValue(x))
    print(U1)


