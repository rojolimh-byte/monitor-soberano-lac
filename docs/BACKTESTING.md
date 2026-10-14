# Backtesting

## Implementación actual

El backtesting usa directamente `resultados/serie_tiempo_vulnerabilidad_continua.csv`.

Episodios positivos disponibles:

- Argentina 2000, asociado a la crisis de 2001.
- Argentina 2017, asociado a la crisis de 2018.

Ecuador 1998, Turquía 2017 y Sri Lanka 2021 no están disponibles en la serie histórica actual, por lo que no pueden incluirse todavía.

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

La muestra actual contiene solo dos episodios positivos. Por ello, las métricas son ilustrativas y no permiten inferir un AUC robusto ni afirmar que el indicador predice crisis.

Para ampliar el backtesting hay que incorporar la serie histórica de Ecuador antes de 1999, Turquía antes de 2018 y Sri Lanka antes de 2022, además de controles sin crisis.
