# Metodología

## Indicador central

El monitor usa el saldo neto predeterminado en divisa sobre reservas oficiales totales del IRFCL:

\[
R =
\frac{\text{Saldo neto predeterminado}}
{\text{Reservas oficiales totales}}
\]

Donde:

- **Saldo neto predeterminado**: entradas contractuales menos salidas contractuales en moneda extranjera (`RAPFA_USD`).
- **Reservas oficiales totales**: reservas oficiales totales (`RAFA_USD`).

## Convención de signos

- \(R < 0\): las salidas predeterminadas superan las entradas; existe presión potencial sobre reservas.
- \(R > 0\): las entradas superan las salidas; existe holgura contractual.
- Un valor más negativo implica mayor vulnerabilidad de liquidez externa.

Ejemplo: Panamá con \(R=-2.47\) tiene salidas netas predeterminadas equivalentes a 2.47 veces sus reservas.

## Umbrales absolutos

### Economías emisoras

| Rango | Clasificación |
|---:|---|
| \(R \ge 0\) | Holgura |
| \(-1.0 < R < 0\) | Moderada |
| \(-2.0 < R \le -1.0\) | Alta |
| \(R \le -2.0\) | Crítica |

### Economías dolarizadas

Panamá, Ecuador y El Salvador no tienen prestamista de última instancia en moneda propia. Por ello, sus umbrales son más estrictos:

| Rango | Clasificación |
|---:|---|
| \(R \ge -0.5\) | Holgura o baja |
| \(-1.0 < R \le -0.5\) | Moderada |
| \(-2.0 < R \le -1.0\) | Alta |
| \(R \le -2.0\) | Emergencia |

## Segmentación

Los países se analizan en dos grupos:

1. **Emisoras**: banco central emisor con capacidad de proveer liquidez en moneda propia.
2. **Dolarizadas**: Panamá, Ecuador y El Salvador.

No se comparan umbrales entre grupos.

## Drenajes contingentes

Garantías, puttable bonds, líneas de crédito no dibujadas y opciones se reportan y desagregan, pero no entran en el ratio base. Se publica un ratio alternativo ajustado por contingencias.

## Reservas y conciliación

El denominador principal es `RAFA_USD` del IRFCL por comparabilidad internacional. Cuando exista una cifra del banco central, se publica un ratio alternativo y un rango por definición de reservas.

Las diferencias entre IRFCL y bancos centrales pueden provenir de:

- Fecha de corte distinta.
- Valuación de oro, DEG y posiciones en el FMI.
- Activos pignorados o no disponibles.
- Swaps activos o potenciales.
- Depósitos del Tesoro, encajes y pasivos en divisas.

La plantilla de conciliación está en [`docs/RESERVES_RECONCILIATION.md`](docs/RESERVES_RECONCILIATION.md).

## Incertidumbre

Se reportan tres capas:

1. **Definición de reservas**: ratio con IRFCL frente a ratio con reservas locales.
2. **Revisiones históricas**: distribución de revisiones del IRFCL.
3. **Contingencias**: ratio base frente a ratio que incluye pasivos contingentes.

Estos rangos son análisis de sensibilidad, no intervalos de confianza estadísticos.

## Backtesting

Ver [`docs/BACKTESTING.md`](docs/BACKTESTING.md). El objetivo es evaluar si el ratio anticipa crisis de balanza de pagos, crisis cambiarias o defaults externos con horizontes de 12 y 24 meses.

## Limitaciones

- No incorpora flujos futuros de exportaciones, IED o remesas.
- La muestra de crisis para backtesting es pequeña.
- La cobertura de validación local aún es parcial.
- No es asesoría de inversión ni una predicción de crisis.
