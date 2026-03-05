"""
ui/tab_sensibilidad.py
──────────────────────
Pestaña 4: Análisis de sensibilidad de parámetros del modelo.
"""

import streamlit as st
from graficos import fig_efecto_k, fig_sensibilidad, fig_heatmap


def render_tab_sensibilidad(lam: float, mu: float, K: int):

    # ── Efecto de K ───────────────────────────────────────────────────
    st.markdown('<div class="section-header">Efecto de la Capacidad K</div>',
                unsafe_allow_html=True)

    K_max = st.slider("K máximo para el análisis", 5, 50, 25, 5)
    st.plotly_chart(fig_efecto_k(lam, mu, K_max), use_container_width=True, key="sens_efecto_k")

    st.markdown("---")

    # ── Curvas L y Pk vs rho ─────────────────────────────────────────
    st.markdown('<div class="section-header">Curvas L y Pₖ vs ρ para Distintos K</div>',
                unsafe_allow_html=True)

    K_list = st.multiselect(
        "Valores de K a comparar",
        [2, 3, 5, 8, 10, 15, 20, 30],
        default=[3, 5, 10, 20],
    )
    if K_list:
        st.plotly_chart(fig_sensibilidad(mu, K_list), use_container_width=True, key="sens_curvas")
    else:
        st.info("Selecciona al menos un valor de K.")

    st.markdown("---")

    # ── Heatmap ───────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Heatmap: L en función de λ y K</div>',
                unsafe_allow_html=True)

    K_max_hm = st.slider("K máximo para el heatmap", 5, 40, 20, 5)
    st.plotly_chart(fig_heatmap(mu, K_max_hm), use_container_width=True, key="sens_heatmap")
