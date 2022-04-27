import sys
pyFoam_string = 'pyFoamPlotRunner.py'
solver_name = 'pimpleFoam'

core_OF = 4
core_elmer = 4
pyFoam = True
run_command = ''
mode = 'EOF'
logFlag = True

if mode == 'common':
    run_command = f'{solver_name}'
elif mode =='parallel':
    run_command = f'mpirun -np {core_OF} {solver_name} -parallel :'
elif mode =='EOF':
    run_command = f'mpirun -np {core_OF} {solver_name} -parallel : -np {core_elmer} ElmerSolver_mpi'
else:
    sys.exit('''you write not correct mode
     Plesease chose from following modes:
     common - general mode onlt for OpenFOAM;
     parallel is the mode to run your case in parallel calculations
     EOF is the mode to run your case with Elmer together''')

if pyFoam == True:
    run_command = 'pyFoamPlotRunner.py ' + run_command
if logFlag == True:
    run_command += ' | tee log -a'
print(run_command)