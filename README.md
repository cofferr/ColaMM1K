# Cola M/M/1/K/∞ — Simulación Interactiva

Aplicación Streamlit para simular y analizar el modelo de colas **M/M/1/K/∞**
usando el framework de agentes **Mesa**.

## Estructura del Proyecto

```
cola_mm1k/
├── app.py                  # Punto de entrada — ejecutar con streamlit
├── modelo.py               # Agentes Mesa (ClienteAgente, ServidorAgente, ColaMM1K)
├── teoria.py               # Fórmulas analíticas del modelo M/M/1/K/∞
├── graficos.py             # Todas las funciones de visualización (Plotly)
├── requirements.txt
├── README.md
└── ui/
    ├── __init__.py
    ├── sidebar.py          # Sliders y parámetros
    ├── tab_cola.py         # Pestaña: visualización gráfica + animación
    ├── tab_resultados.py   # Pestaña: métricas, gráficas, comparación
    ├── tab_matematico.py   # Pestaña: modelo matemático con LaTeX
    ├── tab_sensibilidad.py # Pestaña: análisis de sensibilidad
    └── tab_datos.py        # Pestaña: datos crudos y descarga CSV
```

## Instalación y Ejecución

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la aplicación
streamlit run app.py
```

## Descripción de Módulos

| Archivo | Responsabilidad |
|---------|----------------|
| `modelo.py` | Lógica de simulación DES con Mesa. Agentes y modelo. |
| `teoria.py` | Cálculo analítico de P₀, Pₙ, L, Lq, W, Wq, U. |
| `graficos.py` | Funciones Plotly: cola visual, evolución, Pₙ, histogramas, heatmap. |
| `ui/sidebar.py` | Controles interactivos (λ, μ, K, T_max, seed). |
| `ui/tab_cola.py` | Diagrama de la cola + animación paso a paso. |
| `ui/tab_resultados.py` | Métricas simuladas vs teóricas + 4 gráficas. |
| `ui/tab_matematico.py` | Teoría completa con fórmulas LaTeX renderizadas. |
| `ui/tab_sensibilidad.py` | Curvas L/Pₖ vs ρ, efecto de K, heatmap. |
| `ui/tab_datos.py` | DataCollector de Mesa, eventos, descarga CSV. |

## Parámetros del Modelo

| Parámetro | Descripción | Rango |
|-----------|-------------|-------|
| **λ** | Tasa de llegadas | 0.5 – 10.0 |
| **μ** | Tasa de servicio | 0.5 – 10.0 |
| **K** | Capacidad máxima | 2 – 30 |
| **T_max** | Tiempo de simulación | 500 – 20 000 |
| **seed** | Semilla aleatoria | 0 – 9999 |
