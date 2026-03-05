"""
graficos.py
───────────
Todas las funciones de visualización con Plotly para la app Streamlit.
"""

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from teoria import teorico_mm1k


# ─────────────────────────────────────────────────────────────────────────────
#  COLORES CORPORATIVOS
# ─────────────────────────────────────────────────────────────────────────────
AZUL_OSCURO  = "#1F4E79"
AZUL_MEDIO   = "#2E75B6"
AZUL_CLARO   = "rgba(235,243,251,0.3)"
ROJO         = "#E74C3C"
VERDE        = "#27AE60"
MORADO       = "#8E44AD"
NARANJA      = "#F39C12"
GRIS         = "#BDC3C7"

PALETA = [AZUL_OSCURO, AZUL_MEDIO, ROJO, VERDE, MORADO, NARANJA]
LAYOUT_BASE = dict(
    paper_bgcolor="white",
    plot_bgcolor=AZUL_CLARO,
    margin=dict(l=50, r=40, t=50, b=40),
)


# ─────────────────────────────────────────────────────────────────────────────
#  GRÁFICO VISUAL DE LA COLA
# ─────────────────────────────────────────────────────────────────────────────

def grafico_cola(n_cola: int, servidor_ocupado: bool, K: int,
                 rechazado: bool = False) -> go.Figure:
    """
    Dibuja el estado actual del sistema de colas:
    - Casillas azules  = clientes esperando
    - Casillas vacías  = slots libres
    - Servidor verde   = libre | naranja = ocupado
    - Indicador rojo   = cliente rechazado
    """
    fig   = go.Figure()
    ancho = 0.8
    alto  = 0.8
    gap   = 0.25
    n_slots = K - 1   # slots de cola (el K-ésimo es el servidor)

    # ── Flecha de llegadas ────────────────────────────────────────────
    fig.add_annotation(
        x=-2.2, y=0.5, ax=-3.2, ay=0.5,
        xref="x", yref="y", axref="x", ayref="y",
        text="", showarrow=True,
        arrowhead=3, arrowsize=1.5, arrowwidth=2.5, arrowcolor=AZUL_OSCURO,
    )
    fig.add_annotation(
        x=-3.5, y=0.5, text="<b>Llegadas<br>λ</b>",
        showarrow=False, font=dict(size=11, color=AZUL_OSCURO),
        xref="x", yref="y",
    )

    # ── Slots de cola ─────────────────────────────────────────────────
    for i in range(n_slots):
        x0      = -1.5 - i * (ancho + gap)
        filled  = i < n_cola
        fc      = AZUL_MEDIO if filled else "rgba(200,220,240,0.3)"
        bc      = AZUL_OSCURO if filled else "#AED6F1"

        fig.add_shape(type="rect",
            x0=x0, y0=0, x1=x0 + ancho, y1=alto,
            fillcolor=fc, line=dict(color=bc, width=2), layer="below")

        if filled:
            fig.add_annotation(
                x=x0 + ancho / 2, y=alto / 2,
                text="👤", showarrow=False,
                font=dict(size=18), xref="x", yref="y")

        fig.add_annotation(
            x=x0 + ancho / 2, y=-0.35,
            text=f'<span style="font-size:9px;color:#888">{i+1}</span>',
            showarrow=False, xref="x", yref="y")

    # ── Etiqueta "COLA" ───────────────────────────────────────────────
    if n_slots > 0:
        cx = -1.5 - (n_slots - 1) * (ancho + gap) / 2
        fig.add_annotation(
            x=cx, y=alto + 0.5,
            text=f"<b>COLA</b> ({n_cola}/{n_slots})",
            showarrow=False, font=dict(size=11, color=AZUL_OSCURO),
            xref="x", yref="y")

    # ── Flecha cola → servidor ────────────────────────────────────────
    fig.add_annotation(
        x=1.0, y=0.5, ax=0.0, ay=0.5,
        xref="x", yref="y", axref="x", ayref="y",
        text="", showarrow=True,
        arrowhead=3, arrowsize=1.5, arrowwidth=2.5, arrowcolor=AZUL_OSCURO,
    )

    # ── Servidor ──────────────────────────────────────────────────────
    srv_fc    = VERDE  if servidor_ocupado else GRIS
    srv_emoji = "⚙️"   if servidor_ocupado else "💤"
    srv_label = "OCUPADO" if servidor_ocupado else "LIBRE"
    srv_bc    = VERDE  if servidor_ocupado else "#7F8C8D"

    fig.add_shape(type="rect",
        x0=1.1, y0=-0.15, x1=2.5, y1=alto + 0.15,
        fillcolor=srv_fc, opacity=0.25,
        line=dict(color=srv_bc, width=3))
    fig.add_annotation(
        x=1.8, y=alto / 2, text=srv_emoji,
        showarrow=False, font=dict(size=30), xref="x", yref="y")
    fig.add_annotation(
        x=1.8, y=alto + 0.55,
        text=f"<b>SERVIDOR<br>{srv_label}</b>",
        showarrow=False, font=dict(size=10, color=srv_bc),
        xref="x", yref="y")

    # ── Flecha de salida ──────────────────────────────────────────────
    fig.add_annotation(
        x=3.5, y=0.5, ax=2.6, ay=0.5,
        xref="x", yref="y", axref="x", ayref="y",
        text="", showarrow=True,
        arrowhead=3, arrowsize=1.5, arrowwidth=2.5, arrowcolor=VERDE,
    )
    fig.add_annotation(
        x=3.7, y=0.5, text="<b>Salida</b>",
        showarrow=False, font=dict(size=11, color=VERDE),
        xref="x", yref="y")

    # ── Cliente rechazado ─────────────────────────────────────────────
    if rechazado and n_slots > 0:
        rx = -1.5 - n_slots * (ancho + gap)
        fig.add_annotation(
            x=rx, y=alto + 0.3,
            text="🚫 Rechazado", showarrow=True,
            arrowhead=2, arrowcolor=ROJO,
            font=dict(size=11, color=ROJO),
            xref="x", yref="y",
            ax=rx - 0.5, ay=0.5, axref="x", ayref="y")

    # ── Caja de capacidad K ───────────────────────────────────────────
    x_total = -1.5 - (n_slots - 1) * (ancho + gap) - 0.3 if n_slots > 0 else -0.3
    fig.add_shape(type="rect",
        x0=x_total, y0=-0.6, x1=2.5, y1=alto + 0.85,
        fillcolor="rgba(0,0,0,0)",
        line=dict(color="#AED6F1", width=1.5, dash="dot"))
    fig.add_annotation(
        x=(x_total + 2.5) / 2, y=alto + 1.05,
        text=f"<b>Sistema — Capacidad K = {K}</b>",
        showarrow=False, font=dict(size=10, color=AZUL_MEDIO),
        xref="x", yref="y")

    x_min = x_total - 1.8
    fig.update_layout(
        xaxis=dict(range=[x_min, 4.2], showgrid=False,
                   zeroline=False, showticklabels=False),
        yaxis=dict(range=[-0.8, 1.8], showgrid=False,
                   zeroline=False, showticklabels=False,
                   scaleanchor="x", scaleratio=1),
        margin=dict(l=10, r=10, t=10, b=10),
        height=200,
        paper_bgcolor="rgba(235,243,251,0.4)",
        plot_bgcolor="rgba(235,243,251,0.4)",
        showlegend=False,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  EVOLUCIÓN TEMPORAL
# ─────────────────────────────────────────────────────────────────────────────

def fig_evolucion(historial_t, historial_n, historial_q,
                  teo: dict, sim: dict, K: int) -> go.Figure:
    n_show = min(600, len(historial_t))
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        subplot_titles=("Clientes en el Sistema N(t)", "Clientes en Cola Nq(t)"),
        vertical_spacing=0.12,
    )

    # N(t)
    fig.add_trace(go.Scatter(
        x=historial_t[:n_show], y=historial_n[:n_show],
        mode="lines", line=dict(color=AZUL_OSCURO, width=1.5, shape="hv"),
        name="N(t) simulado", fill="tozeroy",
        fillcolor="rgba(31,78,121,0.08)"), row=1, col=1)
    fig.add_hline(y=teo["L"],     line=dict(color=ROJO,  dash="dash", width=2),
                  annotation_text=f"L teórico={teo['L']:.3f}", row=1, col=1)
    fig.add_hline(y=sim["L_sim"], line=dict(color=VERDE, dash="dot",  width=2),
                  annotation_text=f"L simulado={sim['L_sim']:.3f}", row=1, col=1)
    fig.add_hline(y=K, line=dict(color=NARANJA, dash="dashdot", width=1.5),
                  annotation_text=f"K={K}", row=1, col=1)

    # Nq(t)
    fig.add_trace(go.Scatter(
        x=historial_t[:n_show], y=historial_q[:n_show],
        mode="lines", line=dict(color=MORADO, width=1.5, shape="hv"),
        name="Nq(t) simulado", fill="tozeroy",
        fillcolor="rgba(142,68,173,0.08)"), row=2, col=1)
    fig.add_hline(y=teo["Lq"],     line=dict(color=ROJO,  dash="dash", width=2),
                  annotation_text=f"Lq teórico={teo['Lq']:.3f}", row=2, col=1)
    fig.add_hline(y=sim["Lq_sim"], line=dict(color=VERDE, dash="dot",  width=2),
                  annotation_text=f"Lq simulado={sim['Lq_sim']:.3f}", row=2, col=1)

    fig.update_layout(height=420, showlegend=False, **LAYOUT_BASE)
    fig.update_xaxes(title_text="Tiempo", row=2, col=1)
    fig.update_yaxes(title_text="N(t)",  row=1, col=1)
    fig.update_yaxes(title_text="Nq(t)", row=2, col=1)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  DISTRIBUCIÓN Pn
# ─────────────────────────────────────────────────────────────────────────────

def fig_pn(estados_sim: list, teo: dict, K: int) -> go.Figure:
    labels = [f"n={i}" for i in range(K + 1)]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels, y=estados_sim, name="Simulada",
        marker_color=AZUL_MEDIO, opacity=0.85,
        text=[f"{v:.3f}" for v in estados_sim], textposition="outside"))
    fig.add_trace(go.Bar(
        x=labels, y=teo["Pn"], name="Teórica",
        marker_color=ROJO, opacity=0.85,
        text=[f"{v:.3f}" for v in teo["Pn"]], textposition="outside"))
    fig.update_layout(
        barmode="group", height=360,
        title=f"Distribución P_n  —  ρ = {teo['rho']:.3f}",
        xaxis_title="Estado n (clientes en sistema)",
        yaxis_title="Probabilidad P_n",
        legend=dict(x=0.75, y=0.95),
        **LAYOUT_BASE,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  HISTOGRAMA DE TIEMPOS
# ─────────────────────────────────────────────────────────────────────────────

def fig_histogramas(tq_list: list, ts_list: list, teo: dict) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=tq_list, name="Wq (cola)", nbinsx=40,
        marker_color=MORADO, opacity=0.7, histnorm="probability density"))
    fig.add_trace(go.Histogram(
        x=ts_list, name="W (sistema)", nbinsx=40,
        marker_color=AZUL_OSCURO, opacity=0.6, histnorm="probability density"))
    fig.add_vline(x=teo["Wq"], line=dict(color=ROJO,  dash="dash", width=2),
                  annotation_text=f"Wq={teo['Wq']:.3f}")
    fig.add_vline(x=teo["W"],  line=dict(color=VERDE, dash="dash", width=2),
                  annotation_text=f"W={teo['W']:.3f}")
    fig.update_layout(
        barmode="overlay", height=360,
        xaxis_title="Tiempo", yaxis_title="Densidad",
        legend=dict(x=0.7, y=0.95),
        **LAYOUT_BASE,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  COMPARACIÓN BARRAS SIM VS TEO
# ─────────────────────────────────────────────────────────────────────────────

def fig_comparacion(sim: dict, teo: dict) -> go.Figure:
    nombres = ["Pₖ", "L", "Lq", "W", "Wq", "U"]
    v_sim   = [sim["P_K_sim"], sim["L_sim"], sim["Lq_sim"],
               sim["W_sim"],   sim["Wq_sim"], sim["U_sim"]]
    v_teo   = [teo["P_K"], teo["L"], teo["Lq"],
               teo["W"],   teo["Wq"], teo["U"]]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=nombres, y=v_sim, name="Simulado",
        marker_color=AZUL_MEDIO, opacity=0.85,
        text=[f"{v:.3f}" for v in v_sim], textposition="outside"))
    fig.add_trace(go.Bar(
        x=nombres, y=v_teo, name="Teórico",
        marker_color=ROJO, opacity=0.85,
        text=[f"{v:.3f}" for v in v_teo], textposition="outside"))
    fig.update_layout(
        barmode="group", height=380,
        title="Comparación Simulado vs Teórico",
        yaxis_title="Valor",
        legend=dict(x=0.75, y=0.95),
        **LAYOUT_BASE,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  SENSIBILIDAD — CURVAS L y Pk vs ρ
# ─────────────────────────────────────────────────────────────────────────────

def fig_sensibilidad(mu: float, K_list: list) -> go.Figure:
    lambdas = np.linspace(0.1, mu * 0.999, 100)
    fig = make_subplots(rows=1, cols=2, subplot_titles=("L vs ρ", "Pₖ vs ρ"))
    for i, k in enumerate(K_list):
        c   = PALETA[i % len(PALETA)]
        Ls  = [teorico_mm1k(l, mu, k)["L"]   for l in lambdas]
        PKs = [teorico_mm1k(l, mu, k)["P_K"] for l in lambdas]
        fig.add_trace(go.Scatter(
            x=lambdas / mu, y=Ls, mode="lines",
            line=dict(color=c, width=2), name=f"K={k}"), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=lambdas / mu, y=PKs, mode="lines",
            line=dict(color=c, width=2), name=f"K={k}",
            showlegend=False), row=1, col=2)
    fig.update_xaxes(title_text="ρ = λ/μ")
    fig.update_yaxes(title_text="L",  row=1, col=1)
    fig.update_yaxes(title_text="Pₖ", row=1, col=2)
    fig.update_layout(height=380, legend=dict(x=0.02, y=0.98), **LAYOUT_BASE)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  EFECTO DE K
# ─────────────────────────────────────────────────────────────────────────────

def fig_efecto_k(lam: float, mu: float, K_max: int = 25) -> go.Figure:
    Ks   = list(range(1, K_max + 1))
    data = [teorico_mm1k(lam, mu, k) for k in Ks]
    fig  = make_subplots(rows=1, cols=3,
                         subplot_titles=("L vs K", "Pₖ vs K", "W vs K"))
    opts = dict(mode="lines+markers", marker=dict(size=5))
    fig.add_trace(go.Scatter(x=Ks, y=[d["L"]   for d in data],
                             line=dict(color=AZUL_OSCURO, width=2), **opts), row=1, col=1)
    fig.add_trace(go.Scatter(x=Ks, y=[d["P_K"] for d in data],
                             line=dict(color=ROJO,        width=2), **opts), row=1, col=2)
    fig.add_trace(go.Scatter(x=Ks, y=[d["W"]   for d in data],
                             line=dict(color=VERDE,       width=2), **opts), row=1, col=3)
    fig.update_xaxes(title_text="K")
    fig.update_layout(height=350, showlegend=False, **LAYOUT_BASE)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  HEATMAP L en función de λ y K
# ─────────────────────────────────────────────────────────────────────────────

def fig_heatmap(mu: float, K_max: int = 20) -> go.Figure:
    lambdas = np.linspace(0.1, mu * 0.98, 30)
    Ks      = list(range(2, K_max + 1))
    Z = [[teorico_mm1k(l, mu, k)["L"] for l in lambdas] for k in Ks]
    fig = go.Figure(go.Heatmap(
        x=[f"{l:.2f}" for l in lambdas],
        y=[str(k) for k in Ks],
        z=Z,
        colorscale="Blues",
        colorbar=dict(title="L"),
    ))
    fig.update_layout(
        height=400,
        xaxis_title="λ (tasa de llegadas)",
        yaxis_title="K (capacidad)",
        **LAYOUT_BASE,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  CONTEO DE EVENTOS
# ─────────────────────────────────────────────────────────────────────────────

def fig_eventos(df_eventos) -> go.Figure:
    cnt = df_eventos["tipo"].value_counts()
    color_map = {
        "llegada_directa": VERDE,
        "llegada_cola"   : AZUL_MEDIO,
        "salida"         : AZUL_OSCURO,
        "rechazo"        : ROJO,
    }
    fig = go.Figure(go.Bar(
        x=cnt.index, y=cnt.values,
        marker_color=[color_map.get(t, GRIS) for t in cnt.index],
        text=cnt.values, textposition="outside",
    ))
    fig.update_layout(height=300, showlegend=False,
                      xaxis_title="Tipo de evento",
                      yaxis_title="Cantidad",
                      **LAYOUT_BASE)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  ANIMACIÓN NATIVA PLOTLY (frames)
# ─────────────────────────────────────────────────────────────────────────────

def generar_figura_animada(historial_eventos: list, K: int) -> go.Figure:
    """
    Construye una go.Figure con frames Plotly para animar la cola M/M/1/K.

    Cada frame representa el estado del sistema tras un evento:
    - Slots de cola (azul=ocupado, gris claro=vacío) como scatter square markers
    - Servidor (verde=ocupado, gris=libre) como scatter square marker
    - Íconos de personas y servidor como scatter text
    - Título del frame con tiempo, n, nq y tipo de evento
    - Controles Play/Pausa y slider de navegación integrados

    Parámetros
    ----------
    historial_eventos : lista de dicts {t, tipo, n, nq} del modelo ColaMM1K
    K                 : capacidad máxima del sistema
    """
    n_slots = K - 1
    ancho   = 0.8
    gap     = 0.25
    alto    = 0.8

    # Centros de los marcadores de cada slot de cola
    slot_cx = [-1.5 - i * (ancho + gap) + ancho / 2 for i in range(n_slots)]
    slot_cy = [alto / 2] * n_slots
    srv_cx  = 1.8
    srv_cy  = alto / 2

    TIPO_LABEL = {
        "llegada_directa": "🟢 Llegada directa al servidor",
        "llegada_cola"   : "🔵 Cliente entra a la cola",
        "salida"         : "✅ Fin de servicio",
        "rechazo"        : "🚫 Cliente rechazado",
    }

    # ── Constructor de las 4 trazas para un estado dado ───────────────────────
    def _trazas(nq: int, n: int) -> list:
        srv_ocup   = (n - nq) >= 1
        q_colors   = [AZUL_MEDIO if i < nq else "rgba(200,220,240,0.5)"
                      for i in range(n_slots)]
        q_borders  = [AZUL_OSCURO if i < nq else "#AED6F1"
                      for i in range(n_slots)]
        srv_color  = VERDE if srv_ocup else GRIS
        srv_border = VERDE if srv_ocup else "#7F8C8D"

        # Traza 0 — fondo de los slots de cola
        t0 = go.Scatter(
            x=slot_cx, y=slot_cy,
            mode="markers",
            marker=dict(
                symbol="square",
                size=38,
                color=q_colors,
                line=dict(color=q_borders, width=2),
            ),
            showlegend=False,
        )

        # Traza 1 — fondo del servidor
        t1 = go.Scatter(
            x=[srv_cx], y=[srv_cy],
            mode="markers",
            marker=dict(
                symbol="square",
                size=60,
                color=srv_color,
                opacity=0.35,
                line=dict(color=srv_border, width=3),
            ),
            showlegend=False,
        )

        # Traza 2 — íconos de personas en la cola
        # Siempre K-1 posiciones; vacías tienen texto ""
        people = ["👤" if i < nq else "" for i in range(n_slots)]
        t2 = go.Scatter(
            x=slot_cx, y=slot_cy,
            mode="text",
            text=people,
            textfont=dict(size=17),
            showlegend=False,
        )

        # Traza 3 — ícono del servidor
        t3 = go.Scatter(
            x=[srv_cx], y=[srv_cy],
            mode="text",
            text=["⚙️" if srv_ocup else "💤"],
            textfont=dict(size=26),
            showlegend=False,
        )

        return [t0, t1, t2, t3]

    # ── Construir frames ──────────────────────────────────────────────────────
    frames = []
    for i, ev in enumerate(historial_eventos):
        label = TIPO_LABEL.get(ev["tipo"], ev["tipo"])
        title = (
            f"Evento {i+1}  |  "
            f"t = {ev['t']:.3f}  |  "
            f"Sistema: {ev['n']}  |  Cola: {ev['nq']}  |  {label}"
        )
        frames.append(go.Frame(
            data=_trazas(ev["nq"], ev["n"]),
            name=str(i),
            layout=go.Layout(title_text=title),
        ))

    # ── Estado inicial (primer evento) ────────────────────────────────────────
    if historial_eventos:
        fe = historial_eventos[0]
        init_data  = _trazas(fe["nq"], fe["n"])
        init_title = (
            f"Evento 1  |  "
            f"t = {fe['t']:.3f}  |  Sistema: {fe['n']}  |  Cola: {fe['nq']}  |  "
            + TIPO_LABEL.get(fe["tipo"], fe["tipo"])
        )
    else:
        init_data  = _trazas(0, 0)
        init_title = "Sin eventos registrados"

    # ── Pasos del slider ──────────────────────────────────────────────────────
    slider_steps = [
        dict(
            args=[[str(i)], {
                "frame": {"duration": 0, "redraw": True},
                "mode": "immediate",
                "transition": {"duration": 0},
            }],
            label=str(i + 1),
            method="animate",
        )
        for i in range(len(frames))
    ]

    # ── Rango X ───────────────────────────────────────────────────────────────
    x_min = (min(slot_cx) - 1.8) if n_slots > 0 else -3.5
    # "Llegadas λ" lives to the LEFT of the system bounding box (x_min + 0.2)
    x_label = x_min - 0.9   # text anchor, always outside the box
    x_arr_base = x_min - 0.1  # arrow tail
    x_arr_tip  = x_min + 0.2  # arrow head → left edge of system box

    # ── Anotaciones y formas estáticas ────────────────────────────────────────
    static_annotations = [
        # Arrow: outside → system box
        dict(
            x=x_arr_tip, y=alto / 2, ax=x_arr_base, ay=alto / 2,
            xref="x", yref="y", axref="x", ayref="y",
            text="", showarrow=True,
            arrowhead=3, arrowsize=1.5, arrowwidth=2.5, arrowcolor=AZUL_OSCURO,
        ),
        # "Llegadas λ" text, always left of the system box
        dict(x=x_label, y=alto / 2, text="<b>Llegadas<br>λ</b>",
             showarrow=False, font=dict(size=10, color=AZUL_OSCURO),
             xref="x", yref="y"),
        dict(x=3.75, y=alto / 2, text="<b>Salida</b>",
             showarrow=False, font=dict(size=10, color=VERDE),
             xref="x", yref="y"),
        dict(x=srv_cx, y=alto + 0.58, text="<b>SERVIDOR</b>",
             showarrow=False, font=dict(size=9, color=AZUL_OSCURO),
             xref="x", yref="y"),
        dict(
            x=(sum(slot_cx) / len(slot_cx)) if n_slots > 0 else -1.5,
            y=alto + 0.58, text="<b>COLA</b>",
            showarrow=False, font=dict(size=9, color=AZUL_OSCURO),
            xref="x", yref="y",
        ),
        dict(x=(x_min + 2.5) / 2, y=alto + 0.95,
             text=f"<b>Capacidad K = {K}</b>",
             showarrow=False, font=dict(size=9, color=AZUL_MEDIO),
             xref="x", yref="y"),
    ]
    static_shapes = [
        dict(type="rect",
             x0=x_min + 0.2, y0=-0.55, x1=2.5, y1=alto + 0.78,
             fillcolor="rgba(0,0,0,0)",
             line=dict(color="#AED6F1", width=1.5, dash="dot"),
             xref="x", yref="y"),
    ]

    # ── Figura ────────────────────────────────────────────────────────────────
    fig = go.Figure(
        data=init_data,
        frames=frames,
        layout=go.Layout(
            title=dict(text=init_title, x=0.01, font=dict(size=12, color=AZUL_OSCURO)),
            xaxis=dict(range=[x_min - 1.4, 4.5],
                       showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[-0.9, 1.9],
                       showgrid=False, zeroline=False, showticklabels=False,
                       scaleanchor="x", scaleratio=1),
            height=330,
            margin=dict(l=10, r=10, t=45, b=110),
            paper_bgcolor="rgba(235,243,251,0.4)",
            plot_bgcolor="rgba(235,243,251,0.4)",
            showlegend=False,
            annotations=static_annotations,
            shapes=static_shapes,
            updatemenus=[dict(
                type="buttons",
                showactive=False,
                direction="left",
                x=0.5, y=-0.18,
                xanchor="center",
                yanchor="top",
                pad=dict(r=8, t=8),
                font=dict(size=13),
                buttons=[
                    dict(
                        label="▶ Play",
                        method="animate",
                        args=[None, {
                            "frame": {"duration": 380, "redraw": True},
                            "fromcurrent": True,
                            "transition": {"duration": 0},
                        }],
                    ),
                    dict(
                        label="⏸ Pausa",
                        method="animate",
                        args=[[None], {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0},
                        }],
                    ),
                ],
            )],
            sliders=[dict(
                active=0,
                steps=slider_steps,
                x=0.05, y=-0.05,
                len=0.9,
                xanchor="left",
                yanchor="top",
                pad=dict(b=10, t=45),
                currentvalue=dict(
                    prefix="Evento ",
                    visible=False,
                    xanchor="center",
                    font=dict(size=11, color=AZUL_OSCURO),
                ),
                transition=dict(duration=0),
            )],
        ),
    )

    return fig
