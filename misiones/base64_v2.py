# -*- coding: utf-8 -*-
"""
Misión 02 — BASE64: "Transmisión Encubierta" (VERSIÓN SIMPLIFICADA)
Decodifica el mensaje y adivina la operación.
"""

import random
import time
import pygame

from config import (
    ANCHO, ALTO, reloj, pantalla,
    FOSF_VERDE, FOSF_DIM, FOSF_DARK, AMBER, ROJO_ALERTA,
    ROJO_DIM, BLANCO, CYAN_SCAN, GRIS_PANEL,
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


# ═══════════════════════════════════════════════════════════════════════════════
#  MISIONES BASE64: Nombres + Mensajes + Pistas
# ═══════════════════════════════════════════════════════════════════════════════
MISIONES = {
    "NOCTUA": {
        "mensaje": "Ave nocturna que caza en la oscuridad. Su visión perfeccionada le permite ver donde otros son ciegos.",
        "pistas": [
            "Búho: Rapaz nocturna",
            "Ojos adaptados a la oscuridad",
            "Cazadora silenciosa",
        ],
    },
    "VORTEX": {
        "mensaje": "Un remolino que absorbe todo a su paso. Gira sin dirección, atrapando en su ciclo infinito.",
        "pistas": [
            "Movimiento circular",
            "Absorbe todo en su trayecto",
            "Sin escape una vez dentro",
        ],
    },
    "SPECTRE": {
        "mensaje": "Fantasma sin huella física. No aparece en cámaras, dejando cero evidencia material de su existencia.",
        "pistas": [
            "Invisible en cámaras",
            "Sin huellas dactilares",
            "Desaparece sin dejar rastro",
        ],
    },
    "KRONOS": {
        "mensaje": "El devorador del tiempo que devora sus propios hijos. Cuando el reloj llegue a cero, todo termina.",
        "pistas": [
            "Titán griego del tiempo",
            "Cuenta regresiva iniciada",
            "El fin llega cuando el reloj marca cero",
        ],
    },
    "ECLIPSE": {
        "mensaje": "Cuando la luz se apaga, el mundo retiene el aliento. Siete minutos de oscuridad absoluta.",
        "pistas": [
            "La Luna entre la Tierra y el Sol",
            "Duración: 7 minutos",
            "Comunicaciones cortadas durante el evento",
        ],
    },
    "PHANTOM": {
        "mensaje": "El que no existe en registro alguno pero opera desde todas partes. Invisible hasta que golpea.",
        "pistas": [
            "Agente fantasma sin identidad",
            "Múltiples avistamientos no confirmados",
            "Aparece donde menos se espera",
        ],
    },
    "CIPHER": {
        "mensaje": "Código secreto que esconde la verdad entre letras cifradas. Solo con la llave correcta se descifra.",
        "pistas": [
            "Mensaje codificado en múltiples capas",
            "Solo la llave maestra abre el contenido",
            "Antiguo método de encriptación",
        ],
    },
    "NEXUS": {
        "mensaje": "El punto donde todos los hilos convergen. Un nudo imposible de desatar por la fuerza bruta.",
        "pistas": [
            "Red central conectada",
            "Múltiples operaciones convergen aquí",
            "Cortar el nodo colapsa toda la estructura",
        ],
    },
}


def mision_base64():
    """
    Misión simplificada de Base64.
    El usuario decodifica el mensaje y adivina el nombre de la operación.
    """
    teletipo([
        ("TRANSMISIÓN INTERCEPTADA — NIVEL CRÍTICO", ROJO_ALERTA),
        ("", FOSF_DIM),
        ("Hemos capturado un mensaje Base64 de KRONOS.", BLANCO),
        ("Tu trabajo: DECODIFICAR el mensaje y ADIVINAR el nombre de la operación.", FOSF_VERDE),
        ("Las tres pistas te guiarán hacia la respuesta correcta.", CYAN_SCAN),
    ])
    briefing_mision(2, "TRANSMISIÓN ENCUBIERTA", [
        "Paso 1: Lee el mensaje Base64 en la pantalla.",
        "Paso 2: Haz clic en DECODIFICAR para revelar el mensaje.",
        "Paso 3: Lee las 3 pistas que aparecen debajo.",
        "Paso 4: Escribe el nombre de la operación.",
    ], CYAN_SCAN, 40)

    # ── Elegir misión aleatoria ──
    op_nombre = random.choice(list(MISIONES.keys()))
    op_data = MISIONES[op_nombre]
    mensaje_original = op_data["mensaje"]
    pistas = op_data["pistas"]
    mensaje_codificado = b64enc(mensaje_original)

    # ── Estado de la misión ──
    texto_respuesta = ""
    vidas = 3
    msg_ret = ""
    col_msg = BLANCO
    resuelto = False
    TMAX = 60.0
    t_ini = time.time()
    t_mision = 0.0
    
    decodificado = False
    pista_usada = False
    foco = "respuesta"

    aria.decir("Lee el mensaje Base64. Decodifícalo para descubrir la verdad.", CYAN_SCAN, 0.5)
    aria.decir("Las pistas te dirán qué operación buscas. Elige sabiamente.", AMBER, 5)

    # ── Bucle principal ──
    while True:
        dt = reloj.tick(60) / 1000.0
        tt = time.time()
        t_rest = max(0, TMAX - (tt - t_ini)) if not resuelto else TMAX
        mouse = pygame.mouse.get_pos()
        sfx.update(dt)

        if t_rest <= 0 and not resuelto:
            resuelto = True
            msg_ret = f"✗ TIEMPO AGOTADO. La operación era: {op_nombre}"
            col_msg = ROJO_ALERTA
            t_mision = TMAX

        # ── Renderizado ──
        fondo_terminal()
        tick_particles()
        lluvia_data(1)
        hud_superior(2, "TRANSMISIÓN ENCUBIERTA", CYAN_SCAN, vidas)

        # ── Sección 1: Mensaje Base64 ──
        panel(20, 70, ANCHO - 40, 100, col=(0, 12, 22), borde=CYAN_SCAN, radio=6)
        txt("◉ MENSAJE BASE64 INTERCEPTADO:", F_SMALL, CYAN_SCAN, 35, 75)
        pygame.draw.line(pantalla, CYAN_SCAN, (35, 95), (ANCHO - 35, 95), 1)
        
        # Mostrar Base64 codificado en múltiples líneas
        b64_lines = []
        chars_por_linea = 50
        for i in range(0, len(mensaje_codificado), chars_por_linea):
            b64_lines.append(mensaje_codificado[i:i + chars_por_linea])
        
        for i, linea in enumerate(b64_lines[:2]):  # Mostrar 2 líneas máximo
            txt(linea, F_MICRO, FOSF_DIM, 35, 102 + i * 18)

        # ── Sección 2: Timing ──
        panel(20, 175, ANCHO - 40, 40, borde=FOSF_DIM, radio=4)
        txt("DECODIFICAR EN:", F_MICRO, CYAN_SCAN, 35, 180)
        barra_tiempo(200, 185, ANCHO - 260, 14, t_rest, TMAX, CYAN_SCAN, AMBER, ROJO_ALERTA)

        # ── Sección 3: Controles ──
        col_x = 20
        col_w = (ANCHO - 60) // 2

        # Botón DECODIFICAR
        btn_decode = boton("▶ DECODIFICAR",
                          col_x + 10, 225, 180, 36,
                          (10, 40, 60), (20, 80, 120), mouse, F_SMALL,
                          enabled=not decodificado and not resuelto)

        # ── Sección 4: Mensaje Decodificado ──
        if decodificado:
            panel(col_x, 275, col_w, 200, col=GRIS_PANEL, borde=FOSF_VERDE, radio=4)
            txt("◈ MENSAJE DECODIFICADO:", F_TINY, FOSF_VERDE, col_x + 8, 280)
            pygame.draw.line(pantalla, FOSF_VERDE, (col_x + 8, 298), (col_x + col_w - 8, 298), 1)

            # Word-wrap del mensaje
            msg_lines = []
            msg_temp = ""
            for word in mensaje_original.split():
                if len(msg_temp) + len(word) + 1 > 35:
                    msg_lines.append(msg_temp.strip())
                    msg_temp = word
                else:
                    msg_temp += " " + word
            if msg_temp:
                msg_lines.append(msg_temp.strip())

            y_msg = 305
            for linea in msg_lines[:5]:  # Máximo 5 líneas
                txt(linea, F_TINY, BLANCO, col_x + 12, y_msg)
                y_msg += 18
        else:
            panel(col_x, 275, col_w, 200, col=GRIS_PANEL, borde=FOSF_DIM, radio=4)
            txt("◈ MENSAJE DECODIFICADO:", F_TINY, FOSF_DIM, col_x + 8, 280)
            txt("(Presiona DECODIFICAR para revelar)", F_SMALL, FOSF_DIM, col_x + 12, 330, centro=False)

        # ── Sección 5: Pistas ──
        an_x = col_x + col_w + 20
        panel(an_x, 275, col_w, 200, col=GRIS_PANEL, borde=AMBER, radio=4)
        txt("◈ PISTAS CLAVE:", F_TINY, AMBER, an_x + 8, 280)
        pygame.draw.line(pantalla, AMBER, (an_x + 8, 298), (an_x + col_w - 8, 298), 1)

        y_pista = 310
        for i, pista in enumerate(pistas):
            # Número de pista
            txt(f"{i+1}.", F_BOLD, CYAN_SCAN, an_x + 12, y_pista)
            
            # Texto de pista (word-wrap)
            pista_lines = []
            pista_temp = ""
            for word in pista.split():
                if len(pista_temp) + len(word) + 1 > 28:
                    pista_lines.append(pista_temp.strip())
                    pista_temp = word
                else:
                    pista_temp += " " + word
            if pista_temp:
                pista_lines.append(pista_temp.strip())

            for j, linea in enumerate(pista_lines):
                txt(linea, F_TINY, BLANCO, an_x + 30, y_pista + j * 16)
            
            y_pista += len(pista_lines) * 16 + 8

        # ── Sección 6: Respuesta ──
        resp_activo = (foco == "respuesta" and not resuelto)
        resp_borde = FOSF_VERDE if resp_activo else FOSF_DIM
        if resp_activo:
            s_br = pygame.Surface((ANCHO - 360, 65), pygame.SRCALPHA)
            s_br.fill((*FOSF_VERDE, 12))
            pantalla.blit(s_br, (col_x, 490))
        
        panel(col_x, 490, ANCHO - 360, 65, col=(5, 15, 5), borde=resp_borde, radio=4)
        txt(f"◉ OPERACIÓN {'◀ ACTIVA' if resp_activo else ''}", F_TINY, 
            FOSF_VERDE if resp_activo else FOSF_DIM, col_x + 8, 495)
        
        input_box(texto_respuesta, col_x + 8, 515, ANCHO - 376, 
                  activo=not resuelto, placeholder="Nombre de la operación...")

        btn_verify = boton("▶ VERIFICAR", col_x + ANCHO - 361, 515, 140, 28,
                          (0, 50, 15), (0, 100, 30), mouse, F_TINY,
                          enabled=not resuelto and decodificado)

        # ── Mensaje de resultado ──
        if msg_ret:
            bg = (0, 35, 12) if col_msg == FOSF_VERDE else (40, 0, 0)
            panel(20, ALTO - 110, ANCHO - 40, 35, col=bg, borde=col_msg, radio=4)
            txt(msg_ret, F_BOLD, col_msg, ANCHO // 2, ALTO - 93, centro=True)

        btn_sig = None
        if resuelto:
            btn_sig = boton("SIGUIENTE MISIÓN ▶▶",
                           ANCHO // 2 - 110, ALTO - 55, 220, 38,
                           (0, 60, 20), (0, 120, 40), mouse)

        # ── Overlays ──
        aria.actualizar()
        aria.dibujar()
        indicador_progreso(1)
        logros.draw()
        sfx.draw()
        tick_floats()

        pygame.display.flip()

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
                        if foco == "respuesta" and decodificado:
                            # Verificar respuesta
                            t_mision = tt - t_ini
                            if texto_respuesta.upper().strip() == op_nombre:
                                agente.acierto()
                                tb = max(0, (t_rest / TMAX) * 0.5)
                                pts = agente.sumar(300, vidas, tb)
                                msg_ret = f"✓ CORRECTO: {op_nombre} | +{pts} pts"
                                col_msg = FOSF_VERDE
                                resuelto = True
                                if not pista_usada:
                                    logros.intentar("SIN_PISTA")
                                if t_mision < 15:
                                    logros.intentar("VELOCISTA")
                                logros.intentar("DECODIFICADOR")
                                sfx.flash(FOSF_VERDE, 0.2)
                                sfx.shake(4, 0.2)
                                boom(ANCHO // 2, 400, FOSF_VERDE, 50)
                                play("ok")
                                add_float(f"+{pts}", ANCHO // 2, 350, FOSF_VERDE, 30)
                                aria.decir(f"¡{op_nombre} confirmada!", FOSF_VERDE)
                            else:
                                vidas -= 1
                                agente.fallo()
                                sfx.shake(8, 0.3)
                                sfx.flash(ROJO_ALERTA, 0.15)
                                boom(ANCHO // 2, 400, ROJO_ALERTA, 20)
                                play("error")
                                msg_ret = f"✗ INCORRECTO. Vidas: {vidas}"
                                col_msg = ROJO_ALERTA
                                texto_respuesta = ""
                                
                                if vidas == 0:
                                    t_mision = TMAX
                                    msg_ret = f"✗ SIN ACCESOS. Era: {op_nombre}"
                                    col_msg = ROJO_ALERTA
                                    resuelto = True
                                else:
                                    aria.decir("Reintenta. Las pistas son tuya aliada.", ROJO_ALERTA)
                    
                    elif ev.key == pygame.K_BACKSPACE and foco == "respuesta":
                        texto_respuesta = texto_respuesta[:-1]
                    elif ev.unicode.isalnum() and len(texto_respuesta) < 20:
                        texto_respuesta += ev.unicode.upper()
            
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if btn_decode.collidepoint(mouse) and not decodificado and not resuelto:
                    decodificado = True
                    play("nivel")
                    sfx.flash(CYAN_SCAN, 0.15)
                    aria.decir("Mensaje decodificado. Lee sus secretos.", CYAN_SCAN)
                
                if btn_verify.collidepoint(mouse) and not resuelto and decodificado:
                    # Simular RETURN
                    t_mision = tt - t_ini
                    if texto_respuesta.upper().strip() == op_nombre:
                        agente.acierto()
                        tb = max(0, (t_rest / TMAX) * 0.5)
                        pts = agente.sumar(300, vidas, tb)
                        msg_ret = f"✓ CORRECTO: {op_nombre} | +{pts} pts"
                        col_msg = FOSF_VERDE
                        resuelto = True
                        if not pista_usada:
                            logros.intentar("SIN_PISTA")
                        if t_mision < 15:
                            logros.intentar("VELOCISTA")
                        logros.intentar("DECODIFICADOR")
                        sfx.flash(FOSF_VERDE, 0.2)
                        sfx.shake(4, 0.2)
                        boom(ANCHO // 2, 400, FOSF_VERDE, 50)
                        play("ok")
                        add_float(f"+{pts}", ANCHO // 2, 350, FOSF_VERDE, 30)
                        aria.decir(f"¡{op_nombre} confirmada!", FOSF_VERDE)
                    else:
                        vidas -= 1
                        agente.fallo()
                        sfx.shake(8, 0.3)
                        sfx.flash(ROJO_ALERTA, 0.15)
                        boom(ANCHO // 2, 400, ROJO_ALERTA, 20)
                        play("error")
                        msg_ret = f"✗ INCORRECTO. Vidas: {vidas}"
                        col_msg = ROJO_ALERTA
                        texto_respuesta = ""
                        
                        if vidas == 0:
                            t_mision = TMAX
                            msg_ret = f"✗ SIN ACCESOS. Era: {op_nombre}"
                            col_msg = ROJO_ALERTA
                            resuelto = True
                        else:
                            aria.decir("Reintenta. Las pistas son tuya aliada.", ROJO_ALERTA)
                
                if btn_sig and btn_sig.collidepoint(mouse) and resuelto:
                    return True, t_mision, True
