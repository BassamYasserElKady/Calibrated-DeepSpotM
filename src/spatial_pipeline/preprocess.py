"""Gene intersection and tile-assignment helpers."""

from __future__ import annotations

import numpy as np


def intersect_genes(deepspot_genes: list[str], xenium_genes: list[str]) -> list[str]:
    xenium = set(xenium_genes)
    return [gene for gene in deepspot_genes if gene in xenium]


def assign_xy_to_tiles(xy_he: np.ndarray, tile_size: float, origin: tuple[float, float] = (0.0, 0.0)) -> np.ndarray:
    points = np.asarray(xy_he, dtype=np.float64)
    if points.ndim != 2 or points.shape[1] != 2 or tile_size <= 0:
        raise ValueError("xy_he must have shape [n, 2] and tile_size must be positive")
    origin_array = np.asarray(origin, dtype=np.float64)
    return np.floor((points - origin_array) / float(tile_size)).astype(np.int64)
