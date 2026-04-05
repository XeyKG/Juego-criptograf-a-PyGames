# -*- coding: utf-8 -*-
"""
Misión 04 — DIFFIE-HELLMAN: "Protocolo D-H"
Con visualización interactiva del intercambio de claves.
"""

import random
import time
import pygame

from config import (
    ANCHO, ALTO, reloj, pantalla,
    FOSF_VERDE, FOSF_DIM, FOSF_DARK, AMBER, ROJO_ALERTA,
    MORADO, ORO, BLANCO, GRIS_PANEL,
    F_SMALL, F_MICRO, F_BOLD, F_TINY,
)
from criptografia import diffie_hellman
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
from componentes.dh_visual import DHVisual
from escenas.teletipo import teletipo, briefing_mision


def mision_diffie():
    """
    Ejecuta la misión Diffie-Hellman.
    Retorna (exitosa, tiempo_empleado, puntos_mision).
    """
    teletipo([
        ("PROTOCOLO DE INTERCEPCIÓN — DIFICULTAD MÁXIMA", ROJO_ALERTA),
        ("", FOSF_DIM),
        ("KRONOS usa Diffie-Hellman para establecer claves secretas.", BLANCO),
        ("Observa el intercambio y calcula el SECRETO COMPARTIDO.", FOSF_VERDE),
        ("Si conoces los parámetros y un secreto privado, puedes calcularlo.", AMBER),
    ])
    briefing_mision(4, "PROTOCOLO D-H", [
        "Alice y Bob intercambian claves públicas.",
        "Tú conoces p, g, y el secreto privado de Alice (a).",
        "Calcula: secreto = B^a mod p",
    ], MORADO, 50)

    # ── Parámetros (primos pequeños para que sea calculable mentalmente) ──
    primos = [23, 29, 31, 37, 41, 43, 47, 53, 59, 61]
    p = random.choice(primos)
    g = random.choice([2, 3, 5])
    a = random.randint(2, p - 2)
    b = random.randint(2, p - 2)
    A_pub = pow(g, a, p)
    B_pub = pow(g, b, p)
    secreto = pow(B_pub, a, p)

    # ── Opciones de respuesta (1 correcta + 3 distractores) ──
    opciones_resp = [secreto]
    while len(opciones_resp) < 4:
        margen = max(1, secreto // 3)
        fake = secreto + random.randint(-margen, margen)
        if fake > 0 and fake not in opciones_resp and fake < p:
            opciones_resp.append(fake)
    random.shuffle(opciones_resp)

    # ── Estado ──
    vidas = 3
    msg_ret = ""
    col_msg = BLANCO
    resuelto = False
    TMAX = 50.0
    t_ini = time.time()
    t_mision = 0.0
    pista_usada = False
    seleccion_resp = -1

    # Visualización DH
    dh_vis = DHVisual(20, 220, ANCHO - 40, 180)
    dh_vis.setup(p, g, a, b)

    aria.decir("Diffie-Hellman: secreto = B^a mod p", MORADO, 0.5)
    aria.decir(f"Tienes: p={p}, g={g}, a={a}, B={B_pub}", (0, 230, 230), 4)
    aria.decir("Avanza por los pasos del protocolo.", FOSF_VERDE, 8)

    while True:
        dt = reloj.tick(60) / 1000.0
        tt = time.time()
        t_rest = max(0, TMAX - (tt - t_ini)) if not resuelto else TMAX
        mouse = pygame.mouse.get_pos()
        sfx.update(dt)
        dh_vis.update()

        fondo_terminal()
        tick_particles()
        lluvia_data(1)
        hud_superior(4, "PROTOCOLO D-H", MORADO, vidas)

        # ── Parámetros ──
        panel(20, 68, ANCHO - 40, 70,
              col=(10, 5, 25), borde=MORADO, radio=6)
        txt("◉ PARÁMETROS DEL PROTOCOLO:", F_SMALL, MORADO, 35, 73)
        pygame.draw.line(pantalla, MORADO,
                         (35, 90), (ANCHO - 50, 90), 1)
        txt(f"p (primo) = {p}    |    g (generador) = {g}    |    "
            f"a (secreto Alice) = {a}    |    B (clave pública Bob) = {B_pub}",
            F_SMALL, AMBER, 35, 96)

        # ── Tiempo ──
        panel(20, 146, ANCHO - 40, 38, borde=FOSF_DIM, radio=4)
        txt("INTERCEPCIÓN EN:", F_MICRO, ROJO_ALERTA, 35, 150)
        barra_tiempo(180, 154, ANCHO - 230, 14, t_rest, TMAX)

        if t_rest <= 0 and not resuelto:
            vidas = 0
            resuelto = True
            t_mision = TMAX
            msg_ret = f"TIEMPO. Secreto era: {secreto}"
            col_msg = ROJO_ALERTA
            agente.fallo()
            sfx.shake(12, 0.5)
            sfx.flash(ROJO_ALERTA, 0.3)
            boom(ANCHO // 2, ALTO // 2, ROJO_ALERTA, 50)
            play("alerta")

        # ── Visualización DH ──
        dh_vis.draw(mouse)

        # ── Botón avanzar fase ──
        btn_av = None
        if dh_vis.fase < 3 and not resuelto:
            nombres_fase = [
                "Calcular A y B",
                "Intercambiar claves",
                "Calcular secreto",
            ]
            btn_av = boton(
                f"▶ {nombres_fase[dh_vis.fase]}",
                ANCHO // 2 - 100, 408, 200, 32,
                (30, 15, 50), (60, 30, 100), mouse, F_SMALL,
            )

        # ── Opciones de respuesta (aparecen en fase 3) ──
        botones_resp = []
        btn_conf = None

        if dh_vis.fase >= 3:
            txt("◉ ¿CUÁL ES EL SECRETO COMPARTIDO?",
                F_BOLD, MORADO, ANCHO // 2, 448, centro=True)

            for i, op_val in enumerate(opciones_resp):
                bx = 25 + (i % 2) * (ANCHO // 2 + 5)
                by = 470 + (i // 2) * 45
                rect_op = pygame.Rect(bx, by, ANCHO // 2 - 30, 38)
                sel = (i == seleccion_resp)
                es_correcto = (op_val == secreto)
                hov = rect_op.collidepoint(mouse)

                if sel:
                    bord = ORO
                    bg = (30, 20, 0)
                elif hov:
                    bord = MORADO
                    bg = (20, 10, 30)
                else:
                    bord = FOSF_DIM
                    bg = GRIS_PANEL

                panel(bx, by, ANCHO // 2 - 30, 38,
                      col=bg, borde=bord, radio=5)
                txt(f"Opción {i + 1}: {op_val}",
                    F_BOLD, ORO if sel else BLANCO, bx + 15, by + 10)

                if sel and es_correcto:
                    txt("✓", F_BOLD, FOSF_VERDE,
                        bx + ANCHO // 2 - 60, by + 10)

                botones_resp.append((rect_op, i))

            btn_conf = boton(
                "▶ CONFIRMAR SELECCIÓN",
                ANCHO // 2 - 110, 565, 220, 34,
                (30, 15, 50), (60, 30, 100), mouse, F_SMALL,
                enabled=not resuelto and seleccion_resp >= 0,
            )

        # ── Fórmula de ayuda ──
        panel(20, 408, ANCHO - 250, 80,
              col=GRIS_PANEL, borde=FOSF_DIM, radio=4)
        txt("◈ FÓRMULA:", F_TINY, FOSF_DIM, 30, 412)
        txt("A = g^a mod p  (clave pública Alice)",
            F_TINY, (0, 230, 230), 30, 428)
        txt("B = g^b mod p  (clave pública Bob)",
            F_TINY, AMBER, 30, 444)
        txt("Secreto = B^a mod p = A^b mod p",
            F_TINY, FOSF_VERDE, 30, 460)
        txt(f"→ {B_pub}^{a} mod {p} = ?", F_TINY, MORADO, 30, 476)

        # ── Pista ──
        btn_pst = boton(
            "◈ PISTA (−1 vida)", ANCHO - 220, 408, 190, 32,
            (50, 40, 0), (100, 80, 0), mouse, F_SMALL,
            enabled=not resuelto and vidas > 1 and not pista_usada,
        )

        # ── Mensaje de resultado ──
        if msg_ret:
            bg = (0, 35, 12) if col_msg == FOSF_VERDE else (40, 0, 0)
            panel(20, 605, ANCHO - 40, 35, col=bg, borde=col_msg, radio=4)
            txt(msg_ret, F_BOLD, col_msg, ANCHO // 2, 613, centro=True)

        if resuelto:
            btn_sig = boton(
                "VER INFORME FINAL ▶▶",
                ANCHO // 2 - 120, ALTO - 55, 240, 38,
                (0, 60, 20), (0, 120, 40), mouse,
            )

        # ── Overlays ──
        aria.actualizar()
        aria.dibujar()
        indicador_progreso(3)
        logros.draw()
        sfx.draw()
        tick_floats()
        pygame.display.flip()

        # ── Confirmar selección ──
        def confirmar():
            nonlocal vidas, msg_ret, col_msg, resuelto, t_mision, seleccion_resp
            t_mision = tt - t_ini
            if (seleccion_resp >= 0
                    and opciones_resp[seleccion_resp] == secreto):
                agente.acierto()
                tb = max(0, (t_rest / TMAX) * 0.5)
                pts = agente.sumar(500, vidas, tb)
                msg_ret = (f"✓ SECRETO INTERCEPTADO: {secreto} "
                           f"| +{pts} pts")
                col_msg = FOSF_VERDE
                resuelto = True
                logros.intentar("PROTOCOLO")
                if t_mision < 15:
                    logros.intentar("VELOCISTA")
                sfx.flash(MORADO, 0.3)
                sfx.shake(6, 0.3)
                boom(ANCHO // 2, 400, MORADO, 60)
                play("ok")
                add_float(f"+{pts}", ANCHO // 2, 580, MORADO, 32)
                add_float("PROTOCOLO ROTO", ANCHO // 2, 550,
                          ORO, 22, 3)
            else:
                vidas -= 1
                agente.fallo()
                sfx.shake(10, 0.4)
                sfx.flash(ROJO_ALERTA, 0.2)
                boom(ANCHO // 2, 400, ROJO_ALERTA, 30)
                play("error")
                if vidas == 0:
                    t_mision = TMAX
                    msg_ret = f"✗ SECRETO PERDIDO. Era: {secreto}"
                    col_msg = ROJO_ALERTA
                    resuelto = True
                else:
                    msg_ret = f"✗ SECRETO INCORRECTO. Vidas: {vidas}"
                    col_msg = ROJO_ALERTA
                    seleccion_resp = -1

        # ── Eventos ──
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return False, t_mision, False
                # Seleccionar opción con teclas 1-4
                if not resuelto and vidas > 0 and dh_vis.fase >= 3:
                    num = ev.key - pygame.K_1
                    if 0 <= num < len(opciones_resp):
                        seleccion_resp = num
                        play("click")
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if not resuelto and vidas > 0:
                    # Avanzar fase
                    if btn_av and btn_av.collidepoint(ev.pos):
                        dh_vis.advance()
                        if dh_vis.fase == 3:
                            aria.decir(
                                "Selecciona el secreto compartido "
                                "correcto.", MORADO)
                    # Seleccionar opción
                    for rect_op, idx in botones_resp:
                        if rect_op.collidepoint(ev.pos):
                            seleccion_resp = idx
                            play("click")
                    # Confirmar
                    if btn_conf and btn_conf.collidepoint(ev.pos):
                        confirmar()
                    # Pista
                    if btn_pst.collidepoint(ev.pos):
                        vidas -= 1
                        agente.usar_pista()
                        pista_usada = True
                        msg_ret = (f"◈ PISTA: Calcula {B_pub}^{a} mod {p}. "
                                   f"Usa calculadora si necesitas.")
                        col_msg = AMBER
                        play("beep")
                if resuelto:
                    try:
                        if btn_sig.collidepoint(ev.pos):
                            play("mision")
                            return vidas > 0, t_mision, True
                    except NameError:
                        pass