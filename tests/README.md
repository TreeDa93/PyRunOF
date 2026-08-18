# Tests and integration fixtures

This directory is primarily for automated tests and their OpenFOAM fixtures.
User-facing examples now live in [`../examples`](../examples/README.md).

- `unit/` contains fast pytest tests that do not require an OpenFOAM solver.
- `integration/` contains checks that require a real OpenFOAM environment.
- `legacy/` contains older test implementations retained for later migration.
- All runnable scenarios and their OpenFOAM cases are stored under `examples/`.

Run the default unit suite from the repository root:

```bash
uv run pytest
```

Files outside `unit/` are not collected by default because many of them require
OpenFOAM, MPI, mesh generators, or case-specific local configuration.
