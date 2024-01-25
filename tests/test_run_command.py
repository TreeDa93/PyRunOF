import os
import subprocess
import pathlib as pl
import pyRunOF
import shutil

def main():
    print('I start here')
    subprocess.run('pwd')
    path_bash = pl.Path(pyRunOF.__file__).parent / 'files' / 'bash' / 'interactive_bash'
    run_path = pl.Path(pyRunOF.__file__).parents[1]
    # Test. Make file not executable!
    subprocess.run(f'chmod -x {path_bash}', shell=True)

    def is_executable(file_path):
        # Using shutil.which() to get the executable path
        executable_path = shutil.which(file_path)

        # Check if the executable path is not None and is executable
        if executable_path and os.access(executable_path, os.X_OK):
            return True
        else:
            return False


    if is_executable(path_bash):
        print(f"{path_bash} is executable.")
    else:
        subprocess.run(f'chmod +x {path_bash}', shell=True)
        print(f"{path_bash} is not executable or not found in the PATH.")

    command1 = 'salome -t'
    #print(path_bash)
    subprocess.Popen(command1, shell=True, executable=path_bash, cwd=run_path, start_new_session=True)
    print('I finish here')
    subprocess.run('pwd')
    subprocess.run(command1, shell=True, executable=path_bash, cwd=run_path, start_new_session=True)


if __name__ == '__main__':
    main()
