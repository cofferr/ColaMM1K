"""
app.py
──────
Punto de entrada principal de la aplicación Streamlit.

Ejecutar con:
    streamlit run app.py
"""

import streamlit as st

from ui.sidebar import render_sidebar
from ui.tab_cola import render_tab_cola
from ui.tab_resultados import render_tab_resultados
from ui.tab_matematico import render_tab_matematico
from ui.tab_sensibilidad import render_tab_sensibilidad
from ui.tab_datos import render_tab_datos

# ─────────────────────────────────────────────────────────────────────────────
#  CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cola M/M/1/K/∞",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
#  ESTILOS GLOBALES
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem; font-weight: 800;
        color: #1F4E79; text-align: center; margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.1rem; color: #2E75B6;
        text-align: center; margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #EBF3FB 0%, #FFFFFF 100%);
        border: 1.5px solid #2E75B6; border-radius: 10px;
        padding: 14px 18px; margin: 4px 0; text-align: center;
    }
    .metric-label {
        font-size: 0.78rem; color: #555; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.05em;
    }
    .metric-sim  { font-size: 1.5rem; font-weight: 800; color: #1F4E79; }
    .metric-teo  { font-size: 0.82rem; color: #E74C3C; font-weight: 600; }
    .section-header {
        font-size: 1.3rem; font-weight: 700; color: #1F4E79;
        border-bottom: 2px solid #2E75B6;
        padding-bottom: 6px; margin: 1rem 0 0.7rem 0;
    }
    .info-box {
        background: #D1ECF1; border-left: 4px solid #17A2B8;
        border-radius: 6px; padding: 10px 14px;
        margin: 6px 0; font-size: 0.9rem;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #EBF3FB; border-radius: 8px 8px 0 0;
        color: #1F4E79; font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  CABECERA
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title"> Cola M/M/1/K/∞</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">'
    "Simulación Interactiva con MESA · Modelado Matemático · Análisis de Sensibilidad"
    "</div>",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
lam, mu, K, T_max, seed, ejecutar = render_sidebar()

# ─────────────────────────────────────────────────────────────────────────────
#  PESTAÑAS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Visualización de Cola",
    "Resultados y Gráficas",
    "Modelo Matemático",
    "Análisis de Sensibilidad",
    "Datos Crudos",
])

with tab1:
    render_tab_cola(lam, mu, K, T_max, seed)

with tab2:
    render_tab_resultados(lam, mu, K, T_max, seed, ejecutar)

with tab3:
    render_tab_matematico(lam, mu, K)

with tab4:
    render_tab_sensibilidad(lam, mu, K)

with tab5:
    render_tab_datos()
