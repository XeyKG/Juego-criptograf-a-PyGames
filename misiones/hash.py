# -*- coding: utf-8 -*-
"""
Misión 03 — SHA-256: "Identidad Fantasma"
Con calculadora de hash interactiva en tiempo real.
"""

import random
import time
import pygame

from config import (
    ANCHO, ALTO, reloj, pantalla,
    FOSF_VERDE, FOSF_DIM, AMBER, ROJO_ALERTA,
    ROJO_DIM, BLANCO, GRIS_PANEL, ORO,
    F_BOLD, F_SMALL, F_TINY, F_MICRO,
)
from criptografia import sha256
from ui import (
    fondo_terminal, txt, panel, boton, barra_tiempo,
    hud_superior, indicador_progreso,
)
from estado import agente
from aria import aria
from efectos import (
    sfx, tick_particles, lluvia_data, boom, add_float, tick_floats,
)
from sonidos import play
from logros import logros
from componentes.hash_calc import HashCalc
from escenas.teletipo import teletipo, briefing_mision


def mision_hash():
    """
    Ejecuta la misión SHA-256.
    Retorna (exitosa, tiempo_empleado, puntos_mision).
    """
    teletipo([
        ("ALERTA MÁXIMA — INFILTRADO EN LA AGENCIA", ROJO_ALERTA),
        ("", FOSF_DIM),
        ("KRONOS tiene un espía. Tenemos su firma SHA-256.", BLANCO),
        ("Usa la CALCULADORA DE HASH: escribe cada nombre y compara.", FOSF_VERDE),
        ("SHA-256 es irreversible. Solo puedes verificar.", AMBER),
    ])
    briefing_mision(3, "IDENTIDAD FANTASMA", [
        "4 sospechosos. Solo uno tiene esa huella digital.",
        "Escribe cada nombre en la calculadora y compara.",
        "Cuando el hash coincida, tendrás al infiltrado.",
    ], AMBER, 45)

    # ── Datos ──
    sospechosos = [
        "MORGAN", "REEVES", "CARVER", "BISHOP", "HOLDEN",
        "PIERCE", "LARKIN", "WESTON", "CALLUM", "DECKER",
    ]
    opciones = random.sample(sospechosos, 4)
    culpable = random.choice(opciones)
    hash_real = sha256(culpable)

    # ── Estado ──
    vidas = 3
    msg_ret = ""
    col_msg = BLANCO
    resuelto = False
    TMAX = 45.0
    t_ini = time.time()
    t_mision = 0.0
    pista_usada = False
    seleccionado = -1

    # Calculadora interactiva
    calc = HashCalc(20, 230, ANCHO - 40, 110)
    calc.activo = True

    aria.decir("Escribe nombres en la calculadora. Compara hashes.",
               ROJO_ALERTA, 0.5)
    aria.decir("Cuando coincidan, selecciona al sospechoso.", AMBER, 4)

    while True:
        dt = reloj.tick(60) / 1000.0
        tt = time.time()
        t_rest = max(0, TMAX - (tt - t_ini)) if not resuelto else TMAX
        mouse = pygame.mouse.get_pos()
        sfx.update(dt)
        calc.update()

        fondo_terminal()
        tick_particles()
        lluvia_data(1)
        hud_superior(3, "IDENTIDAD FANTASMA", AMBER, vidas)

        # ── Huella digital objetivo ──
        panel(20, 68, ANCHO - 40, 80,
              col=(25, 15, 0), borde=ROJO_ALERTA, radio=6)
        txt("◉ HUELLA DEL INFILTRADO — SHA-256:",
            F_SMALL, ROJO_ALERTA, 35, 73)
        pygame.draw.line(pantalla, ROJO_ALERTA,
                         (35, 90), (ANCHO - 50, 90), 1)

        # Hash con efecto scan
        scan = int((tt * 30) % 64)
        h1 = ""
        for i, c in enumerate(hash_real[:32]):
            h1 += (random.choice("0123456789abcdef")
                   if i == scan and not resuelto else c)
        h2 = ""
        for i, c in enumerate(hash_real[32:]):
            h2 += (random.choice("0123456789abcdef")
                   if i + 32 == scan and not resuelto else c)
        txt(h1, F_SMALL, AMBER, 35, 95)
        txt(h2, F_SMALL, AMBER, 35, 113)
        txt("(64 chars hexadecimales)", F_TINY, FOSF_DIM, ANCHO - 180, 113)

        # ── Tiempo ──
        panel(20, 156, ANCHO - 40, 38, borde=FOSF_DIM, radio=4)
        txt("INFILTRADO HUYE EN:", F_MICRO, ROJO_ALERTA, 35, 160)
        barra_tiempo(180, 164, ANCHO - 230, 14, t_rest, TMAX)

        if t_rest <= 0 and not resuelto:
            vidas = 0
            resuelto = True
            t_mision = TMAX
            msg_ret = f"TARDE. Infiltrado: {culpable}"
            col_msg = ROJO_ALERTA
            agente.fallo()
            sfx.shake(12, 0.5)
            sfx.flash(ROJO_ALERTA, 0.3)
            boom(ANCHO // 2, ALTO // 2, ROJO_ALERTA, 50)
            play("alerta")

        # ── Calculadora de hash ──
        calc.draw(target_hash=hash_real, mouse=mouse)

        # ── Tarjetas de sospechosos ──
        txt("◉ SOSPECHOSOS — CLIC PARA SELECCIONAR:",
            F_BOLD, AMBER, ANCHO // 2, 350, centro=True)

        botones_sosp = []
        bw_s = ANCHO // 2 - 30
        bh_s = 55
        posiciones = [
            (25, 370), (ANCHO // 2 + 5, 370),
            (25, 435), (ANCHO // 2 + 5, 435),
        ]

        for i, (sosp, p) in enumerate(zip(opciones, posiciones)):
            rect_sosp = pygame.Rect(p[0], p[1], bw_s, bh_s)
            hov = rect_sosp.collidepoint(mouse)
            sel = (i == seleccionado)
            hash_sosp = sha256(sosp)
            es_culpable = (hash_sosp == hash_real)

            if sel:
                bord_col = ORO if es_culpable else AMBER
                bg_col = (30, 20, 0) if es_culpable else (20, 15, 0)
            elif hov:
                bord_col = AMBER
                bg_col = (15, 10, 0)
            else:
                bord_col = FOSF_DIM
                bg_col = GRIS_PANEL

            panel(p[0], p[1], bw_s, bh_s, col=bg_col, borde=bord_col, radio=5)

            # Feedback de coincidencia con la calculadora
            if calc.texto.upper() == sosp:
                if es_culpable:
                    txt("✓ COINCIDE", F_TINY, FOSF_VERDE,
                        p[0] + bw_s - 90, p[1] + 5)
                    s = pygame.Surface((bw_s, bh_s), pygame.SRCALPHA)
                    s.fill((*FOSF_VERDE, 20))
                    pantalla.blit(s, (p[0], p[1]))
                else:
                    txt("✗ no coincide", F_TINY, ROJO_DIM,
                        p[0] + bw_s - 110, p[1] + 5)

            # Avatar circular
            ax = p[0] + 25
            ay = p[1] + bh_s // 2
            col_avatar = FOSF_VERDE if sel else FOSF_DIM
            pygame.draw.circle(pantalla, col_avatar, (ax, ay), 16)
            txt(sosp[0], F_BOLD, (0, 0, 0), ax, ay - 8, centro=True)

            # Nombre y mini-hash
            txt(sosp, F_BOLD, AMBER if sel else BLANCO, p[0] + 50, p[1] + 8)
            txt(f"SHA: {hash_sosp[:20]}...", F_TINY, FOSF_DIM,
                p[0] + 50, p[1] + 28)
            if sel:
                txt("▶ SELECCIONADO", F_TINY, ORO, p[0] + 50, p[1] + 42)

            botones_sosp.append(rect_sosp)

        # ── Botones de acción ──
        btn_acu = boton(
            "▶ ACUSAR SELECCIONADO", 25, 502, 250, 34,
            (60, 30, 0), (120, 60, 0), mouse, F_SMALL,
            enabled=not resuelto and seleccionado >= 0,
        )
        btn_pst = boton(
            "◈ PISTA (−1 vida)", 290, 502, 180, 34,
            (50, 40, 0), (100, 80, 0), mouse, F_SMALL,
            enabled=not resuelto and vidas > 1 and not pista_usada,
        )
        btn_lim = boton(
            "◈ LIMPIAR CALCULADORA", 485, 502, 220, 34,
            (20, 30, 20), (40, 70, 40), mouse, F_SMALL,
            enabled=not resuelto,
        )

        # ── Mensaje de resultado ──
        if msg_ret:
            bg = (0, 35, 12) if col_msg == FOSF_VERDE else (40, 0, 0)
            panel(20, 545, ANCHO - 40, 35, col=bg, borde=col_msg, radio=4)
            txt(msg_ret, F_BOLD, col_msg, ANCHO // 2, 553, centro=True)

        if resuelto:
            btn_sig = boton(
                "SIGUIENTE MISIÓN ▶▶",
                ANCHO // 2 - 110, ALTO - 55, 220, 38,
                (0, 60, 20), (0, 120, 40), mouse,
            )

        # ── Overlays ──
        aria.actualizar()
        aria.dibujar()
        indicador_progreso(2)
        logros.draw()
        sfx.draw()
        tick_floats()
        pygame.display.flip()

        # ── Acusar ──
        def acusar():
            nonlocal vidas, msg_ret, col_msg, resuelto, t_mision, seleccionado
            t_mision = tt - t_ini
            if seleccionado >= 0 and opciones[seleccionado] == culpable:
                agente.acierto()
                tb = max(0, (t_rest / TMAX) * 0.5)
                pts = agente.sumar(400, vidas, tb)
                msg_ret = (f"✓ INFILTRADO IDENTIFICADO: {culpable} "
                           f"| +{pts} pts")
                col_msg = FOSF_VERDE
                resuelto = True
                logros.intentar("HUELLA")
                if t_mision < 10:
                    logros.intentar("VELOCISTA")
                sfx.flash(FOSF_VERDE, 0.3)
                sfx.shake(6, 0.3)
                boom(ANCHO // 2, 400, FOSF_VERDE, 60)
                play("ok")
                add_float(f"+{pts}", ANCHO // 2, 380, FOSF_VERDE, 32)
                add_float("INFILTRADO DETENIDO", ANCHO // 2, 350,
                          (255, 215, 0), 20, 3)
            else:
                vidas -= 1
                agente.fallo()
                sfx.shake(10, 0.4)
                sfx.flash(ROJO_ALERTA, 0.2)
                sfx.glitch(0.5)
                boom(ANCHO // 2, 400, ROJO_ALERTA, 30)
                play("error")
                if vidas == 0:
                    t_mision = TMAX
                    msg_ret = (f"✗ AGENTE INOCENTE LIBERADO. "
                               f"Era: {culpable}")
                    col_msg = ROJO_ALERTA
                    resuelto = True
                else:
                    msg_ret = (f"✗ INCORRECTO. Agente inocente. "
                               f"Vidas: {vidas}")
                    col_msg = ROJO_ALERTA
                    seleccionado = -1

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
                    if ev.key == pygame.K_BACKSPACE:
                        calc.texto = calc.texto[:-1]
                        calc.set_texto(calc.texto)
                        calc.set_target(hash_real)
                    elif ev.unicode.isalpha() and len(calc.texto) < 12:
                        calc.texto += ev.unicode.upper()
                        calc.set_texto(calc.texto)
                        calc.set_target(hash_real)
                        play("tecla")
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if not resuelto and vidas > 0:
                    # Seleccionar sospechoso
                    for i, br in enumerate(botones_sosp):
                        if br.collidepoint(ev.pos):
                            seleccionado = i
                            play("click")
                    if btn_acu.collidepoint(ev.pos):
                        acusar()
                    if btn_pst.collidepoint(ev.pos):
                        vidas -= 1
                        agente.usar_pista()
                        pista_usada = True
                        msg_ret = (f"◈ PISTA: {len(culpable)} letras, "
                                   f"empieza con '{culpable[0]}'")
                        col_msg = AMBER
                        play("beep")
                    if btn_lim.collidepoint(ev.pos):
                        calc.texto = ""
                        calc.set_texto("")
                        play("beep")
                if resuelto:
                    try:
                        if btn_sig.collidepoint(ev.pos):
                            play("mision")
                            return vidas > 0, t_mision, True
                    except NameError:
                        pass