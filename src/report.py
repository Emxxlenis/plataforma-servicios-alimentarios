"""Reporte en texto de la asignación.

    python3 -m src.report                  # casos de data/cases.json
    python3 -m src.report otro_archivo.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from src.match import assign

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "data" / "cases.json"


def load_cases(path: Path = CASES_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def format_row(row: dict) -> str:
    lines = []
    if row["provider"] is None:
        lines.append(f"{row['family']}: sin asignación")
        lines.append(f"  regla que falló: {row['failed_rule']} ({row['reason']})")
    else:
        lines.append(f"{row['family']} -> {row['provider']}: {row['score']} puntos, horario {row['slot']}")
        for item in row["breakdown"]:
            lines.append(f"  {item['rule']:<8}{item['points']:>3} de {item['max']:<3} {item['detail']}")
    for other in row["others"]:
        note = f"{other['score']} puntos, {other['detail']}" if other["eligible"] else other["detail"]
        lines.append(f"  descartada {other['provider']}: {note}")
    return "\n".join(lines)


def format_report(rows: list[dict]) -> str:
    assigned = sum(1 for row in rows if row["provider"] is not None)
    header = f"Asignadas: {assigned} de {len(rows)}. Sin asignación: {len(rows) - assigned}."
    return "\n\n".join([header, *(format_row(row) for row in rows)])


def main(argv: list[str]) -> int:
    cases = load_cases(Path(argv[0])) if argv else load_cases()
    print(format_report(assign(cases["providers"], cases["families"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
