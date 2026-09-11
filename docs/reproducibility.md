# Reproducibility protocol

## Before running an experiment

1. Record the version and license of every dataset.
2. Set the seed, maximum iterations, and FCM tolerance in the configuration.
3. Pin the tokenizer, lemmatizer, POS tagger, WordNet resource, Porter stemmer, and BERT model versions.
4. Capture the environment and exact commit.
5. Verify that no absolute paths are present and that test data is not mixed with training or tuning data.

## During execution

- Compute per-document metrics before computing the macro-average.
- Preserve the six individual measures, their normalized values, and the aggregated DSR.
- Preserve the FCM membership matrix, graph weights, ranking, and selection reason for each phrase.
- Record the execution time for each stage and the number of candidate phrases.
- Never overwrite a previous run.

## Article validation

The experimental matrix must cover:

- six individual measures;
- OWA combinations of six, five, and four measures;
- DBSCAN, HAC, and FCM;
- first phrase, highest frequency, centroid, and combined selection criteria;
- NUS, SemEval-2010, SemEval-2017, Inspec, and 500N-KPCrowd;
- macro-averaged precision, recall, and F1;
- the Friedman test and Bergmann-Hommel post-hoc procedure for the best variants;
- the Qwen3.5-4B baseline isolated from the main implementation.

## Pre-publication review

- Run all tests from a clean environment.
- Regenerate tables and figures only from versioned or archived results.
- Compare metrics against a declared tolerance through regression tests.
- Archive the configuration, manifest, predictions, results, and checksums in a persistent repository.
