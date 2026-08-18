# PyRunOF examples

The examples are grouped by what must be installed and by the amount of work
they perform. Run commands from the repository root after `uv sync --extra dev`.

## 1. Pure Python — OpenFOAM is not required

These are the best starting point. They do not read or modify case directories
and do not start external programs.

| Example | What it demonstrates |
| --- | --- |
| [`basic/01_product_sweep.py`](basic/01_product_sweep.py) | Cartesian product of parameter values, `SweepPoint`, safe case names and callback results. |
| [`basic/02_zip_sweep.py`](basic/02_zip_sweep.py) | Pairwise parameter combinations and validation of list lengths. |
| [`basic/03_error_handling.py`](basic/03_error_handling.py) | Continuing a study after a failed point and inspecting `SweepExecutionError`. |
| [`basic/04_parallel_sweep.py`](basic/04_parallel_sweep.py) | Concurrent cases, live case logs, combined progress, and a timestamped JSON journal. |

```bash
uv run python examples/basic/01_product_sweep.py
uv run python examples/basic/02_zip_sweep.py
uv run python examples/basic/03_error_handling.py
uv run python examples/basic/04_parallel_sweep.py
```

## 2. Parsing OpenFOAM cases — `foamDictionary` is required

These examples use existing cases below `examples/workflows/` as read-only fixtures. They do
not start a solver. Generated files are written to `examples/openfoam/output/`,
which is ignored by Git.

| Example | What it demonstrates |
| --- | --- |
| [`openfoam/01_parse_case.py`](openfoam/01_parse_case.py) | Parsing selected dictionaries and reading a nested value. |
| [`openfoam/02_generate_case_schema.py`](openfoam/02_generate_case_schema.py) | Creating `config.json`, `schema.json`, and IDE-friendly `types.py`. |
| [`openfoam/03_typed_sweep_snapshots.py`](openfoam/03_typed_sweep_snapshots.py) | Combining generated `CaseSettings` with `ParametricSweep` and writing configuration snapshots. |

Run the schema generator before the typed example:

```bash
uv run python examples/openfoam/01_parse_case.py
uv run python examples/openfoam/02_generate_case_schema.py
uv run python examples/openfoam/03_typed_sweep_snapshots.py
```

The generated Python type describes the exact dictionaries found in the base
case. Regenerate it whenever the case structure changes.

## 3. Full OpenFOAM workflows

The following scenarios and their case directories live under `examples/workflows/`.
They may copy
cases, generate meshes, run solvers, or require a particular OpenFOAM setup.
Read the flags near the top of each script before running it.

| Existing scenario | Requirements and behavior |
| --- | --- |
| [`workflows/poiseuille_flow/run.py`](workflows/poiseuille_flow/run.py) | Configures and runs the Poiseuille-flow case through the current API. |
| [`workflows/parallel/run.py`](workflows/parallel/run.py) | Parallel OpenFOAM execution; requires MPI and the configured solver. |
| [`workflows/planar_couette/run_planarCouette.py`](workflows/planar_couette/run_planarCouette.py) | Planar Couette-flow application. |
| [`workflows/obstacle_laminar/run_single_sol.py`](workflows/obstacle_laminar/run_single_sol.py) | Laminar obstacle case with mesh preparation and `icoFoam`. |
| [`workflows/obstacle_laminar/run_single_sol.ipynb`](workflows/obstacle_laminar/run_single_sol.ipynb) | Notebook version of the laminar obstacle workflow. |
| [`workflows/obstacle_laminar/compute.py`](workflows/obstacle_laminar/compute.py) | Older combined case-preparation and computation script. |
| [`workflows/obstacle_turbulent/run_single_sol.py`](workflows/obstacle_turbulent/run_single_sol.py) | Turbulent obstacle case and `pimpleFoam`. |
| [`workflows/obstacle_turbulent/run_single_sol.ipynb`](workflows/obstacle_turbulent/run_single_sol.ipynb) | Notebook version of the turbulent obstacle workflow. |
| [`workflows/obstacle_turbulent/residual.py`](workflows/obstacle_turbulent/residual.py) | Case-specific residual plotting helper; requires solver output. |
| [`workflows/parametric_sweep/run_ps.py`](workflows/parametric_sweep/run_ps.py) | Current API: prepares a set of copied cases; solver execution is controlled by `TEST_MODE`. |
| [`workflows/parametric_sweep/run_ps_foam_dict.py`](workflows/parametric_sweep/run_ps_foam_dict.py) | Applies sweep settings through `CaseParser.apply`; needs `foamDictionary` even in test mode. |

Some case directories also contain mesh-generation helpers and notebooks. They
are case-specific assets rather than introductory library examples:

- `workflows/obstacle_laminar/settings/create_obstacle_mesh.py` prepares obstacle
  geometry, while `exportMesh.py` exports it for the case;
- `workflows/obstacle_turbulent/settings/create_obstacle_mesh.py` and
  `create_obstacle_mesh2.py` contain alternative turbulent-case mesh setups;
- the adjacent `data.py` files define paths, solver names, geometry, and runtime
  values used by those workflows.

## 4. Compatibility and historical examples

These files document APIs that are still supported for migration but should not
be copied into new projects:

| Existing scenario | Notes |
| --- | --- |
| [`workflows/poiseuille_flow/run_legacy.py`](workflows/poiseuille_flow/run_legacy.py) | Historical flat `pyRunOF` API. |
| [`workflows/parametric_sweep/run_ps_legacy.py`](workflows/parametric_sweep/run_ps_legacy.py) | Historical callback state, `update_vars`, and legacy sweep modes. |
| [`parser_original/01_parse_case.py`](parser_original/01_parse_case.py) | Original selective parsing example. |
| [`parser_original/02_export_case_to_json.py`](parser_original/02_export_case_to_json.py) | Original JSON export example. |
| [`parser_original/03_copy_and_apply_settings.py`](parser_original/03_copy_and_apply_settings.py) | Copies a case, applies changes, and exports the result. It modifies only the copy. |
| [`parser_original/04_generate_case_schema.py`](parser_original/04_generate_case_schema.py) | Original three-artifact schema generation example. |
| [`parser_original/05_use_generated_case_types.py`](parser_original/05_use_generated_case_types.py) | Original generated `TypedDict` usage example; run example 4 first. |
| [`parser_original/06_typed_parametric_settings.py`](parser_original/06_typed_parametric_settings.py) | Original typed sweep snapshot example; does not run a solver. |
| [`legacy/scratch/`](legacy/scratch/) | Early Python and API experiments moved out of `tests`; retained for project history, not as supported usage guidance. |
| [`legacy_archive/`](../legacy_archive/) | Archived implementation and debugging scripts; not supported as public API. |

## Choosing an example

- To learn parameter sweeps, start with `basic/01_product_sweep.py`.
- To configure an existing case, run `openfoam/01_parse_case.py` and then inspect
  `parser_original/03_copy_and_apply_settings.py`.
- To get IDE suggestions for case keys, run
  `openfoam/02_generate_case_schema.py`, then open
  `openfoam/03_typed_sweep_snapshots.py`.
- To run an actual solver, choose a full workflow matching your installed
  OpenFOAM version and inspect all paths and execution flags first.
