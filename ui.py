# -*- coding: utf-8 -*-
"""
Componentes de interfaz reutilizables:
fondo, texto, paneles, botones, inputs, barras, HUD.
"""

import math
import time

import pygame

from config import (
    ANCHO, ALTO, pantalla, reloj, t,
    FOSF_VERDE, FOSF_DIM, FOSF_DARK, AMBER, AMBER_DIM,
    ROJO_ALERTA, ROJO_DIM, CYAN_SCAN, BLANCO,
    GRIS_PANEL, GRIS_BORDE, FONDO,
    F_GIANT, F_TITULO, F_GRANDE, F_MEDIA, F_SMALL,
    F_MICRO, F_BOLD, F_TINY,
)
from estado import agente


# ═══════════════════════════════════════════════════════════════════════════════
#  FONDO TERMINAL
# ═══════════════════════════════════════════════════════════════════════════════

def fondo_terminal():
    """Dibuja el fondo con scanlines y grid sutil."""
    pantalla.fill(FONDO)
    # Scanlines
    s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    for y in range(0, ALTO, 3):
        pygame.draw.line(s, (0, 0, 0, 50), (0, y), (ANCHO, y))
    pantalla.blit(s, (0, 0))
    # Grid
    for x in range(0, ANCHO, 80):
        pygame.draw.line(pantalla, (0, 18, 6), (x, 0), (x, ALTO))
    for y in range(0, ALTO, 80):
        pygame.draw.line(pantalla, (0, 18, 6), (0, y), (ANCHO, y))


# ═══════════════════════════════════════════════════════════════════════════════
#  TEXTO
# ═══════════════════════════════════════════════════════════════════════════════

def txt(texto, fnt, col, x, y, centro=False):
    """Dibuja texto y retorna el rect."""
    sup = fnt.render(str(texto), True, col)
    r = sup.get_rect()
    if centro:
        r.centerx = int(x)
    else:
        r.x = int(x)
    r.y = int(y)
    pantalla.blit(sup, r)
    return r


def txt_glow(texto, fnt, col, x, y, centro=False):
    """Texto con efecto de neón/glow."""
    glow = tuple(min(255, c // 3) for c in col)
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        s = fnt.render(str(texto), True, glow)
        r = s.get_rect()
        if centro:
            r.centerx = int(x) + dx
        else:
            r.x = int(x) + dx
        r.y = int(y) + dy
        pantalla.blit(s, r)
    return txt(texto, fnt, col, x, y, centro)


# ═══════════════════════════════════════════════════════════════════════════════
#  PANEL
# ═══════════════════════════════════════════════════════════════════════════════

def panel(x, y, w, h, col=None, borde=None, radio=6, alpha=210):
    """Panel semitransparente con borde."""
    col = col or GRIS_PANEL
    borde = borde or GRIS_BORDE
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (*col, alpha), (0, 0, w, h), border_radius=radio)
    pantalla.blit(s, (x, y))
    pygame.draw.rect(pantalla, borde, (x, y, w, h), 1, border_radius=radio)


# ═══════════════════════════════════════════════════════════════════════════════
#  BOTÓN
# ═══════════════════════════════════════════════════════════════════════════════

def boton(texto, x, y, w, h, col_n, col_h, mouse,
          fnt=None, icono="", enabled=True):
    """Botón con hover y estado disabled. Retorna Rect."""
    fnt = fnt or F_MEDIA
    r = pygame.Rect(x, y, w, h)

    if not enabled:
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(s, (*col_n, 80), (0, 0, w, h), border_radius=5)
        pantalla.blit(s, (x, y))
        pygame.draw.rect(pantalla, FOSF_DARK, r, 1, border_radius=5)
        txt(icono + texto, fnt, FOSF_DARK,
            x + w // 2, y + h // 2 - fnt.get_height() // 2, centro=True)
        return r

    hov = r.collidepoint(mouse)
    c = col_h if hov else col_n
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (*c, 200), (0, 0, w, h), border_radius=5)
    if hov:
        pygame.draw.rect(s, (255, 255, 255, 20), (0, 0, w, h // 2),
                         border_radius=5)
    pantalla.blit(s, (x, y))
    bord = FOSF_VERDE if hov else FOSF_DIM
    pygame.draw.rect(pantalla, bord, r, 1, border_radius=5)
    txt(icono + texto, fnt, BLANCO if hov else FOSF_DIM,
        x + w // 2, y + h // 2 - fnt.get_height() // 2, centro=True)
    return r


# ═══════════════════════════════════════════════════════════════════════════════
#  INPUT BOX
# ═══════════════════════════════════════════════════════════════════════════════

def input_box(texto, x, y, w, activo=True, placeholder="", max_len=20):
    """Caja de texto con cursor parpadeante."""
    col_b = FOSF_VERDE if activo else FOSF_DIM
    r = pygame.Rect(x, y, w, 36)
    s = pygame.Surface((w, 36), pygame.SRCALPHA)
    pygame.draw.rect(s, (0, 20, 8, 220), (0, 0, w, 36), border_radius=4)
    pantalla.blit(s, (x, y))
    pygame.draw.rect(pantalla, col_b, r, 1, border_radius=4)
    if activo:
        pygame.draw.rect(pantalla, (*FOSF_VERDE, 60),
                         (x - 1, y - 1, w + 2, 38), 1, border_radius=5)
    cur = "|" if activo and int(time.time() * 2) % 2 == 0 else ""
    if not texto and placeholder:
        txt(placeholder, F_MEDIA, FOSF_DARK, x + 8, y + 9)
    else:
        txt(texto + cur, F_BOLD, FOSF_VERDE, x + 8, y + 8)


# ═══════════════════════════════════════════════════════════════════════════════
#  BARRA DE TIEMPO
# ═══════════════════════════════════════════════════════════════════════════════

def barra_tiempo(x, y, w, h, restante, maximo,
                 col_ok=FOSF_VERDE, col_warn=AMBER, col_crit=ROJO_ALERTA):
    """Barra de progreso con cambio de color según urgencia."""
    pygame.draw.rect(pantalla, GRIS_PANEL, (x, y, w, h), border_radius=3)
    ratio = max(0, restante / maximo)
    fw = int(w * ratio)
    col = col_ok if ratio > 0.5 else (col_warn if ratio > 0.25 else col_crit)
    if fw > 0:
        pygame.draw.rect(pantalla, col, (x, y, fw, h), border_radius=3)
        # Brillo superior
        s = pygame.Surface((fw, h // 2), pygame.SRCALPHA)
        s.fill((255, 255, 255, 20))
        pantalla.blit(s, (x, y))
    pygame.draw.rect(pantalla, FOSF_DIM, (x, y, w, h), 1, border_radius=3)
    # Parpadeo cuando es crítico
    if ratio < 0.25 and int(t() * 8) % 2 == 0:
        pygame.draw.rect(pantalla, BLANCO, (x, y, fw, h), border_radius=3)
    txt(f"{max(0, int(restante))}s", F_MICRO, col, x + w + 6, y + 1)


# ═══════════════════════════════════════════════════════════════════════════════
#  HUD SUPERIOR (barra de estado durante misiones)
# ═══════════════════════════════════════════════════════════════════════════════

def hud_superior(mision_num, titulo, color, vidas):
    """Dibuja la barra superior con info del agente y misión."""
    s = pygame.Surface((ANCHO, 55), pygame.SRCALPHA)
    pygame.draw.rect(s, (0, 12, 4, 240), (0, 0, ANCHO, 55))
    pantalla.blit(s, (0, 0))
    pygame.draw.line(pantalla, color, (0, 55), (ANCHO, 55), 2)

    # ── Izquierda: ID y rango ──
    rango_nombre, rango_col = agente.rango()
    txt("AGT. CIPHER", F_TINY, FOSF_DIM, 12, 5)
    txt(rango_nombre, F_SMALL, rango_col, 12, 19)

    # Cobertura mini
    for i in range(10):
        c = FOSF_VERDE if i < agente.cobertura // 10 else FOSF_DARK
        pygame.draw.rect(pantalla, c, (12 + i * 13, 38, 9, 10),
                         border_radius=2)
    cov_col = FOSF_VERDE if agente.cobertura > 50 else ROJO_ALERTA
    txt(f"{agente.cobertura}%", F_TINY, cov_col, 12 + 10 * 13 + 4, 38)

    # ── Centro: misión ──
    txt_glow(f"[ MISIÓN 0{mision_num}: {titulo} ]",
             F_BOLD, color, ANCHO // 2, 5, centro=True)
    txt("CLASIFICADO — OJOS SOLO AUTORIZADOS",
        F_TINY, FOSF_DIM, ANCHO // 2, 28, centro=True)

    # ── Herramientas ──
    hx = ANCHO // 2 - 90
    txt(f"◉ Scanner:{agente.herramientas['scanner']}", F_TINY, CYAN_SCAN, hx, 42)
    txt(f"◉ Acel:{agente.herramientas['acelerador']}", F_TINY, AMBER, hx + 100, 42)
    txt(f"◉ Escudo:{agente.herramientas['escudo']}", F_TINY, FOSF_VERDE, hx + 190, 42)

    # ── Derecha: puntos, racha, vidas ──
    txt(f"PUNTOS: {agente.pts:06d}", F_SMALL, AMBER, ANCHO - 180, 5)
    if agente.racha > 1:
        if agente.racha >= 5:
            racha_col = (255, 215, 0)
        elif agente.racha >= 3:
            racha_col = ROJO_ALERTA
        else:
            racha_col = AMBER
        txt(f"RACHA ×{agente.racha}", F_SMALL, racha_col, ANCHO - 180, 22)

    for i in range(3):
        c = FOSF_VERDE if i < vidas else ROJO_DIM
        cx = ANCHO - 165 + i * 22
        cy = 42
        pygame.draw.circle(pantalla, c, (cx, cy), 7)
        if i < vidas:
            c_brillo = tuple(min(255, x + 60) for x in c)
            pygame.draw.circle(pantalla, c_brillo, (cx - 2, cy - 2), 3)


# ═══════════════════════════════════════════════════════════════════════════════
#  INDICADOR DE PROGRESO (barra inferior con 4 misiones)
# ═══════════════════════════════════════════════════════════════════════════════

def indicador_progreso(mision_actual):
    """Dibuja la barra de progreso de misiones en la parte inferior."""
    nombres = ["CÉSAR", "BASE64", "SHA-256", "DIFFIE-H."]
    y = ALTO - 28
    w = (ANCHO - 80) // 4
    for i in range(4):
        x = 40 + i * w
        completada = i < mision_actual
        actual = i == mision_actual
        col_borde = (FOSF_VERDE if completada
                     else (AMBER if actual else FOSF_DIM))
        col_fondo = ((0, 35, 12) if completada
                     else (GRIS_PANEL if actual else FONDO))
        pygame.draw.rect(pantalla, col_fondo,
                         (x + 1, y, w - 2, 16), border_radius=4)
        pygame.draw.rect(pantalla, col_borde,
                         (x + 1, y, w - 2, 16), 1, border_radius=4)
        if completada:
            txt("✓ " + nombres[i], F_TINY, FOSF_VERDE,
                x + w // 2, y + 2, centro=True)
        elif actual:
            txt("▶ " + nombres[i], F_TINY, AMBER,
                x + w // 2, y + 2, centro=True)
        else:
            txt("— " + nombres[i], F_TINY, FOSF_DARK,
                x + w // 2, y + 2, centro=True)