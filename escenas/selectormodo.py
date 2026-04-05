# -*- coding: utf-8 -*-
"""
Pantalla de selección de modo de juego.
"""

import pygame
import math
import time

from config import (
    ANCHO, ALTO, reloj, pantalla, MODO_PRACTICA,
    FOSF_VERDE, FOSF_DIM, AMBER, ROJO_ALERTA, MORADO,
    BLANCO, GRIS_PANEL, F_GIANT, F_BOLD, F_SMALL, F_TINY,
)
from ui import fondo_terminal, txt, txt_glow, panel, boton
from efectos import tick_particles, lluvia_data
from sonidos import play


def pantalla_seleccionar_modo():
    """
    Permite al jugador elegir entre:
    - MISIÓN CLASIFICADA: Con límite de tiempo
    - MODO ENTRENAMIENTO: Sin límite de tiempo
    
    Retorna el modo seleccionado.
    """
    t0 = time.time()
    
    while True:
        fondo_terminal()
        lluvia_data(1)
        tick_particles()
        mouse = pygame.mouse.get_pos()
        
        # Fondo
        pw, ph = 900, 500
        px = ANCHO // 2 - pw // 2
        py = ALTO // 2 - ph // 2
        panel(px, py, pw, ph, col=GRIS_PANEL, borde=FOSF_VERDE,
              radio=10, alpha=240)
        
        # Encabezado
        txt_glow("SELECCIONA TU MODO DE OPERACIÓN",
                F_GIANT, FOSF_VERDE, ANCHO // 2, py + 30, centro=True)
        pygame.draw.line(pantalla, FOSF_VERDE,
                        (px + 50, py + 65), (px + pw - 50, py + 65), 2)
        
        # Descripción
        txt("Elige cómo deseas enfrentarte a KRONOS",
            F_SMALL, FOSF_DIM, ANCHO // 2, py + 85, centro=True)
        
        # Panel Modo Clasificado
        px1 = px + 50
        py1 = py + 130
        pw1 = 350
        ph1 = 300
        
        hov1 = (px1 <= mouse[0] <= px1 + pw1 and py1 <= mouse[1] <= py1 + ph1)
        panel(px1, py1, pw1, ph1, 
              col=(20 if hov1 else 8, 30 if hov1 else 18, 8),
              borde=AMBER, radio=8, alpha=220)
        
        txt("⚔ MISIÓN CLASIFICADA", F_BOLD, AMBER, px1 + pw1 // 2, py1 + 20, centro=True)
        pygame.draw.line(pantalla, AMBER, (px1 + 20, py1 + 45), (px1 + pw1 - 20, py1 + 45), 1)
        
        info_mision = [
            "• 4 misiones encadenadas",
            "• Límite de tiempo por misión",
            "• Contador de vidas",
            "• Puntuación competitiva",
            "• Guarda récords",
            "",
            "⏱ Dificultad: MEDIA-ALTA",
        ]
        
        y_info = py1 + 60
        for linea in info_mision:
            col = AMBER if linea.startswith("•") else FOSF_DIM
            txt(linea, F_TINY, col, px1 + 20, y_info)
            y_info += 22
        
        # Botón Misión Clasificada
        btn_mision = boton("INICIAR MISIÓN",
                          px1 + 50, py1 + ph1 - 45, 250, 38,
                          (80, 50, 0) if hov1 else (40, 30, 0),
                          (150, 80, 0), mouse)
        
        # Panel Modo Entrenamiento
        px2 = px + 500
        py2 = py + 130
        pw2 = 350
        ph2 = 300
        
        hov2 = (px2 <= mouse[0] <= px2 + pw2 and py2 <= mouse[1] <= py2 + ph2)
        panel(px2, py2, pw2, ph2,
              col=(30 if hov2 else 8, 8, 30 if hov2 else 10),
              borde=MORADO, radio=8, alpha=220)
        
        txt("📚 MODO ENTRENAMIENTO", F_BOLD, MORADO, px2 + pw2 // 2, py2 + 20, centro=True)
        pygame.draw.line(pantalla, MORADO, (px2 + 20, py2 + 45), (px2 + pw2 - 20, py2 + 45), 1)
        
        info_entrenamiento = [
            "• Práctica sin presión",
            "• SIN límite de tiempo",
            "• Pistas ilimitadas",
            "• Modo educativo",
            "• Aprende a tu propio ritmo",
            "",
            "📖 Dificultad: PRINCIPIANTE",
        ]
        
        y_info = py2 + 60
        for linea in info_entrenamiento:
            col = MORADO if linea.startswith("•") else FOSF_DIM
            txt(linea, F_TINY, col, px2 + 20, y_info)
            y_info += 22
        
        # Botón Entrenamiento
        btn_entrenamiento = boton("INICIAR ENTRENAMIENTO",
                                 px2 + 30, py2 + ph2 - 45, 290, 38,
                                 (80, 0, 80) if hov2 else (40, 0, 40),
                                 (150, 0, 150), mouse)
        
        pygame.display.flip()
        reloj.tick(60)
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return None  # Volver al menú
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btn_mision.collidepoint(ev.pos):
                    play("mision")
                    return "normal"  # Modo clasificado
                if btn_entrenamiento.collidepoint(ev.pos):
                    play("beep")
                    return "practica"  # Modo entrenamiento
