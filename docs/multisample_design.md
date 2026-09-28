# Multi-sample design

## Unit of separation

The manifest is the source of truth. Every sample has one split label. A patient
must not appear in both development and final-test splits. The final-test split is
never used to calculate normalization statistics, select genes, tune
hyperparameters, or choose checkpoints.

## Coordinate alignment

Each sample records the H&E image dimensions, tile size, Xenium scale, and an
affine transform. Xenium coordinates are first expressed in the declared Xenium
coordinate system, scaled using the per-sample Xenium scale, and transformed with
the stored 2-D affine matrix into H&E pixel coordinates. DeepSpot-M tiles are
indexed by their H&E pixel-space origin/center. The pipeline rejects missing or
ambiguous transform and geometry records before processing.

## Targets and genes

Transcript counts are assigned to tiles in H&E pixel space. Counts are converted
to CP10K within each tile and normalized as `log1p(CP10K)`. The usable gene set is
the intersection of the DeepSpot-M output genes and the Xenium panel genes. The
intersection is recorded explicitly; it is not silently inferred from a model
checkpoint. Training-only normalization statistics are then applied to both
development validation data and final-test data.

## Model

The baseline adapter accepts only the DeepSpot-M tile vector. It has a nonlinear
encoder, a residual correction head, and learned per-gene scale and bias. No bulk,
microarray, scRNA-seq, or patient-level metadata is supplied to the model.

## Evaluation

Development evaluation uses grouped sample-level validation. Reported metrics are:

- gene-wise spatial Pearson correlation across tiles;
- per-tile gene-rank Spearman correlation;
- aggregate gene-abundance Pearson and Spearman correlations;
- mean squared error;
- per-sample and pooled summaries.

The final-test samples, or whatever samples are explicitly marked `final_test` in
the manifest, are evaluated only after model selection is frozen. The old
single-sample tile split is not an acceptable final evaluation design.
