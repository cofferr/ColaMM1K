"""
ui/sidebar.py
─────────────
Sidebar de Streamlit: sliders de parámetros y fórmulas clave.
"""

import streamlit as st
from teoria import teorico_mm1k, estado_carga


def render_sidebar() -> tuple[float, float, int, int, int, bool]:
    """
    Renderiza el sidebar y retorna los parámetros seleccionados.

    Retorna
    -------
    (lam, mu, K, T_max, seed, ejecutar)
    """
    with st.sidebar:
        st.markdown("## Parámetros del Sistema")
        st.markdown("---")

        lam = st.slider(
            "**λ — Tasa de llegadas**", 0.5, 10.0, 4.0, 0.1,
            help="Clientes que llegan por unidad de tiempo (Proceso de Poisson)",
        )
        mu = st.slider(
            "**μ — Tasa de servicio**", 0.5, 10.0, 6.0, 0.1,
            help="Clientes atendidos por unidad de tiempo (distribución exponencial)",
        )
        K = st.slider(
            "**K — Capacidad máxima**", 2, 30, 5, 1,
            help="Número máximo de clientes en el sistema (cola + servidor)",
        )

        st.markdown("---")
        st.markdown("## Parámetros de Simulación")

        T_max = st.select_slider(
            "**Tiempo máximo T_max**",
            options=[500, 1000, 2000, 5000, 10_000, 20_000],
            value=5000,
        )
        seed = st.number_input("**Semilla (seed)**", 0, 9999, 42, 1)

        st.markdown("---")

        # Indicador de carga
        rho = lam / mu
        msg, tipo = estado_carga(rho)
        getattr(st, tipo)(msg)
        st.markdown(f"**λ/μ = {lam}/{mu} = {rho:.3f}**")

        ejecutar = st.button(
            "Ejecutar Simulación",
            use_container_width=True,
            type="primary",
        )

        # Fórmulas rápidas en el sidebar
        st.markdown("---")
        st.markdown("### Fórmulas Clave")
        st.latex(r"P_0 = \frac{1-\rho}{1-\rho^{K+1}}")
        st.latex(r"P_n = P_0 \cdot \rho^n")
        st.latex(r"L = \frac{\rho}{1-\rho} - \frac{(K+1)\rho^{K+1}}{1-\rho^{K+1}}")
        st.latex(r"W = \frac{L}{\lambda_{ef}}")

    return lam, mu, K, T_max, seed, ejecutar
