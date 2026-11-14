import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.match import assign


def test_known_case_assigns_five_and_leaves_one_without_slot():
    cases = json.loads((ROOT / "data" / "cases.json").read_text())
    rows = assign(cases["providers"], cases["families"])
    paired = {row["family"]: row["provider"] for row in rows}
    assert paired["Familia Ríos"] == "Ana"
    assert paired["Familia León"] == "Dora"
    assert paired["Familia Gómez"] == "Carmen"
    assert paired["Familia Paz"] == "Beatriz"
    assert paired["Familia Ortiz"] == "Elena"
    assert paired["Familia Sol"] is None
