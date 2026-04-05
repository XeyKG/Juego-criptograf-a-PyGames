# -*- coding: utf-8 -*-
"""
Pantalla de informe final de la operación.
"""

import pygame

from config import (
    ANCHO, ALTO, reloj, pantalla, FOSF_VERDE, AMBER, ROJO_ALERTA,
    ORO, FOSF_DIM, F_GRANDE, F_BOLD, F_SMALL, F_TINY,
)
from ui import fondo_terminal, txt, panel, boton
from efectos import tick_particles, lluvia_data
from estado import agente
from logros import logros, LOGROS_DEF


def pantalla_resultados(resultados_misiones):
    """
    Muestra el informe final.
    resultados_misiones: lista de (exitosa, puntos, tiempo_segundos)
    """
    while True:
        fondo_terminal()
        lluvia_data(2)
        tick_particles()
        mouse = pygame.mouse.get_pos()

        pw, ph = 700, 520
        px = ANCHO // 2 - pw // 2
        py = ALTO // 2 - ph // 2
        panel(px, py, pw, ph, col=(12, 18, 12), borde=ORO,
              radio=8, alpha=230)

        txt("◈ INFORME DE OPERACIÓN — OPERACIÓN SOMBRA ◈",
            F_BOLD, ORO, ANCHO // 2, py + 15, centro=True)
        pygame.draw.line(pantalla, ORO,
                         (px + 20, py + 38), (px + pw - 20, py + 38), 1)

        rango_nombre, rango_col = agente.rango()
        txt(f"RANGO FINAL: {rango_nombre}",
            F_GRANDE, rango_col, ANCHO // 2, py + 50, centro=True)
        txt(f"PUNTOS TOTALES: {agente.pts:06d}",
            F_GRANDE, AMBER, ANCHO // 2, py + 78, centro=True)
        txt(f"RACHA MÁXIMA: ×{agente.racha_max}  |  "
            f"TIEMPO: {int(agente.tiempo())}s",
            F_SMALL, FOSF_DIM, ANCHO // 2, py + 108, centro=True)

        # Detalle por misión
        nombres = ["M1: CÉSAR", "M2: BASE64", "M3: SHA-256", "M4: DIFFIE-H."]
        y = py + 135
        for i, (nom, (ok, pts, t_seg)) in enumerate(
                zip(nombres, resultados_misiones)):
            col = FOSF_VERDE if ok else ROJO_ALERTA
            icon = "✓" if ok else "✗"
            panel(px + 30, y, pw - 60, 42, borde=col, radio=4)
            txt(f"{icon} {nom}", F_BOLD, col, px + 45, y + 5)
            txt(f"+{pts} pts  |  {t_seg:.1f}s",
                F_SMALL, FOSF_DIM, px + 45, y + 23)
            y += 50

        # Logros especiales
        y += 10
        if agente.sin_errores:
            txt("★ OPERACIÓN LIMPIA — Sin errores ★",
                F_SMALL, ORO, ANCHO // 2, y, centro=True)
            logros.intentar("PERFECTO")
            y += 20
        if agente.sin_pistas:
            txt("◈ PURA INTUICIÓN — Sin pistas usadas ◈",
                F_SMALL, AMBER, ANCHO // 2, y, centro=True)
            y += 20

        # Lista de logros desbloqueados
        if logros.desbloqueados:
            y += 5
            txt("LOGROS:", F_TINY, FOSF_DIM, px + 30, y)
            y += 16
            for lid in logros.desbloqueados:
                if lid in LOGROS_DEF:
                    nombre, _, col, icono = LOGROS_DEF[lid]
                    txt(f"{icono} {nombre}", F_TINY, col, px + 40, y)
                    y += 14

        btn_v = boton("VOLVER AL CUARTEL",
                      ANCHO // 2 - 110, py + ph - 52, 220, 40,
                      (0, 60, 20), (0, 120, 40), mouse)

        pygame.display.flip()
        reloj.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and btn_v.collidepoint(ev.pos):
                return
            if ev.type == pygame.KEYDOWN:
                return