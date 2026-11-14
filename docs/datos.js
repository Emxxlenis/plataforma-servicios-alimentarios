// Archivo generado por `python3 -m src.build_demo`. No editar a mano.
// Fuente de la regla: src/match.py. Fuente de los casos: data/cases.json.
const DEMO = {
  "rules": [
    "zona",
    "horario",
    "dieta",
    "cupo"
  ],
  "weights": {
    "zona": 40,
    "horario": 30,
    "dieta": 20,
    "cupo": 10
  },
  "providers": [
    {
      "name": "Ana",
      "zone": "Sur",
      "slots": [
        "lv-almuerzo"
      ],
      "diet": "casera",
      "capacity": 2
    },
    {
      "name": "Beatriz",
      "zone": "Norte",
      "slots": [
        "sab-almuerzo",
        "sab-cena"
      ],
      "diet": "general",
      "capacity": 1
    },
    {
      "name": "Carmen",
      "zone": "Oriente",
      "slots": [
        "lv-almuerzo"
      ],
      "diet": "baja en sal",
      "capacity": 1
    },
    {
      "name": "Dora",
      "zone": "Sur",
      "slots": [
        "lv-cena"
      ],
      "diet": "casera",
      "capacity": 1
    },
    {
      "name": "Elena",
      "zone": "Oeste",
      "slots": [
        "lv-almuerzo"
      ],
      "diet": "vegetariana",
      "capacity": 1
    }
  ],
  "families": [
    {
      "name": "Familia Ríos",
      "zone": "Sur",
      "slots": [
        "lv-almuerzo"
      ],
      "diet": "casera"
    },
    {
      "name": "Familia Gómez",
      "zone": "Oriente",
      "slots": [
        "lv-almuerzo"
      ],
      "diet": "baja en sal"
    },
    {
      "name": "Familia Paz",
      "zone": "Norte",
      "slots": [
        "sab-almuerzo"
      ],
      "diet": "general"
    },
    {
      "name": "Familia León",
      "zone": "Sur",
      "slots": [
        "lv-cena"
      ],
      "diet": "casera"
    },
    {
      "name": "Familia Ortiz",
      "zone": "Oeste",
      "slots": [
        "lv-almuerzo"
      ],
      "diet": "vegetariana"
    },
    {
      "name": "Familia Sol",
      "zone": "Norte",
      "slots": [
        "lv-almuerzo"
      ],
      "diet": "casera"
    }
  ],
  "rows": [
    {
      "family": "Familia Ríos",
      "zone": "Sur",
      "diet": "casera",
      "turn": 2,
      "provider": "Ana",
      "slot": "lv-almuerzo",
      "score": 90,
      "breakdown": [
        {
          "rule": "zona",
          "ok": true,
          "points": 40,
          "max": 40,
          "detail": "misma zona (Sur)"
        },
        {
          "rule": "horario",
          "ok": true,
          "points": 20,
          "max": 30,
          "detail": "1 horario en común (lv-almuerzo)"
        },
        {
          "rule": "dieta",
          "ok": true,
          "points": 20,
          "max": 20,
          "detail": "misma dieta (casera)"
        },
        {
          "rule": "cupo",
          "ok": true,
          "points": 10,
          "max": 10,
          "detail": "cupo libre 2 de 2"
        }
      ],
      "failed_rule": null,
      "reason": "misma zona, horario en común, dieta compatible y cupo libre",
      "others": [
        {
          "provider": "Beatriz",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "horario"
          ],
          "detail": "zona distinta (Norte y Sur); sin horario en común"
        },
        {
          "provider": "Carmen",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "dieta"
          ],
          "detail": "zona distinta (Oriente y Sur); dieta incompatible (baja en sal y casera)"
        },
        {
          "provider": "Dora",
          "eligible": false,
          "score": null,
          "failed": [
            "horario"
          ],
          "detail": "sin horario en común"
        },
        {
          "provider": "Elena",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "dieta"
          ],
          "detail": "zona distinta (Oeste y Sur); dieta incompatible (vegetariana y casera)"
        }
      ]
    },
    {
      "family": "Familia Gómez",
      "zone": "Oriente",
      "diet": "baja en sal",
      "turn": 3,
      "provider": "Carmen",
      "slot": "lv-almuerzo",
      "score": 90,
      "breakdown": [
        {
          "rule": "zona",
          "ok": true,
          "points": 40,
          "max": 40,
          "detail": "misma zona (Oriente)"
        },
        {
          "rule": "horario",
          "ok": true,
          "points": 20,
          "max": 30,
          "detail": "1 horario en común (lv-almuerzo)"
        },
        {
          "rule": "dieta",
          "ok": true,
          "points": 20,
          "max": 20,
          "detail": "misma dieta (baja en sal)"
        },
        {
          "rule": "cupo",
          "ok": true,
          "points": 10,
          "max": 10,
          "detail": "cupo libre 1 de 1"
        }
      ],
      "failed_rule": null,
      "reason": "misma zona, horario en común, dieta compatible y cupo libre",
      "others": [
        {
          "provider": "Ana",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "dieta"
          ],
          "detail": "zona distinta (Sur y Oriente); dieta incompatible (casera y baja en sal)"
        },
        {
          "provider": "Beatriz",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "horario"
          ],
          "detail": "zona distinta (Norte y Oriente); sin horario en común"
        },
        {
          "provider": "Dora",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "horario",
            "dieta"
          ],
          "detail": "zona distinta (Sur y Oriente); sin horario en común; dieta incompatible (casera y baja en sal)"
        },
        {
          "provider": "Elena",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "dieta"
          ],
          "detail": "zona distinta (Oeste y Oriente); dieta incompatible (vegetariana y baja en sal)"
        }
      ]
    },
    {
      "family": "Familia Paz",
      "zone": "Norte",
      "diet": "general",
      "turn": 4,
      "provider": "Beatriz",
      "slot": "sab-almuerzo",
      "score": 90,
      "breakdown": [
        {
          "rule": "zona",
          "ok": true,
          "points": 40,
          "max": 40,
          "detail": "misma zona (Norte)"
        },
        {
          "rule": "horario",
          "ok": true,
          "points": 20,
          "max": 30,
          "detail": "1 horario en común (sab-almuerzo)"
        },
        {
          "rule": "dieta",
          "ok": true,
          "points": 20,
          "max": 20,
          "detail": "misma dieta (general)"
        },
        {
          "rule": "cupo",
          "ok": true,
          "points": 10,
          "max": 10,
          "detail": "cupo libre 1 de 1"
        }
      ],
      "failed_rule": null,
      "reason": "misma zona, horario en común, dieta compatible y cupo libre",
      "others": [
        {
          "provider": "Ana",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "horario"
          ],
          "detail": "zona distinta (Sur y Norte); sin horario en común"
        },
        {
          "provider": "Carmen",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "horario",
            "cupo"
          ],
          "detail": "zona distinta (Oriente y Norte); sin horario en común; sin cupo libre (0 de 1)"
        },
        {
          "provider": "Dora",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "horario"
          ],
          "detail": "zona distinta (Sur y Norte); sin horario en común"
        },
        {
          "provider": "Elena",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "horario"
          ],
          "detail": "zona distinta (Oeste y Norte); sin horario en común"
        }
      ]
    },
    {
      "family": "Familia León",
      "zone": "Sur",
      "diet": "casera",
      "turn": 5,
      "provider": "Dora",
      "slot": "lv-cena",
      "score": 90,
      "breakdown": [
        {
          "rule": "zona",
          "ok": true,
          "points": 40,
          "max": 40,
          "detail": "misma zona (Sur)"
        },
        {
          "rule": "horario",
          "ok": true,
          "points": 20,
          "max": 30,
          "detail": "1 horario en común (lv-cena)"
        },
        {
          "rule": "dieta",
          "ok": true,
          "points": 20,
          "max": 20,
          "detail": "misma dieta (casera)"
        },
        {
          "rule": "cupo",
          "ok": true,
          "points": 10,
          "max": 10,
          "detail": "cupo libre 1 de 1"
        }
      ],
      "failed_rule": null,
      "reason": "misma zona, horario en común, dieta compatible y cupo libre",
      "others": [
        {
          "provider": "Ana",
          "eligible": false,
          "score": null,
          "failed": [
            "horario"
          ],
          "detail": "sin horario en común"
        },
        {
          "provider": "Beatriz",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "horario",
            "cupo"
          ],
          "detail": "zona distinta (Norte y Sur); sin horario en común; sin cupo libre (0 de 1)"
        },
        {
          "provider": "Carmen",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "horario",
            "dieta",
            "cupo"
          ],
          "detail": "zona distinta (Oriente y Sur); sin horario en común; dieta incompatible (baja en sal y casera); sin cupo libre (0 de 1)"
        },
        {
          "provider": "Elena",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "horario",
            "dieta"
          ],
          "detail": "zona distinta (Oeste y Sur); sin horario en común; dieta incompatible (vegetariana y casera)"
        }
      ]
    },
    {
      "family": "Familia Ortiz",
      "zone": "Oeste",
      "diet": "vegetariana",
      "turn": 6,
      "provider": "Elena",
      "slot": "lv-almuerzo",
      "score": 90,
      "breakdown": [
        {
          "rule": "zona",
          "ok": true,
          "points": 40,
          "max": 40,
          "detail": "misma zona (Oeste)"
        },
        {
          "rule": "horario",
          "ok": true,
          "points": 20,
          "max": 30,
          "detail": "1 horario en común (lv-almuerzo)"
        },
        {
          "rule": "dieta",
          "ok": true,
          "points": 20,
          "max": 20,
          "detail": "misma dieta (vegetariana)"
        },
        {
          "rule": "cupo",
          "ok": true,
          "points": 10,
          "max": 10,
          "detail": "cupo libre 1 de 1"
        }
      ],
      "failed_rule": null,
      "reason": "misma zona, horario en común, dieta compatible y cupo libre",
      "others": [
        {
          "provider": "Ana",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "dieta"
          ],
          "detail": "zona distinta (Sur y Oeste); dieta incompatible (casera y vegetariana)"
        },
        {
          "provider": "Beatriz",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "horario",
            "cupo"
          ],
          "detail": "zona distinta (Norte y Oeste); sin horario en común; sin cupo libre (0 de 1)"
        },
        {
          "provider": "Carmen",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "dieta",
            "cupo"
          ],
          "detail": "zona distinta (Oriente y Oeste); dieta incompatible (baja en sal y vegetariana); sin cupo libre (0 de 1)"
        },
        {
          "provider": "Dora",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "horario",
            "dieta",
            "cupo"
          ],
          "detail": "zona distinta (Sur y Oeste); sin horario en común; dieta incompatible (casera y vegetariana); sin cupo libre (0 de 1)"
        }
      ]
    },
    {
      "family": "Familia Sol",
      "zone": "Norte",
      "diet": "casera",
      "turn": 1,
      "provider": null,
      "slot": null,
      "score": null,
      "breakdown": [],
      "failed_rule": "horario",
      "reason": "en la zona Norte ninguna oferta tiene un horario en común",
      "others": [
        {
          "provider": "Ana",
          "eligible": false,
          "score": null,
          "failed": [
            "zona"
          ],
          "detail": "zona distinta (Sur y Norte)"
        },
        {
          "provider": "Beatriz",
          "eligible": false,
          "score": null,
          "failed": [
            "horario"
          ],
          "detail": "sin horario en común"
        },
        {
          "provider": "Carmen",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "dieta"
          ],
          "detail": "zona distinta (Oriente y Norte); dieta incompatible (baja en sal y casera)"
        },
        {
          "provider": "Dora",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "horario"
          ],
          "detail": "zona distinta (Sur y Norte); sin horario en común"
        },
        {
          "provider": "Elena",
          "eligible": false,
          "score": null,
          "failed": [
            "zona",
            "dieta"
          ],
          "detail": "zona distinta (Oeste y Norte); dieta incompatible (vegetariana y casera)"
        }
      ]
    }
  ]
};

if (typeof module !== "undefined") {
  module.exports = { DEMO };
}
