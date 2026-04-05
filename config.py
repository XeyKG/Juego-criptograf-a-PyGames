# -*- coding: utf-8 -*-
"""
Configuración global del proyecto.
"""

import time
import subprocess
import sys

import pygame

pygame.init()

# ─── AUDIO ────────────────────────────────────────────────────────────────────
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    AUDIO_OK = True
except Exception:
    AUDIO_OK = False

# ─── PANTALLA ─────────────────────────────────────────────────────────────────
ANCHO, ALTO = 1280, 800
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("OPERACIÓN SOMBRA v3.0 — Agencia de Inteligencia Cifrada")
reloj = pygame.time.Clock()

# ─── PALETA DE COLORES ────────────────────────────────────────────────────────
NEGRO       = (0, 0, 0)
FOSF_VERDE  = (0, 255, 70)
FOSF_DIM    = (0, 140, 40)
FOSF_DARK   = (0, 40, 12)
AMBER       = (255, 180, 0)
AMBER_DIM   = (140, 90, 0)
ROJO_ALERTA = (255, 30, 30)
ROJO_DIM    = (100, 10, 10)
AZUL_DATA   = (30, 180, 255)
CYAN_SCAN   = (0, 230, 230)
BLANCO      = (220, 230, 220)
GRIS_PANEL  = (12, 18, 12)
GRIS_BORDE  = (0, 80, 25)
FONDO       = (4, 8, 4)
ORO         = (255, 215, 0)
MORADO      = (180, 60, 255)

# ─── FUENTES ──────────────────────────────────────────────────────────────────
def _fuente(tam, bold=False):
    for nombre in ["Courier New", "Courier", "Consolas",
                    "DejaVu Sans Mono", "monospace"]:
        try:
            return pygame.font.SysFont(nombre, tam, bold=bold)
        except Exception:
            pass
    return pygame.font.Font(None, tam)

F_GIANT  = _fuente(52, True)
F_TITULO = _fuente(34, True)
F_GRANDE = _fuente(24, True)
F_MEDIA  = _fuente(18)
F_SMALL  = _fuente(14)
F_MICRO  = _fuente(12)
F_BOLD   = _fuente(18, True)
F_TINY   = _fuente(11)

# ─── TIMER GLOBAL ─────────────────────────────────────────────────────────────
_t0 = time.time()

def t():
    return time.time() - _t0