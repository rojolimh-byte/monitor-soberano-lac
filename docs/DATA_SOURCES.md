# Fuentes de datos

## IMF IRFCL

- URL: https://data.imf.org/en/datasets/IMF.STA:IRFCL
- Series principales: `RAPFA_USD` y `RAFA_USD`.
- Frecuencia: anual, mensual, trimestral o diaria según país.
- Uso: saldo neto predeterminado y reservas oficiales totales.

## IMF WEO

- URL: https://www.imf.org/en/Publications/WEO
- Uso: contexto macroeconómico; no es componente del ratio principal.

## Bancos centrales

- Uso: validación y conciliación de reservas locales.
- Prioridad: Argentina, Brasil, Chile, Colombia, México y Perú.
- Campos obligatorios: fecha de corte, reservas en millones de USD, valuación, swaps y activos no disponibles.

## Reglas

- Toda descarga debe registrar fecha, URL y versión.
- Toda brecha IRFCL-banco central debe documentarse en `docs/RESERVES_RECONCILIATION.md`.
- Los datos de backtesting deben incluir controles sin crisis y validación temporal.
