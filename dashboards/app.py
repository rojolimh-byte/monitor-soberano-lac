
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Monitor Soberano LAC", page_icon="🌎", layout="wide")

ROOT = Path(__file__).resolve().parent.parent
RUTA_RESULTADOS = ROOT / "resultados" / "indice_vulnerabilidad_integral_latam_2025.csv"
RUTA_SERIE = ROOT / "resultados" / "serie_tiempo_vulnerabilidad_continua.csv"
DOLARIZADAS = ["Panama", "Ecuador", "El Salvador"]

@st.cache_data
def cargar_datos():
    df = pd.read_csv(RUTA_RESULTADOS)
    df = df.rename(columns={"COUNTRY": "pais"})
        # El CSV ya trae indice_vulnerabilidad calculado; solo normalizamos nombres
    df = df.rename(columns={"COUNTRY": "pais", "predeterminados_sobre_reservas": "ratio"})
    df["pais"] = df["pais"].replace({
        "Panama": "Panamá", "Brazil": "Brasil", "Mexico": "México",
        "Peru": "Perú", "Dominican Republic": "República Dominicana",
    })

    df_serie = None
    if RUTA_SERIE.exists():
        ds = pd.read_csv(RUTA_SERIE)
        ds = ds[(ds["anio"] >= 2010) & (ds["reservas"] > 100)].copy()
        # La serie ya viene con el índice corregido; si no, recalcularlo igual
        if "indice_vulnerabilidad" not in ds.columns or ds["indice_vulnerabilidad"].isna().all():
            ds["indice_vulnerabilidad"] = ds.groupby("anio")["ratio_drenaje_reservas"].rank(pct=True, ascending=False)
        df_serie = ds
    return df, df_serie

df, df_serie = cargar_datos()

st.title("🌎 Monitor Soberano LAC")
st.caption("Vulnerabilidad externa (drenajes IRFCL / reservas) para 16 países de América Latina y el Caribe · Datos a 2025 · Fuente: IMF IRFCL")
st.warning("⚠️ Herramienta de análisis. No constituye asesoría de inversión.")

st.sidebar.header("Filtros")
paises = st.sidebar.multiselect("Países", options=sorted(df["pais"].unique()), default=sorted(df["pais"].unique()))
umbral = st.sidebar.slider("Umbral de alerta (índice)", 0.0, 1.0, 0.7, 0.05)
df_f = df[df["pais"].isin(paises)].copy()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Países monitoreados", len(df_f))
col2.metric("Países en alerta", int((df_f["indice_vulnerabilidad"] >= umbral).sum()))
col3.metric("Mayor vulnerabilidad", df_f.loc[df_f["indice_vulnerabilidad"].idxmax(), "pais"])
col4.metric("Menor vulnerabilidad", df_f.loc[df_f["indice_vulnerabilidad"].idxmin(), "pais"])

st.divider()
st.subheader("Ranking de vulnerabilidad externa (2025)")
df_rank = df_f.sort_values("indice_vulnerabilidad", ascending=True)
fig_rank = px.bar(df_rank, x="indice_vulnerabilidad", y="pais", orientation="h",
                  color="indice_vulnerabilidad", color_continuous_scale="RdYlGn_r",
                  range_color=[0, 1],
                  labels={"indice_vulnerabilidad": "Índice (0-1, relativo)", "pais": ""},
                  title="Índice de vulnerabilidad — ranking relativo")
fig_rank.update_layout(height=600, showlegend=False)
st.plotly_chart(fig_rank, use_container_width=True)
st.info("**Nota**: el índice es un ranking relativo; ratio más negativo (drenajes que superan reservas) = mayor vulnerabilidad.")

st.subheader("Ratio crudo: drenajes / reservas")
df_ratio = df_f[["pais", "ratio", "reservas_usd", "drenajes_usd", "indice_vulnerabilidad"]].sort_values("ratio")
st.dataframe(df_ratio.style.background_gradient(subset=["ratio"], cmap="RdYlGn"), use_container_width=True, hide_index=True)

if df_serie is not None and not df_serie.empty:
    st.subheader("Evolución del índice (2010-2024)")
    paises_disponibles = sorted(df_serie["pais"].unique())
    defaults = [p for p in ["Argentina", "Brasil", "Chile", "Ecuador", "México"] if p in paises_disponibles]
    paises_serie = st.multiselect("Países a comparar", options=paises_disponibles, default=defaults)
    df_s = df_serie[df_serie["pais"].isin(paises_serie)].sort_values(["pais", "anio"])
    if not df_s.empty:
        fig_serie = px.line(df_s, x="anio", y="indice_vulnerabilidad", color="pais", markers=True,
                            labels={"indice_vulnerabilidad": "Índice", "anio": "Año"},
                            title="Índice de vulnerabilidad en el tiempo")
        fig_serie.update_layout(height=450, yaxis_range=[0, 1.05])
        st.plotly_chart(fig_serie, use_container_width=True)
    else:
        st.warning("No hay datos para los países seleccionados.")
else:
    st.info("Serie de tiempo no disponible.")

st.divider()
st.subheader("Nota sobre economías dolarizadas")
st.markdown(f"**{', '.join(DOLARIZADAS)}** no emiten moneda propia. No tienen prestamista de última instancia en moneda propia, por lo que un ratio drenajes/reservas alto indica vulnerabilidad **más severa**, no menor.")

with st.expander("📖 Metodología"):
    st.markdown("""
- **Drenajes predeterminados**: obligaciones en divisa con vencimiento cierto en los próximos 12 meses.
- **Ratio**: drenajes netos / reservas. Negativo = drenajes superan reservas.
- **Índice**: rank percentil del ratio por año — el ratio más negativo recibe índice 1.0 (mayor vulnerabilidad).
- **Filtro serie**: se excluyen observaciones con reservas < 100 M USD.
    """)

