"""Manifest validation and sample-level leakage protection."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
    "sample_id", "patient_id", "section", "position", "split",
    "he_image_path", "xenium_archive_path", "cell_group_csv_path",
    "alignment_csv_path", "deepspot_tiles_path", "transform_json_path",
    "geometry_path", "xenium_scale", "tile_size",
}


def validate_manifest(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate and return a normalized copy of a sample manifest."""
    missing = sorted(REQUIRED_COLUMNS - set(frame.columns))
    if missing:
        raise ValueError(f"manifest is missing required columns: {missing}")
    result = frame.copy()
    for column in ("sample_id", "patient_id", "split"):
        result[column] = result[column].astype(str).str.strip()
    if result.empty:
        raise ValueError("manifest must contain at least one sample")
    if result["sample_id"].duplicated().any():
        dup = result.loc[result["sample_id"].duplicated(), "sample_id"].tolist()
        raise ValueError(f"duplicate sample_id values: {dup}")
    if result["sample_id"].isna().any() or (result["sample_id"] == "").any():
        raise ValueError("sample_id must be non-empty")
    unknown = sorted(set(result["split"]) - {"development", "final_test"})
    if unknown:
        raise ValueError(f"unknown split labels: {unknown}")
    patient_splits = result.groupby("patient_id")["split"].nunique()
    overlapping = patient_splits[patient_splits > 1].index.tolist()
    if overlapping:
        raise ValueError(f"patient appears in multiple splits: {overlapping}")
    if (pd.to_numeric(result["xenium_scale"], errors="coerce") <= 0).any():
        raise ValueError("xenium_scale must be positive")
    if (pd.to_numeric(result["tile_size"], errors="coerce") <= 0).any():
        raise ValueError("tile_size must be positive")
    return result


def load_manifest(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    return validate_manifest(pd.read_csv(path))


def split_sample_ids(frame: pd.DataFrame, split: str) -> list[str]:
    return validate_manifest(frame).loc[lambda f: f["split"].eq(split), "sample_id"].astype(str).tolist()


def validate_required_paths(frame: pd.DataFrame, root: str | Path) -> list[str]:
    """Return missing path descriptions without reading any data files."""
    root = Path(root)
    path_columns = [column for column in REQUIRED_COLUMNS if column.endswith("_path")]
    missing: list[str] = []
    for _, row in frame.iterrows():
        for column in path_columns:
            path = Path(str(row[column]))
            if not path.is_absolute():
                path = root / path
            if not path.exists():
                missing.append(f"{row['sample_id']}: {column}={path}")
    return missing
