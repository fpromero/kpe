# Original-code migration

## Imported material

The original folder contained 19 Python files, three pattern files used by the implementation, 497 local abstract documents, a non-portable virtual environment, IDE metadata, and Python caches.

The Python modules and operational pattern files were imported into `src/ftm_kpe/legacy/`. Local datasets, the virtual environment, IDE metadata, caches, and the two POS-reference tables that were not consumed by the code were not copied.

`legacy-source-manifest.sha256` records the SHA-256 digest of every imported source file before repository adaptations, making the migration auditable without embedding a machine-specific path.

## Compatibility strategy

The prototype remains in a dedicated compatibility package rather than being split immediately across the new scientific modules. This avoids a large refactor before baseline behavior has regression tests. New development should target the stage-specific packages in `src/ftm_kpe/`; validated pieces can then move out of `legacy/` incrementally.

The repository provides two separate experiment configurations:

- `legacy_current.yaml` describes what the imported code currently computes;
- `ftm_kpe_v1.yaml` describes the main article configuration and is the target for the reproducible implementation.

## Known implementation gaps

The imported prototype is not yet an exact implementation of the article configuration:

- its main distance matrix aggregates four measures rather than the reported five-measure variant;
- WordNet semantic measures are present but disabled in the main aggregation path;
- topic-graph edges use phrase-position distance instead of mean DSR;
- the legacy default OWA quantifier is Pasi, whereas the article describes the Feng-Dillon quantifier;
- the BERT forward pass still follows the prototype's positional-argument convention and requires validation against the intended token-type handling;
- several utility and summarization modules are exploratory or incomplete;
- the legacy environment refers to a Python installation that no longer exists and does not record every imported dependency.

These gaps are documented rather than silently changed because altering them could change the historical baseline. Each gap should be addressed with a regression fixture and an explicit experiment configuration.

## Data handling

The 497 abstract files remain in the original folder. If they are required for an experiment, place or link an authorized copy under the appropriate `data/raw/<dataset>/` directory and record its provenance, license, and checksums. The contents of `data/` are ignored by Git.
