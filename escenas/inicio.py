# -*- coding: utf-8 -*-
"""
Pantalla de menú principal.
"""

import random
import math
import pygame

from config import (
    ANCHO, ALTO, reloj, pantalla,
    FOSF_VERDE, FOSF_DIM, FOSF_DARK, AMBER, ROJO_ALERTA,
    CYAN_SCAN, BLANCO, MORADO, GRIS_PANEL,
    F_GIANT, F_TITULO, F_SMALL, F_TINY, F_BOLD,
)
from ui import fondo_terminal, txt, txt_glow, panel, boton
from efectos import tick_particles, lluvia_data
from sonidos import play
from escenas.expedientes import pantalla_expedientes
from escenas.cargapartida import pantalla_carga_partida


def pantalla_inicio(rec):
    """Menú principal. Retorna 'jugar' o None."""
    import time
    t0 = time.time()

    chars = list("ABCDEF0123456789@#$%^&*")
    matrix = [
        (random.randint(0, ANCHO), random.randint(0, ALTO),
         random.choice(chars), random.uniform(20, 80),
         random.uniform(0, math.tau))
        for _ in range(80)
    ]
    play("mision")

    while True:
        tt = time.time() - t0
        fondo_terminal()
        lluvia_data(2)
        tick_particles()
        mouse = pygame.mouse.get_pos()

        # Matrix rain de fondo
        for i, (fx, fy, ch, spd, fase) in enumerate(matrix):
            ny = (fy + spd * (tt % 100)) % ALTO
            a = abs(math.sin(tt * 0.3 + fase)) * 0.4
            col = tuple(int(c * a) for c in FOSF_VERDE)
            pantalla.blit(F_TINY.render(ch, True, col), (fx, int(ny)))
            if random.random() < 0.002:
                matrix[i] = (fx, fy, random.choice(chars), spd, fase)

        # ── Panel central ──
        pw, ph = 720, 510
        px = ANCHO // 2 - pw // 2
        py = ALTO // 2 - ph // 2
        panel(px, py, pw, ph, col=GRIS_PANEL, borde=FOSF_DIM,
              radio=8, alpha=230)

        # Esquinas decorativas
        for sx, sy, dx, dy in [
            (px, py, 1, 1), (px + pw, py, -1, 1),
            (px, py + ph, 1, -1), (px + pw, py + ph, -1, -1)
        ]:
            pygame.draw.line(pantalla, FOSF_VERDE,
                             (sx, sy), (sx + dx * 50, sy), 2)
            pygame.draw.line(pantalla, FOSF_VERDE,
                             (sx, sy), (sx, sy + dy * 50), 2)

        if int(tt * 3) % 2 == 0:
            pygame.draw.line(pantalla, ROJO_ALERTA,
                             (px + 5, py + 5), (px + pw - 5, py + 5), 1)

        txt("◉ AGENCIA DE INTELIGENCIA CIFRADA — ACCESO RESTRINGIDO ◉",
            F_TINY, FOSF_DIM, ANCHO // 2, py + 12, centro=True)
        pygame.draw.line(pantalla, FOSF_DIM,
                         (px + 20, py + 26), (px + pw - 20, py + 26), 1)

        # Logo pulsante
        pulse = 0.85 + 0.15 * math.sin(tt * 2.5)
        col_logo = tuple(int(c * pulse) for c in FOSF_VERDE)
        txt_glow("OPERACIÓN", F_TITULO, FOSF_DIM,
                 ANCHO // 2, py + 36, centro=True)
        txt_glow("SOMBRA", F_GIANT, col_logo,
                 ANCHO // 2, py + 66, centro=True)

        pygame.draw.line(pantalla, FOSF_DIM,
                         (px + 20, py + 128), (px + pw - 20, py + 128), 1)

        txt("KRONOS planea el mayor ataque criptográfico de la historia.",
            F_SMALL, BLANCO, ANCHO // 2, py + 138, centro=True)
        txt("Eres el Agente CIPHER. Descifra. Detén el caos.",
            F_SMALL, FOSF_DIM, ANCHO // 2, py + 158, centro=True)

        # ── Lista de misiones ──
        misiones = [
            ("01", "CIFRADO CÉSAR", "Rueda interactiva — descifra el desplazamiento",
             FOSF_VERDE, "★☆☆"),
            ("02", "BASE64", "Decodifica transmisión con analizador visual",
             CYAN_SCAN, "★★☆"),
            ("03", "HUELLA SHA-256", "Calculadora en tiempo real — identifica al infiltrado",
             AMBER, "★★★"),
            ("04", "DIFFIE-HELLMAN", "Visualiza el intercambio de claves y calcula",
             MORADO, "★★★"),
        ]
        y_m = py + 185
        for num, nom, desc, col, dif in misiones:
            hov = (px + 20 <= mouse[0] <= px + pw - 20
                   and y_m <= mouse[1] <= y_m + 42)
            bg = (0, 25, 10) if hov else GRIS_PANEL
            panel(px + 20, y_m, pw - 40, 42, col=bg, borde=col, radio=4)
            pygame.draw.rect(pantalla, col,
                             (px + 20, y_m, 4, 42), border_radius=2)
            txt(f"M{num}", F_TINY, col, px + 32, y_m + 6)
            txt(nom, F_BOLD, col, px + 65, y_m + 4)
            txt(desc, F_TINY, FOSF_DIM, px + 65, y_m + 22)
            txt(dif, F_TINY, AMBER, px + pw - 80, y_m + 16)
            y_m += 50

        # Récords
        pygame.draw.line(pantalla, FOSF_DIM,
                         (px + 20, y_m + 5), (px + pw - 20, y_m + 5), 1)
        if rec["mejor_pts"] > 0:
            txt(
                f"MEJOR: {rec['mejor_pts']:06d} pts | "
                f"RANGO: {rec['mejor_rango']} | ÉXITOS: {rec['exitos']}",
                F_TINY, AMBER, ANCHO // 2, y_m + 14, centro=True
            )

        # Botones
        by = py + ph - 58
        btn_op = boton("▶ NUEVA OPERACIÓN",
                       px + 40, by, 200, 42,
                       (0, 60, 20), (0, 120, 40), mouse)
        btn_carg = boton("⟲ CARGAR",
                        px + 255, by, 140, 42,
                        (20, 40, 20), (40, 80, 40), mouse)
        btn_rec = boton("◈ EXPEDIENTES",
                       px + 410, by, 160, 42,
                       (40, 40, 0), (80, 80, 0), mouse)
        btn_sal = boton("✖ ABORTAR",
                       px + 585, by, 120, 42,
                       (40, 0, 0), (100, 0, 0), mouse)

        txt("v3.0  //  INTERFAZ MEJORADA  //  MECÁNICAS INTERACTIVAS",
            F_TINY, FOSF_DARK, px + 20, py + ph - 14)

        pygame.display.flip()
        reloj.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btn_op.collidepoint(ev.pos):
                    play("mision")
                    return "jugar"
                if btn_carg.collidepoint(ev.pos):
                    play("beep")
                    partida_data, _ = pantalla_carga_partida()
                    if partida_data:
                        return ("cargar", partida_data)
                if btn_rec.collidepoint(ev.pos):
                    play("beep")
                    pantalla_expedientes(rec)
                if btn_sal.collidepoint(ev.pos):
                    pygame.quit(); import sys; sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    return "jugar"
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit(); import sys; sys.exit()