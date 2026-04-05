# -*- coding: utf-8 -*-
"""
Pantalla de victoria y acceso negado para transiciones entre misiones.
"""

import math
import random
import time
import pygame
import sys

from config import (
    ANCHO, ALTO, reloj, pantalla, 
    FOSF_VERDE, FOSF_DIM, AMBER, ROJO_ALERTA, MORADO,
    ORO, BLANCO, F_GIANT, F_BOLD, F_SMALL, F_MICRO,
)
from ui import fondo_terminal, txt, txt_glow, panel
from efectos import tick_particles, lluvia_data, boom as boom_effect


def pantalla_victoria(mision_num, pts_ganados, tiempo_usado):
    """
    Pantalla de victoria cuando completas una misión.
    Efectos visuales: partículas, animaciones, brillo.
    """
    t0 = time.time()
    dur = 4.0
    
    # Generar explosión de efectos
    boom_effect(ANCHO // 2, ALTO // 2, ORO, n=50)
    
    while time.time() - t0 < dur:
        fondo_terminal()
        lluvia_data(3)
        tick_particles()
        
        # Borde pulsante
        tt = (time.time() - t0) / dur
        pulse = math.sin(tt * 12 * math.pi) * 0.5 + 0.5
        border_width = int(3 + pulse * 3)
        
        pygame.draw.rect(pantalla, 
                        tuple(int(c * (0.5 + pulse * 0.5)) for c in FOSF_VERDE),
                        (40, 80, ANCHO - 80, ALTO - 160),
                        border_width)
        
        # Texto principal
        alpha_main = min(1.0, (time.time() - t0) * 2)
        txt_color = tuple(int(c * alpha_main) for c in ORO)
        txt_glow("✓ MISIÓN COMPLETADA", F_GIANT, txt_color,
                ANCHO // 2, ALTO // 2 - 80, centro=True)
        
        # Detalles
        if time.time() - t0 > 0.5:
            alpha_det = min(1.0, (time.time() - t0 - 0.5) * 2)
            det_color = tuple(int(c * alpha_det) for c in FOSF_VERDE)
            
            txt(f"Puntos adquiridos: +{pts_ganados:05d}",
                F_BOLD, det_color, ANCHO // 2, ALTO // 2 + 10, centro=True)
            txt(f"Tiempo utilizado: {tiempo_usado:.1f}s",
                F_SMALL, det_color, ANCHO // 2, ALTO // 2 + 45, centro=True)
            txt(f"Misión 0{mision_num} → Siguiente encargo cargando...",
                F_MICRO, (FOSF_DIM if tt < 0.8 else AMBER),
                ANCHO // 2, ALTO - 50, centro=True)
        
        pygame.display.flip()
        reloj.tick(60)
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def pantalla_acceso_negado(mision_num):
    """
    Pantalla de 'Acceso Negado' cuando fallas una misión.
    Efecto de glitch y interferencia.
    """
    t0 = time.time()
    dur = 3.0
    
    while time.time() - t0 < dur:
        fondo_terminal()
        lluvia_data(5)  # lluvia intensa
        tick_particles()
        
        # Efecto glitch aleatorio
        if random.random() < 0.3:
            glitch_y = random.randint(0, ALTO)
            glitch_h = random.randint(5, 50)
            glitch_x = random.randint(0, ANCHO)
            glitch_w = random.randint(50, 300)
            
            s = pygame.Surface((glitch_w, glitch_h), pygame.SRCALPHA)
            s.fill((*ROJO_ALERTA, random.randint(30, 100)))
            pantalla.blit(s, (glitch_x, glitch_y))
        
        # Líneas de interferencia
        for _ in range(3):
            y = random.randint(0, ALTO)
            pygame.draw.line(pantalla, 
                           (255, random.randint(0, 50), random.randint(0, 50)),
                           (0, y), (ANCHO, y), random.randint(1, 3))
        
        # Texto central
        tt = (time.time() - t0) / dur
        
        if tt < 0.5:
            alpha = int(200 * (tt * 2))
            txt_col = tuple(int(c * alpha / 200) for c in ROJO_ALERTA)
        else:
            alpha = 200
            txt_col = ROJO_ALERTA
        
        txt_glow("⚠ ACCESO DENEGADO ⚠", F_GIANT, txt_col,
                ANCHO // 2, ALTO // 2 - 60, centro=True)
        
        txt("IDENTIDAD COMPROMISED", F_BOLD, 
            (200, random.randint(0, 100), 0),
            ANCHO // 2, ALTO // 2 + 20, centro=True)
        
        txt(f"Misión 0{mision_num} — FALLIDA", F_SMALL, ROJO_ALERTA,
            ANCHO // 2, ALTO // 2 + 70, centro=True)
        
        # Línea de error parpadeante
        if int(time.time() * 5) % 2:
            pygame.draw.line(pantalla, ROJO_ALERTA,
                           (ANCHO // 2 - 150, ALTO // 2 + 120),
                           (ANCHO // 2 + 150, ALTO // 2 + 120), 3)
        
        pygame.display.flip()
        reloj.tick(60)
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def pantalla_carga_mision(num_siguiente):
    """Transición visual cuando cargas la siguiente misión."""
    t0 = time.time()
    dur = 2.0
    
    while time.time() - t0 < dur:
        fondo_terminal()
        lluvia_data(1)
        tick_particles()
        
        tt = (time.time() - t0) / dur
        
        # Barra de carga
        barra_w = 300
        barra_x = ANCHO // 2 - barra_w // 2
        barra_y = ALTO // 2 + 40
        
        pygame.draw.rect(pantalla, FOSF_VERDE, 
                        (barra_x, barra_y, barra_w, 20), 2)
        
        relleno = int(barra_w * tt)
        pygame.draw.rect(pantalla, FOSF_VERDE,
                        (barra_x + 2, barra_y + 2, relleno - 4, 16))
        
        txt("Cargando siguiente operativo...", F_SMALL, FOSF_DIM,
            ANCHO // 2, ALTO // 2 - 40, centro=True)
        
        txt(f"Misión 0{num_siguiente}", F_BOLD, AMBER,
            ANCHO // 2, ALTO // 2 + 80, centro=True)
        
        # Puntos de espera animados
        dots = "." * ((int(time.time() * 3) % 3) + 1)
        txt(f"Sincronizando{dots}", F_MICRO, FOSF_DIM,
            ANCHO // 2, ALTO // 2 + 120, centro=True)
        
        pygame.display.flip()
        reloj.tick(60)
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
