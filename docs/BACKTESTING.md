# Backtesting

## Estado actual

El backtesting disponible es **preliminar** y no constituye una validación empírica del monitor.

La muestra vigente contiene solo dos episodios positivos, ambos de Argentina:

- Argentina 2000, asociado a la crisis de 2001.
- Argentina 2017, asociado a la crisis de 2018.

Por ello, no se calcula ni se presenta un AUC.

## Alcance geográfico

La evaluación vigente se limita a países del continente americano con datos disponibles.

El código ya contempla episodios candidatos de economías comparables —incluidos Turquía y Sri Lanka—, pero estos no se evalúan hasta incorporar sus series históricas de saldo neto predeterminado y reservas.

## Episodios disponibles

| País | Año de crisis | Año previo utilizado |
|---|---:|---:|
| Argentina | 2001 | 2000 |
| Argentina | 2018 | 2017 |

Ecuador 1999 no puede incluirse todavía porque su observación de 1998 no está disponible en la serie histórica actual.

## Regla de alerta

Una alerta se define como:

\[
R \le \text{umbral}
\]

donde \(R\) es el saldo neto predeterminado sobre reservas. Valores más negativos implican mayor presión potencial sobre reservas.

## Marco ampliado

`src/backtesting.py` implementa:

- Lista ampliada de episodios candidatos.
- AUC mediante la estadística U de Mann-Whitney.
- Intervalo bootstrap al 95% con 10.000 réplicas.
- Validación temporal walk-forward.
- Calibración de umbrales mediante recall, precisión y F1.

El AUC se calculará únicamente cuando la muestra tenga al menos cinco episodios positivos en múltiples países.

## Criterios de validación

Para considerar validados los umbrales se requiere:

- Al menos 12 episodios de crisis.
- Al menos 8 países distintos.
- AUC con intervalo bootstrap al 95%.
- Intervalo de confianza con ancho inferior a 0.20.
- F1 superior a 0.5 para el umbral óptimo.
- Precisión superior a 50% para el umbral óptimo.

## Limitación crítica

Con solo dos episodios positivos, ambos de Argentina, las métricas son ilustrativas. No se puede afirmar que el indicador anticipe crisis ni validar empíricamente los umbrales de -1.0 ni -2.0.

Para ampliar el backtesting hay que incorporar la serie histórica de Ecuador antes de 1999, episodios de crisis en otros países americanos y controles sin crisis adicionales.
