import math
import random
import time
import pygame
import sys

from config import (
    ANCHO, ALTO, reloj, pantalla,
    FOSF_VERDE, FOSF_DIM, AMBER, ROJO_ALERTA, MORADO,
    ORO, BLANCO, F_GIANT, F_BOLD, F_SMALL, F_MICRO, F_GRANDE, F_MEDIA,
    GRIS_PANEL,
)
from ui import fondo_terminal, txt, txt_glow, panel
from efectos import tick_particles, lluvia_data, boom as boom_effect


def pantalla_victoria(mision_num, pts_ganados, tiempo_usado):
    """Pantalla de victoria. Mejoras: panel de fondo, texto más grande."""
    t0 = time.time()
    dur = 4.0

    boom_effect(ANCHO // 2, ALTO // 2, ORO, n=50)

    while time.time() - t0 < dur:
        fondo_terminal()
        lluvia_data(3)
        tick_particles()

        tt = (time.time() - t0) / dur
        pulse = math.sin(tt * 12 * math.pi) * 0.5 + 0.5

        # Panel de fondo para los textos
        panel(ANCHO // 2 - 320, ALTO // 2 - 110,
              640, 220,
              col=(8, 22, 8), borde=ORO, radio=10, alpha=230)

        border_width = int(3 + pulse * 3)
        pygame.draw.rect(pantalla,
                        tuple(int(c * (0.5 + pulse * 0.5)) for c in FOSF_VERDE),
                        (40, 80, ANCHO - 80, ALTO - 160),
                        border_width)

        alpha_main = min(1.0, (time.time() - t0) * 2)
        txt_color = tuple(int(c * alpha_main) for c in ORO)
        txt_glow("✓ MISIÓN COMPLETADA", F_GIANT, txt_color,
                ANCHO // 2, ALTO // 2 - 85, centro=True)

        if time.time() - t0 > 0.5:
            alpha_det = min(1.0, (time.time() - t0 - 0.5) * 2)
            det_color = tuple(int(c * alpha_det) for c in FOSF_VERDE)

            txt(f"Puntos adquiridos:  +{pts_ganados:05d}",
                F_GRANDE, det_color, ANCHO // 2, ALTO // 2 + 5, centro=True)
            txt(f"Tiempo utilizado:  {tiempo_usado:.1f}s",
                F_MEDIA, det_color, ANCHO // 2, ALTO // 2 + 45, centro=True)

        # Mensaje de siguiente misión
        col_sig = FOSF_DIM if tt < 0.8 else AMBER
        txt(f"Misión 0{mision_num} completada — Siguiente encargo cargando...",
            F_SMALL, col_sig, ANCHO // 2, ALTO - 60, centro=True)

        pygame.display.flip()
        reloj.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def pantalla_acceso_negado(mision_num):
    """Pantalla de Acceso Negado. Mejoras: texto más claro."""
    t0 = time.time()
    dur = 3.0

    while time.time() - t0 < dur:
        fondo_terminal()
        lluvia_data(5)
        tick_particles()

        if random.random() < 0.3:
            glitch_y = random.randint(0, ALTO)
            glitch_h = random.randint(5, 50)
            glitch_x = random.randint(0, ANCHO)
            glitch_w = random.randint(50, 300)
            s = pygame.Surface((glitch_w, glitch_h), pygame.SRCALPHA)
            s.fill((*ROJO_ALERTA, random.randint(30, 100)))
            pantalla.blit(s, (glitch_x, glitch_y))

        for _ in range(3):
            y = random.randint(0, ALTO)
            pygame.draw.line(pantalla,
                           (255, random.randint(0, 50), random.randint(0, 50)),
                           (0, y), (ANCHO, y), random.randint(1, 3))

        tt = (time.time() - t0) / dur

        # Panel de fondo
        panel(ANCHO // 2 - 300, ALTO // 2 - 100,
              600, 200,
              col=(20, 5, 5), borde=ROJO_ALERTA, radio=8, alpha=220)

        if tt < 0.5:
            alpha = int(200 * (tt * 2))
            txt_col = tuple(int(c * alpha / 200) for c in ROJO_ALERTA)
        else:
            txt_col = ROJO_ALERTA

        txt_glow("⚠ ACCESO DENEGADO ⚠", F_GIANT, txt_col,
                ANCHO // 2, ALTO // 2 - 65, centro=True)

        txt("IDENTIDAD COMPROMETIDA", F_BOLD,
            (220, random.randint(30, 120), 0),
            ANCHO // 2, ALTO // 2 + 15, centro=True)

        txt(f"Misión 0{mision_num} — FALLIDA", F_MEDIA, ROJO_ALERTA,
            ANCHO // 2, ALTO // 2 + 60, centro=True)

        if int(time.time() * 5) % 2:
            pygame.draw.line(pantalla, ROJO_ALERTA,
                           (ANCHO // 2 - 180, ALTO // 2 + 105),
                           (ANCHO // 2 + 180, ALTO // 2 + 105), 3)

        pygame.display.flip()
        reloj.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def pantalla_carga_mision(num_siguiente):
    """Transición visual — v3.1."""
    t0 = time.time()
    dur = 2.0

    while time.time() - t0 < dur:
        fondo_terminal()
        lluvia_data(1)
        tick_particles()

        tt = (time.time() - t0) / dur

        # Panel de carga
        panel(ANCHO // 2 - 250, ALTO // 2 - 80,
              500, 160,
              col=(8, 14, 8), borde=FOSF_DIM, radio=8, alpha=220)

        txt("Cargando siguiente operativo...", F_MEDIA, FOSF_DIM,
            ANCHO // 2, ALTO // 2 - 50, centro=True)

        # Barra de carga más grande
        barra_w = 380
        barra_h = 22
        barra_x = ANCHO // 2 - barra_w // 2
        barra_y = ALTO // 2 - 5

        pygame.draw.rect(pantalla, (0, 40, 15),
                        (barra_x, barra_y, barra_w, barra_h), border_radius=4)
        relleno = int(barra_w * tt)
        if relleno > 4:
            pygame.draw.rect(pantalla, FOSF_VERDE,
                            (barra_x + 2, barra_y + 2, relleno - 4, barra_h - 4),
                            border_radius=3)
        pygame.draw.rect(pantalla, FOSF_DIM,
                        (barra_x, barra_y, barra_w, barra_h), 2, border_radius=4)

        txt(f"MISIÓN  0{num_siguiente}", F_BOLD, AMBER,
            ANCHO // 2, ALTO // 2 + 35, centro=True)

        dots = "." * ((int(time.time() * 3) % 3) + 1)
        txt(f"Sincronizando{dots}", F_SMALL, FOSF_DIM,
            ANCHO // 2, ALTO // 2 + 65, centro=True)

        pygame.display.flip()
        reloj.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()