"""
teoria.py
─────────
Cálculo analítico de las métricas en estado estacionario
del modelo M/M/1/K/∞.
"""


def teorico_mm1k(lam: float, mu: float, K: int) -> dict:
    """
    Calcula las métricas teóricas del modelo M/M/1/K/∞.

    Parámetros
    ----------
    lam : tasa de llegadas λ
    mu  : tasa de servicio μ
    K   : capacidad máxima del sistema

    Retorna
    -------
    dict con: rho, P0, Pn, P_K, lambda_ef, L, Lq, W, Wq, U
    """
    rho = lam / mu

    if abs(rho - 1.0) < 1e-10:          # caso ρ = 1
        P0 = 1.0 / (K + 1)
        Pn = [P0] * (K + 1)
        L  = K / 2.0
    else:                                 # caso ρ ≠ 1
        P0 = (1 - rho) / (1 - rho ** (K + 1))
        Pn = [P0 * rho ** n for n in range(K + 1)]
        L  = (rho / (1 - rho)) - ((K + 1) * rho ** (K + 1)) / (1 - rho ** (K + 1))

    PK     = Pn[K]
    lam_ef = lam * (1 - PK)
    Lq     = L - (1 - P0)
    W      = L  / lam_ef if lam_ef > 0 else float("inf")
    Wq     = W - (1 / mu) if lam_ef > 0 else float("inf")
    U      = 1 - P0

    return {
        "rho"       : rho,
        "P0"        : P0,
        "Pn"        : Pn,
        "P_K"       : PK,
        "lambda_ef" : lam_ef,
        "L"         : L,
        "Lq"        : Lq,
        "W"         : W,
        "Wq"        : Wq,
        "U"         : U,
    }


def estado_carga(rho: float) -> tuple[str, str]:
    """
    Retorna (etiqueta, color_streamlit) según la intensidad de tráfico.
    """
    if rho < 0.95:
        return f"ρ = {rho:.3f} — Sistema poco cargado", "success"
    elif rho <= 1.05:
        return f"ρ = {rho:.3f} — Sistema en el límite", "warning"
    else:
        return f"ρ = {rho:.3f} — Sistema sobrecargado", "error"
