"""Asignación de servicios alimentarios: única fuente de la regla.

Empareja a quien ofrece un servicio de comida con una familia. Cuatro reglas,
todas obligatorias y siempre evaluadas en este orden:

    zona     la zona tiene que ser la misma
    horario  tiene que haber al menos un horario en común
    dieta    la dieta tiene que ser compatible
    cupo     a la oferta le tiene que quedar cupo

Si una sola falla no hay par: la familia queda sin asignación antes que en un
cruce malo. Cuando las cuatro pasan, cada una aporta puntos (ver WEIGHTS) y el
total sirve solo para elegir entre varias ofertas válidas.

La demo de docs/ no reimplementa nada de esto: muestra el resultado que
src/build_demo.py genera llamando a assign().

Los casos de data/cases.json son de demostración.
"""

from __future__ import annotations

RULES = ("zona", "horario", "dieta", "cupo")

# Puntos máximos por regla. Suman 100.
WEIGHTS = {"zona": 40, "horario": 30, "dieta": 20, "cupo": 10}

SLOT_BASE = 20  # un horario en común
SLOT_EXTRA = 5  # cada horario en común adicional, hasta WEIGHTS["horario"]
DIET_VIA_GENERAL = 10  # compatible solo porque una de las dos partes es "general"

GENERAL = "general"

REASON_ASSIGNED = "misma zona, horario en común, dieta compatible y cupo libre"


def diet_fits(provider_diet: str, family_diet: str) -> bool:
    """`general` acepta la dieta de la otra parte. Si no, tienen que ser iguales."""
    if provider_diet == GENERAL or family_diet == GENERAL:
        return True
    return provider_diet == family_diet


def _check(rule: str, ok: bool, points: int, detail: str) -> dict:
    return {"rule": rule, "ok": ok, "points": points if ok else 0, "max": WEIGHTS[rule], "detail": detail}


def _check_zone(provider: dict, family: dict) -> dict:
    if provider["zone"] == family["zone"]:
        return _check("zona", True, WEIGHTS["zona"], f"misma zona ({family['zone']})")
    return _check("zona", False, 0, f"zona distinta ({provider['zone']} y {family['zone']})")


def _check_slots(provider: dict, family: dict) -> dict:
    shared = sorted(set(provider["slots"]) & set(family["slots"]))
    if not shared:
        return _check("horario", False, 0, "sin horario en común")
    points = min(WEIGHTS["horario"], SLOT_BASE + SLOT_EXTRA * (len(shared) - 1))
    label = "1 horario en común" if len(shared) == 1 else f"{len(shared)} horarios en común"
    return _check("horario", True, points, f"{label} ({', '.join(shared)})")


def _check_diet(provider: dict, family: dict) -> dict:
    offered, wanted = provider["diet"], family["diet"]
    if offered == wanted:
        return _check("dieta", True, WEIGHTS["dieta"], f"misma dieta ({wanted})")
    if diet_fits(offered, wanted):
        return _check("dieta", True, DIET_VIA_GENERAL, f"compatible por dieta general ({offered} y {wanted})")
    return _check("dieta", False, 0, f"dieta incompatible ({offered} y {wanted})")


def _check_capacity(provider: dict, remaining: int) -> dict:
    capacity = provider["capacity"]
    if remaining <= 0:
        return _check("cupo", False, 0, f"sin cupo libre (0 de {capacity})")
    points = WEIGHTS["cupo"] * remaining // capacity
    return _check("cupo", True, points, f"cupo libre {remaining} de {capacity}")


def evaluate(provider: dict, family: dict, remaining: int | None = None) -> dict:
    """Evalúa las cuatro reglas para un par. Nunca corta en la primera que falla.

    `remaining` es el cupo que le queda a la oferta en este momento. Si no se
    pasa, se usa el cupo completo.
    """
    if remaining is None:
        remaining = provider["capacity"]
    breakdown = [
        _check_zone(provider, family),
        _check_slots(provider, family),
        _check_diet(provider, family),
        _check_capacity(provider, remaining),
    ]
    failed = [item["rule"] for item in breakdown if not item["ok"]]
    return {
        "provider": provider["name"],
        "eligible": not failed,
        # Un par que no cumple las cuatro reglas no tiene puntaje.
        "score": None if failed else sum(item["points"] for item in breakdown),
        "failed": failed,
        "breakdown": breakdown,
    }


def assign(providers: list[dict], families: list[dict]) -> list[dict]:
    """Asigna cada familia a lo sumo a una oferta. Devuelve una fila por familia,
    en el orden de entrada.

    Orden de atención (campo `turn`): primero las familias con menos ofertas
    posibles; a igualdad, el orden de entrada.
    Elección: la oferta válida con más puntaje; a igual puntaje, la primera por
    nombre en orden alfabético.
    """
    _validate(providers, families)
    remaining = {provider["name"]: provider["capacity"] for provider in providers}
    options = [sum(evaluate(provider, family)["eligible"] for provider in providers) for family in families]
    order = sorted(range(len(families)), key=lambda index: (options[index], index))

    rows: list[dict] = [{} for _ in families]
    for turn, index in enumerate(order, start=1):
        family = families[index]
        evaluations = [evaluate(provider, family, remaining[provider["name"]]) for provider in providers]
        eligible = [item for item in evaluations if item["eligible"]]
        base = {"family": family["name"], "zone": family["zone"], "diet": family["diet"], "turn": turn}
        if not eligible:
            rule, reason = _why_unassigned(family, evaluations)
            rows[index] = {
                **base,
                "provider": None,
                "slot": None,
                "score": None,
                "breakdown": [],
                "failed_rule": rule,
                "reason": reason,
                "others": [_summary(item) for item in evaluations],
            }
            continue
        best = min(eligible, key=lambda item: (-item["score"], item["provider"]))
        chosen = next(provider for provider in providers if provider["name"] == best["provider"])
        remaining[chosen["name"]] -= 1
        rows[index] = {
            **base,
            "provider": chosen["name"],
            "slot": sorted(set(chosen["slots"]) & set(family["slots"]))[0],
            "score": best["score"],
            "breakdown": best["breakdown"],
            "failed_rule": None,
            "reason": REASON_ASSIGNED,
            "others": [_summary(item) for item in evaluations if item is not best],
        }
    return rows


def _summary(evaluation: dict) -> dict:
    """Resumen de una oferta no elegida: qué reglas fallaron, o con qué puntaje perdió."""
    failed_details = [item["detail"] for item in evaluation["breakdown"] if not item["ok"]]
    return {
        "provider": evaluation["provider"],
        "eligible": evaluation["eligible"],
        "score": evaluation["score"],
        "failed": evaluation["failed"],
        "detail": "; ".join(failed_details) if failed_details else "válida, pero no fue la elegida",
    }


def _why_unassigned(family: dict, evaluations: list[dict]) -> tuple[str, str]:
    """Regla que dejó afuera a la familia: la primera que falló en la oferta que
    más lejos llegó (zona, horario, dieta, cupo, en ese orden)."""
    if not evaluations:
        return "oferta", "no hay ninguna oferta cargada"
    reached = max(RULES.index(item["failed"][0]) for item in evaluations)
    rule = RULES[reached]
    zone = family["zone"]
    reasons = {
        "zona": f"no hay ninguna oferta en la zona {zone}",
        "horario": f"en la zona {zone} ninguna oferta tiene un horario en común",
        "dieta": f"en la zona {zone} hay horario en común, pero ninguna dieta compatible",
        "cupo": f"la oferta compatible de la zona {zone} ya no tiene cupo",
    }
    return rule, reasons[rule]


def _validate(providers: list[dict], families: list[dict]) -> None:
    for kind, items, keys in (
        ("oferta", providers, ("name", "zone", "slots", "diet", "capacity")),
        ("familia", families, ("name", "zone", "slots", "diet")),
    ):
        seen = set()
        for item in items:
            missing = [key for key in keys if key not in item]
            if missing:
                raise ValueError(f"{kind} {item.get('name', '(sin nombre)')}: faltan campos {missing}")
            if item["name"] in seen:
                raise ValueError(f"{kind} repetida: {item['name']}")
            seen.add(item["name"])
    for provider in providers:
        capacity = provider["capacity"]
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 0:
            raise ValueError(f"oferta {provider['name']}: el cupo tiene que ser un entero mayor o igual a 0")
