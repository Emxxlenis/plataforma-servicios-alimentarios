const { assign, CASES } = require("../docs/logic");

const paired = Object.fromEntries(assign(CASES.providers, CASES.families).map((row) => [row.family, row.provider]));
const expected = {
  "Familia Ríos": "Ana",
  "Familia León": "Dora",
  "Familia Gómez": "Carmen",
  "Familia Paz": "Beatriz",
  "Familia Ortiz": "Elena",
  "Familia Sol": null,
};
for (const [family, provider] of Object.entries(expected)) {
  if (paired[family] !== provider) {
    throw new Error(family + " got " + paired[family] + " expected " + provider);
  }
}
console.log("match logic ok");
