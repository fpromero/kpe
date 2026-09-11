# Data

Data is kept outside Git. Every downloaded file or dataset must be recorded with its source URL, access date, license, version, and checksum.

```text
raw/        Immutable copy of the original datasets
external/   Auxiliary external resources, models, and metadata
interim/    Intermediate conversions or annotations
processed/  Final deterministic input consumed by experiments
```

Datasets evaluated in the article:

- `nus/`
- `semeval2010/`
- `semeval2017/`
- `inspec/`
- `500n_kpcrowd/`

Do not edit `interim/` or `processed/` manually: both must be reproducible from `raw/` through versioned scripts. Do not redistribute a corpus until its license has been verified.
