// Prueba de la presentación de la demo. La regla se prueba en tests/test_match.py;
// acá se verifica que la página muestre lo que Python generó en docs/datos.js.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const { DEMO } = require("../docs/datos");
const { renderResults, renderRow, renderWeights } = require("../docs/app");

const cases = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "data", "cases.json"), "utf8"));
assert.deepEqual(DEMO.providers, cases.providers, "datos.js y data/cases.json tienen distintas ofertas");
assert.deepEqual(DEMO.families, cases.families, "datos.js y data/cases.json tienen distintas familias");

const paired = Object.fromEntries(DEMO.rows.map((row) => [row.family, row.provider]));
assert.deepEqual(paired, {
  "Familia Ríos": "Ana",
  "Familia Gómez": "Carmen",
  "Familia Paz": "Beatriz",
  "Familia León": "Dora",
  "Familia Ortiz": "Elena",
  "Familia Sol": null,
});

for (const row of DEMO.rows) {
  const html = renderRow(row);
  if (row.provider === null) {
    assert.ok(html.includes("sin asignación"), row.family);
    assert.ok(html.includes("<b>" + row.failed_rule + "</b>"), row.family + ": falta la regla que falló");
    assert.ok(html.includes(row.reason), row.family + ": falta el motivo");
    continue;
  }
  assert.ok(html.includes(row.score + " puntos"), row.family + ": falta el total");
  const total = row.breakdown.reduce((sum, item) => sum + item.points, 0);
  assert.equal(total, row.score, row.family + ": el total no es la suma del desglose");
  for (const item of row.breakdown) {
    assert.ok(html.includes(">" + item.rule + "<"), row.family + ": falta la regla " + item.rule);
    assert.ok(html.includes(item.points + " de " + item.max), row.family + ": faltan los puntos de " + item.rule);
    assert.ok(html.includes(item.detail), row.family + ": falta el detalle de " + item.rule);
  }
}

const page = renderResults(DEMO);
assert.ok(page.includes("Asignadas: 5 de 6. Sin asignación: 1."));
assert.equal(renderWeights(DEMO), "zona hasta 40 · horario hasta 30 · dieta hasta 20 · cupo hasta 10");
assert.ok(renderRow({ ...DEMO.rows[0], family: "<script>" }).includes("&lt;script&gt;"), "el texto se escapa");

const index = fs.readFileSync(path.join(__dirname, "..", "docs", "index.html"), "utf8");
for (const id of ["run", "out", "providers", "families", "weights"]) {
  assert.ok(index.includes('id="' + id + '"'), "index.html no tiene #" + id);
}
assert.ok(index.includes('src="datos.js"') && index.includes('src="app.js"'));

console.log("demo ok");
