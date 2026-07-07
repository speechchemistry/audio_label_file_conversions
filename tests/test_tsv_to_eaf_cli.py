from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "saymore_tsv_to_saymore_eaf.py"
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "tsv_to_eaf"
INPUTS_DIR = FIXTURES_DIR / "inputs"
APPROVED_DIR = FIXTURES_DIR / "approved"
RECEIVED_DIR = FIXTURES_DIR / "received"
DUMMY_AUTHOR = "DUMMY_AUTHOR"
DUMMY_DATE = "2000-01-01T00:00:00+00:00"
DUMMY_URN = "DUMMY_URN"
DUMMY_LAST_USED_ANNOTATION = "0"


def _get_input_fixtures():
    # Each TSV input fixture is matched with approved/<stem>.approved.eaf.
    input_files = sorted(INPUTS_DIR.glob("*.tsv"))
    if not input_files:
        raise AssertionError(f"No TSV fixtures found in {INPUTS_DIR}")

    pairs = []
    for input_path in input_files:
        approved_path = APPROVED_DIR / f"{input_path.stem}.approved.eaf"
        if not approved_path.exists():
            raise AssertionError(
                f"Missing approved fixture for {input_path.name}: {approved_path.name}"
            )
        pairs.append((input_path, approved_path))
    return pairs


def _strip_whitespace_nodes(element: ET.Element):
    if element.text is not None and element.text.strip() == "":
        element.text = None
    if element.tail is not None and element.tail.strip() == "":
        element.tail = None
    for child in element:
        _strip_whitespace_nodes(child)


def _scrub_eaf_root(xml_text: str):
    root = ET.fromstring(xml_text.replace("\r\n", "\n").rstrip() + "\n")

    # Replace volatile metadata with stable dummy values.
    root.attrib["AUTHOR"] = DUMMY_AUTHOR
    root.attrib["DATE"] = DUMMY_DATE

    header = root.find("HEADER")
    if header is None:
        header = ET.SubElement(root, "HEADER")

    for prop in list(header.findall("PROPERTY")):
        if prop.attrib.get("NAME") in {
            "URN",
            "lastUsedAnnotation",
            "lastUsedAnnotationId",
        }:
            header.remove(prop)

    ET.SubElement(header, "PROPERTY", {"NAME": "URN"}).text = DUMMY_URN
    ET.SubElement(
        header,
        "PROPERTY",
        {"NAME": "lastUsedAnnotationId"},
    ).text = DUMMY_LAST_USED_ANNOTATION

    _strip_whitespace_nodes(root)
    return root


def _scrub_and_normalize_eaf(xml_text: str):
    root = _scrub_eaf_root(xml_text)
    serialized = ET.tostring(root, encoding="unicode")
    return ET.canonicalize(xml_data=serialized)


def _scrub_and_pretty_print_eaf(xml_text: str):
    root = _scrub_eaf_root(xml_text)
    ET.indent(root, space="  ")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(
        root, encoding="unicode"
    ) + "\n"


def _assert_approved(input_path: Path, approved_path: Path, actual_xml: str):
    # Emily Bache style flow: compare against approved; write received on mismatch.
    RECEIVED_DIR.mkdir(parents=True, exist_ok=True)
    received_path = RECEIVED_DIR / f"{input_path.stem}.received.eaf"

    approved_normalized = _scrub_and_normalize_eaf(
        approved_path.read_text(encoding="utf-8")
    )
    actual_normalized = _scrub_and_normalize_eaf(actual_xml)
    if actual_normalized != approved_normalized:
        received_path.write_text(
            _scrub_and_pretty_print_eaf(actual_xml), encoding="utf-8"
        )
        pytest.fail(
            f"Approval mismatch for {input_path.name}. "
            f"Approved file: {approved_path}. Review {received_path}."
        )

    if received_path.exists():
        received_path.unlink()


@pytest.mark.parametrize("input_path,approved_path", _get_input_fixtures())
def test_tsv_stdin_converts_to_approved_output(input_path: Path, approved_path: Path):

    # End-to-end CLI test: feed TSV via stdin and assert EAF from stdout.
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        input=input_path.read_text(encoding="utf-8"),
        capture_output=True,
        text=True,
        check=True,
        cwd=REPO_ROOT,
    )

    assert result.stderr == ""
    _assert_approved(input_path, approved_path, result.stdout)