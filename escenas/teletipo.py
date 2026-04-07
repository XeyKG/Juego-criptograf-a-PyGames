# -*- coding: utf-8 -*-
"""
Animación de texto tipo teletipo — v3.1 LEGIBILIDAD MEJORADA
Cambios: márgenes más amplios, fuente más grande, panel de fondo,
         instrucciones más claras, espaciado entre líneas aumentado.
"""

import random
import math
import time
import sys

import pygame

from config import (
    ANCHO, ALTO, reloj, pantalla,
    FOSF_VERDE, FOSF_DIM, FOSF_DARK, AMBER, ROJO_ALERTA, BLANCO,
    F_MEDIA, F_SMALL, F_MICRO, F_GRANDE, F_GIANT, F_BOLD, F_TINY,
    GRIS_PANEL,
)
from ui import txt, txt_glow, panel
from efectos import tick_particles, lluvia_data, boom
from sonidos import play


def teletipo(lineas, vel=0.035):
    """
    Muestra líneas de texto como teletipo.
    lineas: lista de (texto, color).
    Mejoras v3.1: panel de fondo, márgenes amplios, espaciado mayor.
    """
    from ui import fondo_terminal

    mostrado = []
    idx_linea = 0
    idx_char = 0
    t_ultimo = time.time()
    cur_txt = ""
    mientras = True

    # Área de texto con márgenes generosos
    MARGEN_X = 80
    MARGEN_Y = 55
    ANCHO_TXT = ANCHO - MARGEN_X * 2
    INTERLINEA = 30  # era 24 — más espacio entre líneas

    while mientras and idx_linea < len(lineas):
        fondo_terminal()
        tick_particles()
        lluvia_data(1)

        # Panel de fondo para mejorar contraste del texto
        panel(MARGEN_X - 20, MARGEN_Y - 15,
              ANCHO_TXT + 40, ALTO - MARGEN_Y * 2 + 10,
              col=(8, 14, 8), borde=FOSF_DIM, radio=6, alpha=200)

        txt(">> TRANSMISIÓN ENTRANTE — AGENCIA CIPHER <<",
            F_SMALL, FOSF_DIM, ANCHO // 2, MARGEN_Y - 8, centro=True)
        pygame.draw.line(pantalla, FOSF_DIM,
                         (MARGEN_X, MARGEN_Y + 10),
                         (ANCHO - MARGEN_X, MARGEN_Y + 10), 1)

        y = MARGEN_Y + 22
        for lt, lc in mostrado:
            if lt:
                txt(lt, F_MEDIA, lc, MARGEN_X, y)
            y += INTERLINEA

        if idx_linea < len(lineas):
            la, ca = lineas[idx_linea]
            now = time.time()
            if now - t_ultimo >= vel:
                if idx_char < len(la):
                    cur_txt += la[idx_char]
                    idx_char += 1
                    t_ultimo = now
                    play("tecla")
                else:
                    mostrado.append((cur_txt, ca))
                    cur_txt = ""
                    idx_char = 0
                    idx_linea += 1
            if cur_txt:
                cursor = "|" if int(time.time() * 3) % 2 == 0 else ""
                txt(cur_txt + cursor, F_MEDIA, ca, MARGEN_X, y)
        else:
            mientras = False

        # Instrucción más visible
        panel(ANCHO - 280, ALTO - 38, 260, 28,
              col=(15, 25, 15), borde=FOSF_DARK, radio=4, alpha=180)
        txt("[ ESPACIO para saltar ]", F_MICRO, FOSF_DIM,
            ANCHO - 155, ALTO - 30, centro=True)

        pygame.display.flip()
        reloj.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    mostrado = list(lineas)
                    idx_linea = len(lineas)
                    mientras = False
                if ev.key == pygame.K_ESCAPE:
                    return

    # Espera a que presione una tecla
    while True:
        fondo_terminal()
        tick_particles()
        lluvia_data(1)

        panel(MARGEN_X - 20, MARGEN_Y - 15,
              ANCHO_TXT + 40, ALTO - MARGEN_Y * 2 + 10,
              col=(8, 14, 8), borde=FOSF_DIM, radio=6, alpha=200)

        txt(">> TRANSMISIÓN COMPLETA <<",
            F_SMALL, FOSF_DIM, ANCHO // 2, MARGEN_Y - 8, centro=True)
        pygame.draw.line(pantalla, FOSF_DIM,
                         (MARGEN_X, MARGEN_Y + 10),
                         (ANCHO - MARGEN_X, MARGEN_Y + 10), 1)

        y = MARGEN_Y + 22
        for lt, lc in mostrado:
            if lt:
                txt(lt, F_MEDIA, lc, MARGEN_X, y)
            y += INTERLINEA

        # Botón pulsante de continuar
        pulse = 0.7 + 0.3 * math.sin(time.time() * 3)
        col_btn = tuple(int(c * pulse) for c in AMBER)
        panel(ANCHO // 2 - 330, ALTO - 52, 660, 38,
              col=(30, 25, 0), borde=AMBER, radio=5, alpha=200)
        txt("[ PRESIONA CUALQUIER TECLA PARA CONTINUAR ]",
            F_SMALL, col_btn, ANCHO // 2, ALTO - 38, centro=True)

        pygame.display.flip()
        reloj.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return


def briefing_mision(num, titulo, lineas, col, tlim):
    """Pantalla de briefing cinematográfica — v3.1."""
    from ui import fondo_terminal

    t0 = time.time()
    dur = 7.0

    while time.time() - t0 < dur:
        tt = (time.time() - t0) / dur
        fondo_terminal()
        lluvia_data(2)
        tick_particles()

        # Interferencia inicial
        if tt < 0.3:
            for _ in range(6):
                import random
                s = pygame.Surface(
                    (random.randint(20, 200), random.randint(2, 6)),
                    pygame.SRCALPHA)
                s.fill((*FOSF_VERDE, random.randint(20, 60)))
                pantalla.blit(s, (random.randint(0, ANCHO),
                                  random.randint(0, ALTO)))

        sc = min(1.0, tt * 2.5)
        mw = int(860 * sc)   # un poco más ancho
        mh = int(500 * sc)   # un poco más alto
        if mw > 10:
            mx = ANCHO // 2 - mw // 2
            my = ALTO // 2 - mh // 2
            panel(mx, my, mw, mh, col=(10, 16, 10), borde=col,
                  radio=8, alpha=230)

            # Esquinas
            lg = 45
            for sx, sy, dx, dy in [
                (mx, my, 1, 1), (mx + mw, my, -1, 1),
                (mx, my + mh, 1, -1), (mx + mw, my + mh, -1, -1)
            ]:
                pygame.draw.line(pantalla, col,
                                 (sx, sy), (sx + dx * lg, sy), 3)
                pygame.draw.line(pantalla, col,
                                 (sx, sy), (sx, sy + dy * lg), 3)

            if sc > 0.4:
                a = min(1.0, (tt - 0.16) * 3)
                ca = tuple(int(c * a) for c in col)
                txt(f"MISIÓN 0{num}", F_SMALL, ca,
                    ANCHO // 2, my + 28, centro=True)
                pygame.draw.line(pantalla, ca,
                                 (mx + 30, my + 52), (mx + mw - 30, my + 52), 1)

            if sc > 0.55:
                a = min(1.0, (tt - 0.22) * 4)
                txt_glow(titulo, F_GIANT,
                         tuple(int(c * a) for c in col),
                         ANCHO // 2, my + 68, centro=True)

            if sc > 0.7:
                a = min(1.0, (tt - 0.28) * 5)
                ct = tuple(int(c * a) for c in BLANCO)
                for i, l in enumerate(lineas[:4]):
                    txt(l, F_SMALL, ct,
                        ANCHO // 2, my + 158 + i * 32, centro=True)

            if sc > 0.85:
                a = min(1.0, (tt - 0.34) * 6)
                ct = tuple(int(c * a) for c in ROJO_ALERTA)
                txt(f"TIEMPO LÍMITE: {tlim}s", F_BOLD, ct,
                    ANCHO // 2, my + mh - 65, centro=True)

        boom(ANCHO // 2, ALTO // 2, col, 1, "esfera")
        pygame.display.flip()
        reloj.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                return
