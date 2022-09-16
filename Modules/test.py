import json
import os
import sys

base_path = "/home/kirill/Shmakov/Verification/Scripts/obstacle/obstacle_base"
mesh_path = "/home/kirill/Shmakov/Verification/Scripts/obstacle/obstacle_base"

def move2base_salomeMesh(base_path, mesh_path):
    source = '/home/tuhingfg/Documents/source'
    destination = '/home/tuhingfg/Documents/destination'
     
    # gather all files
    allfiles = os.listdir(source)
     
    # iterate on all files to move them to destination folder
    for f in allfiles:
        src_path = os.path.join(source, f)
        dst_path = os.path.join(destination, f)
        os.rename(src_path, dst_path)


def create_salomeMesh(script_name, parameters_path):
    """
    The method creates salome mesh from salome scripts
    """
    command = f"salome -t {script_name} args:{parameters_path}"
#    Executer.run_command(command)
    os.system(command)
    return None








