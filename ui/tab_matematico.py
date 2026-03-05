"""
ui/tab_matematico.py
────────────────────
Pestaña 3: Modelo matemático completo con fórmulas LaTeX.
"""

import pandas as pd
import streamlit as st

from teoria import teorico_mm1k


def render_tab_matematico(lam: float, mu: float, K: int):
    teo = teorico_mm1k(lam, mu, K)

    # ── Notación de Kendall ───────────────────────────────────────────
    st.markdown('<div class="section-header">Notación de Kendall: M/M/1/K/∞</div>',
                unsafe_allow_html=True)

    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.markdown("""
        | Símbolo | Significado | Valor |
        |---------|-------------|-------|
        | **M** (llegadas) | Distribución exponencial — Proceso de Poisson | tasa λ |
        | **M** (servicio) | Distribución exponencial | tasa μ |
        | **1** | Número de servidores | 1 servidor |
        | **K** | Capacidad máxima | K clientes |
        | **∞** | Fuente de clientes | Infinita |
        """)
    with col_k2:
        st.markdown(f"""
        **Valores actuales:**
        - λ = **{lam}** cl/t
        - μ = **{mu}** cl/t
        - K = **{K}**
        - ρ = λ/μ = **{teo['rho']:.4f}**
        - P₀ = **{teo['P0']:.4f}**
        - Pₖ = **{teo['P_K']:.4f}**
        """)

    st.markdown("---")

    # ── Cadena de Markov ──────────────────────────────────────────────
    st.markdown('<div class="section-header">Cadena de Markov y Ecuaciones de Balance</div>',
                unsafe_allow_html=True)

    st.markdown("**Espacio de estados:**")
    st.latex(r"\mathcal{S} = \{0, 1, 2, \ldots, K\}")

    st.markdown("**Ecuaciones de balance en estado estacionario:**")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("*Estado 0:*")
        st.latex(r"\mu P_1 = \lambda P_0")
    with c2:
        st.markdown("*Estados intermedios:*")
        st.latex(r"(\lambda+\mu)P_n = \lambda P_{n-1} + \mu P_{n+1}")
    with c3:
        st.markdown("*Estado K:*")
        st.latex(r"\mu P_K = \lambda P_{K-1}")

    st.markdown("---")

    # ── Distribución de probabilidades ────────────────────────────────
    st.markdown('<div class="section-header">Distribución de Probabilidades</div>',
                unsafe_allow_html=True)

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("**Relación recursiva:**")
        st.latex(r"P_n = \rho^n \cdot P_0 \qquad \rho = \frac{\lambda}{\mu}")
        st.markdown("**Probabilidad del sistema vacío P₀:**")
        st.latex(r"P_0 = \begin{cases} \dfrac{1-\rho}{1-\rho^{K+1}} & \rho \neq 1 \\[8pt] \dfrac{1}{K+1} & \rho = 1 \end{cases}")
    with col_f2:
        st.markdown("**Distribución completa:**")
        st.latex(r"P_n = \begin{cases} \dfrac{(1-\rho)\,\rho^n}{1-\rho^{K+1}} & \rho \neq 1 \\[8pt] \dfrac{1}{K+1} & \rho = 1 \end{cases}")

    st.markdown("**Probabilidades con los parámetros actuales:**")
    df_pn = pd.DataFrame({
        "Estado n"   : list(range(K + 1)),
        "P_n teórica": [f"{p:.4f}" for p in teo["Pn"]],
        "P_n (%)"    : [f"{p*100:.2f}%" for p in teo["Pn"]],
    })
    st.dataframe(df_pn, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Métricas de desempeño ─────────────────────────────────────────
    st.markdown('<div class="section-header">Métricas de Desempeño</div>',
                unsafe_allow_html=True)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("**Probabilidad de rechazo y tasa efectiva:**")
        st.latex(r"P_K = P_0 \cdot \rho^K")
        st.latex(r"\lambda_{ef} = \lambda\,(1 - P_K)")
        st.markdown("**Número promedio en sistema:**")
        st.latex(r"L = \frac{\rho}{1-\rho} - \frac{(K+1)\rho^{K+1}}{1-\rho^{K+1}}")
        st.markdown("**Número promedio en cola:**")
        st.latex(r"L_q = L - (1 - P_0)")
    with col_m2:
        st.markdown("**Ley de Little:**")
        st.latex(r"L = \lambda_{ef} \cdot W \qquad L_q = \lambda_{ef} \cdot W_q")
        st.markdown("**Tiempo promedio en sistema:**")
        st.latex(r"W = \frac{L}{\lambda_{ef}}")
        st.markdown("**Tiempo promedio en cola:**")
        st.latex(r"W_q = W - \frac{1}{\mu}")
        st.markdown("**Utilización del servidor:**")
        st.latex(r"U = 1 - P_0 = \frac{\lambda_{ef}}{\mu}")

    st.markdown("---")

    # ── Tabla resumen ─────────────────────────────────────────────────
    st.markdown('<div class="section-header">Tabla Resumen con Valores Actuales</div>',
                unsafe_allow_html=True)

    resumen = pd.DataFrame({
        "Métrica"     : ["P₀", "Pₖ", "λef", "L", "Lq", "W", "Wq", "U", "ρ"],
        "Descripción" : [
            "Prob. sistema vacío", "Prob. sistema lleno / rechazo",
            "Tasa efectiva de llegadas", "Clientes promedio en sistema",
            "Clientes promedio en cola", "Tiempo promedio en sistema",
            "Tiempo promedio en cola", "Utilización del servidor",
            "Intensidad de tráfico",
        ],
        "Valor Teórico": [
            f"{teo['P0']:.4f}", f"{teo['P_K']:.4f}",
            f"{teo['lambda_ef']:.4f}", f"{teo['L']:.4f}",
            f"{teo['Lq']:.4f}", f"{teo['W']:.4f}",
            f"{teo['Wq']:.4f}", f"{teo['U']:.4f}",
            f"{teo['rho']:.4f}",
        ],
    })
    st.dataframe(resumen, use_container_width=True, hide_index=True)
