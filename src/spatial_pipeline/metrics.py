"""Spatial transcriptomic evaluation metrics."""

from __future__ import annotations

import numpy as np
from scipy.stats import pearsonr, spearmanr


def safe_pearson(x: np.ndarray, y: np.ndarray) -> float:
    if np.std(x) == 0 or np.std(y) == 0:
        return float("nan")
    return float(pearsonr(x, y).statistic)


def safe_spearman(x: np.ndarray, y: np.ndarray) -> float:
    if np.std(x) == 0 or np.std(y) == 0:
        return float("nan")
    return float(spearmanr(x, y).statistic)


def gene_wise_spatial_pearson(prediction: np.ndarray, target: np.ndarray) -> np.ndarray:
    prediction = np.asarray(prediction)
    target = np.asarray(target)
    if prediction.shape != target.shape or prediction.ndim != 2:
        raise ValueError("prediction and target must have matching shape [tiles, genes]")
    return np.asarray([safe_pearson(prediction[:, j], target[:, j]) for j in range(prediction.shape[1])])


def per_tile_gene_rank_spearman(prediction: np.ndarray, target: np.ndarray) -> float:
    prediction = np.asarray(prediction)
    target = np.asarray(target)
    values = [safe_spearman(prediction[i], target[i]) for i in range(len(prediction))]
    return float(np.nanmean(values))


def aggregate_abundance_metrics(prediction: np.ndarray, target: np.ndarray) -> dict[str, float]:
    predicted = np.asarray(prediction).mean(axis=0)
    observed = np.asarray(target).mean(axis=0)
    return {
        "aggregate_pearson": safe_pearson(predicted, observed),
        "aggregate_spearman": safe_spearman(predicted, observed),
        "mse": float(np.mean((np.asarray(prediction) - np.asarray(target)) ** 2)),
    }
