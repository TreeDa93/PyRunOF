"""Legacy Poiseuille-flow example using the historical flat API."""

import pathlib as pl

import pyRunOF

from data_legacy import *  # noqa: F403


def main():
    mp = pyRunOF.ModelConfigurator()
    mp.create_path_from_dir(dir_path=pl.Path.cwd(), folder_name=base_case, path_key="src")  # noqa: F405
    mp.create_name("solved", name_base=base_case, name_key="dst")  # noqa: F405
    mp.create_path_from_dir(dir_path=pl.Path.cwd(), folder_name_key="dst", path_key="dst")
    mp.duplicate_case(src_key="src", dist_key="dst", mode="rewrite")

    system = pyRunOF.System(case_path=mp.get_path("dst"))
    system.set_controlDict(data)  # noqa: F405

    mesh = pyRunOF.Mesh(case_path=mp.get_path("dst"))
    mesh.set_blockMesh(data)  # noqa: F405

    init_val = pyRunOF.InitialValues(case_path=mp.get_path("dst"))
    calculated_data = init_val.calcInitVal(A, B, Uin, nu)  # noqa: F405
    init_val.set_var(data, calculated_data)  # noqa: F405

    constant = pyRunOF.Constant(case_path=mp.get_path("dst"))
    constant.set_transportProp(data)  # noqa: F405
    constant.turbulent_model(turbulent_type="kEpsilon")

    mesh.run_blockMesh()

    runner = pyRunOF.Run(case_path=mp.get_path("dst"), solver="pimpleFoam")
    runner.run()


if __name__ == "__main__":
    main()
