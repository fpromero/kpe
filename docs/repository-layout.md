# Repository design

## Principles

1. **Method alignment**: the `src/ftm_kpe/` hierarchy follows the stages described in the article.
2. **Immutable data**: `data/raw/` is never modified; transformations produce new data levels.
3. **Configuration outside the code**: every experimental variant is defined in YAML and archived with its results.
4. **Isolated results**: one run never overwrites another.
5. **Traceability**: intermediate values explaining the final selection are preserved.
6. **Thin notebooks**: notebooks call the package and contain no logic required to reproduce results.

## Package modules

```text
src/ftm_kpe/
├── legacy/         Compatibility copy of the original flat-module prototype
├── preprocessing/  Segmentation, tokenization, lemmatization, stopwords, and POS
├── candidates/     Lexical-syntactic patterns and occurrences
├── relatedness/    Distance, PMI, LCH, JCN, syntactic similarity, and embeddings
├── aggregation/    Score orientation, normalization, and OWA
├── clustering/     FCM and the experimental DBSCAN/HAC variants
├── ranking/        Topic graph, weights, and PageRank-style ranking
├── selection/      First-phrase, frequency, centroid, and combined criteria
├── evaluation/     Matching, P/R/F1, bootstrap, and statistical tests
├── baselines/      Isolated adapters for comparison methods
└── io/             Schemas, data loading, and artifact serialization
```

Dependencies must flow from orchestration into these modules. Scientific modules must not know absolute paths or write directly to `results/`.

## Run contract

Each `results/runs/<run-id>/` directory must contain at least:

```text
config.yaml
environment.json
manifest.json
metrics/
predictions/
traces/
├── normalized_relatedness/
├── dsr/
├── memberships/
├── topic_graphs/
└── selections/
logs/
```

`manifest.json` must identify the commit, working-tree state, dataset and checksum, seed, platform, dependency versions, WordNet resource, and embedding model.

## What is versioned

Versioned files include code, configurations, tests, documentation, small metadata files, and final results required by the article. Corpora, model weights, caches, complete runs, and secrets are not versioned.
