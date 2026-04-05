# -*- coding: utf-8 -*-
"""
Pantalla de expedientes / récords.
"""

import pygame

from config import ANCHO, ALTO, reloj, pantalla, FOSF_VERDE, AMBER, CYAN_SCAN, FOSF_DIM, F_GRANDE, F_SMALL, F_MEDIA
from ui import fondo_terminal, txt, txt_glow, panel, boton
from efectos import tick_particles, lluvia_data


def pantalla_expedientes(rec):
    """Muestra los récords guardados. Se cierra con clic o tecla."""
    while True:
        fondo_terminal()
        lluvia_data(1)
        tick_particles()
        mouse = pygame.mouse.get_pos()

        panel(80, 50, ANCHO - 160, ALTO - 100, borde=AMBER, radio=8)
        txt("◈ EXPEDIENTES DE AGENTES ◈",
            F_GRANDE, AMBER, ANCHO // 2, 68, centro=True)
        pygame.draw.line(pantalla, AMBER, (110, 95), (ANCHO - 110, 95), 1)

        filas = [
            ("MEJOR PUNTAJE",  f"{rec['mejor_pts']:06d} pts", FOSF_VERDE),
            ("MEJOR RANGO",    rec["mejor_rango"],            AMBER),
            ("MISIONES ÉXITO", str(rec["exitos"]),             CYAN_SCAN),
            ("OPERACIONES",    str(rec["partidas"]),           FOSF_DIM),
        ]
        for i, (etq, val, col) in enumerate(filas):
            y = 115 + i * 75
            panel(120, y, ANCHO - 240, 58, borde=col, radio=5)
            txt(etq, F_SMALL, FOSF_DIM, 145, y + 8)
            txt_glow(val, F_GRANDE, col, ANCHO // 2 + 80, y + 14, centro=True)

        if rec["mejor_pts"] == 0:
            txt("SIN REGISTROS.", F_MEDIA, FOSF_DIM,
                ANCHO // 2, 420, centro=True)

        btn_v = boton("← VOLVER", ANCHO // 2 - 80, ALTO - 75, 160, 40,
                      (0, 40, 12), (0, 80, 25), mouse)

        pygame.display.flip()
        reloj.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if (ev.type == pygame.MOUSEBUTTONDOWN
                    and btn_v.collidepoint(ev.pos)):
                return
            if ev.type == pygame.KEYDOWN and ev.key in (
                    pygame.K_ESCAPE, pygame.K_RETURN):
                return