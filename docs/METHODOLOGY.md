# Metodología

## Indicador central

El monitor se basa en el ratio de **drenajes predeterminados sobre reservas internacionales** del template IRFCL del FMI:

\[
\text{ratio} = \frac{\text{drenajes netos predeterminados}}{\text{reservas oficiales totales}}
\]

- **Drenajes predeterminados** (`RAPFA_USD`): obligaciones en moneda extranjera con vencimiento cierto en los próximos 12 meses — amortizaciones de deuda externa, forwards/futuros, repos y otros pasivos por determinar.
- **Reservas oficiales totales** (`RAFA_USD`): incluyen divisa convertible, títulos, oro, DEG y posición de reserva en el FMI.

## Convención de signos

En la serie histórica, un drenaje negativo indica salida neta de divisas. Por lo tanto:

- Ratio más negativo = los drenajes superan las reservas = **mayor vulnerabilidad**.
- El índice se calcula como rank percentil del ratio dentro de la muestra de 16 países por año, asignando índice 1.0 al ratio más negativo.

## Normalización

El índice es un **ranking relativo** dentro de la muestra, no una medida absoluta de vulnerabilidad. Una diferencia de 0.06 entre países consecutivos no implica que la brecha real de drenajes sea pequeña; para la magnitud se consulta el ratio crudo.

## Drenajes contingentes

Los pasivos contingentes (garantías colaterales, puttable bonds, líneas de crédito no dibujadas, opciones) se reportan y desagregan por instrumento, pero **no entran en el cálculo del ratio principal**.

## Filtros y validación

- Se excluyen observaciones con reservas menores a 100 M USD para evitar ratios distorsionados.
- Las reservas de la serie histórica provienen de `RAFA_USD` (reservas totales), validadas contra valores de referencia públicos para 2024 (Brasil ~330k M, México ~232k M, Perú ~79k M, etc.).
- Validación cruzada con reservas oficiales locales (BCRA, BCH, BanRep) para Argentina, Chile y Colombia.

## Economías dolarizadas

Panamá, Ecuador y El Salvador no emiten moneda propia. Sus reservas cumplen una función de liquidez sin prestamista de última instancia en moneda propia, por lo que un ratio elevado indica vulnerabilidad **más severa**, no directamente comparable con países emisores.

## Limitaciones

- Mide vulnerabilidad de stock; no incorpora flujos futuros de ingresos de divisas (exportaciones, IED, remesas).
- La cobertura histórica varía por país (Ecuador y Panamá tienen menos años disponibles).
- No es asesoría de inversión.


## Nota sobre México (validación 2024)

El cociente IRFCL/referencia para México (1.01) se ubica levemente por encima de 1, a diferencia del resto de los países validados. Esto refleja una diferencia de definición o fecha de corte entre la serie IRFCL y las reservas totales publicadas por Banxico, y se documenta como tal para transparencia.


## Changelog de cálculo

**2026-10**: se regeneró el índice desde la serie consolidada `vulnerabilidad_reservas_latam_2025_completa.csv`, que incorpora observaciones actualizadas de IRFCL y una definición uniforme de drenajes netos predeterminados (entradas contractuales menos salidas en el horizonte de 12 meses). Como resultado, los ratios y el ranking cambiaron respecto de la versión anterior (por ejemplo, Panamá pasó de -1.04 a -2.47 y Argentina de -2.06 a -1.53). La versión vigente es la publicada en `resultados/indice_vulnerabilidad_integral_latam_2025.csv`.

**Denominador del índice**: se usa la serie IRFCL `RAFA_USD` (reservas oficiales totales del FMI). Para Argentina, cuyo cociente de validación es 0.72, se mantiene el denominador IRFCL por consistencia metodológica entre países; la brecha frente a la referencia del BCRA se documenta en el README y su causa específica está pendiente de verificación.
