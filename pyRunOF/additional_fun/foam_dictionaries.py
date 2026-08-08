from ..additional_fun.auxiliary_functions import run_command


def _run_foam_dictionary(case_path, rel_path, *arguments):
    """Run ``foamDictionary`` with explicit argument boundaries."""
    command = ["foamDictionary", *map(str, arguments), str(rel_path)]
    return run_command(command, case_path)


def print_content(case_path, rel_path):
    """

    The function prints content of openfoam dictionary according specify path.

    Arguments:
        * case_path is the path to openFoam case, where openFoam dictionary
        is located.
        * rel_foamDict_path is the realtive path to openFoam dictionary in
        the specify openfoam case.
    """

    return _run_foam_dictionary(case_path, rel_path)


def get_solution_time(case_path):
    """
    The method returns all name of non-zero folders of existing solution.
    """
    return run_command(["foamListTimes"], case_path)


def print_sub_content(foamDict_key, case_path, rel_path):
    """
    The method returns content in specify key from opnefoam dict.

    EXAMPLE
    *  foamDictionary -entry divSchemes system/fvSchemes

    * foamDictionary -entry "divSchemes/div(phi,U)" system/fvSchemes

    TEMPLATE: foamDict -entry "key" path_to_of_dict
    """
    return _run_foam_dictionary(case_path, rel_path, "-entry", foamDict_key)


def print_dict_value(foamDict_key, case_path, rel_path):
    """
    The method returns in output values of specify key from openfaom dict.

    run command : foamDictionary -entry "divSchemes/div(phi,U)" -value system/fvSchemes

    Output:

    bounded Gauss linearUpwind grad(U)
    """

    return _run_foam_dictionary(case_path, rel_path, "-entry", foamDict_key, "-value")


def print_foamDict_keys(case_path=".", rel_path="system/fvSchemes", entry="divSchemes"):
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
    return _run_foam_dictionary(case_path, rel_path, "-entry", entry, "-keywords")


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
    values = ", ".join(f"{key}={value}" for key, value in foam_items.items())
    return _run_foam_dictionary(case_path, rel_path, "-set", values)


def add_foamDict_items(foamDict_key, value, case_path, rel_path):
    """
    The function adds new items in openfoam dict


    foamDictionary -entry "divSchemes.turbulence" -add "bounded Gauss upwind" system/fvSchemes

    foamDict_key : divSchemes.turbulence
    value : bounded Gauss upwind

    """
    return _run_foam_dictionary(case_path, rel_path, "-entry", foamDict_key, "-add", value)
