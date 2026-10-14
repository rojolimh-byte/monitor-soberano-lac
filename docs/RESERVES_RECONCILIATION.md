# Conciliación de reservas

## Objetivo

Documentar, para los 16 países, las diferencias entre las reservas IRFCL (`RAFA_USD`) y las reservas reportadas por cada banco central.

Una brecha no se trata automáticamente como error: debe descomponerse por concepto, fecha de corte, valuación y disponibilidad de activos.

## Prioridad

1. **Argentina**: brecha del 28%; debe resolverse o mantenerse fuera de conclusiones comparativas fuertes.
2. **Panamá, Ecuador y El Salvador**: economías dolarizadas con clasificación crítica o alta.
3. **Brasil, Chile, Colombia, México y Perú**: países con referencias locales ya identificadas.
4. Resto de la muestra.

## Protocolo por país

1. Identificar la fuente oficial local.
2. Igualar la fecha de corte con la observación IRFCL.
3. Descargar reservas en millones de USD.
4. Descomponer la brecha por componentes.
5. Documentar cada componente con fuente y monto.
6. Publicar el estado: `reconciled`, `documented_gap` o `unresolved`.

## Componentes a documentar

| Componente | Descripción |
|---|---|
| Divisas convertibles | Disponibilidades en moneda extranjera |
| Oro monetario | Incluye valuación y tipo de cambio |
| DEG | Derechos Especiales de Giro |
| Posición de reserva en el FMI | Posición trasmisible de inmediato |
| Swaps activos | Recursos efectivamente recibidos |
| Swaps potenciales | Líneas no dibujadas |
| Letras intransferibles | Activos no negociables, si aplican |
| Encajes bancarios | Requisitos de liquidez en divisas, si aplican |
| Depósitos del sector público | Depósitos del Tesoro u otros organismos |
| Activos pignorados | Activos comprometidos o no disponibles |
| Diferencias de valuación | Tipo de cambio, precio del oro y metodología |

## Regla de publicación

- `reconciled`: diferencia dentro de ±2%; se usa IRFCL como denominador principal.
- `documented_gap`: brecha explicada por componentes; se publican ratio IRFCL y ratio alternativo.
- `unresolved`: brecha no explicada; el país se excluye de conclusiones comparativas fuertes.

## Argentina

Argentina se reporta como **no conciliado** hasta que se documenten los componentes de la brecha del 28%.

No se incorporan montos estimados de swaps con China, letras intransferibles, encajes o diferencias de valuación hasta contar con fuentes oficiales.

Mientras tanto:

- Se reporta únicamente el ratio base IRFCL.
- Se muestra una advertencia visible en el dashboard.
- Su clasificación absoluta no debe utilizarse para conclusiones comparativas fuertes.

## Implementación

`src/reserves_reconciliation.py` permite:

- Descomponer la brecha por componentes.
- Calcular la diferencia explicada y no explicada.
- Calcular el ratio base IRFCL.
- Calcular el ratio alternativo con reservas locales.
- Generar un rango por definición de reservas.
