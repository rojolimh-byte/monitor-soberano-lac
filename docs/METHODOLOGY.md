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
