# OpenFOAM parser examples

These examples use existing OpenFOAM cases from `examples/workflows` and require the
`foamDictionary` command from an installed OpenFOAM environment.

Run them from the repository root:

```bash
uv run python examples/parser_original/01_parse_case.py
uv run python examples/parser_original/02_export_case_to_json.py
uv run python examples/parser_original/03_copy_and_apply_settings.py
uv run python examples/parser_original/04_generate_case_schema.py
uv run python examples/parser_original/05_use_generated_case_types.py
uv run python examples/parser_original/06_typed_parametric_settings.py
```

1. `01_parse_case.py` parses a Poiseuille-flow case and reads selected values
   from `0`, `constant`, and `system`.
2. `02_export_case_to_json.py` exports the parametric-sweep base case to one
   JSON document.
3. `03_copy_and_apply_settings.py` copies the `pitzDaily` case, updates its
   inlet velocity and time-control settings, and exports the result to JSON.
4. `04_generate_case_schema.py` generates `config.json`, `schema.json`, and
   `types.py` for selected dictionaries of the parametric-study base case.
5. `05_use_generated_case_types.py` imports `CaseSettings` and demonstrates
   IDE completion for nested OpenFOAM dictionary keys.
6. `06_typed_parametric_settings.py` combines generated types with
   `ParametricSweep` and writes two configuration snapshots without changing
   or running the source case.

Run example 4 before examples 5 and 6 so that the generated `types.py` module
exists. OpenFOAM is required for parsing; the examples do not start a solver.

Generated files and modified case copies are written below the local `output`
directory. The original examples are not changed.
