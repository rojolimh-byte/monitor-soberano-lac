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
R =
\frac{\text{Saldo neto predeterminado}}
{\text{Reservas oficiales totales}}
\]

Donde:

- **Saldo neto predeterminado**: entradas contractuales menos salidas contractuales en moneda extranjera (`RAPFA_USD`).
- **Reservas oficiales totales**: reservas oficiales totales (`RAFA_USD`).

Un valor negativo implica que las salidas predeterminadas superan las entradas: existe presión potencial sobre las reservas.

Un valor positivo implica entradas netas contractuales: existe holgura de liquidez externa.

Un valor más negativo implica mayor vulnerabilidad de liquidez externa.

## Umbrales absolutos

Los umbrales siguientes son una clasificación descriptiva de severidad contable. **No están validados empíricamente como umbrales de alerta temprana.**

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
| Argentina | -1.53 | No conciliado | Emisora |
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

El ranking relativo se conserva como referencia, pero la métrica central es el ratio crudo.

## Evaluación preliminar del backtesting

El backtesting disponible es preliminar y no constituye una validación empírica del monitor.

La muestra contiene solo dos episodios positivos, ambos de Argentina:

- Argentina 2000, asociado a la crisis de 2001.
- Argentina 2017, asociado a la crisis de 2018.

Con un umbral de -1.0, el indicador identificó ambos episodios, pero generó 9 falsos positivos. La precisión fue de 18.2%.

El umbral de -2.0 no identificó ningún episodio en la muestra disponible. Por ello, los umbrales de -1.0 y -2.0 no están validados empíricamente como umbrales de alerta temprana.

No se calcula ni se presenta un AUC: con solo dos episodios positivos, cualquier métrica de discriminación sería estadísticamente insuficiente.

**Conclusión:** el backtesting actual permite examinar la consistencia interna del indicador, pero no permite afirmar que anticipe crisis ni validar los umbrales de clasificación.

## Reservas: doble reporte

Mientras la conciliación no esté completa, el proyecto reporta:

- **Ratio base IRFCL**: denominador `RAFA_USD`, comparable entre países.
- **Ratio alternativo con reservas locales**: denominador reportado por el banco central, cuando esté disponible.
- **Rango por definición de reservas**: resultado de usar ambas denominaciones.

La conciliación se documenta país por país en [`docs/RESERVES_RECONCILIATION.md`](docs/RESERVES_RECONCILIATION.md).

## Estado de conciliación de reservas

| Estado | Países | Detalle |
|---|---:|---|
| Conciliado dentro de ±2% | 2 | Perú (0.99), México (1.01) |
| Brecha documentada | 3 | Colombia (0.94), Brasil (0.93), Chile (0.89) |
| No conciliado | 1 | Argentina (0.72) |
| Sin validación local | 10 | Resto de la muestra |

Argentina mantiene la brecha más grande: 28%. Hasta resolver la conciliación, se muestra únicamente con el ratio IRFCL y una advertencia visible. Su clasificación absoluta no debe utilizarse para conclusiones comparativas fuertes.

## Incertidumbre y escenarios

Cada país debe reportar:

- Ratio base IRFCL.
- Rango por definición de reservas: IRFCL frente a reservas locales.
- Rango por revisión histórica de datos IRFCL.
- Ratio ajustado por drenajes contingentes.

Estos rangos no deben presentarse como intervalos de confianza estadísticos: son escenarios de sensibilidad basados en definiciones, revisiones y supuestos.

## Hoja de ruta

| Prioridad | Módulo | Entregable |
|---:|---|---|
| 1 | Conciliación de reservas | Resolver la brecha argentina y completar la validación local de los 16 países |
| 2 | Ampliación del backtesting | Incorporar al menos 10 episodios de crisis en múltiples países, con controles y validación temporal |
| 3 | Flujos externos | Añadir exportaciones/PIB, concentración de exportaciones, IED/PIB y remesas/PIB como contexto |
| 4 | CDS y calificaciones | Incorporar CDS a 5 años y calificaciones en moneda extranjera como validadores de mercado |
| 5 | Alertas automáticas | Automatizar IRFCL y reservas locales; generar alertas al cruzar umbrales |
| 6 | Validación externa | Comparar con EMBI y otros indicadores de vulnerabilidad; someter la metodología a revisión externa |

Los flujos y los indicadores de mercado no deben modificar el ratio base: sirven para contextualizar la vulnerabilidad de stock y detectar divergencias entre fundamentos y percepción de mercado.

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
- El backtesting tiene una muestra extremadamente pequeña y no valida los umbrales de clasificación.

## Licencia

MIT
