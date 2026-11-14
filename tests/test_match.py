import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.build_demo import OUTPUT_PATH, render  # noqa: E402
from src.match import RULES, WEIGHTS, assign, evaluate  # noqa: E402
from src.report import format_report, load_cases  # noqa: E402


def provider(name="Ana", zone="Sur", slots=("lv-almuerzo",), diet="casera", capacity=1):
    return {"name": name, "zone": zone, "slots": list(slots), "diet": diet, "capacity": capacity}


def family(name="Familia Uno", zone="Sur", slots=("lv-almuerzo",), diet="casera"):
    return {"name": name, "zone": zone, "slots": list(slots), "diet": diet}


def points(row):
    return {item["rule"]: item["points"] for item in row["breakdown"]}


# --- Caso de muestra -------------------------------------------------------


def test_sample_case_assigns_five_and_leaves_sol_out_by_schedule():
    cases = load_cases()
    rows = assign(cases["providers"], cases["families"])
    assert [row["family"] for row in rows] == [item["name"] for item in cases["families"]]
    assert {row["family"]: row["provider"] for row in rows} == {
        "Familia Ríos": "Ana",
        "Familia Gómez": "Carmen",
        "Familia Paz": "Beatriz",
        "Familia León": "Dora",
        "Familia Ortiz": "Elena",
        "Familia Sol": None,
    }
    sol = rows[-1]
    assert sol["failed_rule"] == "horario"
    assert sol["score"] is None
    assert "Norte" in sol["reason"]
    beatriz = next(other for other in sol["others"] if other["provider"] == "Beatriz")
    # Beatriz ofrece dieta general y todavía tiene cupo: lo único que falla es el horario.
    assert beatriz["failed"] == ["horario"]


def test_sample_case_scores_are_the_sum_of_the_breakdown():
    cases = load_cases()
    for row in assign(cases["providers"], cases["families"]):
        if row["provider"] is None:
            continue
        assert [item["rule"] for item in row["breakdown"]] == list(RULES)
        assert row["score"] == sum(item["points"] for item in row["breakdown"])
        assert points(row) == {"zona": 40, "horario": 20, "dieta": 20, "cupo": 10}


# --- Puntaje desglosado ----------------------------------------------------


def test_weights_add_up_to_100():
    assert sum(WEIGHTS.values()) == 100
    assert set(WEIGHTS) == set(RULES)


def test_score_is_not_flat():
    slots = ("lv-almuerzo", "lv-cena", "sab-almuerzo")
    best = evaluate(provider(slots=slots, capacity=2), family(slots=slots))
    assert best["score"] == 100
    one_slot = evaluate(provider(capacity=2), family())
    assert one_slot["score"] == 90
    via_general = evaluate(provider(diet="general"), family())
    assert via_general["score"] == 80
    half_capacity = evaluate(provider(capacity=2), family(), remaining=1)
    assert half_capacity["score"] == 85


def test_extra_shared_slots_add_points_up_to_the_cap():
    def slot_points(count):
        slots = [f"h{number}" for number in range(count)]
        return evaluate(provider(slots=slots), family(slots=slots))["breakdown"][1]["points"]

    assert [slot_points(count) for count in (1, 2, 3, 4)] == [20, 25, 30, 30]


def test_diet_points_exact_beats_general():
    def diet_points(offered, wanted):
        return evaluate(provider(diet=offered), family(diet=wanted))["breakdown"][2]["points"]

    assert diet_points("casera", "casera") == 20
    assert diet_points("general", "general") == 20
    assert diet_points("general", "casera") == 10
    assert diet_points("casera", "general") == 10


def test_evaluate_reports_every_failed_rule_not_only_the_first():
    result = evaluate(provider(zone="Norte", slots=("sab-cena",), diet="vegetariana", capacity=0), family())
    assert result["failed"] == list(RULES)
    assert result["eligible"] is False
    assert result["score"] is None
    assert all(item["points"] == 0 for item in result["breakdown"])


# --- Reglas obligatorias ---------------------------------------------------


def test_capacity_two_reaches_two_families_and_not_a_third():
    families = [family("Familia Uno"), family("Familia Dos"), family("Familia Tres")]
    rows = assign([provider(capacity=2)], families)
    assert [row["provider"] for row in rows] == ["Ana", "Ana", None]
    # El cupo libre baja con cada asignación y eso se ve en los puntos.
    assert [points(row)["cupo"] for row in rows[:2]] == [10, 5]
    assert [row["score"] for row in rows[:2]] == [90, 85]
    assert rows[2]["failed_rule"] == "cupo"
    assert rows[2]["others"][0]["detail"] == "sin cupo libre (0 de 2)"


def test_incompatible_diet_leaves_family_unassigned():
    rows = assign([provider(diet="vegetariana")], [family(diet="baja en sal")])
    assert rows[0]["provider"] is None
    assert rows[0]["failed_rule"] == "dieta"
    assert rows[0]["others"][0]["failed"] == ["dieta"]


def test_incompatible_schedule_leaves_family_unassigned():
    rows = assign([provider(slots=("sab-cena",))], [family(slots=("lv-almuerzo",))])
    assert rows[0]["provider"] is None
    assert rows[0]["failed_rule"] == "horario"
    assert rows[0]["others"][0]["failed"] == ["horario"]


def test_different_zone_leaves_family_unassigned_even_if_everything_else_fits():
    rows = assign([provider(zone="Norte", capacity=5)], [family(zone="Sur")])
    assert rows[0]["provider"] is None
    assert rows[0]["failed_rule"] == "zona"
    assert rows[0]["others"][0]["failed"] == ["zona"]


def test_family_without_any_offer():
    rows = assign([], [family()])
    assert rows == [
        {
            "family": "Familia Uno",
            "zone": "Sur",
            "diet": "casera",
            "turn": 1,
            "provider": None,
            "slot": None,
            "score": None,
            "breakdown": [],
            "failed_rule": "oferta",
            "reason": "no hay ninguna oferta cargada",
            "others": [],
        }
    ]


def test_unassigned_reason_names_the_rule_of_the_closest_offer():
    providers = [
        provider("Lejana", zone="Norte"),
        provider("Cercana", slots=("lv-almuerzo",), diet="vegetariana"),
    ]
    rows = assign(providers, [family()])
    assert rows[0]["failed_rule"] == "dieta"


# --- Elección entre ofertas válidas ---------------------------------------


def test_higher_score_wins():
    providers = [provider("Ana", diet="general"), provider("Zulma", diet="casera")]
    rows = assign(providers, [family()])
    assert rows[0]["provider"] == "Zulma"
    assert rows[0]["score"] == 90
    assert rows[0]["others"] == [
        {
            "provider": "Ana",
            "eligible": True,
            "score": 80,
            "failed": [],
            "detail": "válida, pero no fue la elegida",
        }
    ]


@pytest.mark.parametrize("names", [("Ana", "Berta"), ("Berta", "Ana")])
def test_score_tie_is_broken_by_name_whatever_the_input_order(names):
    providers = [provider(name) for name in names]
    assert evaluate(providers[0], family())["score"] == evaluate(providers[1], family())["score"]
    rows = assign(providers, [family()])
    assert rows[0]["provider"] == "Ana"


def test_family_with_fewer_options_goes_first():
    providers = [provider("Ana", slots=("lv-almuerzo", "lv-cena"))]
    flexible = family("Familia Flexible", slots=("lv-almuerzo", "lv-cena"))
    providers.append(provider("Berta", slots=("lv-cena",)))
    restricted = family("Familia Restringida", slots=("lv-almuerzo",))
    rows = assign(providers, [flexible, restricted])
    assert {row["family"]: (row["provider"], row["turn"]) for row in rows} == {
        "Familia Restringida": ("Ana", 1),
        "Familia Flexible": ("Berta", 2),
    }


def test_assign_does_not_mutate_its_input():
    providers, families = [provider(capacity=2)], [family()]
    assign(providers, families)
    assert providers == [provider(capacity=2)]
    assert families == [family()]


@pytest.mark.parametrize(
    "providers, families",
    [
        ([{"name": "Ana", "zone": "Sur"}], []),
        ([provider(capacity=-1)], []),
        ([provider(capacity=1.5)], []),
        ([provider("Ana"), provider("Ana")], []),
        ([], [family("Familia Uno"), family("Familia Uno")]),
    ],
)
def test_invalid_input_is_rejected(providers, families):
    with pytest.raises(ValueError):
        assign(providers, families)


# --- Reporte y demo --------------------------------------------------------


def test_report_explains_points_and_failed_rule():
    cases = load_cases()
    report = format_report(assign(cases["providers"], cases["families"]))
    assert "Asignadas: 5 de 6. Sin asignación: 1." in report
    assert "Familia Ríos -> Ana: 90 puntos, horario lv-almuerzo" in report
    assert "zona     40 de 40  misma zona (Sur)" in report
    assert "Familia Sol: sin asignación" in report
    assert "regla que falló: horario" in report


def test_demo_data_is_generated_from_the_python_rule():
    assert OUTPUT_PATH.read_text(encoding="utf-8") == render(), (
        "docs/datos.js quedó viejo. Corré: python3 -m src.build_demo"
    )


def test_demo_has_no_second_copy_of_the_rule():
    assert not (ROOT / "docs" / "logic.js").exists()
    app = (ROOT / "docs" / "app.js").read_text(encoding="utf-8")
    for token in ("capacity -", "remaining", ".sort(", "=== \"general\""):
        assert token not in app
