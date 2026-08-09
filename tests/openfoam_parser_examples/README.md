# OpenFOAM parser examples

These examples use existing OpenFOAM cases from `tests` and require the
`foamDictionary` command from an installed OpenFOAM environment.

Run them from the repository root:

```bash
uv run python tests/openfoam_parser_examples/01_parse_case.py
uv run python tests/openfoam_parser_examples/02_export_case_to_json.py
uv run python tests/openfoam_parser_examples/03_copy_and_apply_settings.py
```

1. `01_parse_case.py` parses a Poiseuille-flow case and reads selected values
   from `0`, `constant`, and `system`.
2. `02_export_case_to_json.py` exports the parametric-sweep base case to one
   JSON document.
3. `03_copy_and_apply_settings.py` copies the `pitzDaily` case, updates its
   inlet velocity and time-control settings, and exports the result to JSON.

Generated files and modified case copies are written below the local `output`
directory. The original examples are not changed.
