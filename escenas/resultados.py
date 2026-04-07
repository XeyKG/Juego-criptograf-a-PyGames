# -*- coding: utf-8 -*-
"""
Pantalla de informe final — v3.1 LEGIBILIDAD MEJORADA
Cambios: fuentes más grandes, más espacio entre filas, contraste mejorado.
"""

import time
import pygame

from config import (
    ANCHO, ALTO, reloj, pantalla, FOSF_VERDE, AMBER, ROJO_ALERTA,
    ORO, FOSF_DIM, MORADO, BLANCO, F_GRANDE, F_BOLD, F_SMALL, F_TINY,
    F_MEDIA, F_MICRO, F_TITULO, GRIS_PANEL,
)
from ui import fondo_terminal, txt, txt_glow, panel, boton
from efectos import tick_particles, lluvia_data
from estado import agente
from logros import logros, LOGROS_DEF


def pantalla_resultados(resultados_misiones):
    """
    Informe final — v3.1
    resultados_misiones: lista de (exitosa, puntos, tiempo_segundos)
    """
    t_inicio = time.time()
    mientras = True

    while mientras:
        fondo_terminal()
        lluvia_data(2)
        tick_particles()
        mouse = pygame.mouse.get_pos()

        # Panel principal — más alto
        pw, ph = 820, 620
        px = ANCHO // 2 - pw // 2
        py = ALTO // 2 - ph // 2
        panel(px, py, pw, ph, col=(12, 18, 12), borde=ORO,
              radio=10, alpha=245)

        # Encabezado
        txt_glow("◆ INFORME FINAL — OPERACIÓN SOMBRA ◆",
                F_BOLD, ORO, ANCHO // 2, py + 18, centro=True)
        pygame.draw.line(pantalla, ORO,
                         (px + 20, py + 46), (px + pw - 20, py + 46), 2)

        # Estadísticas generales
        rango_nombre, rango_col = agente.rango()
        tiempo_desde_inicio = time.time() - t_inicio

        txt(f"RANGO ASIGNADO:  {rango_nombre}",
            F_GRANDE, rango_col, ANCHO // 2, py + 58, centro=True)

        if tiempo_desde_inicio < 2.0:
            progreso = tiempo_desde_inicio / 2.0
            pts_mostrados = int(agente.pts * progreso)
            txt(f"PUNTOS: {pts_mostrados:06d}",
                F_GRANDE, AMBER, ANCHO // 2, py + 92, centro=True)
        else:
            txt(f"PUNTOS: {agente.pts:06d}",
                F_GRANDE, AMBER, ANCHO // 2, py + 92, centro=True)

        pygame.draw.line(pantalla, FOSF_DIM,
                         (px + 30, py + 118), (px + pw - 30, py + 118), 1)

        # Estadísticas en dos columnas
        y = py + 130
        tot_pts = sum(r[1] for r in resultados_misiones)
        tot_tiempo = sum(r[2] for r in resultados_misiones)
        completadas = sum(1 for r in resultados_misiones if r[0])

        col_izq = px + 50
        col_der = px + pw // 2 + 20

        txt("ESTADÍSTICAS", F_SMALL, FOSF_VERDE, col_izq, y)
        y += 24

        stats_izq = [
            (f"Misiones: {completadas}/4",
             FOSF_VERDE if completadas == 4 else AMBER),
            (f"Tiempo total: {tot_tiempo:.1f}s", FOSF_DIM),
        ]
        stats_der = [
            (f"Racha máx: ×{agente.racha_max}",
             MORADO if agente.racha_max > 3 else FOSF_DIM),
            (f"Sesión: {int(agente.tiempo())}s", FOSF_DIM),
        ]

        for (t_i, c_i), (t_d, c_d) in zip(stats_izq, stats_der):
            txt(t_i, F_SMALL, c_i, col_izq, y)
            txt(t_d, F_SMALL, c_d, col_der, y)
            y += 22

        # Detalle por misión
        y += 8
        pygame.draw.line(pantalla, FOSF_DIM,
                         (px + 30, y), (px + pw - 30, y), 1)
        y += 10
        txt("DETALLE POR MISIÓN", F_SMALL, FOSF_VERDE, col_izq, y)
        y += 26

        nombres = ["M1: CIFRADO CÉSAR", "M2: BASE64",
                   "M3: SHA-256", "M4: DIFFIE-HELLMAN"]
        FILA_H = 38  # era 32 — más espacio
        for i, (nom, (ok, pts, t_seg)) in enumerate(
                zip(nombres, resultados_misiones)):
            col = FOSF_VERDE if ok else ROJO_ALERTA
            icon = "✓" if ok else "✗"

            # Fondo de fila con color según resultado
            fondo = (0, 30, 10) if ok else (30, 5, 5)
            panel(px + 35, y - 4, pw - 70, FILA_H,
                  col=fondo, borde=col, radio=4, alpha=200)

            txt(f"{icon}", F_BOLD, col, px + 50, y + 8)
            txt(nom, F_SMALL, col, px + 75, y + 8)
            txt(f"+{pts:05d} pts", F_SMALL, AMBER if ok else FOSF_DIM,
                px + pw - 220, y + 8)
            txt(f"{t_seg:.1f}s", F_SMALL, FOSF_DIM,
                px + pw - 100, y + 8)
            y += FILA_H + 4

        # Bonificaciones
        y += 4
        if agente.sin_errores or agente.sin_pistas:
            pygame.draw.line(pantalla, FOSF_DIM,
                             (px + 30, y), (px + pw - 30, y), 1)
            y += 10
            txt("★ BONIFICACIONES", F_SMALL, ORO, col_izq, y)
            y += 22
            if agente.sin_errores:
                txt("  ✓  OPERACIÓN LIMPIA — Sin errores",
                    F_SMALL, ORO, px + 50, y)
                y += 20
            if agente.sin_pistas:
                txt("  ◈  PURA INTUICIÓN — Sin ayuda",
                    F_SMALL, AMBER, px + 50, y)
                y += 20

        # Botón más grande
        btn_v = boton("VOLVER AL CUARTEL",
                      ANCHO // 2 - 140, py + ph - 58, 280, 46,
                      (0, 65, 22), (0, 130, 45), mouse)

        pygame.display.flip()
        reloj.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and btn_v.collidepoint(ev.pos):
                mientras = False
            if ev.type == pygame.KEYDOWN:
                mientras = False
