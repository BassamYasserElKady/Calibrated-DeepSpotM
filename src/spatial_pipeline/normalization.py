"""Training-only target and prediction normalization."""

from __future__ import annotations

import numpy as np


def log1p_cp10k(counts: np.ndarray) -> np.ndarray:
    values = np.asarray(counts, dtype=np.float32)
    if values.ndim != 2 or np.any(values < 0):
        raise ValueError("counts must be a non-negative 2-D array")
    totals = values.sum(axis=1, keepdims=True)
    normalized = np.divide(values * 10000.0, totals, out=np.zeros_like(values), where=totals > 0)
    return np.log1p(normalized)


def fit_zscore(values: np.ndarray, epsilon: float = 1e-6) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(values, dtype=np.float32)
    mean = values.mean(axis=0)
    std = np.where(values.std(axis=0) < epsilon, 1.0, values.std(axis=0))
    return mean.astype(np.float32), std.astype(np.float32)


def apply_zscore(values: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    return (np.asarray(values, dtype=np.float32) - mean) / std
