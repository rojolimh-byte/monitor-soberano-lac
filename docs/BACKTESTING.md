# Backtesting

## Alcance y advertencia

El backtesting disponible es **preliminar** y no constituye una validación empírica del monitor.

La muestra contiene solo dos episodios positivos, ambos de Argentina. No se calcula ni se presenta un AUC.

## Alcance geográfico

El backtesting se limita a países del continente americano.

No se incluyen Turquía ni Sri Lanka como episodios de evaluación.

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

## Umbrales evaluados

- -3.0
- -2.0
- -1.5
- -1.0
- -0.5
- 0.0

## Métricas

- Verdaderos positivos.
- Falsos positivos.
- Falsos negativos.
- Verdaderos negativos.
- Recall.
- Precisión.
- Tasa de falsos positivos.

## Limitación crítica

La muestra actual contiene solo dos episodios positivos, ambos de Argentina. Por ello:

- No se calcula ni se presenta un AUC.
- Las métricas son ilustrativas.
- No se puede afirmar que el indicador anticipe crisis.
- No se pueden validar empíricamente los umbrales de -1.0 ni -2.0.

Para ampliar el backtesting hay que incorporar la serie histórica de Ecuador antes de 1999, episodios de crisis en otros países americanos y controles sin crisis adicionales.
