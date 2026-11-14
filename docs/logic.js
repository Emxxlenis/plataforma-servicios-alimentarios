const CASES = {
  providers: [
    { name: "Ana", zone: "Sur", slots: ["lv-almuerzo"], diet: "casera", capacity: 2 },
    { name: "Beatriz", zone: "Norte", slots: ["sab-almuerzo", "sab-cena"], diet: "general", capacity: 1 },
    { name: "Carmen", zone: "Oriente", slots: ["lv-almuerzo"], diet: "baja en sal", capacity: 1 },
    { name: "Dora", zone: "Sur", slots: ["lv-cena"], diet: "casera", capacity: 1 },
    { name: "Elena", zone: "Oeste", slots: ["lv-almuerzo"], diet: "vegetariana", capacity: 1 },
  ],
  families: [
    { name: "Familia Ríos", zone: "Sur", slots: ["lv-almuerzo"], diet: "casera" },
    { name: "Familia Gómez", zone: "Oriente", slots: ["lv-almuerzo"], diet: "baja en sal" },
    { name: "Familia Paz", zone: "Norte", slots: ["sab-almuerzo"], diet: "general" },
    { name: "Familia León", zone: "Sur", slots: ["lv-cena"], diet: "casera" },
    { name: "Familia Ortiz", zone: "Oeste", slots: ["lv-almuerzo"], diet: "vegetariana" },
    { name: "Familia Sol", zone: "Norte", slots: ["lv-almuerzo"], diet: "casera" },
  ],
};

function dietFits(providerDiet, familyDiet) {
  if (providerDiet === "general" || familyDiet === "general") return true;
  return providerDiet === familyDiet;
}

function scorePair(provider, family) {
  if (provider.zone !== family.zone) return null;
  if (provider.remaining <= 0) return null;
  const shared = provider.slots.filter((slot) => family.slots.includes(slot));
  if (!shared.length) return null;
  if (!dietFits(provider.diet, family.diet)) return null;
  return 50 + 30 + 20;
}

function assign(providers, families) {
  const pool = providers.map((person) => ({ ...person, remaining: person.capacity }));
  const options = (family) => pool.filter((provider) => scorePair(provider, family) !== null).length;
  const ordered = [...families].sort((a, b) => options(a) - options(b));
  return ordered.map((family) => {
    const candidates = pool
      .map((provider) => ({ points: scorePair(provider, family), provider }))
      .filter((item) => item.points !== null);
    if (!candidates.length) {
      return { family: family.name, provider: null, reason: "sin cupo compatible" };
    }
    candidates.sort((a, b) => b.points - a.points || a.provider.remaining - b.provider.remaining);
    const chosen = candidates[0].provider;
    chosen.remaining -= 1;
    const shared = chosen.slots.filter((slot) => family.slots.includes(slot)).sort();
    return {
      family: family.name,
      provider: chosen.name,
      zone: family.zone,
      diet: family.diet,
      slot: shared[0],
      reason: "misma zona, horario común y dieta compatible",
    };
  });
}

if (typeof module !== "undefined") {
  module.exports = { CASES, assign };
}
