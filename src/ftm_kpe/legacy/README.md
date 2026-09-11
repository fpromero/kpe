# Original research prototype

This package contains the original flat-module implementation with only compatibility-oriented changes:

- local imports use package-relative paths;
- pattern files are resolved relative to the installed module;
- obsolete `joblib` access to `xrange` uses Python's built-in `range`;
- comments and user-facing messages are in English;
- Flask adapters pass the complete current extraction signature;
- notebook-only dependency rendering was removed from preprocessing.

Function names, module names, algorithms, control flow, and variable names remain otherwise recognizable so that results can be compared with the original source.

Use `ftm-kpe-legacy` or `python -m ftm_kpe.cli` instead of running `legacy/main.py`, whose batch defaults refer to the former local directory layout.

The `datas/`, `venv/`, `.idea/`, and `__pycache__/` directories from the source folder were deliberately excluded. The original source folder remains unchanged.
