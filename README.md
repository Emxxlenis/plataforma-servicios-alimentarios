# Asignación de servicios alimentarios

Empareja a quien ofrece un servicio de comida con una familia, y explica cada decisión: cuántos puntos sumó cada regla cuando hay par, y cuál regla falló cuando no lo hay.

**Demo:** https://emxxlenis.github.io/plataforma-servicios-alimentarios/

Los nombres de `data/cases.json` son casos de demostración, no personas reales. El proyecto no tiene usuarias ni métricas de impacto medidas: es la regla de asignación, sus tests y una página que muestra el resultado.

## Problema

Hay personas que ofrecen un servicio de comida y familias que lo necesitan. Un cruce solo sirve si la comida puede llegar (misma zona), si coinciden en algún horario, si la dieta que se cocina es la que la familia puede comer, y si a quien ofrece todavía le queda cupo. Un cruce que no cumple alguna de esas condiciones es peor que no cruzar: la familia cree que tiene el servicio resuelto y no lo tiene.

## Regla de asignación

Cuatro reglas, todas obligatorias, evaluadas siempre en este orden:

| Regla | Condición para que haya par | Puntos |
|---|---|---|
| zona | La zona es la misma. | 40 |
| horario | Hay al menos un horario en común. | 20 por el primero, 5 por cada uno adicional, hasta 30 |
| dieta | Es la misma dieta, o una de las dos partes es `general`. | 20 si es la misma, 10 si es compatible solo por `general` |
| cupo | A la oferta le queda cupo libre. | 10 por la proporción de cupo libre (cupo 2 con 1 libre: 5) |

El máximo es 100. El puntaje no decide si hay par: eso lo deciden las cuatro condiciones. El puntaje decide a cuál oferta va la familia cuando hay más de una válida.

Cómo se recorre:

1. Se atiende primero a la familia con menos ofertas posibles. A igualdad, se respeta el orden de entrada.
2. Para esa familia se evalúan todas las ofertas con el cupo que les queda en ese momento.
3. Gana la oferta válida con más puntaje. Si hay empate de puntaje, gana la primera por nombre en orden alfabético, así el resultado no depende del orden del archivo.
4. Se descuenta un cupo a la oferta elegida. El horario asignado es el primero en común, por orden alfabético.

## Por qué una familia puede quedar sin pareja

Porque no se fuerza un cruce malo. Si ninguna oferta cumple las cuatro reglas, la familia queda sin asignación y el resultado dice cuál regla la dejó afuera (`failed_rule`):

- `oferta`: no hay ninguna oferta cargada.
- `zona`: no hay ofertas en su zona.
- `horario`: hay ofertas en su zona, pero ninguna con un horario en común.
- `dieta`: hay zona y horario, pero ninguna dieta compatible.
- `cupo`: había una oferta compatible, pero ya no le queda cupo.

Cuando hay varias ofertas, la regla informada es la de la oferta que más cerca estuvo. Además, cada fila trae en `others` el detalle de todas las ofertas descartadas, con todas las reglas que le fallaron a cada una.

## Caso de muestra

Con los seis casos de `data/cases.json`, `python3 -m src.report` da cinco asignaciones y una familia sin asignación:

| Familia | Oferta | Puntaje | zona | horario | dieta | cupo |
|---|---|---|---|---|---|---|
| Familia Ríos | Ana | 90 | 40 | 20 | 20 | 10 |
| Familia Gómez | Carmen | 90 | 40 | 20 | 20 | 10 |
| Familia Paz | Beatriz | 90 | 40 | 20 | 20 | 10 |
| Familia León | Dora | 90 | 40 | 20 | 20 | 10 |
| Familia Ortiz | Elena | 90 | 40 | 20 | 20 | 10 |
| Familia Sol | sin asignación | | | | | |

Familia Sol queda sin asignación por la regla `horario`: vive en la zona Norte y pide `lv-almuerzo`. La única oferta de esa zona es Beatriz, que atiende `sab-almuerzo` y `sab-cena`. La dieta sería compatible (Beatriz ofrece `general`) y Beatriz tenía cupo cuando se evaluó a Familia Sol, pero no hay horario en común.

En esta muestra todos los pares suman 90 porque cada uno comparte un solo horario, tiene la misma dieta y encuentra el cupo completo. Los casos donde el puntaje cambia (varios horarios, dieta por `general`, cupo ya usado) están en los tests.

## Arquitectura

```
data/cases.json      casos de demostración (entrada)
src/match.py         la regla: evaluate() puntúa un par, assign() reparte. Única implementación.
src/report.py        reporte en texto por consola
src/build_demo.py    genera docs/datos.js llamando a assign()
docs/index.html      página estática de la demo
docs/app.js          solo presentación: dibuja lo que hay en datos.js
docs/datos.js        archivo generado, no se edita a mano
tests/test_match.py  regla, reporte y vigencia de docs/datos.js
tests/demo.test.js   presentación de la demo
```

La regla existe en un solo lugar, `src/match.py`. La demo no la reimplementa en JavaScript: `src/build_demo.py` corre `assign()` sobre `data/cases.json` y deja casos, pesos y resultado en `docs/datos.js`. El botón Asignar muestra ese resultado. Un test falla si `docs/datos.js` no coincide con lo que Python genera hoy, de modo que Python y la demo no pueden contradecirse sin que los tests lo avisen.

No hay backend, base de datos, dependencias de ejecución ni secretos. Python 3.10 o superior; `pytest` para los tests; Node solo para el test de la demo.

## Cómo correr

Tests:

```bash
python3 -m pytest -q
node tests/demo.test.js
```

Reporte por consola:

```bash
python3 -m src.report
```

Después de cambiar la regla o los casos, regenerar los datos de la demo:

```bash
python3 -m src.build_demo            # reescribe docs/datos.js
python3 -m src.build_demo --check    # solo verifica, sale con 1 si quedó viejo
```

Demo local: abrir `docs/index.html` en el navegador, o servir la carpeta:

```bash
python3 -m http.server 8000 --directory docs
```

y entrar a http://localhost:8000.

## Límites conocidos

- El reparto es voraz: atiende una familia a la vez y no deshace decisiones. Atender primero a quien tiene menos opciones reduce el problema, pero no garantiza la mayor cantidad posible de asignaciones en todos los casos.
- Zona, horario y dieta se comparan como texto exacto. `Sur` y `sur` son zonas distintas.
- Cada familia ocupa un cupo y recibe una sola oferta.
