"""Asignación de servicios alimentarios.

Empareja a quien ofrece el servicio con una familia por zona, horario y dieta.
La zona tiene que coincidir. Si no hay cupo o no hay horario común, no hay asignación.
Los casos de data/cases.json son de demostración.
"""

from __future__ import annotations


def diet_fits(provider_diet: str, family_diet: str) -> bool:
    if provider_diet == "general" or family_diet == "general":
        return True
    return provider_diet == family_diet


def score_pair(provider: dict, family: dict) -> int | None:
    if provider["zone"] != family["zone"]:
        return None
    if provider["remaining"] <= 0:
        return None
    shared_slots = set(provider["slots"]) & set(family["slots"])
    if not shared_slots:
        return None
    if not diet_fits(provider["diet"], family["diet"]):
        return None
    return 50 + 30 + 20


def assign(providers: list[dict], families: list[dict]) -> list[dict]:
    pool = [dict(person, remaining=person["capacity"]) for person in providers]
    # Primero las familias con menos ofertas posibles.
    ordered = sorted(families, key=lambda family: _options(pool, family))
    result = []
    for family in ordered:
        candidates = []
        for provider in pool:
            points = score_pair(provider, family)
            if points is None:
                continue
            candidates.append((points, provider))
        if not candidates:
            result.append({"family": family["name"], "provider": None, "reason": "sin cupo compatible"})
            continue
        _, chosen = max(candidates, key=lambda item: (item[0], -item[1]["remaining"]))
        chosen["remaining"] -= 1
        shared = sorted(set(chosen["slots"]) & set(family["slots"]))
        result.append({
            "family": family["name"],
            "provider": chosen["name"],
            "zone": family["zone"],
            "diet": family["diet"],
            "slot": shared[0],
            "reason": "misma zona, horario común y dieta compatible",
        })
    return result


def _options(providers: list[dict], family: dict) -> int:
    return sum(1 for provider in providers if score_pair(provider, family) is not None)
