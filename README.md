# Asignación de servicios alimentarios

Empareja a quien ofrece un servicio de comida con una familia. La zona tiene que coincidir. Además hace falta un horario en común y una dieta compatible. Si no hay cupo, la familia queda sin asignación.

**Demo:** https://emxxlenis.github.io/plataforma-servicios-alimentarios/

Los seis casos de `data/cases.json` son de demostración. Las reglas son las que corre la demo.

## Regla

- Zona distinta: no hay par.
- Sin horario en común: no hay par.
- Dieta incompatible: no hay par. `general` acepta la dieta de la otra parte.
- Se asigna primero a quien tiene menos opciones, y se descuenta el cupo.

`src/match.py` y `docs/logic.js` implementan la misma regla.

## Run

```bash
python3 -m pytest -q tests/test_match.py
node tests/logic.test.js
```
