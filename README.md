# FTM-KPE

Code repository for **Keyphrase extraction based on semantic topic modeling with a fuzzy approach**.

FTM-KPE is an unsupervised keyphrase extraction method that combines lexical-syntactic patterns, multiple semantic-relatedness measures, OWA aggregation, fuzzy clustering, and topic ranking.

> Current status: the original research prototype has been imported as a compatibility layer. Its behavior still needs to be validated against the article configuration.

## Method workflow

1. Linguistic preprocessing.
2. Candidate phrase extraction using POS patterns.
3. Computation, normalization, and OWA aggregation of relatedness measures.
4. Fuzzy topic identification and topic ranking.
5. Keyphrase selection and evaluation.

The `src/ftm_kpe/` package mirrors this decomposition so that each stage can be tested, profiled, and replaced independently.

## Repository organization

```text
configs/       Versioned dataset and experiment configurations
data/          Local data organized by processing level (not versioned)
docs/          Design decisions and reproducibility protocol
notebooks/     Exploration and analysis; no production logic
paper/         Manuscript material and final figures and tables
results/       Experiment runs and generated artifacts
scripts/       Entry points for downloading, running, and aggregating results
src/ftm_kpe/   Reusable method implementation
tests/         Unit, integration, and regression tests
```

See [`docs/repository-layout.md`](docs/repository-layout.md) for the detailed structure and [`docs/reproducibility.md`](docs/reproducibility.md) for the experimental protocol.

## Imported original code

The original flat-module prototype is available under `src/ftm_kpe/legacy/`. It was kept together to minimize behavioral changes while allowing package-based imports and portable resource paths. The source folder's virtual environment, IDE files, caches, and local dataset were not copied.

See [`docs/legacy-migration.md`](docs/legacy-migration.md) for the migration decisions and the documented differences between the current prototype and the method described in the article.

Create an isolated environment and install the project before downloading the required language resources:

```bash
python -m venv .venv
python -m pip install -e .
```

The compatibility command accepts either direct text or a UTF-8 input file:

```bash
python -m spacy download en_core_web_sm
python -m nltk.downloader wordnet omw-1.4
ftm-kpe-legacy --input-file path/to/document.txt --language en --top-k 15
```

The first run may download `bert-base-uncased`. Use a locally cached model or an explicit model identifier when running in an offline or controlled environment.

## Reference configuration

`configs/experiments/ftm_kpe_v1.yaml` captures the main variant described in the article: five measures (excluding syntactic similarity), OWA, Fuzzy C-Means, and highest-frequency selection. Parameters not stated explicitly in the manuscript remain `null` and must be fixed before a publishable run. `configs/experiments/legacy_current.yaml` separately records the behavior of the imported prototype.

## Data

NUS, SemEval-2010, SemEval-2017, Inspec, and 500N-KPCrowd are external datasets and are not redistributed in this repository. See [`data/README.md`](data/README.md) for local storage and provenance, license, and checksum requirements.

## Reproducible results

Each run must be written to a separate directory under `results/runs/` and preserve:

- the resolved configuration;
- code, environment, model, and linguistic-resource versions;
- per-document predictions and metrics;
- intermediate values required to reconstruct each decision;
- execution times and logs.

## Citation and license

Use [`CITATION.cff`](CITATION.cff) to cite the software. The code is distributed under the Apache 2.0 license included in [`LICENSE`](LICENSE). Datasets, models, and external resources retain their own licenses.
