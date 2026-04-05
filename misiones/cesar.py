# -*- coding: utf-8 -*-
"""
Misión 01 — CIFRADO CÉSAR: "El Código del Topo"
Con rueda de cifrado interactiva.
"""

import random
import time
import pygame

from config import (
    ANCHO, ALTO, reloj, pantalla,
    FOSF_VERDE, FOSF_DIM, FOSF_DARK, AMBER, ROJO_ALERTA,
    ROJO_DIM, BLANCO, GRIS_PANEL, GRIS_BORDE,
    F_GRANDE, F_SMALL, F_MICRO, F_BOLD, F_TINY,
)
from criptografia import cesar, desc_cesar
from ui import (
    txt, txt_glow, panel, boton, input_box, barra_tiempo,
    hud_superior, indicador_progreso,
)
from estado import agente
from aria import aria
from efectos import (
    sfx, tick_particles, lluvia_data, boom, add_float,
    tick_floats,
)
from sonidos import play
from logros import logros
from componentes.rueda_cesar import RuedaCesar
from escenas.teletipo import teletipo, briefing_mision


def mision_cesar():
    """
    Ejecuta la misión de cifrado César.
    Retorna (exitosa, tiempo_empleado, puntos_mision).
    """
    teletipo([
        ("TRANSMISIÓN INTERCEPTADA — AGENTE CIPHER", ROJO_ALERTA),
        ("", FOSF_DIM),
        ("Hemos capturado una comunicación cifrada con César.", BLANCO),
        ("Usa la RUEDA DE CIFRADO para encontrar el desplazamiento K.", FOSF_VERDE),
        ("Haz clic en ▲/▼ para rotar la rueda y descifra la palabra.", FOSF_DIM),
        ("Cada error delata nuestra posición. Actúa con precisión.", AMBER),
    ])
    briefing_mision(1, "EL CÓDIGO DEL TOPO", [
        "Usa la rueda de cifrado interactiva.",
        "Rota hasta que la palabra descifrada tenga sentido.",
        "Puedes escribir la respuesta directamente también.",
    ], FOSF_VERDE, 35)

    # ── Datos de la misión ──
    banco = [
        ("BERLIN", "Operación en BERLIN a medianoche"),
        ("MOSCOVA", "Paquete a MOSCOVA vía tren"),
        ("PRAGA", "Intercambio en PRAGA bajo el puente"),
        ("VIENA", "Contacto en VIENA estación central"),
        ("TOKIO", "Documentos salen por TOKIO"),
        ("ZURICH", "Fondos desde ZURICH"),
        ("ATENAS", "Submarino desde ATENAS a las 0300"),
        ("LISBOA", "Exfiltración vía LISBOA"),
    ]
    ciudad, msg_completo = random.choice(banco)
    k = random.randint(3, 15)
    ciudad_cifrada = cesar(ciudad, k)
    msg_cifrado = cesar(msg_completo, k)

    # ── Estado de la misión ──
    texto_inp = ""
    vidas = 3
    msg_ret = ""
    col_msg = BLANCO
    resuelto = False
    TMAX = 35.0
    t_ini = time.time()
    pista_usada = False
    t_mision = 0.0
    rueda = RuedaCesar(ANCHO - 140, 310, 95)

    aria.decir("Usa la rueda de cifrado. Rota con ▲ ▼.", (0, 230, 230), 0.5)
    aria.decir(f"Palabra cifrada: {ciudad_cifrada}. Busca una ciudad.",
               FOSF_VERDE, 4)

    # ── Bucle principal ──
    while True:
        dt = reloj.tick(60) / 1000.0
        tt = time.time()
        t_rest = max(0, TMAX - (tt - t_ini)) if not resuelto else TMAX
        mouse = pygame.mouse.get_pos()
        sfx.update(dt)
        rueda.update()

        # ── Fondo con offset de shake ──
        ox, oy = sfx.shake_x, sfx.shake_y
        s = pygame.Surface((ANCHO, ALTO))
        s.fill((4, 8, 4))
        for yy in range(0, ALTO, 3):
            pygame.draw.line(s, (0, 0, 0, 50), (0, yy), (ANCHO, yy))
        for xx in range(0, ANCHO, 80):
            pygame.draw.line(s, (0, 18, 6), (xx, 0), (xx, ALTO))
        for yy in range(0, ALTO, 80):
            pygame.draw.line(s, (0, 18, 6), (0, yy), (ANCHO, yy))
        pantalla.blit(s, (ox, oy))

        tick_particles()
        lluvia_data(1)
        hud_superior(1, "EL CÓDIGO DEL TOPO", FOSF_VERDE, vidas)

        # ── Mensaje interceptado ──
        panel(20 + ox, 68 + oy, ANCHO - 300, 95,
              col=(0, 20, 8), borde=ROJO_ALERTA, radio=6)
        txt("◉ TRANSMISIÓN INTERCEPTADA:", F_SMALL, ROJO_ALERTA,
            35 + ox, 73 + oy)
        pygame.draw.line(pantalla, ROJO_ALERTA,
                         (35 + ox, 90 + oy), (ANCHO - 290 + ox, 90 + oy), 1)
        scan_char = int((tt * 15) % len(msg_cifrado))
        msg_disp = ""
        for i, c in enumerate(msg_cifrado):
            if i == scan_char and not resuelto:
                msg_disp += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            else:
                msg_disp += c
        txt(msg_disp, F_SMALL, AMBER, 35 + ox, 95 + oy)
        txt("OBJETIVO →", F_SMALL, FOSF_DIM, 35 + ox, 120 + oy)
        txt_glow(ciudad_cifrada, F_GRANDE, ROJO_ALERTA, 145 + ox, 116 + oy)

        # ── Barra de tiempo ──
        panel(20 + ox, 172 + oy, ANCHO - 300, 44,
              borde=FOSF_DIM, radio=4)
        txt("TIEMPO:", F_MICRO, ROJO_ALERTA, 35 + ox, 176 + oy)
        barra_tiempo(95 + ox, 190 + oy, ANCHO - 360, 14, t_rest, TMAX)

        # ── Tiempo agotado ──
        if t_rest <= 0 and not resuelto:
            vidas = 0
            resuelto = True
            t_mision = TMAX
            msg_ret = f"CANAL DESTRUIDO. Era: {ciudad} (K={k})"
            col_msg = ROJO_ALERTA
            agente.fallo()
            sfx.shake(12, 0.5)
            sfx.flash(ROJO_ALERTA, 0.3)
            sfx.glitch(0.8)
            boom(ANCHO // 2, ALTO // 2, ROJO_ALERTA, 40)
            play("error")

        # ── Rueda de cifrado ──
        panel(ANCHO - 280 + ox, 68 + oy, 265, 460,
              col=(5, 15, 5), borde=FOSF_VERDE, radio=6)
        txt("◈ RUEDA DE CIFRADO CÉSAR", F_TINY, FOSF_VERDE,
            ANCHO - 268 + ox, 74 + oy)
        rueda.cx = ANCHO - 148 + ox
        rueda.cy = 230 + oy
        rueda.draw(palabra_cifrada=ciudad_cifrada, mouse=mouse)

        # Botones de rotación
        btn_up = boton("▲", ANCHO - 168 + ox, 340 + oy, 40, 28,
                       (0, 50, 15), (0, 100, 30), mouse, F_SMALL,
                       enabled=not resuelto)
        btn_dn = boton("▼", ANCHO - 168 + ox, 374 + oy, 40, 28,
                       (0, 50, 15), (0, 100, 30), mouse, F_SMALL,
                       enabled=not resuelto)

        # Decodificación en tiempo real según la rueda
        k_actual = int(round(rueda.desplazamiento)) % 26
        desc_rueda = desc_cesar(ciudad_cifrada, k_actual)
        col_desc = FOSF_VERDE if desc_rueda == ciudad else AMBER
        txt(f"K={k_actual:02d} → {desc_rueda}", F_BOLD, col_desc,
            ANCHO - 120 + ox, 348 + oy, centro=True)
        if desc_rueda == ciudad and not resuelto:
            txt("¡COINCIDENCIA!", F_SMALL, FOSF_VERDE,
                ANCHO - 148 + ox, 400 + oy, centro=True)

        # ── Input directo ──
        panel(20 + ox, 226 + oy, ANCHO - 300, 120,
              col=GRIS_PANEL, borde=FOSF_DIM, radio=4)
        txt("◉ INGRESA LA CIUDAD DESCIFRADA:", F_SMALL, FOSF_VERDE,
            35 + ox, 232 + oy)
        input_box(texto_inp, 35 + ox, 254 + oy, ANCHO - 340,
                  activo=not resuelto, placeholder="Nombre de ciudad...")
        btn_env = boton("▶ VERIFICAR", 35 + ox, 296 + oy, 160, 32,
                        (0, 50, 15), (0, 100, 30), mouse, F_SMALL,
                        enabled=not resuelto)
        btn_pst = boton("◈ PISTA (−1 vida)", 210 + ox, 296 + oy, 180, 32,
                        (50, 40, 0), (100, 80, 0), mouse, F_SMALL,
                        enabled=not resuelto and vidas > 1 and not pista_usada)
        btn_auto = boton("⚡ AUTO-ROTAR A K", 400 + ox, 296 + oy, 180, 32,
                         (20, 30, 20), (40, 70, 40), mouse, F_SMALL,
                         enabled=not resuelto)

        # ── Preview de decodificación ──
        panel(20 + ox, 355 + oy, ANCHO - 300, 55,
              borde=FOSF_DIM, radio=4)
        txt("VISTA PREVIA (mensaje con K actual):", F_TINY, FOSF_DIM,
            35 + ox, 360 + oy)
        preview = desc_cesar(msg_cifrado, k_actual)
        col_prev = FOSF_VERDE if k_actual == k else FOSF_DIM
        txt(preview[:70], F_TINY, col_prev, 35 + ox, 376 + oy)
        if len(preview) > 70:
            txt(preview[70:], F_TINY, col_prev, 35 + ox, 390 + oy)

        # ── Mensaje de resultado ──
        if msg_ret:
            bg = (0, 35, 12) if col_msg == FOSF_VERDE else (40, 0, 0)
            panel(20 + ox, 420 + oy, ANCHO - 40, 35,
                  col=bg, borde=col_msg, radio=4)
            txt(msg_ret, F_BOLD, col_msg, ANCHO // 2, 428 + oy, centro=True)

        if resuelto and col_msg == FOSF_VERDE:
            panel(20 + ox, 462 + oy, ANCHO - 40, 35,
                  col=(0, 30, 10), borde=FOSF_VERDE, radio=4)
            txt(f"DESCIFRADO: {msg_completo}", F_SMALL, FOSF_VERDE,
                35 + ox, 470 + oy)

        if resuelto:
            btn_sig = boton("SIGUIENTE MISIÓN ▶▶",
                            ANCHO // 2 - 110 + ox, ALTO - 55 + oy, 220, 38,
                            (0, 60, 20), (0, 120, 40), mouse)

        # ── Overlays ──
        aria.actualizar()
        aria.dibujar()
        indicador_progreso(0)
        logros.draw()
        sfx.draw()
        tick_floats()

        pygame.display.flip()

        # ── Lógica de verificación ──
        def verificar():
            nonlocal vidas, msg_ret, col_msg, resuelto, pista_usada
            nonlocal texto_inp, t_mision
            t_mision = tt - t_ini
            if texto_inp.upper().strip() == ciudad:
                agente.acierto()
                tb = max(0, (t_rest / TMAX) * 0.5)
                pts = agente.sumar(300, vidas, tb)
                msg_ret = f"✓ CORRECTO: {ciudad} | K={k} | +{pts} pts"
                col_msg = FOSF_VERDE
                resuelto = True
                if not pista_usada:
                    logros.intentar("SIN_PISTA")
                if t_mision < 10:
                    logros.intentar("VELOCISTA")
                logros.intentar("CIFRADOR")
                sfx.flash(FOSF_VERDE, 0.2)
                sfx.shake(4, 0.2)
                boom(ANCHO // 2, 400, FOSF_VERDE, 50)
                play("ok")
                add_float(f"+{pts}", ANCHO // 2, 350, FOSF_VERDE, 30)
                aria.decir("¡Excelente! Punto localizado.", FOSF_VERDE)
            else:
                vidas -= 1
                agente.fallo()
                sfx.shake(8, 0.3)
                sfx.flash(ROJO_ALERTA, 0.15)
                sfx.glitch(0.4)
                boom(ANCHO // 2, 400, ROJO_ALERTA, 20)
                play("error")
                aria.decir("Incorrecto. ¡Cuidado!", ROJO_ALERTA)
                if vidas == 0:
                    t_mision = TMAX
                    msg_ret = f"✗ SIN VIDAS. Era: {ciudad} (K={k})"
                    col_msg = ROJO_ALERTA
                    resuelto = True
                else:
                    msg_ret = f"✗ ERROR. Vidas: {vidas}"
                    col_msg = ROJO_ALERTA
                    texto_inp = ""

        # ── Eventos ──
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
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
                    if btn_up.collidepoint(ev.pos):
                        rueda.click_arriba()
                    if btn_dn.collidepoint(ev.pos):
                        rueda.click_abajo()
                    if btn_pst.collidepoint(ev.pos):
                        vidas -= 1
                        pista_usada = True
                        agente.usar_pista()
                        rueda.set_k(k)
                        msg_ret = f"◈ PISTA: K = {k} (rueda ajustada)"
                        col_msg = AMBER
                        play("beep")
                    if btn_auto.collidepoint(ev.pos):
                        rueda.set_k(k)
                        play("nivel")
                if resuelto:
                    try:
                        if btn_sig.collidepoint(ev.pos):
                            play("mision")
                            return vidas > 0, t_mision, True
                    except NameError:
                        pass