# -*- coding: utf-8 -*-
"""
Misión 04 — DIFFIE-HELLMAN: "KRONOS // Apagón Final"
Misión final épica — tres fases activas, inyección de código dígito a dígito,
ventana de disparo y final cinematográfico.
"""

import random
import time
import math
import pygame

from config import (
    ANCHO, ALTO, reloj, pantalla,
    FOSF_VERDE, FOSF_DIM, FOSF_DARK, AMBER, ROJO_ALERTA,
    MORADO, ORO, BLANCO, GRIS_PANEL,
    F_SMALL, F_MICRO, F_BOLD, F_TINY,
)
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


DOSSIERS = {
    "HELIOS":    "Helios gestiona satélites de baja órbita. Su canal usa claves efímeras rotativas.",
    "CERBERUS":  "Cerberus protege nodos con redundancia triple. Clave correcta = cortafuegos caído.",
    "NOVA":      "Nova sincroniza agentes durmientes. Su tráfico parece ruido aleatorio.",
    "ORION":     "Orion enlaza observadores en cuatro ciudades. Ventana orbital: 70 segundos.",
    "KRONOS":    "KRONOS es el núcleo. Si cae, toda la red queda ciega para siempre.",
    "HELP":      "Comandos: KRONOS, HELIOS, ORION, NOVA, CERBERUS. Busca información táctica.",
    "FORMULA":   "Secreto = B^a mod p. Recuerda: multiplica B por sí mismo 'a' veces, módulo p.",
}


def _wrap_lines(texto, fuente, ancho_max):
    palabras = texto.split()
    lineas, actual = [], ""
    for p in palabras:
        prueba = (actual + " " + p).strip()
        if fuente.size(prueba)[0] <= ancho_max:
            actual = prueba
        else:
            if actual:
                lineas.append(actual)
            actual = p
    if actual:
        lineas.append(actual)
    return lineas


def _build_distractors(correcto, p):
    cands = {correcto}
    while len(cands) < 4:
        delta = random.randint(1, max(3, p // 5))
        f = correcto + random.choice([-delta, delta, -2*delta, 2*delta])
        if 1 <= f < p:
            cands.add(f)
    lst = list(cands)
    random.shuffle(lst)
    return lst


def _calc_opts(correcto, p):
    """3 opciones: 1 correcta + 2 distractoras para la verificación de Fase 1."""
    cands = {correcto}
    while len(cands) < 3:
        f = correcto + random.choice([-2, -1, 1, 2, 3, -3])
        if 1 <= f < p:
            cands.add(f)
    lst = list(cands)
    random.shuffle(lst)
    return lst


def mision_diffie():
    """
    Ejecuta la misión final Diffie-Hellman — KRONOS // Apagón Final.
    Retorna (exitosa, tiempo_empleado, puntos_mision).
    """
    teletipo([
        ("PROTOCOLO FINAL — KRONOS // APAGÓN GLOBAL", ROJO_ALERTA),
        ("", FOSF_DIM),
        ("La red KRONOS va a sellar su última clave efímera.", BLANCO),
        ("Solo tienes una ventana para interceptar el secreto.", MORADO),
        ("Tres fases. Sin margen de error. El mundo depende de ti.", AMBER),
    ])
    briefing_mision(4, "KRONOS // APAGÓN FINAL", [
        "Fase 1: Avanza el protocolo. Verifica las claves A y B.",
        "Fase 2: Selecciona el secreto compartido correcto.",
        "Fase 3: Inyecta el código dígito a dígito. Dispara el apagón.",
    ], MORADO, 75)

    primos = [23, 29, 31, 37, 41, 43, 47, 53]
    p = random.choice(primos)
    g = random.choice([2, 3, 5])
    a = random.randint(2, min(7, p - 2))
    b = random.randint(2, min(7, p - 2))

    A_pub  = pow(g, a, p)
    B_pub  = pow(g, b, p)
    secreto = pow(B_pub, a, p)
    secreto_str = str(secreto)

    objetivo       = random.choice(["KRONOS", "HELIOS", "ORION", "NOVA", "CERBERUS"])
    opciones_resp  = _build_distractors(secreto, p)

    # Fase 1: verificar A y B
    opts_A = _calc_opts(A_pub, p)
    opts_B = _calc_opts(B_pub, p)

    # ── Estado global ──
    vidas          = 3
    msg_ret        = ""
    col_msg        = BLANCO
    resuelto       = False
    TMAX           = 75.0
    t_ini          = time.time()
    t_mision       = 0.0
    pista_nivel    = 0
    seleccion_resp = -1

    # Fase 1 — verificación activa de A y B
    fase1_paso        = 0    # 0=verificar A  1=verificar B  2=completa
    sel_A             = -1
    sel_B             = -1
    fase1_msg         = ""
    fase1_col         = BLANCO

    # Fase 2 — selección del secreto (aparece cuando dh_vis.fase >= 3 y fase1_paso == 2)
    fase2_ok          = False

    # Fase 3 — inyección dígito a dígito
    fase3_activa      = False
    digitos_ok        = []   # dígitos confirmados correctamente
    dig_msg           = ""
    dig_col           = BLANCO
    dig_error_timer   = 0.0

    # Ventana de disparo
    disparo_activo    = False
    senal_pos         = 0.0   # 0.0 → 1.0
    senal_dir         = 1
    SENAL_SPEED       = 0.55
    ZONE_L, ZONE_R    = 0.38, 0.62
    disparo_realizado = False
    disparo_resultado = False  # True si entró en zona
    disparo_timer     = 0.0
    apagon_ok         = False

    # Terminal
    foco_terminal  = False
    terminal_txt   = ""
    terminal_out   = ""
    terminal_col   = FOSF_DIM
    terminal_visible = False
    terminal_timer = 0.0

    dh_vis = DHVisual(20, 206, ANCHO - 40, 170)
    dh_vis.setup(p, g, a, b)

    aria.decir("KRONOS en línea. Última misión del operativo.", ROJO_ALERTA, 0.5)
    aria.decir(f"Parámetros: p={p}, g={g}, a={a}, B={B_pub}", MORADO, 4)
    aria.decir("Verifica las claves públicas antes de avanzar.", FOSF_VERDE, 8)

    while True:
        dt = reloj.tick(60) / 1000.0
        tt = time.time()
        t_rest = max(0, TMAX - (tt - t_ini)) if not resuelto else TMAX
        mouse  = pygame.mouse.get_pos()
        sfx.update(dt)
        dh_vis.update()

        if terminal_visible and terminal_timer > 0:
            terminal_timer -= dt
            if terminal_timer <= 0:
                terminal_visible = False

        if dig_error_timer > 0:
            dig_error_timer -= dt

        # Animación señal de disparo
        if disparo_activo and not disparo_realizado:
            senal_pos += senal_dir * SENAL_SPEED * dt
            if senal_pos >= 1.0:
                senal_pos = 1.0; senal_dir = -1
            elif senal_pos <= 0.0:
                senal_pos = 0.0; senal_dir = 1

        if disparo_realizado:
            disparo_timer += dt

        fondo_terminal()
        tick_particles()
        lluvia_data(1)
        hud_superior(4, "KRONOS // APAGÓN FINAL", MORADO, vidas)

        # ── Header: parámetros ──
        panel(20, 68, ANCHO - 40, 58, col=(10, 5, 25), borde=MORADO, radio=6)
        txt("◉ INTERCEPCIÓN CRÍTICA:", F_SMALL, MORADO, 35, 73)
        pygame.draw.line(pantalla, MORADO, (35, 90), (ANCHO - 50, 90), 1)
        txt(f"OBJETIVO={objetivo}  |  p={p}  |  g={g}  |  a={a}  |  A={A_pub}  |  B={B_pub}",
            F_SMALL, AMBER, 35, 95)

        # ── Barra tiempo ──
        panel(20, 134, ANCHO - 40, 36, borde=FOSF_DIM, radio=4)
        txt("VENTANA:", F_MICRO, ROJO_ALERTA, 35, 138)
        barra_tiempo(108, 144, ANCHO - 158, 14, t_rest, TMAX)

        if t_rest <= 0 and not resuelto:
            vidas = 0; resuelto = True; t_mision = TMAX
            msg_ret = f"TIEMPO AGOTADO — El secreto era {secreto}. KRONOS escapó."
            col_msg = ROJO_ALERTA; agente.fallo()
            sfx.shake(12, 0.5); sfx.flash(ROJO_ALERTA, 0.3); sfx.glitch(0.8)
            boom(ANCHO // 2, ALTO // 2, ROJO_ALERTA, 50); play("alerta")

        # ── Indicadores de fase ──
        col_ind = lambda ok: FOSF_VERDE if ok else AMBER
        txt(f"[FASE 1 {'✓' if fase1_paso == 2 else '…'}] VERIFICAR CLAVES",
            F_TINY, col_ind(fase1_paso == 2), 30, 176)
        txt(f"[FASE 2 {'✓' if fase2_ok else '…'}] DERIVAR SECRETO",
            F_TINY, col_ind(fase2_ok), 280, 176)
        txt(f"[FASE 3 {'✓' if apagon_ok else '…'}] APAGÓN FINAL",
            F_TINY, col_ind(apagon_ok), 520, 176)

        # ── Visualización DH ──
        dh_vis.draw(mouse)

        # ════════════════════════════════════════════════
        # FASE 1: Verificación activa de claves A y B
        # ════════════════════════════════════════════════
        if fase1_paso < 2 and not resuelto:
            panel(20, 382, ANCHO - 40, 195, col=(10, 5, 25), borde=MORADO, radio=6)

            if fase1_paso == 0:
                txt("◈ FASE 1 — VERIFICACIÓN: ¿Cuánto vale A = g^a mod p?", F_SMALL, MORADO, 35, 388)
                txt(f"A = {g}^{a} mod {p}  =  ???", F_SMALL, AMBER, 35, 408)

                botones_f1 = []
                for i, op in enumerate(opts_A):
                    bx = 35 + i * (ANCHO // 3 - 10)
                    rect_f1 = pygame.Rect(bx, 435, ANCHO // 3 - 20, 34)
                    sel = (sel_A == i)
                    hov = rect_f1.collidepoint(mouse)
                    pg = (35, 25, 10) if sel else (20, 10, 30) if hov else GRIS_PANEL
                    bd = ORO if sel else MORADO if hov else FOSF_DIM
                    panel(bx, 435, ANCHO // 3 - 20, 34, col=pg, borde=bd, radio=5)
                    txt(f"A = {op}", F_SMALL, ORO if sel else BLANCO,
                        bx + (ANCHO // 3 - 20) // 2, 444, centro=True)
                    botones_f1.append((rect_f1, i, op))

                if fase1_msg:
                    txt(fase1_msg, F_SMALL, fase1_col, ANCHO // 2, 488, centro=True)

                btn_conf_f1 = boton("► CONFIRMAR A", ANCHO // 2 - 90, 500, 180, 30,
                                    (30, 15, 50), (60, 30, 100), mouse, F_SMALL,
                                    enabled=sel_A >= 0)
            else:
                txt("◈ FASE 1 — VERIFICACIÓN: ¿Cuánto vale B = g^b mod p?", F_SMALL, MORADO, 35, 388)
                txt(f"B = {g}^{b} mod {p}  =  ???", F_SMALL, AMBER, 35, 408)
                txt(f"(Tú no conoces b directamente, pero B viene en el canal)", F_TINY, FOSF_DIM, 35, 424)

                botones_f1 = []
                for i, op in enumerate(opts_B):
                    bx = 35 + i * (ANCHO // 3 - 10)
                    rect_f1 = pygame.Rect(bx, 445, ANCHO // 3 - 20, 34)
                    sel = (sel_B == i)
                    hov = rect_f1.collidepoint(mouse)
                    pg = (35, 25, 10) if sel else (20, 10, 30) if hov else GRIS_PANEL
                    bd = ORO if sel else MORADO if hov else FOSF_DIM
                    panel(bx, 445, ANCHO // 3 - 20, 34, col=pg, borde=bd, radio=5)
                    txt(f"B = {op}", F_SMALL, ORO if sel else BLANCO,
                        bx + (ANCHO // 3 - 20) // 2, 454, centro=True)
                    botones_f1.append((rect_f1, i, op))

                if fase1_msg:
                    txt(fase1_msg, F_SMALL, fase1_col, ANCHO // 2, 492, centro=True)

                btn_conf_f1 = boton("► CONFIRMAR B", ANCHO // 2 - 90, 504, 180, 30,
                                    (30, 15, 50), (60, 30, 100), mouse, F_SMALL,
                                    enabled=sel_B >= 0)

            # Avanzar visual DH también durante fase 1
            if dh_vis.fase < 3:
                btn_av_f1 = boton("▶ Avanzar visualización", ANCHO - 260, 382, 230, 26,
                                  (30, 15, 50), (60, 30, 100), mouse, F_TINY)
            else:
                btn_av_f1 = None

        # ════════════════════════════════════════════════
        # FASE 2: Seleccionar secreto (activa cuando fase1 == 2)
        # ════════════════════════════════════════════════
        botones_resp = []
        btn_conf_f2  = None

        if fase1_paso == 2 and not fase2_ok and not resuelto:
            panel(20, 382, ANCHO - 40, 185, col=(10, 5, 25), borde=MORADO, radio=6)
            txt("◈ FASE 2 — ¿CUÁL ES EL SECRETO COMPARTIDO?  B^a mod p", F_BOLD, MORADO, 35, 388)
            txt(f"  Secreto = {B_pub}^{a} mod {p}", F_SMALL, AMBER, 35, 408)

            if pista_nivel >= 1:
                txt(f"  Pista: multiplica paso a paso. {B_pub}×{B_pub} mod {p} = {(B_pub*B_pub)%p}", F_TINY, FOSF_VERDE, 35, 426)

            for i, op_val in enumerate(opciones_resp):
                bx = 35 + (i % 2) * (ANCHO // 2)
                by = 445 + (i // 2) * 38
                rect_op = pygame.Rect(bx, by, ANCHO // 2 - 55, 32)
                sel = i == seleccion_resp
                hov = rect_op.collidepoint(mouse)
                bd = ORO if sel else MORADO if hov else FOSF_DIM
                bg = (35, 25, 10) if sel else (20, 10, 30) if hov else GRIS_PANEL
                panel(bx, by, ANCHO // 2 - 55, 32, col=bg, borde=bd, radio=4)
                txt(f"  Opción {i+1}: {op_val}", F_SMALL, ORO if sel else BLANCO, bx + 8, by + 8)
                botones_resp.append((rect_op, i))

            btn_conf_f2 = boton("► INYECTAR EN FASE 2", ANCHO // 2 - 110, 528, 220, 32,
                                (30, 15, 50), (60, 30, 100), mouse, F_SMALL,
                                enabled=seleccion_resp >= 0)
            if msg_ret:
                bg = (0, 35, 12) if col_msg == FOSF_VERDE else (40, 0, 0)
                panel(20, 568, ANCHO - 40, 28, col=bg, borde=col_msg, radio=4)
                txt(msg_ret, F_BOLD, col_msg, ANCHO // 2, 575, centro=True)

        # ════════════════════════════════════════════════
        # FASE 3: Inyección dígito a dígito + ventana disparo
        # ════════════════════════════════════════════════
        if fase2_ok and not resuelto:
            py3 = 382
            panel(20, py3, ANCHO - 40, 250, col=(5, 15, 5), borde=FOSF_VERDE, radio=6)
            txt("◉ FASE 3 — INYECCIÓN DE CÓDIGO: escribe el secreto dígito a dígito", F_SMALL, FOSF_VERDE, 35, py3 + 6)

            # Slots de dígitos
            n_dig     = len(secreto_str)
            slot_w    = 52
            slot_h    = 54
            total_w   = n_dig * (slot_w + 10) - 10
            slot_x0   = ANCHO // 2 - total_w // 2
            slot_y    = py3 + 30

            for i, d in enumerate(secreto_str):
                sx = slot_x0 + i * (slot_w + 10)
                confirmado = i < len(digitos_ok)
                es_actual  = i == len(digitos_ok) and not disparo_activo

                if confirmado:
                    bord = FOSF_VERDE
                    bg   = (5, 30, 10)
                    char = digitos_ok[i]
                    col_c = FOSF_VERDE
                elif es_actual and dig_error_timer > 0:
                    bord = ROJO_ALERTA
                    bg   = (30, 5, 5)
                    char = "✗"
                    col_c = ROJO_ALERTA
                elif es_actual:
                    pulso = int(tt * 4) % 2
                    bord  = AMBER if pulso else FOSF_DIM
                    bg    = (18, 14, 4) if pulso else GRIS_PANEL
                    char  = "█" if pulso else "_"
                    col_c = AMBER
                else:
                    bord  = FOSF_DIM
                    bg    = GRIS_PANEL
                    char  = "_"
                    col_c = FOSF_DARK

                panel(sx, slot_y, slot_w, slot_h, col=bg, borde=bord, radio=6)
                txt(char, F_BOLD, col_c, sx + slot_w // 2, slot_y + 12, centro=True)

            # Etiqueta del secreto
            txt(f"[ CÓDIGO DE APAGÓN: {' '.join('_' * n_dig)} ]  →  escribe los dígitos de {secreto_str if pista_nivel >= 2 else '???'}",
                F_TINY, FOSF_DIM, ANCHO // 2, slot_y + slot_h + 8, centro=True)

            # Mensaje dígito
            if dig_msg:
                txt(dig_msg, F_SMALL, dig_col, ANCHO // 2, slot_y + slot_h + 26, centro=True)

            # ── Instrucción de teclado ──
            if not disparo_activo and len(digitos_ok) < n_dig:
                txt("↑ Presiona las teclas numéricas para ingresar cada dígito", F_TINY, FOSF_DIM,
                    ANCHO // 2, slot_y + slot_h + 44, centro=True)

            # ════════════════
            # Ventana de disparo
            # ════════════════
            if disparo_activo:
                disp_y   = py3 + 140
                disp_w   = ANCHO - 80
                disp_x   = 40
                disp_h   = 60

                panel(disp_x, disp_y, disp_w, disp_h, col=(5, 5, 20), borde=MORADO, radio=6)

                # Zona objetivo
                zt_x = int(disp_x + ZONE_L * disp_w)
                zt_w = int((ZONE_R - ZONE_L) * disp_w)
                pygame.draw.rect(pantalla, (30, 80, 30),
                                 pygame.Rect(zt_x, disp_y + 8, zt_w, disp_h - 16),
                                 border_radius=4)
                txt("ZONA", F_TINY, FOSF_VERDE, zt_x + zt_w // 2, disp_y + 12, centro=True)
                txt("OBJETIVO", F_TINY, FOSF_VERDE, zt_x + zt_w // 2, disp_y + 26, centro=True)

                if not disparo_realizado:
                    # Marcador de señal
                    senal_sx = int(disp_x + senal_pos * disp_w)
                    col_senal = FOSF_VERDE if ZONE_L <= senal_pos <= ZONE_R else ROJO_ALERTA
                    pygame.draw.line(pantalla, col_senal,
                                     (senal_sx, disp_y + 4), (senal_sx, disp_y + disp_h - 4), 3)
                    pygame.draw.circle(pantalla, col_senal, (senal_sx, disp_y + disp_h // 2), 8)

                    txt("▼ PRESIONA ESPACIO para disparar cuando la señal esté en la ZONA VERDE",
                        F_TINY, AMBER, ANCHO // 2, disp_y + disp_h + 12, centro=True)
                else:
                    if disparo_resultado:
                        fade = min(1.0, disparo_timer * 2)
                        r, g_, b_ = FOSF_VERDE
                        txt("◉ SEÑAL ANCLADA. EJECUTANDO APAGÓN...", F_BOLD, FOSF_VERDE,
                            ANCHO // 2, disp_y + 20, centro=True)
                        if disparo_timer > 0.8 and not apagon_ok:
                            apagon_ok  = True
                            resuelto   = True
                            t_mision   = tt - t_ini
                            agente.acierto()
                            tb    = max(0, (t_rest / TMAX) * 0.5)
                            bonus = [80, 40, 0][min(pista_nivel, 2)]
                            pts   = agente.sumar(700 + bonus, vidas, tb)
                            msg_ret = f"✓ KRONOS OFFLINE | SECRETO={secreto} | +{pts} pts"
                            col_msg = FOSF_VERDE
                            logros.intentar("PROTOCOLO")
                            if pista_nivel == 0:
                                logros.intentar("SIN_PISTA")
                            if t_mision < 30:
                                logros.intentar("VELOCISTA")
                            sfx.flash(MORADO, 0.4)
                            sfx.shake(10, 0.4)
                            boom(ANCHO // 2, ALTO // 2, MORADO, 80)
                            boom(200, 300, FOSF_VERDE, 50)
                            boom(ANCHO - 200, 300, ORO, 50)
                            play("ok")
                            add_float("KRONOS OFFLINE", ANCHO // 2, ALTO // 2 - 30, ORO, 30, 3)
                            add_float(f"+{pts}", ANCHO // 2, ALTO // 2 + 5, FOSF_VERDE, 34)
                            aria.decir("Objetivo neutralizado. La red cayó.", ORO)
                    else:
                        txt("✗ SEÑAL FUERA DE ZONA. Vuelve a intentarlo.", F_BOLD, ROJO_ALERTA,
                            ANCHO // 2, disp_y + 20, centro=True)
                        if disparo_timer > 1.2:
                            disparo_realizado = False
                            disparo_resultado = False
                            disparo_timer     = 0.0
                            senal_pos = 0.0

        # ── Terminal táctica (siempre disponible) ──
        term_y = 567 if fase2_ok else (func_term_y := 382 if fase1_paso == 2 and fase2_ok else 382)
        # Fijarla abajo
        if not fase2_ok:
            term_y = ALTO - 160

        t_activo = foco_terminal and not resuelto
        panel(20, term_y, ANCHO - 240, 70, col=(5, 12, 18), borde=MORADO if t_activo else FOSF_DIM, radio=4)
        txt(f"◈ TERMINAL TÁCTICA {'[ACTIVA]' if t_activo else '[Tab/Clic para activar]'}", F_TINY,
            MORADO if t_activo else FOSF_DIM, 30, term_y + 5)
        term_input_rect = pygame.Rect(30, term_y + 22, ANCHO - 260, 22)
        pygame.draw.rect(pantalla, (8, 18, 24), term_input_rect, border_radius=3)
        pygame.draw.rect(pantalla, MORADO if t_activo else FOSF_DIM, term_input_rect, 1, border_radius=3)
        txt(terminal_txt if terminal_txt else "escribe: KRONOS, FORMULA, HELP...",
            F_TINY, BLANCO if terminal_txt else FOSF_DARK, 38, term_y + 27)
        btn_scan = boton("▶ SCAN", 30, term_y + 48, 90, 20,
                         (20, 20, 50), (50, 50, 100), mouse, F_TINY,
                         enabled=len(terminal_txt.strip()) > 0 and not resuelto)
        if terminal_visible and terminal_out:
            lines = _wrap_lines(terminal_out, F_TINY, ANCHO - 270)
            txt(f"► {lines[0]}", F_TINY, terminal_col, 30, term_y + 72)
            if len(lines) > 1:
                txt(f"  {lines[1]}", F_TINY, terminal_col, 30, term_y + 87)

        # ── Panel fórmula ──
        panel(ANCHO - 225, term_y, 210, 70, col=GRIS_PANEL, borde=FOSF_DIM, radio=4)
        txt("◈ FÓRMULA", F_TINY, FOSF_DIM, ANCHO - 215, term_y + 5)
        txt(f"A = g^a mod p = {g}^{a} mod {p}", F_TINY, AMBER, ANCHO - 215, term_y + 22)
        txt(f"B = g^b mod p  (b desconocido)", F_TINY, FOSF_DIM, ANCHO - 215, term_y + 38)
        txt(f"S = B^a mod p = {B_pub}^{a} mod {p}", F_TINY, FOSF_VERDE, ANCHO - 215, term_y + 54)

        # ── Pista ──
        btn_pst = boton(f"◈ PISTA ({'bloq.' if pista_nivel >= 2 else '-1 vida'})",
                        ANCHO - 225, term_y + 78, 210, 26,
                        (50, 40, 0), (100, 80, 0), mouse, F_TINY,
                        enabled=not resuelto and vidas > 1 and pista_nivel < 2)

        # ── Resultado final ──
        if msg_ret and (fase2_ok or resuelto):
            bg_ = (0, 35, 12) if col_msg == FOSF_VERDE else (40, 0, 0)
            panel(20, ALTO - 48, ANCHO - 40, 26, col=bg_, borde=col_msg, radio=4)
            txt(msg_ret, F_BOLD, col_msg, ANCHO // 2, ALTO - 41, centro=True)

        if resuelto:
            btn_sig = boton("VER INFORME FINAL ▶▶",
                            ANCHO // 2 - 120, ALTO - 80, 240, 28,
                            (0, 60, 20), (0, 120, 40), mouse)

        aria.actualizar(); aria.dibujar()
        indicador_progreso(3)
        logros.draw(); sfx.draw(); tick_floats()
        pygame.display.flip()

        # ════ Funciones de lógica ════
        def confirmar_fase1():
            nonlocal fase1_paso, sel_A, sel_B, fase1_msg, fase1_col, vidas, t_mision, resuelto, msg_ret, col_msg
            if fase1_paso == 0:
                if sel_A >= 0 and opts_A[sel_A] == A_pub:
                    fase1_paso = 1
                    fase1_msg  = f"✓ A={A_pub} confirmada. Ahora verifica B."
                    fase1_col  = FOSF_VERDE
                    sfx.flash(FOSF_VERDE, 0.1); play("ok")
                    add_float(f"A={A_pub} ✓", 300, 430, FOSF_VERDE, 20)
                    aria.decir(f"A={A_pub} verificada. Ahora verifica B.", FOSF_VERDE)
                else:
                    vidas -= 1; agente.fallo()
                    fase1_msg = f"✗ Incorrecto. Revisa: {g}^{a} mod {p}. Vidas: {vidas}"
                    fase1_col = ROJO_ALERTA
                    sfx.shake(7, 0.3); sfx.flash(ROJO_ALERTA, 0.15); play("error")
                    if vidas <= 0:
                        t_mision = TMAX; resuelto = True
                        msg_ret = f"✗ Sin vidas. El secreto era {secreto}."
                        col_msg = ROJO_ALERTA
            else:
                if sel_B >= 0 and opts_B[sel_B] == B_pub:
                    fase1_paso = 2
                    fase1_msg  = ""
                    sfx.flash(FOSF_VERDE, 0.15); play("ok")
                    sfx.shake(3, 0.15)
                    add_float(f"B={B_pub} ✓", 300, 450, FOSF_VERDE, 20)
                    aria.decir("Claves verificadas. Selecciona el secreto.", MORADO)
                    if dh_vis.fase < 3:
                        dh_vis.fase = 3
                else:
                    vidas -= 1; agente.fallo()
                    fase1_msg = f"✗ Incorrecto. Recuerda que B viene del canal cifrado. Vidas: {vidas}"
                    fase1_col = ROJO_ALERTA
                    sfx.shake(7, 0.3); sfx.flash(ROJO_ALERTA, 0.15); play("error")
                    if vidas <= 0:
                        t_mision = TMAX; resuelto = True
                        msg_ret = f"✗ Sin vidas. El secreto era {secreto}."
                        col_msg = ROJO_ALERTA

        def confirmar_fase2():
            nonlocal vidas, msg_ret, col_msg, resuelto, fase2_ok, t_mision, fase3_activa
            if seleccion_resp >= 0 and opciones_resp[seleccion_resp] == secreto:
                fase2_ok    = True
                fase3_activa = True
                msg_ret     = f"✓ Secreto={secreto} confirmado. Inyecta el código."
                col_msg     = FOSF_VERDE
                sfx.flash(MORADO, 0.2); sfx.shake(4, 0.18); play("ok")
                add_float(f"SECRETO={secreto}", ANCHO // 2, 520, MORADO, 22)
                aria.decir("Secreto derivado. Inyecta el código dígito a dígito.", FOSF_VERDE)
            else:
                vidas -= 1; agente.fallo()
                msg_ret = f"✗ Clave falsa. Vidas: {vidas}"
                col_msg = ROJO_ALERTA
                sfx.shake(9, 0.35); sfx.flash(ROJO_ALERTA, 0.18)
                boom(ANCHO // 2, 510, ROJO_ALERTA, 25); play("error")
                if vidas <= 0:
                    t_mision = TMAX; resuelto = True
                    msg_ret = f"✗ KRONOS selló el canal. Secreto era {secreto}."
                    col_msg = ROJO_ALERTA

        def ingresar_digito(char):
            nonlocal digitos_ok, dig_msg, dig_col, dig_error_timer, disparo_activo, vidas
            nonlocal t_mision, resuelto, msg_ret, col_msg
            idx = len(digitos_ok)
            if idx >= len(secreto_str):
                return
            if char == secreto_str[idx]:
                digitos_ok.append(char)
                sfx.flash(FOSF_VERDE, 0.08); play("ok")
                add_float(char, slot_x0 + idx * (slot_w + 10) + slot_w // 2, slot_y, FOSF_VERDE, 18)
                dig_msg = f"✓ Dígito {idx+1}/{len(secreto_str)} correcto"
                dig_col = FOSF_VERDE
                if len(digitos_ok) == len(secreto_str):
                    dig_msg = "◉ CÓDIGO COMPLETO — Sincroniza la señal y DISPARA"
                    dig_col = ORO
                    disparo_activo = True
                    sfx.shake(4, 0.15); play("nivel")
                    aria.decir("¡Código inyectado! Sincroniza y dispara.", ORO)
            else:
                vidas -= 1; agente.fallo()
                dig_msg       = f"✗ Dígito incorrecto ({char}). Vidas: {vidas}"
                dig_col       = ROJO_ALERTA
                dig_error_timer = 0.5
                sfx.shake(8, 0.3); sfx.flash(ROJO_ALERTA, 0.15); play("error")
                aria.decir("Dígito incorrecto.", ROJO_ALERTA)
                if vidas <= 0:
                    t_mision = TMAX; resuelto = True
                    msg_ret = f"✗ Sin vidas. El secreto era {secreto}."
                    col_msg = ROJO_ALERTA

        def disparar():
            nonlocal disparo_realizado, disparo_resultado, disparo_timer
            disparo_realizado = True
            disparo_timer     = 0.0
            if ZONE_L <= senal_pos <= ZONE_R:
                disparo_resultado = True
                sfx.flash(FOSF_VERDE, 0.15); sfx.shake(5, 0.2)
                play("nivel")
                add_float("ANCLADO", ANCHO // 2, py3 + 155, FOSF_VERDE, 24)
            else:
                disparo_resultado = False
                sfx.flash(ROJO_ALERTA, 0.12); sfx.shake(4, 0.2); play("error")
                add_float("FALLIDO", ANCHO // 2, py3 + 155, ROJO_ALERTA, 24)

        def buscar_terminal():
            nonlocal terminal_out, terminal_col, terminal_visible, terminal_timer, terminal_txt
            q = terminal_txt.strip().upper()
            if not q:
                return
            play("click")
            info = DOSSIERS.get(q)
            if info:
                terminal_out = info
                terminal_col = FOSF_VERDE if q != "KRONOS" else ROJO_ALERTA
                sfx.flash(MORADO, 0.08)
            else:
                terminal_out = f"Sin coincidencias para '{q}'. Prueba: HELP"
                terminal_col = ROJO_ALERTA; sfx.shake(2, 0.1)
            terminal_visible = True; terminal_timer = 5.5; terminal_txt = ""

        # local para slot_x0 y slot_w (disponibles en el scope del while)
        n_dig   = len(secreto_str)
        slot_w  = 52
        slot_x0 = ANCHO // 2 - (n_dig * (slot_w + 10) - 10) // 2
        slot_y  = 382 + 30

        # ════ Eventos ════
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return False, t_mision, False

                if not resuelto and vidas > 0:
                    if ev.key == pygame.K_TAB:
                        foco_terminal = not foco_terminal; play("click")
                    elif ev.key == pygame.K_SPACE:
                        if disparo_activo and not disparo_realizado:
                            disparar()
                    elif foco_terminal:
                        if ev.key == pygame.K_RETURN:
                            buscar_terminal()
                        elif ev.key == pygame.K_BACKSPACE:
                            terminal_txt = terminal_txt[:-1]
                        elif ev.unicode.replace(" ", "").isalpha() or ev.unicode == " ":
                            if len(terminal_txt) < 16:
                                terminal_txt += ev.unicode.upper(); play("tecla")
                    elif fase2_ok and fase3_activa and disparo_activo and not disparo_realizado:
                        if ev.key == pygame.K_SPACE:
                            disparar()
                    elif fase2_ok and fase3_activa and not disparo_activo:
                        if ev.unicode.isdigit():
                            ingresar_digito(ev.unicode)

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if term_input_rect.collidepoint(ev.pos):
                    foco_terminal = True; play("click")
                elif fase2_ok:
                    foco_terminal = False

                if not resuelto and vidas > 0:
                    # Fase 1
                    if fase1_paso < 2:
                        if btn_av_f1 and btn_av_f1.collidepoint(ev.pos):
                            if dh_vis.fase < 3:
                                dh_vis.fase += 1; play("nivel")
                        for rect_f1, idx, _ in botones_f1:
                            if rect_f1.collidepoint(ev.pos):
                                if fase1_paso == 0:
                                    sel_A = idx
                                else:
                                    sel_B = idx
                                play("click")
                        if btn_conf_f1.collidepoint(ev.pos):
                            confirmar_fase1()

                    # Fase 2
                    if fase1_paso == 2 and not fase2_ok:
                        for rect_op, idx in botones_resp:
                            if rect_op.collidepoint(ev.pos):
                                seleccion_resp = idx; play("click")
                        if btn_conf_f2 and btn_conf_f2.collidepoint(ev.pos) and seleccion_resp >= 0:
                            confirmar_fase2()

                    # Pista
                    if btn_pst.collidepoint(ev.pos) and pista_nivel < 2 and vidas > 1:
                        pista_nivel += 1; vidas -= 1; agente.usar_pista(); play("beep")
                        if pista_nivel == 1:
                            aria.decir("Pista 1: multiplica B por sí mismo 'a' veces, módulo p.", AMBER)
                        else:
                            aria.decir(f"Pista 2: el secreto está entre 1 y {p-1}.", AMBER)

                    # Terminal
                    if btn_scan.collidepoint(ev.pos) and terminal_txt.strip():
                        buscar_terminal()

                if resuelto:
                    try:
                        if btn_sig.collidepoint(ev.pos):
                            play("mision"); return vidas > 0, t_mision, True
                    except NameError:
                        pass