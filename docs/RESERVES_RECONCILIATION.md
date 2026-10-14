# Conciliación de reservas

## Objetivo

Documentar, para los 16 países, las diferencias entre las reservas IRFCL (`RAFA_USD`) y las reservas reportadas por cada banco central.

Una brecha no se trata automáticamente como error: debe descomponerse por concepto, fecha de corte, valuación y disponibilidad de activos.

## Campos obligatorios

| Campo | Descripción |
|---|---|
| `country` | País |
| `country_iso3` | Código ISO 3166-1 alfa-3 |
| `irfcl_date` | Fecha de corte IRFCL |
| `local_date` | Fecha de corte de la fuente local |
| `reserves_irfcl_usd_mn` | Reservas IRFCL en millones de USD |
| `reserves_local_usd_mn` | Reservas reportadas por el banco central |
| `difference_usd_mn` | Reservas locales menos IRFCL |
| `ratio_irfcl_local` | IRFCL dividido por reservas locales |
| `fx_valuation_note` | Tipo de cambio y método de valuación |
| `gold_sdr_note` | Tratamiento de oro y DEG |
| `pledged_assets` | Activos pignorados o no disponibles |
| `treasury_deposits` | Depósitos del Tesoro o sector público |
| `reserve_requirements` | Encajes relevantes |
| `swaps_active` | Swaps efectivamente recibidos |
| `swaps_potential` | Líneas de swap no dibujadas |
| `explanation` | Explicación de la brecha |
| `status` | `reconciled`, `documented_gap` o `unresolved` |

## Regla de publicación

- Si el estado es `reconciled`, se usa IRFCL como denominador principal.
- Si el estado es `documented_gap`, se publica el ratio base IRFCL y un ratio alternativo con reservas locales.
- Si el estado es `unresolved`, el país se marca como no conciliado y se excluye de conclusiones comparativas fuertes hasta documentar la brecha.

## Plantilla

La plantilla está en `data/validation/reconciliation_template.csv`.

## Prioridad

1. Argentina, por la brecha documentada frente al BCRA.
2. Brasil, Chile, Colombia, México y Perú, países ya parcialmente validados.
3. Resto de la muestra.
