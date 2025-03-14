from ..additional_fun.auxiliary_functions import run_command
import pathlib as pl


def print_content(case_path, rel_path):
    """
    
    The function prints content of openfoam dictionary according specify path.

    Arguments:
        * case_path is the path to openFoam case, where openFoam dictionary
        is located. 
        * rel_foamDict_path is the realtive path to openFoam dictionary in 
        the specify openfoam case. 
    """

    command = f'foamDictionary {rel_path}'
    run_command(command, case_path)


def get_solution_time(case_path):
    """
    The method returns all name of non-zero folders of existing solution.
    """
    command = 'foamListTimes'
    run_command(command, case_path)


def print_sub_content(foamDict_key, case_path, rel_path):
    """
    The method returns content in specify key from opnefoam dict.

    EXAMPLE
    *  foamDictionary -entry divSchemes system/fvSchemes

    * foamDictionary -entry "divSchemes/div(phi,U)" system/fvSchemes

    TEMPLATE: foamDict -entry "key" path_to_of_dict
    """
    command = f'foamDictionary -entry {foamDict_key} {rel_path}'
    run_command(command, case_path)


def print_dict_value(foamDict_key, case_path, rel_path):
    """
    The method returns in output values of specify key from openfaom dict. 
    
    run command : foamDictionary -entry "divSchemes/div(phi,U)" -value system/fvSchemes

    Output: 
    
    bounded Gauss linearUpwind grad(U)
    """

    command = f'foamDictionary -entry {foamDict_key} -value {rel_path}'
    run_command(command, case_path)

    run_command(f'foamDictionary -entry "divSchemes/div(phi,U)" -value system/fvSchemes')


def print_foamDict_keys():
    """
    foamDictionary -entry {} -keywords system/fvSchemes

    output:
    default
        div(phi,U)
        div(phi,k)
        div(phi,epsilon)
        div(phi,omega)
        div(phi,v2)
        div((nuEff*dev2(T(grad(U)))))
        div(nonlinearStress)
    """
    run_command(f'foamDictionary -entry divSchemes -keywords system/fvSchemes')

def set_foamDict_value(foam_items: dict, case_path, rel_path):
    """
    The method sets value for specify key in openfaom dict. 
    Argements:
        * foam_items [dict] - is the dict consist of key coresponding key in openfoam dict 
        and them values.  

     foamDictionary -entry "divSchemes.div(phi,U)" -set "bounded Gauss upwind" system/fvSchemes
     or
    foamDictionary -set "startFrom=startTime, startTime=0" system/controlDict
    The last command is better
    """
    string_values = ''
    string_values = ''
    for key, val in foam_items.items():
        string_values += f'{key}={val}, '
    command = f'foamDictionary -set "{string_values[:-2]}" {rel_path}'
    run_command(command, case_path)

def add_foamDict_items(foamDict_key, value, case_path, rel_path):
    """
    The function adds new items in openfoam dict


    foamDictionary -entry "divSchemes.turbulence" -add "bounded Gauss upwind" system/fvSchemes

    foamDict_key : divSchemes.turbulence
    value : bounded Gauss upwind

    """
    command = f'foamDictionary -entry "{foamDict_key}" -add "{value}" {rel_path}'
    run_command(command, case_path)
