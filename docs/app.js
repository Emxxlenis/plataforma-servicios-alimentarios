// Presentación de la demo. Acá no hay regla de asignación: solo se dibuja
// el resultado que src/build_demo.py dejó en datos.js.

function esc(value) {
  return String(value).replace(/[&<>"']/g, (char) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]
  ));
}

function renderList(title, rows, line) {
  return "<h2>" + esc(title) + "</h2><ul>" + rows.map((row) => "<li>" + esc(line(row)) + "</li>").join("") + "</ul>";
}

function providerLine(person) {
  return [person.name, person.zone, person.slots.join(", "), person.diet, "cupo " + person.capacity].join(" · ");
}

function familyLine(family) {
  return [family.name, family.zone, family.slots.join(", "), family.diet].join(" · ");
}

function renderWeights(demo) {
  return demo.rules.map((rule) => rule + " hasta " + demo.weights[rule]).join(" · ");
}

function renderBreakdown(breakdown) {
  const lines = breakdown.map((item) =>
    "<tr><th scope=\"row\">" + esc(item.rule) + "</th><td class=\"pts\">" + item.points + " de " + item.max +
    "</td><td>" + esc(item.detail) + "</td></tr>");
  return "<table><tbody>" + lines.join("") + "</tbody></table>";
}

function renderOthers(others) {
  if (!others.length) return "";
  const lines = others.map((other) => {
    const note = other.eligible ? other.score + " puntos, " + other.detail : other.detail;
    return "<li>" + esc(other.provider) + ": " + esc(note) + "</li>";
  });
  return "<details><summary>Ofertas descartadas (" + others.length + ")</summary><ul>" + lines.join("") + "</ul></details>";
}

function renderRow(row) {
  if (row.provider === null) {
    return '<article class="hit miss"><h3>' + esc(row.family) + ": sin asignación</h3>" +
      "<p>Regla que falló: <b>" + esc(row.failed_rule) + "</b>. " + esc(row.reason) + ".</p>" +
      renderOthers(row.others) + "</article>";
  }
  return '<article class="hit"><h3>' + esc(row.family) + " → " + esc(row.provider) +
    ' <span class="score">' + row.score + " puntos</span></h3>" +
    "<p>" + esc([row.zone, row.slot, row.diet].join(" · ")) + ". Turno de atención " + row.turn + ".</p>" +
    renderBreakdown(row.breakdown) + renderOthers(row.others) + "</article>";
}

function renderResults(demo) {
  const assigned = demo.rows.filter((row) => row.provider !== null).length;
  const summary = "<p class=\"summary\">Asignadas: " + assigned + " de " + demo.rows.length +
    ". Sin asignación: " + (demo.rows.length - assigned) + ".</p>";
  return summary + demo.rows.map(renderRow).join("");
}

if (typeof document !== "undefined") {
  document.getElementById("weights").textContent = renderWeights(DEMO);
  document.getElementById("providers").innerHTML = renderList("Quien ofrece", DEMO.providers, providerLine);
  document.getElementById("families").innerHTML = renderList("Familias", DEMO.families, familyLine);
  document.getElementById("run").addEventListener("click", () => {
    document.getElementById("out").innerHTML = renderResults(DEMO);
  });
}

if (typeof module !== "undefined") {
  module.exports = { renderResults, renderRow, renderWeights, providerLine, familyLine };
}
