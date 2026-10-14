# Ingesta histórica IRFCL

Coloca en cada carpeta un archivo CSV con la serie histórica de reservas internacionales del país.

## Formato requerido

- Separador: coma.
- Primera columna: fecha en formato `YYYY-MM-DD`.
- Segunda columna: reservas internacionales en millones de USD.
- Sin encabezado obligatorio; el script lee la primera y segunda columna.
- Nombre de archivo esperado: `irfcl_<iso3>.csv` en minúsculas.

Ejemplo:

```csv
1998-12-31,1234.5
1999-01-31,1250.0
```

## Archivos esperados

| Carpeta | País | Archivo | Años mínimos requeridos |
|---|---|---|---|
| `data/raw/official/ARG/` | Argentina | `irfcl_arg.csv` | 2019 |
| `data/raw/official/ECU/` | Ecuador | `irfcl_ecu.csv` | 1998, 2007 y 2019 |
| `data/raw/official/MEX/` | México | `irfcl_mex.csv` | 1981 y 1993 |
| `data/raw/official/BRA/` | Brasil | `irfcl_bra.csv` | 1982 y 1998 |
| `data/raw/official/CHL/` | Chile | `irfcl_chl.csv` | 1981 |
| `data/raw/official/URY/` | Uruguay | `irfcl_ury.csv` | 2001 |
| `data/raw/official/VEN/` | Venezuela | `irfcl_ven.csv` | 2013 y 2016 |
| `data/raw/official/DOM/` | República Dominicana | `irfcl_dom.csv` | 2002 |
| `data/raw/official/JAM/` | Jamaica | `irfcl_jam.csv` | 2009 |
| `data/raw/official/BRB/` | Barbados | `irfcl_brb.csv` | 2017 |

## Ejecución

```bash
python src/ingest_irfcl_history.py
```

El script genera:

- `data/processed/irfcl_history_reserves.csv`
- `data/quality_reports/irfcl_history_coverage.csv`

El reporte indica qué países y años quedan pendientes.