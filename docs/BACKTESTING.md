# Backtesting

## Objetivo

Evaluar si el saldo neto predeterminado sobre reservas anticipa crisis de balanza de pagos, crisis cambiarias o defaults externos.

## Diseño

- Unidad de observación: país-año.
- Horizontes: 12 y 24 meses antes del episodio.
- Variable dependiente: inicio de crisis de balanza de pagos, crisis cambiaria, default externo o programa financiero no precautorio del FMI.
- Validación: temporal o leave-one-country-out. No se usa una partición aleatoria simple.

## Episodios iniciales

| País | Año | Tipo de episodio |
|---|---:|---|
| Argentina | 2001 | Default y crisis de balanza de pagos |
| Ecuador | 1999 | Crisis bancaria y dolarización |
| Argentina | 2018 | Crisis cambiaria y programa con FMI |
| Turquía | 2018 | Crisis cambiaria, caso externo |
| Sri Lanka | 2022 | Default soberano, caso externo |

Los episodios globales de 2008-2009 y 2020 se tratan como shocks comunes, idealmente con efectos fijos temporales.

## Métricas

- Recall o tasa de verdaderos positivos.
- Precisión.
- Tasa de falsos positivos.
- AUC con intervalo bootstrap.
- Curva ROC y curva de ganancia.

## Umbral

El umbral no se fija por conveniencia. Se selecciona según el costo relativo de un falso positivo frente a un falso negativo.

## Advertencia

Con pocos episodios de crisis, el AUC puede ser muy inestable. Los resultados deben reportarse con intervalos bootstrap y nunca presentarse como prueba causal.
