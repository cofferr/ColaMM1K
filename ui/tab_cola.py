"""
ui/tab_cola.py
──────────────
Pestaña 1: Visualización gráfica de la cola y animación con Plotly frames.
"""

import streamlit as st

from modelo import ColaMM1K
from graficos import grafico_cola, generar_figura_animada
from teoria import teorico_mm1k


def _card(label: str, valor: str) -> str:
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-sim">{valor}</div>
    </div>
    """


def render_tab_cola(lam: float, mu: float, K: int,
                    T_max: int, seed: int):
    teo = teorico_mm1k(lam, mu, K)

    # ── Estado esperado (teórico) ─────────────────────────────────────
    st.markdown('<div class="section-header">Estado Esperado del Sistema (valores teóricos)</div>',
                unsafe_allow_html=True)

    col_vis, col_info = st.columns([3, 1])

    with col_vis:
        nq_esp  = max(0, min(int(round(teo["Lq"])), K - 1))
        srv_esp = teo["U"] > 0.5
        st.plotly_chart(
            grafico_cola(nq_esp, srv_esp, K),
            use_container_width=True,
            config={"displayModeBar": False},
            key="cola_estatica",
        )

    with col_info:
        st.markdown(
            _card("ρ Intensidad",  f"{teo['rho']:.3f}") +
            _card("L Esperado",    f"{teo['L']:.2f}")    +
            _card("Pₖ Rechazo",   f"{teo['P_K']:.3f}")  +
            _card("U Utilización", f"{teo['U']*100:.1f}%"),
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Animación con Plotly frames ───────────────────────────────────
    st.markdown('<div class="section-header">▶ Animación de la Simulación</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    Genera una animación interactiva con todos los eventos precalculados.
    Usa los botones <b>▶ Play</b> / <b>⏸ Pausa</b> y el slider para navegar
    entre eventos. Los slots azules son clientes en cola; el servidor verde indica ocupado.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        n_eventos = st.slider(
            "Eventos a incluir", min_value=50, max_value=500,
            value=150, step=50,
            help="Número de eventos del historial que se incluirán en la animación",
        )
    with col2:
        generar = st.button("🎬 Generar Animación", use_container_width=True)

    # Clave de caché que invalida si cambian los parámetros o el nº de eventos
    cache_key = (lam, mu, K, T_max, seed, n_eventos)

    if generar or (
        "anim_fig" in st.session_state
        and st.session_state.get("anim_params") == cache_key
    ):
        if generar or st.session_state.get("anim_params") != cache_key:
            with st.spinner("⏳ Generando animación..."):
                modelo_anim = ColaMM1K(lam=lam, mu=mu, K=K, T_max=T_max, seed=seed)
                modelo_anim.correr()
                eventos = modelo_anim.historial_eventos[:n_eventos]
                fig_anim = generar_figura_animada(eventos, K)
                st.session_state["anim_fig"]    = fig_anim
                st.session_state["anim_params"] = cache_key
                st.session_state["anim_n"]      = len(eventos)

        st.caption(f"Animación generada con **{st.session_state['anim_n']}** eventos.")
        st.plotly_chart(
            st.session_state["anim_fig"],
            use_container_width=True,
            key="animacion_cola",
        )
    else:
        st.info("Pulsa **🎬 Generar Animación** para visualizar la simulación.")

