# Monitor Soberano LAC

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Data: IMF IRFCL](https://img.shields.io/badge/Data-IMF%20IRFCL-blueviolet)](https://data.imf.org/en/datasets/IMF.STA:IRFCL)
[![Live Demo](https://img.shields.io/badge/Live-Demo-success)](https://monitor-soberano-lac.streamlit.app)

**Monitor de vulnerabilidad externa (IRFCL-FMI) para 16 países de América Latina y el Caribe.**

![Índice de vulnerabilidad](reports/indice_vulnerabilidad_integral_latam_2025.png)

> **Datos a: 2024** (último año con observación anual completa y validada en IMF IRFCL al momento de la construcción del índice).

> ⚠️ **Aviso**: herramienta informativa; no constituye asesoría de inversión ni una predicción de crisis.

## Qué mide

El monitor estima la posición externa predeterminada de un país en los próximos 12 meses:

\[
R = \frac{\text{Entradas contractuales} - \text{Salidas contractuales}}{\text{Reservas oficiales totales}}
\]

- `RAPFA_USD` del IRFCL se interpreta como el **saldo neto predeterminado**: entradas contractuales menos salidas contractuales en divisa.
- `RAFA_USD` corresponde a reservas oficiales totales.
- Un valor **negativo** implica que las salidas predeterminadas superan las entradas: hay presión potencial sobre reservas.
- Un valor **positivo** implica entradas netas contractuales: holgura de liquidez externa.

## Umbrales absolutos

El indicador principal ya no se presenta solo como ranking relativo. Se clasifica con umbrales absolutos:

| Ratio \(R\) | Clasificación | Lectura |
|---:|---|---|
| \(R \ge 0\) | Holgura | Entradas netas predeterminadas |
| \(-1.0 < R < 0\) | Vulnerabilidad moderada | Salidas netas inferiores a las reservas |
| \(-2.0 < R \le -1.0\) | Vulnerabilidad alta | Salidas netas entre 1 y 2 veces las reservas |
| \(R \le -2.0\) | Vulnerabilidad crítica | Salidas netas iguales o superiores a 2 veces las reservas |

Para economías dolarizadas —Panamá, Ecuador y El Salvador— se usan umbrales más estrictos porque no existe prestamista de última instancia en moneda propia:

| Ratio \(R\) | Clasificación dolarizada |
|---:|---|
| \(R \ge -0.5\) | Holgura o vulnerabilidad baja |
| \(-1.0 < R \le -0.5\) | Vulnerabilidad moderada |
| \(-2.0 < R \le -1.0\) | Vulnerabilidad alta |
| \(R \le -2.0\) | Emergencia |

## Segmentación monetaria

El dashboard y los análisis separan:

- **Emisoras**: países con banco central emisor y capacidad de actuar como prestamista de última instancia.
- **Dolarizadas**: Panamá, Ecuador y El Salvador.

No se comparan umbrales entre grupos: un mismo valor de \(R\) tiene implicaciones distintas según el régimen monetario.

## Resultado principal (2024)

| País | Ratio crudo | Clasificación absoluta | Grupo |
|---|---:|---|---|
| Panamá | -2.47 | Crítica | Dolarizada |
| Argentina | -1.53 | Alta | Emisora |
| Ecuador | -1.31 | Alta | Dolarizada |
| El Salvador | -0.55 | Moderada | Dolarizada |
| República Dominicana | -0.51 | Moderada | Emisora |
| Paraguay | -0.28 | Moderada | Emisora |
| Uruguay | -0.22 | Moderada | Emisora |
| Costa Rica | -0.19 | Moderada | Emisora |
| Chile | -0.10 | Moderada | Emisora |
| Nicaragua | -0.10 | Moderada | Emisora |
| Colombia | -0.10 | Moderada | Emisora |
| Honduras | -0.09 | Moderada | Emisora |
| Guatemala | -0.06 | Moderada | Emisora |
| Perú | -0.05 | Moderada | Emisora |
| México | -0.04 | Moderada | Emisora |
| Brasil | 0.04 | Holgura | Emisora |

El ranking relativo se conserva como referencia, pero la métrica central es el ratio crudo y su clasificación absoluta.

## Reservas: doble reporte

Mientras la conciliación no esté completa, el proyecto reporta:

- **Ratio base IRFCL**: denominador `RAFA_USD`, comparable entre países.
- **Ratio alternativo con reservas locales**: denominador reportado por el banco central, cuando esté disponible.
- **Rango por definición de reservas**: resultado de usar ambas denominaciones.

La conciliación se documenta país por país en [`docs/RESERVES_RECONCILIATION.md`](docs/RESERVES_RECONCILIATION.md).

## Incertidumbre y escenarios

Cada país debe reportar:

- Ratio base IRFCL.
- Rango por definición de reservas: IRFCL frente a reservas locales.
- Rango por revisión histórica de datos IRFCL.
- Ratio ajustado por drenajes contingentes.

Estos rangos no deben presentarse como intervalos de confianza estadísticos: son escenarios de sensibilidad basados en definiciones, revisiones y supuestos.

## Backtesting

El backtesting se limita a países del continente americano.

Episodios disponibles en la serie histórica actual:

- Argentina 2001.
- Argentina 2018.

La evaluación utiliza el año previo a cada episodio —Argentina 2000 y Argentina 2017— y todos los demás países y años disponibles como observaciones de control.

La evaluación reporta verdaderos positivos, falsos positivos, falsos negativos, recall, precisión y tasa de falsos positivos para distintos umbrales. Con solo dos episodios positivos, las métricas son ilustrativas y no permiten inferir un AUC robusto.

## Instalación y ejecución

```bash
git clone https://github.com/rojolimh-byte/monitor-soberano-lac.git
cd monitor-soberano-lac
pip install -r requirements.txt
make all
streamlit run dashboards/app.py
pytest -q
```

## Fuentes

- IMF IRFCL: <https://data.imf.org/en/datasets/IMF.STA:IRFCL>
- IMF WEO: <https://www.imf.org/en/Publications/WEO>
- Bancos centrales nacionales para validación de reservas.

## Limitaciones

- El indicador mide posiciones predeterminadas de liquidez; no incorpora flujos futuros como exportaciones, IED o remesas.
- Los drenajes contingentes se reportan, pero no entran en el ratio base.
- La validación local de reservas aún no cubre los 16 países.
- El backtesting tiene una muestra pequeña de crisis y sus métricas deben interpretarse con cautela.

## Licencia

MIT
