# -*- coding: utf-8 -*-
"""
Pantalla de informe final de la operación con estadísticas detalladas.
"""

import time
import pygame

from config import (
    ANCHO, ALTO, reloj, pantalla, FOSF_VERDE, AMBER, ROJO_ALERTA,
    ORO, FOSF_DIM, MORADO, BLANCO, F_GRANDE, F_BOLD, F_SMALL, F_TINY,
)
from ui import fondo_terminal, txt, txt_glow, panel, boton
from efectos import tick_particles, lluvia_data
from estado import agente
from logros import logros, LOGROS_DEF


def pantalla_resultados(resultados_misiones):
    """
    Muestra el informe final mejorado con estadísticas detalladas.
    resultados_misiones: lista de (exitosa, puntos, tiempo_segundos)
    """
    t_inicio = time.time()
    mientras = True
    
    while mientras:
        fondo_terminal()
        lluvia_data(2)
        tick_particles()
        mouse = pygame.mouse.get_pos()

        # Panel principal
        pw, ph = 800, 600
        px = ANCHO // 2 - pw // 2
        py = ALTO // 2 - ph // 2
        panel(px, py, pw, ph, col=(12, 18, 12), borde=ORO,
              radio=8, alpha=240)

        # Encabezado
        txt_glow("◆ INFORME FINAL — OPERACIÓN SOMBRA ◆",
                F_BOLD, ORO, ANCHO // 2, py + 15, centro=True)
        pygame.draw.line(pantalla, ORO,
                         (px + 20, py + 40), (px + pw - 20, py + 40), 2)

        # Estadísticas generales
        rango_nombre, rango_col = agente.rango()
        
        # Animación de conteo si es reciente
        tiempo_desde_inicio = time.time() - t_inicio
        
        txt(f"RANGO ASIGNADO: {rango_nombre}",
            F_GRANDE, rango_col, ANCHO // 2, py + 55, centro=True)
        
        if tiempo_desde_inicio < 2.0:
            # Animación de conteo de puntos
            progreso = tiempo_desde_inicio / 2.0
            pts_mostrados = int(agente.pts * progreso)
            txt(f"PUNTOS: {pts_mostrados:06d}",
                F_GRANDE, AMBER, ANCHO // 2, py + 85, centro=True)
        else:
            txt(f"PUNTOS: {agente.pts:06d}",
                F_GRANDE, AMBER, ANCHO // 2, py + 85, centro=True)

        # Línea de separación
        pygame.draw.line(pantalla, FOSF_DIM,
                         (px + 30, py + 105), (px + pw - 30, py + 105), 1)

        # Estadísticas detalladas
        y = py + 120
        txt("ESTADÍSTICAS", F_SMALL, FOSF_VERDE, px + 30, y, centro=False)
        y += 20
        
        tot_pts = sum(r[1] for r in resultados_misiones)
        tot_tiempo = sum(r[2] for r in resultados_misiones)
        completadas = sum(1 for r in resultados_misiones if r[0])
        
        stats = [
            (f"Misiones completadas: {completadas}/4", FOSF_VERDE if completadas == 4 else AMBER),
            (f"Tiempo total: {tot_tiempo:.1f}s", FOSF_DIM),
            (f"Racha máxima: ×{agente.racha_max}", MORADO if agente.racha_max > 3 else FOSF_DIM),
            (f"Tiempo en sesión: {int(agente.tiempo())}s", FOSF_DIM),
        ]
        
        for stat_texto, stat_col in stats:
            txt(stat_texto, F_SMALL, stat_col, px + 50, y)
            y += 18

        # Detalle por misión (mejorado)
        y += 5
        txt("DETALLE POR MISIÓN", F_SMALL, FOSF_VERDE, px + 30, y, centro=False)
        y += 18
        
        nombres = ["█ M1: CÉSAR", "█ M2: BASE64", "█ M3: SHA-256", "█ M4: DIFFIE-H"]
        for i, (nom, (ok, pts, t_seg)) in enumerate(
                zip(nombres, resultados_misiones)):
            col = FOSF_VERDE if ok else ROJO_ALERTA
            icon = "✓" if ok else "✗"
            
            # Barra de misión
            panel(px + 40, y - 2, pw - 80, 28, borde=col, radio=3, alpha=200)
            txt(f"{icon} {nom}", F_SMALL, col, px + 50, y + 2)
            txt(f"+{pts:05d} pts | {t_seg:.1f}s", F_TINY, FOSF_DIM, px + pw - 100, y + 2)
            y += 32

        # Logros/Bonificaciones
        y += 5
        if agente.sin_errores or agente.sin_pistas:
            txt("★ BONIFICACIONES", F_SMALL, ORO, px + 30, y, centro=False)
            y += 16
            if agente.sin_errores:
                txt("  ✓ OPERACIÓN LIMPIA — Sin errores", F_TINY, ORO, px + 50, y)
                y += 14
            if agente.sin_pistas:
                txt("  ◈ PURA INTUICIÓN — Sin ayuda", F_TINY, AMBER, px + 50, y)
                y += 14

        # Botón
        btn_v = boton("VOLVER AL CUARTEL", 
                      ANCHO // 2 - 120, py + ph - 50, 240, 40,
                      (0, 60, 20), (0, 120, 40), mouse)

        pygame.display.flip()
        reloj.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and btn_v.collidepoint(ev.pos):
                mientras = False
            if ev.type == pygame.KEYDOWN:
                mientras = False