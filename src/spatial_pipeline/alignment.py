"""Explicit Xenium-to-H&E coordinate transforms."""

from __future__ import annotations

import numpy as np


def apply_affine_xy(xy: np.ndarray, affine: np.ndarray) -> np.ndarray:
    """Apply a 3x3 homogeneous or 2x3 affine transform to Nx2 coordinates."""
    points = np.asarray(xy, dtype=np.float64)
    matrix = np.asarray(affine, dtype=np.float64)
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("xy must have shape [n, 2]")
    if matrix.shape == (2, 3):
        matrix = np.vstack([matrix, [0.0, 0.0, 1.0]])
    if matrix.shape != (3, 3):
        raise ValueError("affine must have shape [2, 3] or [3, 3]")
    homogeneous = np.column_stack([points, np.ones(len(points))])
    mapped = homogeneous @ matrix.T
    if np.any(np.abs(mapped[:, 2]) < 1e-12):
        raise ValueError("affine transform produced invalid homogeneous coordinates")
    return mapped[:, :2] / mapped[:, 2:3]


def xenium_to_he(xy_xenium: np.ndarray, xenium_scale: float, affine: np.ndarray) -> np.ndarray:
    if xenium_scale <= 0:
        raise ValueError("xenium_scale must be positive")
    return apply_affine_xy(np.asarray(xy_xenium) * float(xenium_scale), affine)
