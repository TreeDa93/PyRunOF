import os
import csv
from paraview.simple import *

progFilterPath = ''
saveDir = 'C:\\Users\\Ivan\science\\works\\2021_PVpython\\data\\'
outFileName = 'dataOutput2.csv'
savePath = saveDir+outFileName

def runFun(foamPath, savePath):
    ResetSession()

    paraview.simple._DisableFirstRenderCameraReset()
    animationScene1 = GetAnimationScene()

    main_data = OpenFOAMReader(registrationName='res_vol.foam',
                                 FileName=foamPath)
    main_data.MeshRegions = ['inlet', 'internalMesh', 'outlet']
    main_data.CaseType = 'Decomposed Case'

    res_vol = ExtractBlock(registrationName='volume', Input=main_data)
    res_vol.BlockIndices = [1]
    res_inlet = ExtractBlock(registrationName='inlet', Input=main_data)
    res_inlet.BlockIndices = [3]
    res_outlet = ExtractBlock(registrationName='outlet', Input=main_data)
    res_outlet.BlockIndices = [4]

    int_volume = IntegrateVariables(registrationName='volumeIntegral', Input=res_vol)
    int_outlet = IntegrateVariables(registrationName='outletIntegral', Input=res_outlet)
    int_inlet = IntegrateVariables(registrationName='inletIntegral', Input=res_inlet)

    programmableFilter1 = ProgrammableFilter(registrationName='ProgrammableFilter1',
                                             Input=[int_volume, int_outlet, int_inlet])
    programmableFilter1.Script = 'exec(open("C:\\\\Users\\\\Ivan\\\\science\\\\works' \
                                 '\\\\2021_PVpython\\\\progFilterScript2.py").read())'

    animationScene1.UpdateAnimationUsingDataTimeSteps()
    tk = GetTimeKeeper()
    timesteps = tk.TimestepValues
    animationScene1.AnimationTime = timesteps[-1]
    programmableFilter1 = GetActiveSource()
    SetActiveSource(programmableFilter1)
    renderView1 = GetActiveViewOrCreate('RenderView')
    programmableFilter1Display = Show(programmableFilter1, renderView1, 'UnstructuredGridRepresentation')

    dataInfo = programmableFilter1.GetDataInformation()
    keys = programmableFilter1.CellData.keys()
    DataSliceFile = servermanager.Fetch(programmableFilter1)
    numCells = DataSliceFile.GetNumberOfCells()
    data = []
    for key in keys:
        for x in range(numCells):
            data.append(DataSliceFile.GetCellData().GetArray(key).GetValue(x))


    if os.path.exists(savePath) == False:
        with open(savePath, 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(keys)
    with open(savePath, 'a') as csvfile:
        filewriter = csv.writer(csvfile, lineterminator='\n')
        filewriter.writerow(data)







