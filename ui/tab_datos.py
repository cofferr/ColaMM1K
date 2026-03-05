"""
ui/tab_datos.py
───────────────
Pestaña 5: Datos crudos del DataCollector de Mesa y descarga CSV.
"""

import pandas as pd
import streamlit as st

from graficos import fig_eventos


def render_tab_datos():
    if "modelo_resultado" not in st.session_state:
        st.info("Ejecuta la simulación desde la pestaña **Resultados** para ver los datos.")
        return

    modelo = st.session_state["modelo_resultado"]
    df     = st.session_state["df_datacol"]

    # ── DataCollector ─────────────────────────────────────────────────
    st.markdown('<div class="section-header">DataFrame del DataCollector de Mesa</div>',
                unsafe_allow_html=True)
    st.dataframe(df.tail(200), use_container_width=True)

    st.markdown("---")

    # ── Eventos ───────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Historial de Eventos</div>',
                unsafe_allow_html=True)

    if modelo.historial_eventos:
        df_ev = pd.DataFrame(modelo.historial_eventos)
        st.dataframe(df_ev.tail(200), use_container_width=True)
        st.plotly_chart(fig_eventos(df_ev), use_container_width=True, key="datos_eventos")
    else:
        st.info("Sin eventos registrados.")

    st.markdown("---")

    # ── Descarga ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Descargar Resultados</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "Descargar DataCollector (CSV)",
            df.to_csv(index=True),
            "cola_mm1k_datacollector.csv",
            "text/csv",
            use_container_width=True,
        )
    with col2:
        if modelo.historial_eventos:
            df_ev = pd.DataFrame(modelo.historial_eventos)
            st.download_button(
                "Descargar Eventos (CSV)",
                df_ev.to_csv(index=False),
                "cola_mm1k_eventos.csv",
                "text/csv",
                use_container_width=True,
            )
