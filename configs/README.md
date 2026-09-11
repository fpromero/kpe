# Configurations

Configuration files are the source of truth for each experiment and must remain separate from the code.

- `datasets/`: paths, format, license, version, and splits for each corpus.
- `experiments/`: complete definitions of each FTM-KPE variant or baseline.

Before publishing a run, copy its fully resolved configuration into the result directory, with no implicit references or `null` values.
