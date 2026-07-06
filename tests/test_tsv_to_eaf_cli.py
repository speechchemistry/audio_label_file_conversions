from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "saymore_tsv_to_saymore_eaf.py"
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "tsv_to_eaf"
INPUTS_DIR = FIXTURES_DIR / "inputs"
EXPECTED_DIR = FIXTURES_DIR / "expected"


def _get_fixture_pairs():
    input_files = sorted(INPUTS_DIR.glob("*.tsv"))
    if not input_files:
        raise AssertionError(f"No TSV fixtures found in {INPUTS_DIR}")

    pairs = []
    for input_path in input_files:
        expected_path = EXPECTED_DIR / f"{input_path.stem}.eaf"
        if not expected_path.exists():
            raise AssertionError(
                f"Missing expected fixture for {input_path.name}: {expected_path.name}"
            )
        pairs.append((input_path, expected_path))
    return pairs


def _extract_transcription_translation_rows(xml_text: str):
    root = ET.fromstring(xml_text.replace("\r\n", "\n").rstrip() + "\n")

    time_values = {}
    for slot in root.findall(".//TIME_ORDER/TIME_SLOT"):
        time_slot_id = slot.attrib.get("TIME_SLOT_ID")
        time_value = slot.attrib.get("TIME_VALUE")
        if time_slot_id is not None and time_value is not None:
            time_values[time_slot_id] = int(time_value)

    tiers_by_id = {tier.attrib.get("TIER_ID"): tier for tier in root.findall(".//TIER")}
    transcription_tier = tiers_by_id.get("Transcription")
    translation_tier = tiers_by_id.get("Phrase Free Translation")
    if transcription_tier is None or translation_tier is None:
        raise AssertionError(
            "Expected EAF to contain 'Transcription' and 'Phrase Free Translation' tiers"
        )

    transcription_rows = []
    transcription_by_id = {}
    for alignable in transcription_tier.findall(".//ALIGNABLE_ANNOTATION"):
        annotation_id = alignable.attrib["ANNOTATION_ID"]
        start_ms = time_values[alignable.attrib["TIME_SLOT_REF1"]]
        end_ms = time_values[alignable.attrib["TIME_SLOT_REF2"]]
        value = (alignable.findtext("ANNOTATION_VALUE") or "").strip()
        entry = (start_ms, end_ms, value)
        transcription_rows.append((annotation_id, entry))
        transcription_by_id[annotation_id] = entry

    translations_by_parent = {}
    for ref in translation_tier.findall(".//REF_ANNOTATION"):
        parent_id = ref.attrib.get("ANNOTATION_REF")
        value = (ref.findtext("ANNOTATION_VALUE") or "").strip()
        if parent_id:
            translations_by_parent[parent_id] = value

    rows = []
    for annotation_id, (start_ms, end_ms, transcription_value) in transcription_rows:
        rows.append(
            (
                start_ms,
                end_ms,
                transcription_value,
                translations_by_parent.get(annotation_id, ""),
            )
        )
    return rows


@pytest.mark.parametrize("input_path,expected_path", _get_fixture_pairs())
def test_tsv_stdin_converts_to_expected_eaf_stdout(input_path: Path, expected_path: Path):

    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        input=input_path.read_text(encoding="utf-8"),
        capture_output=True,
        text=True,
        check=True,
        cwd=REPO_ROOT,
    )

    assert result.stderr == ""
    assert _extract_transcription_translation_rows(result.stdout) == _extract_transcription_translation_rows(
        expected_path.read_text(encoding="utf-8")
    )