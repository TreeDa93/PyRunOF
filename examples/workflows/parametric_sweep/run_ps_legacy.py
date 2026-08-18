"""Legacy parametric-sweep example using the historical flat API."""

import pyRunOF

from settings.data_legacy import *  # noqa: F403


TEST_MODE = True
GENERATE_JSON_PARAMS = True
DELETE_SOL_FOLDER = False
DELETE_CASES = False


def main():
    ps = pyRunOF.ParametricSweep()
    ps.run(
        ps_params,  # noqa: F405
        fun=run_case,
        update_vars=(data,),  # noqa: F405
        type_set="special series",
    )


def run_case(ps):
    mp = pyRunOF.ModelConfigurator(dir_path=dir_path)  # noqa: F405
    mp.create_path_from_dir(dir_path_key="dir", folder_name="settings", path_key="settings")
    mp.create_path_from_dir(
        dir_path_key="settings", folder_name=src_case, path_key="src"  # noqa: F405
    )
    mp.create_path_from_dir(dir_path_key="dir", folder_name="solution", path_key="solution")

    if DELETE_SOL_FOLDER is True:
        mp.delete_cases(full_pathes=[mp.get_path("solution")])

    if DELETE_CASES is True:
        mp.delete_cases(words=["base_case"], directory=mp.get_path("solution"))

    mp.get_path("solution").mkdir(exist_ok=True)

    mp.create_name(ps.get_cur_name(type_name="index"), name_base=src_case, name_key="dst")  # noqa: F405
    mp.create_path_from_dir(dir_path_key="solution", folder_name_key="dst", path_key="dst")
    mp.duplicate_case(src_key="src", dist_key="dst", mode="rewrite")

    system = pyRunOF.System(case_path=mp.get_path("dst"))
    system.set_controlDict(data)  # noqa: F405
    system.set_any_file(data, files=["decomposeParDict"])  # noqa: F405

    init_val = pyRunOF.InitialValues(case_path=mp.get_path("dst"))
    data.update(  # noqa: F405
        init_val.calcInitVal(data["A_var"], data["B_var"], data["Uin_var"], data["nu_var"])  # noqa: F405
    )
    init_val.set_var(data)  # noqa: F405

    constant = pyRunOF.Constant(case_path=mp.get_path("dst"))
    constant.set_transportProp(data)  # noqa: F405
    constant.turbulent_model(turbulent_type="kOmega")

    mesh = pyRunOF.Mesh(case_path=mp.get_path("dst"))
    mesh.set_blockMesh(data)  # noqa: F405

    runner = pyRunOF.Run(
        case_path=mp.get_path("dst"),
        solver=solverName,  # noqa: F405
        mode="parallel",
        OF_core=coreOF,  # noqa: F405
    )

    if GENERATE_JSON_PARAMS is True:
        json_name = f"params_{ps.cur_i}"
        mp.create_path_from_dir(
            dir_path_key="solution", folder_name=json_name, path_key="params"
        )

    mp.create_json_params(data, save_path=mp.get_path("params"))  # noqa: F405
    if TEST_MODE is not True:
        mesh.run_blockMesh()
        mesh.run_decompose(what="OF")
        runner.run()


if __name__ == "__main__":
    main()
