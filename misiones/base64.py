# -*- coding: utf-8 -*-
"""
Misión 02 — BASE64: "Transmisión Encubierta"
Con analizador visual de decodificación.
"""

import random
import math
import time
import pygame

from config import (
    ANCHO, ALTO, reloj, pantalla,
    FOSF_VERDE, FOSF_DIM, FOSF_DARK, AMBER, ROJO_ALERTA,
    BLANCO, CYAN_SCAN, GRIS_PANEL,
    F_GRANDE, F_SMALL, F_MICRO, F_BOLD, F_TINY,
)
from criptografia import b64enc
from ui import (
    fondo_terminal, txt, panel, boton, input_box, barra_tiempo,
    hud_superior, indicador_progreso,
)
from estado import agente
from aria import aria
from efectos import (
    sfx, tick_particles, lluvia_data, boom, add_float, tick_floats,
)
from sonidos import play
from logros import logros
from escenas.teletipo import teletipo, briefing_mision


def mision_base64():
    """
    Ejecuta la misión Base64.
    Retorna (exitosa, tiempo_empleado, puntos_mision).
    """
    teletipo([
        ("NUEVA TRANSMISIÓN — CLASIFICACIÓN: URGENTE", ROJO_ALERTA),
        ("", FOSF_DIM),
        ("KRONOS usa codificación Base64 para ocultar nombres.", BLANCO),
        ("El ANALIZADOR VISUAL te muestra el proceso de decodificación.", FOSF_VERDE),
        ("Observa cómo los caracteres se transforman bit a bit.", CYAN_SCAN),
    ])
    briefing_mision(2, "TRANSMISIÓN ENCUBIERTA", [
        "Señal capturada en 14.287 MHz.",
        "El nombre está en Base64. Usa el analizador visual.",
        "Cada grupo de 4 chars → 3 bytes originales.",
    ], CYAN_SCAN, 40)

    # ── Datos ──
    ops = ["NOCTUA", "VORTEX", "SPECTRE", "KRONOS", "ECLIPSE",
           "PHANTOM", "CIPHER", "NEXUS", "VECTOR", "UMBRA"]
    op = random.choice(ops)
    encoded = b64enc(op)

    # ── Estado ──
    texto_inp = ""
    vidas = 3
    msg_ret = ""
    col_msg = BLANCO
    resuelto = False
    TMAX = 40.0
    t_ini = time.time()
    mostrar_proceso = False
    decode_progress = 0.0
    t_mision = 0.0

    aria.decir("Base64: 4 chars codificados → 3 bytes originales.",
               CYAN_SCAN, 0.3)
    aria.decir(f"Cadena: {encoded}. Longitud original: {len(op)} letras.",
               FOSF_VERDE, 4)

    while True:
        dt = reloj.tick(60) / 1000.0
        tt = time.time()
        t_rest = max(0, TMAX - (tt - t_ini)) if not resuelto else TMAX
        mouse = pygame.mouse.get_pos()
        sfx.update(dt)

        if mostrar_proceso and not resuelto:
            decode_progress = min(1.0, decode_progress + 0.005)

        fondo_terminal()
        tick_particles()
        lluvia_data(1)
        hud_superior(2, "TRANSMISIÓN ENCUBIERTA", CYAN_SCAN, vidas)

        # ── Señal capturada ──
        panel(20, 68, ANCHO - 40, 100,
              col=(0, 12, 22), borde=CYAN_SCAN, radio=6)
        txt("◉ SEÑAL CAPTURADA — 14.287 MHz:",
            F_SMALL, CYAN_SCAN, 35, 73)
        pygame.draw.line(pantalla, CYAN_SCAN, (35, 90), (ANCHO - 50, 90), 1)

        # Waveform
        for wx in range(0, ANCHO - 80, 3):
            wy = 110 + int(8 * math.sin(wx * 0.08 + tt * 4))
            c = CYAN_SCAN if int(wx / 3) % 2 == 0 else FOSF_DIM
            pygame.draw.circle(pantalla, c, (wx + 35, wy), 1)

        # Caracteres con colores
        char_cols = [FOSF_VERDE, CYAN_SCAN, AMBER, ROJO_ALERTA, BLANCO]
        cx0 = ANCHO // 2 - len(encoded) * 12
        for i, ch in enumerate(encoded):
            pc = 0.7 + 0.3 * math.sin(tt * 3 + i * 0.7)
            if mostrar_proceso and i / len(encoded) < decode_progress:
                cc = tuple(int(c * pc) for c in FOSF_VERDE)
            else:
                cc = tuple(int(c * pc) for c in char_cols[i % len(char_cols)])
            txt(ch, F_GRANDE, cc, cx0 + i * 24, 125)
        txt(f"({len(encoded)} chars B64 → {len(op)} letras)",
            F_TINY, FOSF_DIM, ANCHO // 2, 157, centro=True)

        # ── Tiempo ──
        panel(20, 176, ANCHO - 40, 42, borde=FOSF_DIM, radio=4)
        txt("CAMBIO DE FRECUENCIA EN:", F_MICRO, CYAN_SCAN, 35, 180)
        barra_tiempo(220, 184, ANCHO - 280, 14, t_rest, TMAX,
                     CYAN_SCAN, AMBER, ROJO_ALERTA)

        if t_rest <= 0 and not resuelto:
            vidas = 0
            resuelto = True
            t_mision = TMAX
            msg_ret = f"FRECUENCIA PERDIDA. Era: {op}"
            col_msg = ROJO_ALERTA
            agente.fallo()
            sfx.shake(12, 0.5)
            sfx.flash(ROJO_ALERTA, 0.3)
            boom(ANCHO // 2, ALTO // 2, ROJO_ALERTA, 40)
            play("error")

        # ── Analizador visual ──
        panel(20, 226, ANCHO - 40, 130,
              col=(5, 10, 20), borde=CYAN_SCAN, radio=6)
        txt("◈ ANALIZADOR BASE64 — PROCESO DE DECODIFICACIÓN:",
            F_TINY, CYAN_SCAN, 35, 230)

        if mostrar_proceso:
            chars_mostrados = int(decode_progress * len(encoded))
            groups = [encoded[i:i + 4] for i in range(0, len(encoded), 4)]
            gy = 248
            for gi, grp in enumerate(groups):
                gx = 35 + gi * 180
                if gx > ANCHO - 180:
                    break
                for ci, ch in enumerate(grp):
                    idx_global = gi * 4 + ci
                    if idx_global < chars_mostrados:
                        cc = FOSF_VERDE
                        if idx_global == chars_mostrados - 1:
                            s = pygame.Surface((16, 18), pygame.SRCALPHA)
                            s.fill((*CYAN_SCAN, 60))
                            pantalla.blit(s, (gx + ci * 22 - 2, gy - 2))
                    else:
                        cc = FOSF_DARK
                    txt(ch, F_BOLD, cc, gx + ci * 22, gy)

                if gi * 4 + 4 <= chars_mostrados:
                    start = gi * 3
                    decoded_chars = op[start:start + 3]
                    for di, dch in enumerate(decoded_chars):
                        txt(dch, F_SMALL, FOSF_VERDE, gx + di * 16, gy + 24)
                    txt("→", F_TINY, FOSF_DIM, gx + 88, gy + 10)
                else:
                    txt("→ ???", F_TINY, FOSF_DARK, gx + 88, gy + 10)

            decoded_so_far = op[:chars_mostrados * 3 // 4]
            if decoded_so_far:
                txt(f"Decodificado hasta ahora: {decoded_so_far}",
                    F_SMALL, FOSF_VERDE, 35, gy + 50)
            # Barra de progreso
            pygame.draw.rect(pantalla, FOSF_DIM,
                             (35, gy + 70, ANCHO - 90, 8), border_radius=3)
            pw = int((ANCHO - 90) * decode_progress)
            if pw > 0:
                pygame.draw.rect(pantalla, CYAN_SCAN,
                                 (35, gy + 70, pw, 8), border_radius=3)
            txt(f"{int(decode_progress * 100)}%", F_TINY, CYAN_SCAN,
                ANCHO - 50, gy + 68)
        else:
            txt("Pulsa '◈ ANALIZAR' para ver la decodificación paso a paso.",
                F_SMALL, FOSF_DIM, 35, 250)
            txt("A-Z→0-25 | a-z→26-51 | 0-9→52-61 | +→62 | /→63 | ==padding",
                F_TINY, FOSF_DIM, 35, 275)
            txt("Cada grupo de 4 caracteres Base64 = 3 bytes originales",
                F_TINY, AMBER, 35, 292)

        # ── Input ──
        panel(20, 366, ANCHO - 40, 100, borde=FOSF_DIM, radio=4)
        txt("◉ NOMBRE DE LA OPERACIÓN:", F_SMALL, FOSF_VERDE, 35, 372)
        input_box(texto_inp, 35, 394, ANCHO - 340,
                  activo=not resuelto, placeholder="Nombre decodificado...")
        btn_env = boton("▶ VERIFICAR", 35, 436, 160, 30,
                        (0, 40, 25), (0, 90, 50), mouse, F_SMALL,
                        enabled=not resuelto)
        btn_ana = boton("◈ ANALIZAR", 210, 436, 150, 30,
                        (20, 25, 40), (40, 60, 90), mouse, F_SMALL,
                        enabled=not resuelto and not mostrar_proceso)
        btn_pst = boton("◈ PISTA (−1 vida)", 375, 436, 190, 30,
                        (50, 40, 0), (100, 80, 0), mouse, F_SMALL,
                        enabled=not resuelto and vidas > 1)

        if msg_ret:
            bg = (0, 35, 15) if col_msg == FOSF_VERDE else (40, 0, 0)
            panel(20, 475, ANCHO - 40, 35, col=bg, borde=col_msg, radio=4)
            txt(msg_ret, F_BOLD, col_msg, ANCHO // 2, 483, centro=True)

        if resuelto and col_msg == FOSF_VERDE:
            panel(20, 518, ANCHO - 40, 32,
                  col=(0, 25, 35), borde=CYAN_SCAN, radio=4)
            txt(f"OPERACIÓN: {op} — Intel actualizada",
                F_SMALL, CYAN_SCAN, 35, 525)

        if resuelto:
            btn_sig = boton("SIGUIENTE MISIÓN ▶▶",
                            ANCHO // 2 - 110, ALTO - 55, 220, 38,
                            (0, 60, 20), (0, 120, 40), mouse)

        aria.actualizar()
        aria.dibujar()
        indicador_progreso(1)
        logros.draw()
        sfx.draw()
        tick_floats()
        pygame.display.flip()

        # ── Verificar ──
        def verificar():
            nonlocal vidas, msg_ret, col_msg, resuelto, texto_inp, t_mision
            t_mision = tt - t_ini
            if texto_inp.upper().strip() == op:
                agente.acierto()
                tb = max(0, (t_rest / TMAX) * 0.5)
                pts = agente.sumar(350, vidas, tb)
                msg_ret = f"✓ OPERACIÓN {op} | +{pts} pts"
                col_msg = FOSF_VERDE
                resuelto = True
                logros.intentar("DECODIFICADOR")
                if t_mision < 10:
                    logros.intentar("VELOCISTA")
                sfx.flash(CYAN_SCAN, 0.2)
                sfx.shake(4, 0.2)
                boom(ANCHO // 2, 400, CYAN_SCAN, 50)
                play("ok")
                add_float(f"+{pts}", ANCHO // 2, 400, CYAN_SCAN, 30)
            else:
                vidas -= 1
                agente.fallo()
                sfx.shake(8, 0.3)
                sfx.flash(ROJO_ALERTA, 0.15)
                boom(ANCHO // 2, 400, ROJO_ALERTA, 20)
                play("error")
                if vidas == 0:
                    t_mision = TMAX
                    msg_ret = f"✗ SIN ACCESOS. Era: {op}"
                    col_msg = ROJO_ALERTA
                    resuelto = True
                else:
                    msg_ret = f"✗ DENEGADO. Vidas: {vidas}"
                    col_msg = ROJO_ALERTA
                    texto_inp = ""

        # ── Eventos ──
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return False, t_mision, False
                if not resuelto and vidas > 0:
                    if ev.key == pygame.K_RETURN:
                        verificar()
                    elif ev.key == pygame.K_BACKSPACE:
                        texto_inp = texto_inp[:-1]
                    elif ev.unicode.isalpha() and len(texto_inp) < 12:
                        texto_inp += ev.unicode.upper()
                        play("tecla")
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if not resuelto and vidas > 0:
                    if btn_env.collidepoint(ev.pos):
                        verificar()
                    if btn_ana.collidepoint(ev.pos):
                        mostrar_proceso = True
                        decode_progress = 0
                        play("nivel")
                    if btn_pst.collidepoint(ev.pos):
                        vidas -= 1
                        agente.usar_pista()
                        msg_ret = (f"◈ PISTA: {len(op)} letras, "
                                   f"empieza '{op[0]}', termina '{op[-1]}'")
                        col_msg = AMBER
                        play("beep")
                if resuelto:
                    try:
                        if btn_sig.collidepoint(ev.pos):
                            play("mision")
                            return vidas > 0, t_mision, True
                    except NameError:
                        pass