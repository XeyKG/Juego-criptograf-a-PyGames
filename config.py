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

# ─── MODO DE JUEGO ────────────────────────────────────────────────────────────
MODO_PRACTICA = False

# ─── PANTALLA ─────────────────────────────────────────────────────────────────
ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("OPERACIÓN SOMBRA v3.1 — Agencia de Inteligencia Cifrada")
reloj = pygame.time.Clock()

# ─── PALETA DE COLORES ────────────────────────────────────────────────────────
NEGRO       = (0, 0, 0)
FOSF_VERDE  = (0, 255, 70)
FOSF_DIM    = (0, 180, 55)      # era (0,140,40) — ahora más brillante
FOSF_DARK   = (0, 55, 18)       # era (0,40,12)
AMBER       = (255, 195, 0)     # era (255,180,0) — más vivo
AMBER_DIM   = (170, 100, 0)     # era (140,90,0)
ROJO_ALERTA = (255, 60, 60)     # era (255,30,30) — menos oscuro
ROJO_DIM    = (120, 20, 20)
AZUL_DATA   = (80, 200, 255)    # era (30,180,255) — más legible
CYAN_SCAN   = (0, 240, 240)     # era (0,230,230)
BLANCO      = (235, 245, 235)   # era (220,230,220) — más blanco
GRIS_PANEL  = (14, 22, 14)
GRIS_BORDE  = (0, 100, 30)      # era (0,80,25) — más visible
FONDO       = (5, 10, 5)
ORO         = (255, 215, 0)
MORADO      = (200, 80, 255)    # era (180,60,255)

# ─── FUENTES (TAMAÑOS AUMENTADOS PARA MEJOR LEGIBILIDAD) ─────────────────────
def _fuente(tam, bold=False):
    for nombre in ["Courier New", "Courier", "Consolas",
                    "DejaVu Sans Mono", "monospace"]:
        try:
            return pygame.font.SysFont(nombre, tam, bold=bold)
        except Exception:
            pass
    return pygame.font.Font(None, tam)

# ANTES → AHORA  (incremento ~20-30%)
F_GIANT  = _fuente(56, True)    # era 52
F_TITULO = _fuente(38, True)    # era 34
F_GRANDE = _fuente(28, True)    # era 24
F_MEDIA  = _fuente(22)          # era 18 — diferencia clave
F_SMALL  = _fuente(18)          # era 14 — el más crítico
F_MICRO  = _fuente(15)          # era 12
F_BOLD   = _fuente(22, True)    # era 18
F_TINY   = _fuente(14)          # era 11 — era casi ilegible

# ─── TIMER GLOBAL ─────────────────────────────────────────────────────────────
_t0 = time.time()

def t():
    return time.time() - _t0