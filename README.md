# Calibrated-DeepSpotM

A reproducible multi-sample pipeline for calibrating DeepSpot-M histology-based
spatial-expression predictions against Xenium measurements.

## Scientific design

- Samples are split at the sample/patient level through `data/sample_manifest.csv`.
- Development samples are used for fitting, normalization, and grouped validation.
- Final-test samples remain untouched until the final evaluation command.
- External bulk RNA-seq, microarray, and scRNA-seq data may provide population-level
  priors only; they are never patient-specific conditioning inputs.
- The first trainable model is DeepSpot-M tile predictions → calibration adapter.
- The legacy notebook is not part of this repository and should remain read-only.

## Setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Copy the manifest template and fill in paths relative to the project root:

```bash
cp data/sample_manifest.template.csv data/sample_manifest.csv
python scripts/preflight.py --manifest data/sample_manifest.csv
```

The preflight command validates sample-level split separation and required paths.
It does not download data, extract archives, fit a model, or train anything.

## Repository boundaries

Raw Xenium bundles, H&E images, DeepSpot-M weights, processed matrices, and
experiment results are intentionally excluded by `.gitignore`. Store them locally
and record their relative paths in the manifest.

## Validation

```bash
python -m compileall -q src scripts tests
pytest -q
```

See [docs/multisample_design.md](docs/multisample_design.md) for alignment,
normalization, split, evaluation, and leakage-control details.
