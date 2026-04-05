# -*- coding: utf-8 -*-
"""
Sistema de logros con notificaciones visuales.
"""

import time

import pygame

from config import (
    FOSF_VERDE, AMBER, CYAN_SCAN, AZUL_DATA, ROJO_ALERTA,
    MORADO, ORO, BLANCO, ANCHO, pantalla,
    F_TINY, F_BOLD,
)
from ui import txt
from sonidos import play


LOGROS_DEF = {
    "PRIMERA_SANGRE": ("Primera Sangre",    "Completa tu primera misión",    FOSF_VERDE,  "★"),
    "SIN_PISTA":      ("Pura Intuición",     "Resuelve sin usar pistas",     AMBER,       "◈"),
    "RACHA_3":        ("En Racha",           "3 aciertos consecutivos",      CYAN_SCAN,   "◆"),
    "RACHA_5":        ("Imparable",          "5 aciertos consecutivos",      ORO,         "◆◆"),
    "VELOCISTA":      ("Velocista",          "Resuelve en <10 segundos",     AZUL_DATA,   "⚡"),
    "PERFECTO":       ("Operación Limpia",   "Todas las misiones sin error", MORADO,      "✦"),
    "CIFRADOR":       ("Cifrador Nativo",    "Domina el César",              FOSF_VERDE,  "⟁"),
    "DECODIFICADOR":  ("Decodificador",      "Domina Base64",                CYAN_SCAN,   "⟁"),
    "HUELLA":         ("Rastreador",         "Domina SHA-256",               AMBER,       "⟁"),
    "PROTOCOLO":      ("Maestro del DH",     "Domina Diffie-Hellman",        ROJO_ALERTA, "⟁"),
}


class LogroSystem:
    def __init__(self):
        self.desbloqueados = set()
        self.notificaciones = []

    def intentar(self, logro_id):
        if logro_id not in self.desbloqueados and logro_id in LOGROS_DEF:
            self.desbloqueados.add(logro_id)
            self.notificaciones.append((logro_id, time.time()))
            play("logro")
            return True
        return False

    def draw(self):
        now = time.time()
        self.notificaciones = [
            (lid, t) for lid, t in self.notificaciones if now - t < 4.0
        ]
        for i, (lid, t_aparicion) in enumerate(self.notificaciones):
            prog = (now - t_aparicion) / 4.0
            if prog < 0.15:
                alpha = prog / 0.15
            elif prog > 0.75:
                alpha = (1 - prog) / 0.25
            else:
                alpha = 1.0

            nombre, desc, col, icono = LOGROS_DEF[lid]
            ny = 70 + i * 65
            nw, nh = 380, 55
            nx = ANCHO - nw - 15

            s = pygame.Surface((nw, nh), pygame.SRCALPHA)
            pygame.draw.rect(s, (*col[:3], int(30 * alpha)),
                             (0, 0, nw, nh), border_radius=8)
            pygame.draw.rect(s, (*col[:3], int(180 * alpha)),
                             (0, 0, nw, nh), 2, border_radius=8)
            pantalla.blit(s, (nx, ny))

            c = tuple(max(0, min(255, int(x * alpha))) for x in col)
            txt(f"{icono} LOGRO DESBLOQUEADO", F_TINY, c, nx + 12, ny + 6)
            txt(nombre, F_BOLD, c, nx + 12, ny + 20)
            c_desc = tuple(max(0, min(255, int(x * alpha * 0.7))) for x in BLANCO)
            txt(desc, F_TINY, c_desc, nx + 12, ny + 38)


logros = LogroSystem()