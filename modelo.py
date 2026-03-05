"""
modelo.py
─────────
Agentes y modelo de simulación M/M/1/K/∞ usando Mesa (DES).
"""

from collections import deque
import numpy as np

from mesa import Agent, Model
from mesa.datacollection import DataCollector


# ─────────────────────────────────────────────────────────────────────────────
#  AGENTES
# ─────────────────────────────────────────────────────────────────────────────

class ClienteAgente(Agent):
    """
    Representa un cliente en el sistema M/M/1/K/∞.

    Atributos
    ---------
    tiempo_llegada  : momento en que llegó al sistema
    tiempo_inicio   : momento en que comenzó a ser atendido
    tiempo_salida   : momento en que salió del sistema
    fue_rechazado   : True si llegó con el sistema lleno
    """

    def __init__(self, unique_id: int, model: "ColaMM1K"):
        super().__init__(model)
        self.unique_id      = unique_id
        self.tiempo_llegada = model.tiempo_actual
        self.tiempo_inicio  = None
        self.tiempo_salida  = None
        self.fue_rechazado  = False

    @property
    def tiempo_en_cola(self) -> float | None:
        if self.tiempo_inicio is None:
            return None
        return self.tiempo_inicio - self.tiempo_llegada

    @property
    def tiempo_en_sistema(self) -> float | None:
        if self.tiempo_salida is None:
            return None
        return self.tiempo_salida - self.tiempo_llegada

    def step(self):
        pass


class ServidorAgente(Agent):
    """
    Representa el único servidor del sistema M/M/1/K/∞.

    Atributos
    ---------
    ocupado         : True si está atendiendo a alguien
    cliente_actual  : cliente en servicio (None si libre)
    fin_servicio    : tiempo programado de fin de servicio
    """

    def __init__(self, unique_id: int, model: "ColaMM1K"):
        super().__init__(model)
        self.unique_id      = unique_id
        self.ocupado        = False
        self.cliente_actual = None
        self.fin_servicio   = None

    def iniciar_servicio(self, cliente: ClienteAgente):
        self.ocupado           = True
        self.cliente_actual    = cliente
        cliente.tiempo_inicio  = self.model.tiempo_actual
        duracion               = self.model.random.expovariate(self.model.mu)
        self.fin_servicio      = self.model.tiempo_actual + duracion

    def terminar_servicio(self):
        cliente               = self.cliente_actual
        cliente.tiempo_salida = self.model.tiempo_actual
        self.model.clientes_atendidos.append(cliente)
        self.ocupado          = False
        self.cliente_actual   = None
        self.fin_servicio     = None

    def step(self):
        pass


# ─────────────────────────────────────────────────────────────────────────────
#  MODELO
# ─────────────────────────────────────────────────────────────────────────────

class ColaMM1K(Model):
    """
    Simulación de eventos discretos de la cola M/M/1/K/∞ usando Mesa.

    Parámetros
    ----------
    lam   : tasa de llegadas λ
    mu    : tasa de servicio μ
    K     : capacidad máxima del sistema (cola + servidor)
    T_max : tiempo máximo de simulación
    seed  : semilla para reproducibilidad
    """

    def __init__(
        self,
        lam: float   = 4.0,
        mu: float    = 6.0,
        K: int       = 5,
        T_max: float = 5000.0,
        seed: int    = 42,
    ):
        super().__init__(rng=seed)

        # Parámetros
        self.lam   = lam
        self.mu    = mu
        self.K     = K
        self.T_max = T_max

        # Estado
        self.tiempo_actual = 0.0
        self.cola          = deque()
        self.next_id       = 0
        self.running       = True

        # Servidor
        self.servidor = ServidorAgente(0, self)

        # Registros
        self.clientes_atendidos  = []
        self.clientes_rechazados = []
        self.total_llegadas      = 0

        # Integrales para L y Lq
        self._ultimo_cambio = 0.0
        self._area_sistema  = 0.0
        self._area_cola     = 0.0

        # Historial para gráficas
        self.historial_tiempo    = [0.0]
        self.historial_n_sistema = [0]
        self.historial_n_cola    = [0]
        self.historial_eventos   = []

        # DataCollector de Mesa
        self.datacollector = DataCollector(
            model_reporters={
                "Tiempo"          : lambda m: round(m.tiempo_actual, 4),
                "N_sistema"       : lambda m: m.n_en_sistema,
                "N_cola"          : lambda m: len(m.cola),
                "Servidor_ocupado": lambda m: int(m.servidor.ocupado),
                "Total_llegadas"  : lambda m: m.total_llegadas,
                "Total_atendidos" : lambda m: len(m.clientes_atendidos),
                "Total_rechazados": lambda m: len(m.clientes_rechazados),
            }
        )

        # Primera llegada programada
        self._proxima_llegada = self.random.expovariate(self.lam)

    # ── Propiedades ───────────────────────────────────────────────────────────

    @property
    def n_en_sistema(self) -> int:
        return len(self.cola) + int(self.servidor.ocupado)

    @property
    def sistema_lleno(self) -> bool:
        return self.n_en_sistema >= self.K

    # ── Motor DES interno ─────────────────────────────────────────────────────

    def _actualizar_areas(self, nuevo_tiempo: float):
        delta = nuevo_tiempo - self._ultimo_cambio
        self._area_sistema += self.n_en_sistema * delta
        self._area_cola    += len(self.cola) * delta
        self._ultimo_cambio = nuevo_tiempo

    def _registrar_historial(self):
        self.historial_tiempo.append(self.tiempo_actual)
        self.historial_n_sistema.append(self.n_en_sistema)
        self.historial_n_cola.append(len(self.cola))

    def _procesar_llegada(self):
        self.total_llegadas += 1
        cliente = ClienteAgente(self.next_id, self)
        self.next_id += 1

        if self.sistema_lleno:
            cliente.fue_rechazado = True
            self.clientes_rechazados.append(cliente)
            self._log_evento("rechazo")
        else:
            if not self.servidor.ocupado:
                self.servidor.iniciar_servicio(cliente)
                self._log_evento("llegada_directa")
            else:
                self.cola.append(cliente)
                self._log_evento("llegada_cola")

        self._proxima_llegada = (
            self.tiempo_actual + self.random.expovariate(self.lam)
        )

    def _procesar_fin_servicio(self):
        self.servidor.terminar_servicio()
        self._log_evento("salida")
        if self.cola:
            siguiente = self.cola.popleft()
            self.servidor.iniciar_servicio(siguiente)

    def _log_evento(self, tipo: str):
        self.historial_eventos.append({
            "t"   : self.tiempo_actual,
            "tipo": tipo,
            "n"   : self.n_en_sistema,
            "nq"  : len(self.cola),
        })

    # ── Paso principal ────────────────────────────────────────────────────────

    def step(self):
        if not self.running:
            return

        t_llegada  = self._proxima_llegada
        t_servicio = self.servidor.fin_servicio if self.servidor.ocupado else float("inf")
        t_proximo  = min(t_llegada, t_servicio, self.T_max)

        self._actualizar_areas(t_proximo)
        self.tiempo_actual = t_proximo

        if t_proximo >= self.T_max:
            self.running = False
        elif t_llegada <= t_servicio:
            self._procesar_llegada()
        else:
            self._procesar_fin_servicio()

        self._registrar_historial()
        self.datacollector.collect(self)

    def correr(self) -> "ColaMM1K":
        while self.running:
            self.step()
        return self

    # ── Estadísticas ──────────────────────────────────────────────────────────

    def estadisticas(self) -> dict:
        T         = self.tiempo_actual
        atendidos = self.clientes_atendidos
        rechazados = self.clientes_rechazados

        Pk_sim   = len(rechazados) / self.total_llegadas if self.total_llegadas > 0 else 0
        lam_ef   = self.lam * (1 - Pk_sim)
        L_sim    = self._area_sistema / T if T > 0 else 0
        Lq_sim   = self._area_cola    / T if T > 0 else 0
        t_srv    = sum(
            c.tiempo_salida - c.tiempo_inicio for c in atendidos
            if c.tiempo_inicio is not None and c.tiempo_salida is not None
        )
        U_sim    = t_srv / T if T > 0 else 0
        tq       = [c.tiempo_en_cola    for c in atendidos if c.tiempo_en_cola    is not None]
        ts       = [c.tiempo_en_sistema for c in atendidos if c.tiempo_en_sistema is not None]

        return {
            "P_K_sim"         : Pk_sim,
            "lambda_ef"       : lam_ef,
            "L_sim"           : L_sim,
            "Lq_sim"          : Lq_sim,
            "W_sim"           : float(np.mean(ts)) if ts else 0.0,
            "Wq_sim"          : float(np.mean(tq)) if tq else 0.0,
            "U_sim"           : U_sim,
            "total_llegadas"  : self.total_llegadas,
            "total_atendidos" : len(atendidos),
            "total_rechazados": len(rechazados),
        }
