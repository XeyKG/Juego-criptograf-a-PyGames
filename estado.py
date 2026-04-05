# -*- coding: utf-8 -*-
"""
Estado del agente: puntos, racha, cobertura, rangos.
"""

import time

from config import FOSF_DIM, FOSF_VERDE, AMBER, ROJO_ALERTA, ORO, MORADO


# ─── Rangos ───────────────────────────────────────────────────────────────────
RANGOS = [
    (0,    "RECLUTA",        FOSF_DIM),
    (500,  "OPERATIVO",      FOSF_VERDE),
    (1000, "ESPECIALISTA",   AMBER),
    (1500, "AGENTE ELITE",   ROJO_ALERTA),
    (2500, "MAESTRO CIPHER", ORO),
    (4000, "SOMBRA SUPREMA", MORADO),
]


class Agente:
    def __init__(self):
        self.pts = 0
        self.racha = 0
        self.racha_max = 0
        self.alertas = 0
        self.misiones_ok = 0
        self.t_inicio = time.time()
        self.cobertura = 100
        self.sin_pistas = True
        self.sin_errores = True
        self.herramientas = {"scanner": 0, "acelerador": 0, "escudo": 0}

    def rango(self):
        """Retorna (nombre_rango, color_rango)."""
        for pts_min, nombre, col in reversed(RANGOS):
            if self.pts >= pts_min:
                return nombre, col
        return RANGOS[0][1], RANGOS[0][2]

    def sumar(self, base, vidas, tb=0):
        """Calcula puntos con multiplicadores y los suma."""
        mult = 1.0 + self.racha * 0.3 + vidas * 0.2 + tb * 0.5
        pts = int(base * mult)
        self.pts += pts
        return pts

    def acierto(self):
        self.racha += 1
        self.racha_max = max(self.racha, self.racha_max)
        self.misiones_ok += 1

    def fallo(self):
        self.racha = 0
        self.cobertura = max(0, self.cobertura - 15)
        self.sin_errores = False

    def usar_pista(self):
        self.sin_pistas = False

    def tiempo(self):
        return time.time() - self.t_inicio


# Instancia global
agente = Agente()