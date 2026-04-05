# -*- coding: utf-8 -*-
"""
Animación de texto tipo teletipo y briefing cinematográfico.
"""

import random
import math
import time
import sys

import pygame

from config import (
    ANCHO, ALTO, reloj, pantalla,
    FOSF_VERDE, FOSF_DIM, FOSF_DARK, AMBER, ROJO_ALERTA, BLANCO,
    F_MEDIA, F_SMALL, F_MICRO, F_GRANDE, F_GIANT, F_BOLD,
)
from ui import txt, txt_glow, panel
from efectos import tick_particles, lluvia_data, boom
from sonidos import play


def teletipo(lineas, vel=0.04):
    """
    Muestra líneas de texto como teletipo.
    lineas: lista de (texto, color).
    """
    from ui import fondo_terminal

    mostrado = []
    idx_linea = 0
    idx_char = 0
    t_ultimo = time.time()
    cur_txt = ""
    mientras = True

    while mientras and idx_linea < len(lineas):
        fondo_terminal()
        tick_particles()
        lluvia_data(1)

        txt(">> TRANSMISIÓN ENTRANTE — AGENCIA CIPHER <<",
            F_MICRO, FOSF_DIM, ANCHO // 2, 10, centro=True)
        pygame.draw.line(pantalla, FOSF_DIM, (40, 24), (ANCHO - 40, 24), 1)

        y = 45
        for lt, lc in mostrado:
            txt(lt, F_MEDIA, lc, 50, y)
            y += 24

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
                txt(cur_txt + cursor, F_MEDIA, ca, 50, y)
        else:
            mientras = False

        txt("[ ESPACIO para saltar ]", F_MICRO, FOSF_DARK,
            ANCHO - 190, ALTO - 18)

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

    # Pausa breve
    t_fin = time.time()
    while time.time() - t_fin < 1.0:
        fondo_terminal()
        tick_particles()
        lluvia_data(1)
        txt(">> TRANSMISIÓN COMPLETA <<",
            F_MICRO, FOSF_DIM, ANCHO // 2, 10, centro=True)
        pygame.draw.line(pantalla, FOSF_DIM, (40, 24), (ANCHO - 40, 24), 1)
        y = 45
        for lt, lc in mostrado:
            txt(lt, F_MEDIA, lc, 50, y)
            y += 24
        txt("[ PRESIONA CUALQUIER TECLA ]",
            F_SMALL, AMBER, ANCHO // 2, ALTO - 30, centro=True)
        pygame.display.flip()
        reloj.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return


def briefing_mision(num, titulo, lineas, col, tlim):
    """Pantalla de briefing cinematográfica antes de cada misión."""
    from ui import fondo_terminal

    t0 = time.time()
    dur = 3.0

    while time.time() - t0 < dur:
        tt = (time.time() - t0) / dur
        fondo_terminal()
        lluvia_data(2)
        tick_particles()

        # Interferencia inicial
        if tt < 0.3:
            for _ in range(6):
                s = pygame.Surface(
                    (random.randint(20, 200), random.randint(2, 6)),
                    pygame.SRCALPHA)
                s.fill((*FOSF_VERDE, random.randint(20, 60)))
                pantalla.blit(s, (random.randint(0, ANCHO),
                                  random.randint(0, ALTO)))

        sc = min(1.0, tt * 2.5)
        mw = int(820 * sc)
        mh = int(480 * sc)
        if mw > 10:
            mx = ANCHO // 2 - mw // 2
            my = ALTO // 2 - mh // 2
            panel(mx, my, mw, mh, col=(12, 18, 12), borde=col,
                  radio=6, alpha=220)

            # Esquinas
            lg = 40
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
                    ANCHO // 2, my + 25, centro=True)
                pygame.draw.line(pantalla, ca,
                                 (mx + 30, my + 48), (mx + mw - 30, my + 48), 1)

            if sc > 0.55:
                a = min(1.0, (tt - 0.22) * 4)
                txt_glow(titulo, F_GIANT,
                         tuple(int(c * a) for c in col),
                         ANCHO // 2, my + 62, centro=True)

            if sc > 0.7:
                a = min(1.0, (tt - 0.28) * 5)
                ct = tuple(int(c * a) for c in BLANCO)
                for i, l in enumerate(lineas[:4]):
                    txt(l, F_SMALL, ct,
                        ANCHO // 2, my + 145 + i * 28, centro=True)

            if sc > 0.85:
                a = min(1.0, (tt - 0.34) * 6)
                ct = tuple(int(c * a) for c in ROJO_ALERTA)
                txt(f"TIEMPO LÍMITE: {tlim}s", F_BOLD, ct,
                    ANCHO // 2, my + mh - 70, centro=True)

        boom(ANCHO // 2, ALTO // 2, col, 1, "esfera")
        pygame.display.flip()
        reloj.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                return