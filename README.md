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
|---|---|
| \(R \ge -0.5\) | Holgura o vulnerabilidad baja |
| \(-1.0 < R \le -0.5\) | Vulnerabilidad moderada |
| \(-2.0 < R \le -1.0\) | Vulnerabilidad alta |
| \(R \le -2.0\) | Emergencia |

## Segmentación monetaria

El dashboard y los análisis separan:

- **Emisoras**: países con banco central emisor y capacidad de actuar como prestamista de última instancia.
- **Dolarizadas**: Panamá, Ecuador y El Salvador.

No se comparan umbrales entre grupos: un mismo valor de \(R\) tiene implicaciones distintas según el régimen monetario.

## Muestra de episodios de crisis

Se definieron **18 episodios de crisis** en América Latina y economías comparables (1982-2023) usando criterios operativos de crisis externa:

1. Devaluación nominal superior al 15% en 12 meses.
2. Pérdida de reservas superior al 20% en 12 meses.
3. Default soberano o reestructuración de deuda externa.
4. Programa del FMI con condicionalidad.
5. Crisis bancaria sistémica con presión sobre la liquidez externa.

Los episodios se seleccionaron por su relevancia para la liquidez externa: no todos cumplen los cuatro primeros criterios, pero cada uno implica presión potencial sobre reservas o acceso a financiamiento.

Fuentes de referencia: Reinhart-Rogoff, bases de crisis del FMI y bancos centrales nacionales.

**Estado de evaluabilidad**:

| Estado | N | Definición |
|---|---:|---|
| Definidos | 18 | Episodios incluidos en `CRISIS_EPISODES` |
| Con datos IRFCL disponibles | 2 | Tienen observación del año previo ingesta­da |
| **Evaluables en backtesting** | **2** | Argentina 2000 y Argentina 2017 |

La diferencia entre definidos y evaluables refleja que los archivos IRFCL históricos de los demás episodios aún no fueron cargados ni procesados.

## Resultado principal (2024)

| País | Ratio crudo | Clasificación absoluta | Grupo | Confiabilidad reservas |
|---|---:|---|---|---|
| Panamá | -2.47 | Crítica | Dolarizada | ⚪ Sin validación |
| Argentina | -1.53 | No conciliado | Emisora | 🔴 Brecha crítica (0.72) |
| Ecuador | -1.31 | Alta | Dolarizada | ⚪ Sin validación |
| El Salvador | -0.55 | Moderada | Dolarizada | ⚪ Sin validación |
| República Dominicana | -0.51 | Moderada | Emisora | ⚪ Sin validación |
| Paraguay | -0.28 | Moderada | Emisora | ⚪ Sin validación |
| Uruguay | -0.22 | Moderada | Emisora | ⚪ Sin validación |
| Costa Rica | -0.19 | Moderada | Emisora | ⚪ Sin validación |
| Chile | -0.10 | Moderada | Emisora | 🟡 Brecha menor (0.89) |
| Nicaragua | -0.10 | Moderada | Emisora | ⚪ Sin validación |
| Colombia | -0.10 | Moderada | Emisora | 🟡 Brecha menor (0.94) |
| Honduras | -0.09 | Moderada | Emisora | ⚪ Sin validación |
| Guatemala | -0.06 | Moderada | Emisora | ⚪ Sin validación |
| Perú | -0.05 | Moderada | Emisora | 🟢 Conciliado (0.99) |
| México | -0.04 | Moderada | Emisora | 🟢 Conciliado (1.01) |
| Brasil | 0.04 | Holgura | Emisora | 🟡 Brecha menor (0.93) |

El ranking relativo se conserva como referencia, pero la métrica central es el ratio crudo.

**Nota**: la confiabilidad se refiere exclusivamente al denominador (reservas). El numerador (drenajes netos) proviene del IRFCL y no tiene validación cruzada en este proyecto. Un ratio con reservas conciliadas no implica que el numerador sea exacto.

## Evaluación descriptiva del backtesting

El backtesting disponible es preliminar y no constituye una validación empírica del monitor.

**Advertencia**: esta evaluación es descriptiva sobre 2 episodios positivos; las métricas de discriminación no son estadísticamente interpretables con una muestra tan pequeña.

| Umbral | Crisis anticipadas | Recall | Precisión | Falsos positivos |
|---|---|---|---|---|
| -1.0 | 2 de 2 | 100% | 18.2% | 9 |

El umbral de -2.0 no identificó ningún episodio (recall 0%). La grilla completa de umbrales se genera en `resultados/backtesting_metrics.csv` al ejecutar el pipeline.

**Lectura**: el umbral de -1.0 identifica ambos episodios, pero con 9 falsos positivos. Esto no valida los umbrales; sugiere que la clasificación actual es descriptiva, no predictiva.

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

## Módulos de contexto

Además del ratio base, el proyecto incorpora dos módulos de contexto que **no modifican el ratio** y sirven para detectar divergencias entre fundamentos y percepción de mercado.

### Flujos externos

**Estado**: implementado (v0.1), sin validación externa.

**Indicadores**: exportaciones/PIB, concentración de exportaciones (HHI), IED/PIB y remesas/PIB.

**Uso**: contextualizar la vulnerabilidad de stock con la resiliencia de flujos. Un país con ratio vulnerable pero alta resiliencia de flujos enfrenta una presión distinta.

**Limitación**: los flujos son anuales y tienen rezago; no son indicadores adelantados.

### Mercado (CDS y calificaciones)

**Estado**: implementado (v0.1), sin validación externa.

**Indicadores**: CDS a 5 años, calificación en moneda extranjera y divergencia entre fundamentos y percepción de mercado.

**Uso**: detectar complacencia de mercado o prima de riesgo no explicada por el ratio.

**Limitación**: la cobertura de CDS es incompleta en la muestra.

**Nota**: los módulos de flujos y mercado son contexto, no componentes del ratio. En ningún caso modifican el ratio base.

## Hoja de ruta

| Estado | Módulo | Entregable |
|---|---|---|
| ✅ Implementado v0.1 | Flujos externos | Exportaciones, IED, remesas, HHI |
| ✅ Implementado v0.1 | Mercado | CDS, calificaciones, divergencias |
| 🟡 En progreso | Conciliación de reservas | Framework por componente; faltan 10 países |
| 🟡 En progreso | Backtesting | 18 episodios definidos; 2 evaluables hasta ingestar históricos |
| ⚪ Pendiente | Alertas automáticas | Automatizar IRFCL y reservas locales |
| ⚪ Pendiente | Validación externa | Comparar con EMBI; someter la metodología a revisión externa |

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
- El backtesting tiene 18 episodios definidos, pero solo 2 evaluables con datos disponibles; no valida los umbrales de clasificación.

## Licencia

MIT
