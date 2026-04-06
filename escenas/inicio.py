import random
import math
import pygame

from config import (
    ANCHO, ALTO, reloj, pantalla,
    FOSF_VERDE, FOSF_DIM, FOSF_DARK, AMBER, ROJO_ALERTA,
    CYAN_SCAN, BLANCO, MORADO, GRIS_PANEL,
    F_GIANT, F_TITULO, F_SMALL, F_TINY, F_BOLD, F_MEDIA, F_MICRO,
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

        # Matrix rain de fondo (más tenue)
        for i, (fx, fy, ch, spd, fase) in enumerate(matrix):
            ny = (fy + spd * (tt % 100)) % ALTO
            a = abs(math.sin(tt * 0.3 + fase)) * 0.3  # más sutil
            col = tuple(int(c * a) for c in FOSF_VERDE)
            pantalla.blit(F_TINY.render(ch, True, col), (fx, int(ny)))
            if random.random() < 0.002:
                matrix[i] = (fx, fy, random.choice(chars), spd, fase)

        # ── Panel central — ligeramente más ancho ──
        pw, ph = 760, 540
        px = ANCHO // 2 - pw // 2
        py = ALTO // 2 - ph // 2 - 10
        panel(px, py, pw, ph, col=GRIS_PANEL, borde=FOSF_DIM,
              radio=10, alpha=238)

        # Esquinas decorativas
        for sx, sy, dx, dy in [
            (px, py, 1, 1), (px + pw, py, -1, 1),
            (px, py + ph, 1, -1), (px + pw, py + ph, -1, -1)
        ]:
            pygame.draw.line(pantalla, FOSF_VERDE,
                             (sx, sy), (sx + dx * 55, sy), 2)
            pygame.draw.line(pantalla, FOSF_VERDE,
                             (sx, sy), (sx, sy + dy * 55), 2)

        if int(tt * 3) % 2 == 0:
            pygame.draw.line(pantalla, ROJO_ALERTA,
                             (px + 5, py + 5), (px + pw - 5, py + 5), 1)

        txt("◉ AGENCIA DE INTELIGENCIA CIFRADA — ACCESO RESTRINGIDO ◉",
            F_MICRO, FOSF_DIM, ANCHO // 2, py + 14, centro=True)
        pygame.draw.line(pantalla, FOSF_DIM,
                         (px + 20, py + 30), (px + pw - 20, py + 30), 1)

        # Logo pulsante
        pulse = 0.85 + 0.15 * math.sin(tt * 2.5)
        col_logo = tuple(int(c * pulse) for c in FOSF_VERDE)
        txt_glow("OPERACIÓN", F_TITULO, FOSF_DIM,
                 ANCHO // 2, py + 40, centro=True)
        txt_glow("SOMBRA", F_GIANT, col_logo,
                 ANCHO // 2, py + 72, centro=True)

        pygame.draw.line(pantalla, FOSF_DIM,
                         (px + 20, py + 138), (px + pw - 20, py + 138), 1)

        # Subtítulo más visible
        txt("KRONOS planea el mayor ataque criptográfico de la historia.",
            F_SMALL, BLANCO, ANCHO // 2, py + 148, centro=True)
        txt("Eres el Agente CIPHER. Descifra. Detén el caos.",
            F_SMALL, FOSF_DIM, ANCHO // 2, py + 170, centro=True)

        # ── Lista de misiones — filas más altas ──
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
        y_m = py + 198
        FILA_H = 54  # era 50 — más espacio
        for num, nom, desc, col, dif in misiones:
            hov = (px + 20 <= mouse[0] <= px + pw - 20
                   and y_m <= mouse[1] <= y_m + FILA_H - 4)
            bg = (0, 28, 12) if hov else GRIS_PANEL
            panel(px + 20, y_m, pw - 40, FILA_H - 4,
                  col=bg, borde=col, radio=5)
            pygame.draw.rect(pantalla, col,
                             (px + 20, y_m, 5, FILA_H - 4), border_radius=3)
            txt(f"M{num}", F_MICRO, col, px + 34, y_m + 8)
            txt(nom, F_BOLD, col, px + 70, y_m + 6)            # era F_BOLD de 18
            txt(desc, F_MICRO, FOSF_DIM, px + 70, y_m + 28)    # era F_TINY de 11
            txt(dif, F_MICRO, AMBER, px + pw - 75, y_m + 18)
            y_m += FILA_H

        # Récords
        pygame.draw.line(pantalla, FOSF_DIM,
                         (px + 20, y_m + 6), (px + pw - 20, y_m + 6), 1)
        if rec["mejor_pts"] > 0:
            txt(
                f"MEJOR: {rec['mejor_pts']:06d} pts | "
                f"RANGO: {rec['mejor_rango']} | ÉXITOS: {rec['exitos']}",
                F_MICRO, AMBER, ANCHO // 2, y_m + 15, centro=True
            )

        # Botones — más altos (48px) y mejor distribuidos
        by = py + ph - 62
        BH = 46  # altura botón era 42
        btn_op = boton("▶ NUEVA OPERACIÓN",
                       px + 30, by, 210, BH,
                       (0, 65, 22), (0, 130, 45), mouse)
        btn_carg = boton("⟲ CARGAR",
                        px + 255, by, 150, BH,
                        (20, 45, 20), (45, 90, 45), mouse)
        btn_rec = boton("◈ EXPEDIENTES",
                       px + 420, by, 175, BH,
                       (45, 45, 0), (90, 90, 0), mouse)
        btn_sal = boton("✖ ABORTAR",
                       px + 610, by, 130, BH,
                       (45, 0, 0), (110, 0, 0), mouse)

        txt("v3.1  //  INTERFAZ MEJORADA  //  MECÁNICAS INTERACTIVAS",
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