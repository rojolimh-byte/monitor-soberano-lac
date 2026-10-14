import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from index import classify_regime, classify_vulnerability, definition_range

st.set_page_config(page_title="Monitor Soberano LAC", page_icon="🌎", layout="wide")

RUTA_RESULTADOS = ROOT / "resultados" / "indice_vulnerabilidad_integral_latam_2025.csv"
RUTA_SERIE = ROOT / "resultados" / "serie_tiempo_vulnerabilidad_continua.csv"
DOLARIZADAS = ["Panamá", "Ecuador", "El Salvador"]


@st.cache_data
def cargar_datos():
    df = pd.read_csv(RUTA_RESULTADOS)
    df = df.rename(columns={
        "COUNTRY": "pais",
        "predeterminados_sobre_reservas": "ratio",
    })
    df["pais"] = df["pais"].replace({
        "Panama": "Panamá", "Brazil": "Brasil", "Mexico": "México",
        "Peru": "Perú", "Dominican Republic": "República Dominicana",
    })
    df["regimen"] = df["pais"].apply(classify_regime)
    df["clasificacion_absoluta"] = df.apply(
        lambda row: classify_vulnerability(row["ratio"], row["pais"]), axis=1
    )

    df_serie = None
    if RUTA_SERIE.exists():
        ds = pd.read_csv(RUTA_SERIE)
        ds = ds[(ds["anio"] >= 2010) & (ds["reservas"] > 100)].copy()
        if "indice_vulnerabilidad" not in ds.columns or ds["indice_vulnerabilidad"].isna().all():
            ds["indice_vulnerabilidad"] = ds.groupby("anio")["ratio_drenaje_reservas"].rank(
                pct=True, ascending=False
            )
        df_serie = ds
    return df, df_serie


df, df_serie = cargar_datos()

st.title("🌎 Monitor Soberano LAC")
st.caption(
    "Vulnerabilidad externa predeterminada (IRFCL / reservas) para 16 países de América Latina "
    "y el Caribe · Datos a 2024 · Fuente: IMF IRFCL"
)
st.warning("⚠️ Herramienta de análisis. No constituye asesoría de inversión ni una predicción de crisis.")

st.tabs([
    "📊 Resumen",
    "🏦 Emisoras",
    "💵 Dolarizadas",
    "🔍 Reservas",
    "🧪 Backtesting",
    "📖 Metodología",
])

st.sidebar.header("Filtros")
paises = st.sidebar.multiselect(
    "Países", options=sorted(df["pais"].unique()), default=sorted(df["pais"].unique())
)
df_f = df[df["pais"].isin(paises)].copy()

st.subheader("Clasificación absoluta")
st.dataframe(
    df_f[["pais", "ratio", "clasificacion_absoluta", "regimen", "indice_vulnerabilidad"]]
    .sort_values("ratio")
    .style.background_gradient(subset=["ratio"], cmap="RdYlGn"),
    use_container_width=True,
    hide_index=True,
)

st.subheader("Ratio crudo")
fig = px.bar(
    df_f.sort_values("ratio"),
    x="ratio",
    y="pais",
    orientation="h",
    color="clasificacion_absoluta",
    labels={"ratio": "Saldo neto predeterminado / reservas", "pais": ""},
    title="Posición externa predeterminada (2024)",
)
fig.update_layout(height=600)
st.plotly_chart(fig, use_container_width=True)

st.info(
    "Un valor negativo implica salidas netas predeterminadas y presión potencial sobre reservas. "
    "Un valor positivo implica entradas netas contractuales."
)

if df_serie is not None and not df_serie.empty:
    st.subheader("Evolución 2010-2024")
    paises_disponibles = sorted(df_serie["pais"].unique())
    seleccion = st.multiselect(
        "Países",
        options=paises_disponibles,
        default=[p for p in ["Argentina", "Brasil", "Chile", "Ecuador", "México"] if p in paises_disponibles],
    )
    df_s = df_serie[df_serie["pais"].isin(seleccion)].sort_values(["pais", "anio"])
    if not df_s.empty:
        fig_serie = px.line(
            df_s,
            x="anio",
            y="ratio_drenaje_reservas",
            color="pais",
            markers=True,
            labels={
                "ratio_drenaje_reservas": "Saldo neto / reservas",
                "anio": "Año",
            },
        )
        st.plotly_chart(fig_serie, use_container_width=True)

st.divider()
st.markdown(
    "**Panamá, Ecuador y El Salvador** no tienen prestamista de última instancia en moneda propia. "
    "Sus umbrales son más estrictos y no deben compararse directamente con los de economías emisoras."
)

with st.expander("📖 Metodología"):
    st.markdown(
        """
- **Saldo neto predeterminado**: entradas contractuales menos salidas contractuales en 12 meses.
- **Ratio**: saldo neto predeterminado / reservas IRFCL.
- **Negativo**: salidas netas; mayor vulnerabilidad.
- **Positivo**: entradas netas; holgura.
- **Umbrales emisoras**: 0 a -1 moderada; -1 a -2 alta; menor o igual a -2 crítica.
- **Umbrales dolarizadas**: -0.5 a -1 moderada; -1 a -2 alta; menor o igual a -2 emergencia.
        """
    )
