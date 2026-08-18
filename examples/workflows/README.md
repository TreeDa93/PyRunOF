# Full OpenFOAM workflows

These directories contain complete cases and case-specific scripts. Unlike the
examples in `../basic`, they can execute external OpenFOAM commands and create,
replace, or delete generated case directories. Use an OpenFOAM shell with the
required solver and MPI commands available.

## Poiseuille flow

Location: `poiseuille_flow/`

- `run.py` demonstrates the current `ModelConfigurator` and `OpenFOAMCase` API.
- `run_legacy.py` preserves the historical flat API for migration comparison.
- `PoiseuilleFlow/` is the source case; `data.py` contains execution parameters.

```bash
uv run python examples/workflows/poiseuille_flow/run.py
```

Inspect `TEST_MODE` and destination paths before enabling solver execution.

## Parallel pitzDaily

Location: `parallel/`

This scenario uses the `pitzDaily` case and demonstrates parallel execution.
It requires `blockMesh`, `decomposePar`, MPI, and the configured OpenFOAM solver.

```bash
uv run python examples/workflows/parallel/run.py
```

## Planar Couette flow

Location: `planar_couette/`

`run_planarCouette.py` operates on the included planar Couette case. The folder
also contains previously generated/archived results; source and result folders
should be checked before running cleanup or rewrite operations.

```bash
uv run python examples/workflows/planar_couette/run_planarCouette.py
```

## Laminar obstacle flow

Location: `obstacle_laminar/`

- `run_single_sol.py` prepares and runs one obstacle case with `icoFoam`;
- `run_single_sol.ipynb` is the notebook form;
- `compute.py` is an older combined workflow;
- `settings/create_obstacle_mesh.py` and `settings/exportMesh.py` are
  case-specific mesh helpers.

The mesh helpers can require external geometry/mesh software in addition to
OpenFOAM.

## Turbulent obstacle flow

Location: `obstacle_turbulent/`

- `run_single_sol.py` prepares a turbulent case for `pimpleFoam`;
- `run_single_sol.ipynb` is the notebook form;
- `residual.py` plots residual information after a solver run;
- `settings/create_obstacle_mesh*.py` provide alternative mesh setups;
- `postProcess/*.pvsm` are ParaView state files.

The scripts use values from `settings/data.py` and may create solution folders.

## Parametric OpenFOAM study

Location: `parametric_sweep/`

- `run_ps.py` uses the current high-level API and historical text replacement;
- `run_ps_foam_dict.py` applies settings through `CaseParser.apply` and therefore
  requires `foamDictionary` even when solver execution is disabled;
- `run_ps_legacy.py` demonstrates the old callback state and `update_vars` API;
- `settings/base_case/` is the template copied for every sweep point.

```bash
uv run python examples/workflows/parametric_sweep/run_ps.py
uv run python examples/workflows/parametric_sweep/run_ps_foam_dict.py
```

Both current scripts default to `TEST_MODE = True`: they prepare configurations
but do not start the solver. They can still create, replace, or delete files
inside their solution directories according to the flags near the top of each
script. `WORKERS` selects how many cases run concurrently, `DISPLAY` selects
`progress`, `log`, `all`, or `none`, and every run writes `sweep-journal.json`.
