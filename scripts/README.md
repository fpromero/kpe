# Scripts

Scripts are thin, reproducible entry points. They must delegate all logic to `ftm_kpe`.

Planned conventions:

- `download_*.py`: retrieve and verify external resources;
- `prepare_*.py`: transform data deterministically;
- `run_*.py`: execute a configuration;
- `aggregate_*.py`: aggregate metrics;
- `make_*.py`: generate tables and figures.
