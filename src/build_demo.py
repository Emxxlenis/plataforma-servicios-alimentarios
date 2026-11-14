"""Genera docs/datos.js: los casos y el resultado que muestra la demo.

La página estática no calcula nada. Todo lo que muestra sale de assign(), así
que la demo no puede contradecir a Python.

    python3 -m src.build_demo            # reescribe docs/datos.js
    python3 -m src.build_demo --check    # falla si docs/datos.js quedó viejo
"""

from __future__ import annotations

import json
import sys

from src.match import RULES, WEIGHTS, assign
from src.report import ROOT, load_cases

OUTPUT_PATH = ROOT / "docs" / "datos.js"

HEADER = (
    "// Archivo generado por `python3 -m src.build_demo`. No editar a mano.\n"
    "// Fuente de la regla: src/match.py. Fuente de los casos: data/cases.json.\n"
)


def render() -> str:
    cases = load_cases()
    payload = {
        "rules": list(RULES),
        "weights": WEIGHTS,
        "providers": cases["providers"],
        "families": cases["families"],
        "rows": assign(cases["providers"], cases["families"]),
    }
    body = json.dumps(payload, ensure_ascii=False, indent=2)
    return f'{HEADER}const DEMO = {body};\n\nif (typeof module !== "undefined") {{\n  module.exports = {{ DEMO }};\n}}\n'


def main(argv: list[str]) -> int:
    content = render()
    if "--check" in argv:
        current = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else ""
        if current != content:
            print("docs/datos.js no coincide con src/match.py. Corré: python3 -m src.build_demo")
            return 1
        print("docs/datos.js está al día")
        return 0
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"escrito {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
