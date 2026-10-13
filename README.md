# Monitor Soberano LAC

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Data: IMF IRFCL](https://img.shields.io/badge/Data-IMF%20IRFCL-blueviolet)](https://data.imf.org/en/datasets/IMF.STA:IRFCL)
[![Live Demo](https://img.shields.io/badge/Live-Demo-success)](https://monitor-soberano-lac.streamlit.app)
[![Countries: 16 LAC](https://img.shields.io/badge/Countries-16%20LAC-orange)]()

**Monitor de vulnerabilidad externa para 16 países de América Latina y el Caribe**, basado en el template IRFCL del FMI (International Reserves and Foreign Currency Liquidity).

![Índice de vulnerabilidad](reports/indice_vulnerabilidad_integral_latam_2025.png)

## El problema

Los países de América Latina enfrentan vencimientos de deuda externa, derivados y otros compromisos en moneda extranjera que pueden drenar sus reservas internacionales. Cuando esos drenajes superan las reservas disponibles, el país queda expuesto a crisis de balanza de pagos, devaluaciones y pérdida de acceso a mercados.

**Monitor Soberano LAC** responde una pregunta concreta: *¿qué países de la región no tienen reservas suficientes para cubrir sus compromisos externos de corto plazo?*

## Para quién

- **Analistas de riesgo soberano** que necesitan una lectura rápida de exposición externa.
- **Inversionistas** que evalúan riesgo país antes de asignar capital.
- **Investigadores y hacedores de política pública** que monitorean vulnerabilidad externa regional.

## Qué cubre

| Dimensión | Indicador | Fuente | Cobertura |
|---|---|---|---|
| Vulnerabilidad externa | Drenajes predeterminados y contingentes sobre reservas | IMF IRFCL | 16 países |
| Composición del riesgo | Drenajes por instrumento: deuda, derivados, repos, garantías, líneas de crédito, puttable bonds | IMF IRFCL | 16 países |
| Reservas oficiales | Reservas internacionales (validación cruzada) | BCRA, BCH, BanRep | ARG, CHL, COL |
| Contexto macro | Deuda del gobierno general (% PIB) | IMF WEO | 5 países |

**Países**: Argentina, Brasil, Chile, Colombia, Costa Rica, Ecuador, El Salvador, Guatemala, Honduras, México, Nicaragua, Panamá, Paraguay, Perú, República Dominicana y Uruguay.

## Resultado principal (2025)

| Ranking | País | Índice de vulnerabilidad |
|---|---|---|
| 1 | Panamá | 0.94 |
| 2 | Ecuador | 0.88 |
| 3 | Argentina | 0.81 |
| ... | ... | ... |
| 14 | México | 0.13 |
| 15 | Brasil | 0.06 |
| 16 | Chile | 0.00 |

Los países con drenajes que superan sus reservas (Panamá, Ecuador, Argentina) concentran el mayor riesgo; Chile, Brasil y México muestran el mayor colchón externo, en parte por líneas de crédito contingentes que actúan como fuentes potenciales de divisas.

## Metodología

El índice se construye con el ratio de **drenajes predeterminados sobre reservas** del FMI (IRFCL), normalizado por percentil dentro de cada año:

- **Drenajes predeterminados**: obligaciones en divisa con vencimiento cierto en los próximos 12 meses (amortizaciones de deuda, forwards/futuros, repos).
- **Drenajes contingentes**: pasivos potenciales (garantías colaterales, puttable bonds, líneas de crédito no dibujadas, opciones).
- **Normalización**: rank percentil invertido — un valor cercano a 1 indica que los drenajes superan ampliamente las reservas (alta vulnerabilidad).

La validación cruzada entre reservas del FMI (`RAFA_USD`) y valores de referencia públicos para 2024 confirma la consistencia de la serie para las economías principales (Brasil 0.93, Chile 0.89, Colombia 0.94, Perú 0.99, México 1.01).

Ver [docs/METHODOLOGY.md](docs/METHODOLOGY.md) para el detalle completo.

## Instalación y ejecución

```bash
git clone [https://github.com/rojolimh-byte/monitor-soberano-lac.git](https://github.com/rojolimh-byte/monitor-soberano-lac.git)
cd monitor-soberano-lac
pip install -r requirements.txt

# Dashboard interactivo
streamlit run app.py
```

## Fuentes y frecuencia

- **IMF IRFCL**: actualización mensual/trimestral según país. [https://data.imf.org/en/datasets/IMF.STA:IRFCL](https://data.imf.org/en/datasets/IMF.STA:IRFCL)
- **IMF WEO**: actualización semestral (abril/octubre).
- **Bancos centrales** (ARG, CHL, COL): frecuencia diaria/mensual.

## Limitaciones

- Las reservas locales y la deuda WEO tienen cobertura parcial (3 y 5 países respectivamente), por lo que se usan como validación y contexto, no como componentes del índice.
- El índice mide vulnerabilidad de stock; no incorpora flujos futuros de ingresos de divisas (exportaciones, IED, remesas).
- Las reservas IRFCL usadas en la serie de tiempo corresponden a divisa convertible, excluyendo oro y DEG.

## Próximos pasos

- [x] Dashboard interactivo deployado (Streamlit Cloud) — [ver demo](https://monitor-soberano-lac.streamlit.app)
- [ ] Ampliar cobertura de reservas locales a más países
- [ ] Incorporar spreads de CDS y calificaciones crediticias
- [ ] Backtesting sistemático contra episodios de crisis
- [ ] Alertas automáticas cuando el índice supera umbrales

## Licencia

MIT
