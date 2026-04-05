# -*- coding: utf-8 -*-
"""
Pantalla para cargar partidas guardadas.
"""

import pygame
import sys

from config import (
    ANCHO, ALTO, reloj, pantalla,
    FOSF_VERDE, FOSF_DIM, AMBER, BLANCO, GRIS_PANEL,
    F_BOLD, F_SMALL, F_TINY,
)
from ui import fondo_terminal, txt, txt_glow, panel, boton
from efectos import tick_particles, lluvia_data
from sonidos import play
from records import cargar_partidas_disponibles, cargar_partida


def pantalla_carga_partida():
    """
    Muestra las partidas guardadas disponibles para cargar.
    Retorna (partida_data, timestamp_key) o (None, None) si se cancela.
    """
    partidas_disponibles = cargar_partidas_disponibles()
    
    if not partidas_disponibles:
        # Sin partidas guardadas - mostrar mensaje
        while True:
            fondo_terminal()
            lluvia_data(1)
            tick_particles()
            
            pw, ph = 500, 250
            px = ANCHO // 2 - pw // 2
            py = ALTO // 2 - ph // 2
            panel(px, py, pw, ph, col=GRIS_PANEL, borde=AMBER, radio=8, alpha=240)
            
            txt("NO HAY PARTIDAS GUARDADAS", F_BOLD, AMBER,
                ANCHO // 2, py + 30, centro=True)
            pygame.draw.line(pantalla, AMBER, (px + 30, py + 55), (px + pw - 30, py + 55), 1)
            
            txt("Comienza una nueva operación para crear", F_SMALL, FOSF_DIM,
                ANCHO // 2, py + 80, centro=True)
            txt("tu primer guardado.", F_SMALL, FOSF_DIM,
                ANCHO // 2, py + 105, centro=True)
            
            mouse = pygame.mouse.get_pos()
            btn = boton("VOLVER AL MENÚ",
                       px + 150, py + ph - 55, 200, 40,
                       (40, 30, 0), (80, 60, 0), mouse)
            
            pygame.display.flip()
            reloj.tick(60)
            
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN and btn.collidepoint(ev.pos):
                    return None, None
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    return None, None
    
    # Con partidas disponibles
    scroll = 0
    max_mostrar = 5
    
    while True:
        fondo_terminal()
        lluvia_data(1)
        tick_particles()
        mouse = pygame.mouse.get_pos()
        
        pw, ph = 700, 500
        px = ANCHO // 2 - pw // 2
        py = ALTO // 2 - ph // 2
        panel(px, py, pw, ph, col=GRIS_PANEL, borde=FOSF_VERDE, radio=8, alpha=240)
        
        txt_glow("CARGAR PARTIDA GUARDADA", F_BOLD, FOSF_VERDE,
                ANCHO // 2, py + 20, centro=True)
        pygame.draw.line(pantalla, FOSF_VERDE, (px + 30, py + 48), (px + pw - 30, py + 48), 2)
        
        # Listar partidas
        y = py + 65
        for i in range(scroll, min(scroll + max_mostrar, len(partidas_disponibles))):
            key, datos = partidas_disponibles[i]
            
            # Panel de partida
            hov = (px + 20 <= mouse[0] <= px + pw - 20 and
                   y <= mouse[1] <= y + 50)
            
            panel(px + 20, y, pw - 40, 50,
                  col=(0, 30, 15) if hov else (0, 15, 8),
                  borde=AMBER if hov else FOSF_DIM,
                  radio=4, alpha=200)
            
            misiones_hechas = datos.get("misiones_completadas", 0)
            pts = datos.get("puntos_acumulados", 0)
            fecha = datos.get("fecha", "?")
            
            txt(f"Misión {misiones_hechas + 1} — {pts:06d} pts",
                F_BOLD, AMBER if hov else FOSF_VERDE,
                px + 35, y + 8)
            txt(f"Guardado: {fecha}", F_TINY, FOSF_DIM,
                px + 35, y + 28)
            
            if hov and pygame.mouse.get_pressed()[0]:
                play("ok")
                return datos, key
            
            y += 60
        
        # Botones de navegación
        if len(partidas_disponibles) > max_mostrar:
            if scroll > 0:
                btn_arriba = boton("↑", px + pw - 45, py + 60, 30, 30,
                                   (40, 40, 0), (80, 80, 0), mouse)
                if pygame.mouse.get_pressed()[0] and btn_arriba.collidepoint(mouse):
                    scroll -= 1
            
            if scroll + max_mostrar < len(partidas_disponibles):
                btn_abajo = boton("↓", px + pw - 45, py + ph - 90, 30, 30,
                                  (40, 40, 0), (80, 80, 0), mouse)
                if pygame.mouse.get_pressed()[0] and btn_abajo.collidepoint(mouse):
                    scroll += 1
        
        btn_salir = boton("CANCELAR", px + 250, py + ph - 50, 200, 40,
                         (40, 0, 0), (100, 0, 0), mouse)
        
        pygame.display.flip()
        reloj.tick(60)
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return None, None
                if ev.key == pygame.K_UP and scroll > 0:
                    scroll -= 1
                if ev.key == pygame.K_DOWN and scroll + max_mostrar < len(partidas_disponibles):
                    scroll += 1
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btn_salir.collidepoint(ev.pos):
                    return None, None
