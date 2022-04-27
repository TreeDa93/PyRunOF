import os
# trace generated using paraview version 5.9.0

#### import the simple module from the paraview
from paraview.simple import *

U = [1.2]
u = 1.2
dataPath = 'C:\\Users\\Ivan\\science\\works\\2021_UIE\\results'
foamName = 'res.foam'
current_folder = f'MHD_LES_inlet_U_{u}\\res.foam'
fullpath = os.path.join(dataPath, current_folder, foamName)

path1 = f'C:\\Users\\Ivan\\science\\works\\2021_UIE\\results\\MHD_LES_inlet_U_{u}\\res.foam'

FilePath = "C:\\Users\\Ivan\science\\works\\2021_PVpython\\data\\dataOutput.csv"


for u in U:
    path1 = f'C:\\Users\\Ivan\\science\\works\\2021_UIE\\results\\MHD_LES_inlet_U_{u}\\res.foam'

    ResetSession()

    paraview.simple._DisableFirstRenderCameraReset()
    animationScene1 = GetAnimationScene()

    main_data = OpenFOAMReader(registrationName='res_vol.foam',
                                 FileName=path1)
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

    # create a new 'Programmable Filter'
    programmableFilter1 = ProgrammableFilter(registrationName='ProgrammableFilter1',
                                             Input=[int_volume, int_outlet, int_inlet])
    programmableFilter1.Script = 'exec(open("C:\\\\Users\\\\Ivan\\\\science\\\\works' \
                                 '\\\\2021_PVpython\\\\progFilterScript1.py").read())'

    animationScene1.UpdateAnimationUsingDataTimeSteps()
    tk = GetTimeKeeper()
    timesteps = tk.TimestepValues
    animationScene1.AnimationTime = timesteps[-1]

    # get active source.
    programmableFilter1 = GetActiveSource()

    # set active source
    SetActiveSource(programmableFilter1)

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')
    # show data in view
    programmableFilter1Display = Show(programmableFilter1, renderView1, 'UnstructuredGridRepresentation')





