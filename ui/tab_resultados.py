"""
ui/tab_resultados.py
────────────────────
Pestaña 2: Métricas de desempeño, gráficas y comparación sim vs teoría.
"""

import streamlit as st

from modelo import ColaMM1K
from teoria import teorico_mm1k
from graficos import (
    fig_evolucion,
    fig_pn,
    fig_histogramas,
    fig_comparacion,
)


def _ejecutar_simulacion(lam, mu, K, T_max, seed) -> tuple:
    """Corre la simulación y retorna (modelo, sim_stats, teo_stats, df_col)."""
    modelo = ColaMM1K(lam=lam, mu=mu, K=K, T_max=T_max, seed=seed)
    modelo.correr()
    sim = modelo.estadisticas()
    teo = teorico_mm1k(lam, mu, K)
    df  = modelo.datacollector.get_model_vars_dataframe()
    return modelo, sim, teo, df


def _tarjeta_metrica(label: str, v_sim: float, v_teo: float) -> str:
    delta = (v_sim - v_teo) / (abs(v_teo) + 1e-12) * 100
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-sim">{v_sim:.3f}</div>
        <div class="metric-teo">Teórico: {v_teo:.3f}</div>
        <div style="font-size:0.72rem;color:#888">Δ {delta:+.1f}%</div>
    </div>
    """


def render_tab_resultados(lam: float, mu: float, K: int,
                           T_max: int, seed: int, ejecutar: bool):

    # Ejecutar o reutilizar resultado en session_state
    params_actuales = (lam, mu, K, T_max, seed)
    necesita_correr = (
        ejecutar
        or "modelo_resultado" not in st.session_state
        or st.session_state.get("sim_params") != params_actuales
    )

    if necesita_correr:
        with st.spinner("Ejecutando simulación..."):
            modelo, sim, teo, df = _ejecutar_simulacion(lam, mu, K, T_max, seed)
            st.session_state["modelo_resultado"] = modelo
            st.session_state["sim_stats"]        = sim
            st.session_state["teo_stats"]        = teo
            st.session_state["df_datacol"]       = df
            st.session_state["sim_params"]       = params_actuales

    modelo = st.session_state["modelo_resultado"]
    sim    = st.session_state["sim_stats"]
    teo    = st.session_state["teo_stats"]
    df     = st.session_state["df_datacol"]

    # ── Métricas principales ──────────────────────────────────────────
    st.markdown('<div class="section-header">Métricas de Desempeño</div>',
                unsafe_allow_html=True)

    metricas = [
        ("Pₖ — Rechazo",   sim["P_K_sim"], teo["P_K"]),
        ("λef — T. Efect.", sim["lambda_ef"], teo["lambda_ef"]),
        ("L — En Sistema",  sim["L_sim"],   teo["L"]),
        ("Lq — En Cola",    sim["Lq_sim"],  teo["Lq"]),
        ("W — T. Sistema",  sim["W_sim"],   teo["W"]),
        ("Wq — T. Cola",    sim["Wq_sim"],  teo["Wq"]),
        ("U — Utilización", sim["U_sim"],   teo["U"]),
    ]
    cols = st.columns(len(metricas))
    for col, (label, vs, vt) in zip(cols, metricas):
        with col:
            st.markdown(_tarjeta_metrica(label, vs, vt), unsafe_allow_html=True)

    st.markdown("---")

    # Contadores
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Llegadas",   sim["total_llegadas"])
    c2.metric("Total Atendidos",  sim["total_atendidos"])
    c3.metric("Total Rechazados", sim["total_rechazados"],
              delta=f"{sim['P_K_sim']*100:.1f}% rechazo", delta_color="inverse")

    st.markdown("---")

    # ── Gráficas ──────────────────────────────────────────────────────
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown('<div class="section-header">Evolución Temporal</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(
            fig_evolucion(modelo.historial_tiempo, modelo.historial_n_sistema,
                          modelo.historial_n_cola, teo, sim, K),
            use_container_width=True,
            key="res_evolucion")

    with col_g2:
        st.markdown('<div class="section-header">Distribución Pₙ</div>',
                    unsafe_allow_html=True)
        estados_sim = (
            df["N_sistema"]
            .value_counts(normalize=True)
            .reindex(range(K + 1), fill_value=0)
            .sort_index()
            .values.tolist()
        )
        st.plotly_chart(fig_pn(estados_sim, teo, K), use_container_width=True, key="res_pn")

    col_g3, col_g4 = st.columns(2)

    with col_g3:
        st.markdown('<div class="section-header">Comparación de Métricas</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(fig_comparacion(sim, teo), use_container_width=True, key="res_comparacion")

    with col_g4:
        st.markdown('<div class="section-header">Histograma de Tiempos</div>',
                    unsafe_allow_html=True)
        atendidos = modelo.clientes_atendidos
        tq = [c.tiempo_en_cola    for c in atendidos if c.tiempo_en_cola    is not None]
        ts = [c.tiempo_en_sistema for c in atendidos if c.tiempo_en_sistema is not None]
        st.plotly_chart(fig_histogramas(tq, ts, teo), use_container_width=True, key="res_histogramas")
