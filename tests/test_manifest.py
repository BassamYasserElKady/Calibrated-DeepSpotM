import pandas as pd
import pytest

from spatial_pipeline.manifest import REQUIRED_COLUMNS, validate_manifest


def row(sample_id="S1", patient_id="P1", split="development"):
    values = {column: "placeholder" for column in REQUIRED_COLUMNS}
    values.update(
        sample_id=sample_id,
        patient_id=patient_id,
        section="section_1",
        position="top",
        split=split,
        xenium_scale=1.0,
        tile_size=224,
    )
    return values


def test_manifest_requires_columns():
    with pytest.raises(ValueError, match="missing required columns"):
        validate_manifest(pd.DataFrame([{"sample_id": "S1"}]))


def test_patient_split_overlap_is_rejected():
    frame = pd.DataFrame([row("S1", "P1", "development"), row("S2", "P1", "final_test")])
    with pytest.raises(ValueError, match="patient appears in multiple splits"):
        validate_manifest(frame)


def test_valid_manifest_is_accepted():
    frame = validate_manifest(pd.DataFrame([row()]))
    assert frame.iloc[0]["sample_id"] == "S1"
