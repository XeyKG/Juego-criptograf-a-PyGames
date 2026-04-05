# -*- coding: utf-8 -*-
"""
Misión 01 — CIFRADO CÉSAR: "El Código del Topo"
Con rueda de cifrado + acertijos + terminal de inteligencia.
"""

import random
import time
import pygame

from config import (
    ANCHO, ALTO, reloj, pantalla,
    FOSF_VERDE, FOSF_DIM, FOSF_DARK, AMBER, ROJO_ALERTA,
    ROJO_DIM, BLANCO, GRIS_PANEL, CYAN_SCAN,
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


# ═══════════════════════════════════════════════════════════════════════════════
#  BASE DE DATOS DE INTELIGENCIA
# ═══════════════════════════════════════════════════════════════════════════════
BASE_DATOS = {
    "muro":      "Muro de Berlín (1961-1989). Dividió Alemania Oriental y Occidental.",
    "alemania":  "País europeo. Capital: Berlín. Fue dividida durante la Guerra Fría.",
    "berlin":    "Capital de Alemania. Ciudad dividida por el Muro hasta 1989.",
    "puerta":    "Puerta de Brandeburgo: ícono de Berlín. Símbolo de la reunificación.",
    "moscu":     "Capital de Rusia. Hogar del Kremlin y la Plaza Roja.",
    "moscova":   "Variante del nombre de Moscú. Capital de la Federación Rusa.",
    "rusia":     "Federación de Rusia. País más grande del mundo.",
    "kremlin":   "Fortaleza en el centro de Moscú. Sede del gobierno ruso.",
    "roja":      "Plaza Roja: plaza emblemática de Moscú, junto al Kremlin.",
    "praga":     "Capital de República Checa. 'La ciudad de las cien torres'.",
    "cien":      "Praga es llamada 'la ciudad de las cien torres' por su skyline.",
    "torres":    "Praga: 'ciudad de las cien torres'. Su skyline está lleno de campanarios.",
    "checa":     "República Checa. País europeo central. Capital: Praga.",
    "alquimia":  "Praga tiene fuerte tradición alquímica. El emperador Rodolfo II patrocinó alquimistas.",
    "viena":     "Capital de Austria. Cuna de la música clásica y la ópera.",
    "austria":   "País europeo. Capital: Viena. Centro del Imperio Austrohúngaro.",
    "opera":     "Viena es mundialmente famosa por su ópera. La Ópera Estatal es prestigiosa.",
    "vals":      "El vals vienés: baile originario de Viena. Johann Strauss II, 'rey del vals'.",
    "musica":    "Viena fue hogar de Mozart, Beethoven, Strauss y Haydn.",
    "tokio":     "Capital de Japón. Metrópolis más poblada del mundo: 37 millones.",
    "japon":     "Japón. País insular en Asia del Este. Capital: Tokio.",
    "sol":       "Japón: 'el país del sol naciente' (Nihon). Nombre significa 'origen del sol'.",
    "naciente":  "'Sol naciente': apodo de Japón por su ubicación al este de China.",
    "cenizas":   "Tokio fue reconstruida tras los bombardeos de la Segunda Guerra Mundial.",
    "zurich":    "Ciudad de Suiza. Centro financiero mundial.",
    "suiza":     "Suiza. País famoso por su neutralidad, bancos y chocolates.",
    "banco":     "Zurich es centro bancario global. Finanzas = 15% de su economía.",
    "chocolate": "Suiza y Zurich famosas por chocolates premium: Lindt, Toblerone, Sprüngli.",
    "oro":       "El Franco Suizo fue respaldado por oro hasta 2000.",
    "atenas":    "Capital de Grecia. Cuna de la democracia occidental y la filosofía.",
    "grecia":    "Grecia. País del sureste de Europa. Capital: Atenas.",
    "diosa":     "Atenea: diosa griega de la sabiduría. Patrona de la ciudad de Atenas.",
    "partenon":  "Templo del siglo V a.C. en la Acrópolis de Atenas, dedicado a Atenea.",
    "acropolis": "Colina fortificada de Atenas con el Partenón como templo principal.",
    "colina":    "La Acrópolis es una colina rocosa en el centro de Atenas.",
    "lisboa":    "Capital de Portugal. Ciudad de las siete colinas junto al río Tajo.",
    "portugal":  "Portugal. País europeo ibérico. Capital: Lisboa.",
    "tranvia":   "Tranvía 28 (amarelo) de Lisboa: recorre el barrio histórico por calles estrechas.",
    "amarillo":  "El tranvía amarillo (Tram 28) es símbolo de Lisboa.",
    "poeta":     "Fernando Pessoa, poeta portugués, vivió en Lisboa. Escribió sobre la ciudad.",
    "mapa":      "Pessoa: 'El mapa del mundo no me muestra el lugar donde nací, pues soy de Lisboa'.",
}


def mision_cesar():
    teletipo([
        ("TRANSMISIÓN INTERCEPTADA — AGENTE CIPHER", ROJO_ALERTA),
        ("", FOSF_DIM),
        ("La rueda te dará un mensaje descifrado, pero NO la respuesta directa.", BLANCO),
        ("El mensaje es un ACERTIJO. Deduce la ciudad antes de que sea tarde.", FOSF_VERDE),
        ("Usa la TERMINAL DE INTELIGENCIA — clickeala para escribir, buscá con el botón.", CYAN_SCAN),
        ("Clickea la casilla de RESPUESTA para escribir tu respuesta final.", AMBER),
    ])
    briefing_mision(1, "EL CÓDIGO DEL TOPO", [
        "Paso 1: Usa la rueda para descifrar el mensaje.",
        "Paso 2: Lee el acertijo — busca pistas clave.",
        "Paso 3: CLIC en la terminal → escribe y busca (3 búsquedas).",
        "Paso 4: CLIC en 'RESPUESTA FINAL' → escribe la ciudad → verificar.",
    ], FOSF_VERDE, 55)

    banco = [
        ("BERLIN",   "Donde un muro cayó sin tocar el suelo, dividiendo hermanos por 28 años de silencio"),
        ("MOSCOVA",  "Un ojo rojo vigila desde la torre centinela. Su plaza más famosa guarda un centauro de bronce y un mausoleo de cristal"),
        ("PRAGA",    "Cien torres miran al cielo sobre un puente viejo donde alquimistas buscaron la piedra filosofal"),
        ("VIENA",    "Donde reyes danzaron al compás de un vals eterno y una ópera de mármil sigue resonando cada noche"),
        ("TOKIO",    "Del sol naciente surgió esta ciudad de acero, que renació de las cenizas como un fénix que no olvida"),
        ("ZURICH",   "Bancos que guardan más secretos que personas, y un dulce que vale más que su peso en oro puro"),
        ("ATENAS",   "Una diosa sabia vigila desde una colina fortificada donde un templo perfecto cuenta historias de tres mil años"),
        ("LISBOA",   "Un tranvía amarillo sube colinas empinadas donde un poeta perdió el mapa del mundo"),
    ]
    ciudad, acertijo = random.choice(banco)
    k = random.randint(3, 15)
    mensaje_cifrado = cesar(acertijo, k)

    # ── Estado ──
    texto_terminal = ""
    texto_respuesta = ""
    foco = "terminal"       # "terminal" o "respuesta"
    vidas = 3
    busquedas = 3
    msg_ret = ""
    col_msg = BLANCO
    resuelto = False
    TMAX = 55.0
    t_ini = time.time()
    pista_usada = False
    t_mision = 0.0
    rueda = RuedaCesar(ANCHO - 145, 310, 88)

    terminal_resultado = ""
    terminal_col = FOSF_DIM
    terminal_mostrar = False
    terminal_timer = 0.0
    acertijo_descifrado = False

    aria.decir("Descifra con la rueda. El resultado es un ACERTIJO, no la respuesta.", CYAN_SCAN, 0.5)
    aria.decir("CLIC en la terminal para buscar, CLIC en respuesta para escribir la ciudad.", AMBER, 5)
    aria.decir("Tenés 3 búsquedas. No las desperdicies.", ROJO_ALERTA, 10)

    # ── Bucle principal ──
    while True:
        dt = reloj.tick(60) / 1000.0
        tt = time.time()
        t_rest = max(0, TMAX - (tt - t_ini)) if not resuelto else TMAX
        mouse = pygame.mouse.get_pos()
        sfx.update(dt)
        rueda.update()

        if terminal_mostrar and terminal_timer > 0:
            terminal_timer -= dt
            if terminal_timer <= 0:
                terminal_mostrar = False

        # ── Fondo con shake ──
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
        panel(20 + ox, 68 + oy, ANCHO - 310, 85,
              col=(0, 20, 8), borde=ROJO_ALERTA, radio=6)
        txt("◉ TRANSMISIÓN INTERCEPTADA (cifrada):", F_SMALL, ROJO_ALERTA,
            35 + ox, 73 + oy)
        pygame.draw.line(pantalla, ROJO_ALERTA,
                         (35 + ox, 90 + oy), (ANCHO - 300 + ox, 90 + oy), 1)
        scan_char = int((tt * 15) % len(mensaje_cifrado))
        msg_disp = ""
        for i, c in enumerate(mensaje_cifrado):
            if i == scan_char and not acertijo_descifrado:
                msg_disp += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            else:
                msg_disp += c
        txt(msg_disp, F_TINY, AMBER, 35 + ox, 95 + oy)

        # ── Barra de tiempo ──
        panel(20 + ox, 160 + oy, ANCHO - 310, 38,
              borde=FOSF_DIM, radio=4)
        txt("TIEMPO:", F_MICRO, ROJO_ALERTA, 35 + ox, 164 + oy)
        barra_tiempo(95 + ox, 178 + oy, ANCHO - 370, 12, t_rest, TMAX)

        if t_rest <= 0 and not resuelto:
            vidas = 0; resuelto = True; t_mision = TMAX
            msg_ret = f"TIEMPO AGOTADO. La ciudad era: {ciudad}"
            col_msg = ROJO_ALERTA; agente.fallo()
            sfx.shake(12, 0.5); sfx.flash(ROJO_ALERTA, 0.3)
            sfx.glitch(0.8); boom(ANCHO // 2, ALTO // 2, ROJO_ALERTA, 40)
            play("error")

        # ── RUEDA DE CIFRADO ──
        panel(ANCHO - 290 + ox, 68 + oy, 275, 420,
              col=(5, 15, 5), borde=FOSF_VERDE, radio=6)
        txt("◈ RUEDA DE CIFRADO CÉSAR", F_TINY, FOSF_VERDE,
            ANCHO - 278 + ox, 74 + oy)
        rueda.cx = ANCHO - 153 + ox
        rueda.cy = 215 + oy
        rueda.draw(palabra_cifrada=mensaje_cifrado[:20], mouse=mouse)

        btn_up = boton("▲", ANCHO - 173 + ox, 320 + ox, 40, 26,
                       (0, 50, 15), (0, 100, 30), mouse, F_SMALL,
                       enabled=not resuelto)
        btn_dn = boton("▼", ANCHO - 173 + ox, 350 + ox, 40, 26,
                       (0, 50, 15), (0, 100, 30), mouse, F_SMALL,
                       enabled=not resuelto)

        k_actual = int(round(rueda.desplazamiento)) % 26
        desc_rueda = desc_cesar(mensaje_cifrado, k_actual)
        es_correcto_k = (k_actual == k)

        if es_correcto_k and not acertijo_descifrado:
            acertijo_descifrado = True
            sfx.flash(FOSF_VERDE, 0.15); play("ok")
            aria.decir("¡K encontrado! Lee el acertijo con atención.", FOSF_VERDE)

        col_desc = FOSF_VERDE if es_correcto_k else FOSF_DIM
        preview_lines = []
        linea = ""
        for p in desc_rueda.split():
            prueba = (linea + " " + p).strip()
            if F_TINY.size(prueba)[0] < 245:
                linea = prueba
            else:
                preview_lines.append(linea); linea = p
        if linea:
            preview_lines.append(linea)
        py_preview = 380 + oy
        for i, pl in enumerate(preview_lines[:4]):
            txt(pl, F_TINY, col_desc, ANCHO - 278 + ox, py_preview + i * 14)

        if es_correcto_k:
            txt("✓ K CORRECTO — ACERTIJO REVELADO", F_TINY, FOSF_VERDE,
                ANCHO - 153 + ox, 450 + oy, centro=True)
        else:
            txt(f"K={k_actual:02d} — Ajustando...", F_TINY, FOSF_DARK,
                ANCHO - 153 + ox, 450 + oy, centro=True)

        # ── PANEL CENTRAL ──
        pc_y = 208 + oy
        panel(20 + ox, pc_y, ANCHO - 320, 350,
              col=GRIS_PANEL, borde=FOSF_DIM, radio=4)

        # Sección 1: Acertijo
        txt("◈ ACERTIJO DESCIFRADO:", F_TINY, AMBER, 35 + ox, pc_y + 5)
        if acertijo_descifrado:
            acert_lines = []
            lin_ac = ""
            for p in acertijo.split():
                prueba = (lin_ac + " " + p).strip()
                if F_SMALL.size(prueba)[0] < ANCHO - 360:
                    lin_ac = prueba
                else:
                    acert_lines.append(lin_ac); lin_ac = p
            if lin_ac:
                acert_lines.append(lin_ac)
            for i, al in enumerate(acert_lines[:3]):
                txt(al, F_SMALL, BLANCO, 35 + ox, pc_y + 22 + i * 20)
        else:
            txt("[ Descifra con la rueda para revelar el acertijo ]",
                F_SMALL, FOSF_DARK, 35 + ox, pc_y + 24)

        pygame.draw.line(pantalla, FOSF_DIM,
                         (35 + ox, pc_y + 88), (ANCHO - 300 + ox, pc_y + 88), 1)

        # ── Sección 2: Terminal de inteligencia ──
        term_activo = (foco == "terminal" and not resuelto)
        term_borde = CYAN_SCAN if term_activo else FOSF_DIM
        if term_activo:
            # Brillo sutil cuando está activa
            s_brillo = pygame.Surface((ANCHO - 360, 70), pygame.SRCALPHA)
            s_brillo.fill((*CYAN_SCAN, 12))
            pantalla.blit(s_brillo, (35 + ox, pc_y + 92))
        panel(35 + ox, pc_y + 92, ANCHO - 360, 70,
              col=(5, 12, 18), borde=term_borde, radio=4)
        txt(f"◈ TERMINAL DE INTELIGENCIA  [Busquedas: {busquedas}/3]  {'◀ ACTIVA' if term_activo else ''}",
            F_TINY, CYAN_SCAN if term_activo else FOSF_DIM,
            35 + ox, pc_y + 96)
        input_box(texto_terminal, 35 + ox, pc_y + 114,
                  ANCHO - 360, activo=term_activo,
                  placeholder="Clic aquí → escribir palabra clave...")
        btn_buscar = boton("BUSCAR", 35 + ox, pc_y + 156, 100, 26,
                           (10, 25, 40), (20, 60, 90), mouse, F_TINY,
                           icono="▶ ", enabled=not resuelto and busquedas > 0
                                  and len(texto_terminal.strip()) > 0)
        btn_limp_t = boton("LIMPIAR", 145 + ox, pc_y + 156, 90, 26,
                           (30, 20, 20), (60, 40, 40), mouse, F_TINY,
                           enabled=not resuelto)
        btn_pst = boton(f"◈ PISTA (−1 vida)", 245 + ox, pc_y + 156, 155, 26,
                        (50, 40, 0), (100, 80, 0), mouse, F_TINY,
                        enabled=not resuelto and vidas > 1 and not pista_usada)

        # Resultado de búsqueda
        if terminal_mostrar and terminal_resultado:
            res_bg = (0, 15, 10) if terminal_col != ROJO_ALERTA else (25, 0, 0)
            panel(35 + ox, pc_y + 188, ANCHO - 360, 52,
                  col=res_bg, borde=terminal_col, radio=3)
            res_palabras = terminal_resultado.split()
            res_lineas = []
            res_lin = ""
            for p in res_palabras:
                prueba = (res_lin + " " + p).strip()
                if F_TINY.size(prueba)[0] < ANCHO - 385:
                    res_lin = prueba
                else:
                    res_lineas.append(res_lin); res_lin = p
            if res_lin:
                res_lineas.append(res_lin)
            for i, rl in enumerate(res_lineas[:3]):
                txt(rl, F_TINY, terminal_col, 40 + ox, pc_y + 193 + i * 15)

        pygame.draw.line(pantalla, FOSF_DIM,
                         (35 + ox, pc_y + 248), (ANCHO - 300 + ox, pc_y + 248), 1)

        # ── Sección 3: Respuesta final ──
        resp_activo = (foco == "respuesta" and not resuelto)
        resp_borde = FOSF_VERDE if resp_activo else FOSF_DIM
        if resp_activo:
            s_brillo = pygame.Surface((ANCHO - 360, 65), pygame.SRCALPHA)
            s_brillo.fill((*FOSF_VERDE, 12))
            pantalla.blit(s_brillo, (35 + ox, pc_y + 252))
        panel(35 + ox, pc_y + 252, ANCHO - 360, 65,
              col=(5, 15, 5), borde=resp_borde, radio=4)
        txt(f"◉ RESPUESTA FINAL — ¿Qué ciudad es?  {'◀ ACTIVA' if resp_activo else ''}",
            F_TINY, FOSF_VERDE if resp_activo else FOSF_DIM,
            35 + ox, pc_y + 256)
        input_box(texto_respuesta, 35 + ox, pc_y + 274,
                  ANCHO - 360, activo=resp_activo,
                  placeholder="Clic aquí → escribir la ciudad...")
        btn_env = boton("▶ VERIFICAR", 35 + ox, pc_y + 316, 140, 26,
                        (0, 50, 15), (0, 100, 30), mouse, F_TINY,
                        enabled=not resuelto and len(texto_respuesta.strip()) > 0)

        # ── Mensaje de resultado ──
        if msg_ret:
            bg = (0, 35, 12) if col_msg == FOSF_VERDE else (40, 0, 0)
            panel(20 + ox, pc_y + 350, ANCHO - 40, 35,
                  col=bg, borde=col_msg, radio=4)
            txt(msg_ret, F_BOLD, col_msg, ANCHO // 2, pc_y + 358, centro=True)

        if resuelto:
            btn_sig = boton("SIGUIENTE MISIÓN ▶▶",
                            ANCHO // 2 - 110 + ox, ALTO - 55 + oy, 220, 38,
                            (0, 60, 20), (0, 120, 40), mouse)

        # ── Overlays ──
        aria.actualizar(); aria.dibujar()
        indicador_progreso(0); logros.draw(); sfx.draw(); tick_floats()
        pygame.display.flip()

        # ── Buscar en terminal ──
        def buscar_en_terminal():
            nonlocal busquedas, terminal_resultado, terminal_col
            nonlocal terminal_mostrar, terminal_timer, texto_terminal
            query = texto_terminal.strip().lower()
            if not query:
                return
            busquedas -= 1; play("click")
            mejor = None
            for clave, info in BASE_DATOS.items():
                if clave in query or query in clave:
                    mejor = info; break
            if mejor:
                terminal_resultado = f"► RESULTADO: {mejor}"
                terminal_col = FOSF_VERDE; sfx.flash(CYAN_SCAN, 0.1)
            else:
                terminal_resultado = f"✗ SIN RESULTADOS para '{query}'. Busqueda desperdiciada."
                terminal_col = ROJO_ALERTA; sfx.shake(3, 0.15)
            terminal_mostrar = True; terminal_timer = 6.0; texto_terminal = ""
            if busquedas == 0:
                aria.decir("Sin búsquedas. Razona con lo que tienes.", ROJO_ALERTA)
            elif busquedas == 1:
                aria.decir("Última búsqueda. Úsala bien.", AMBER)

        # ── Verificar ──
        def verificar():
            nonlocal vidas, msg_ret, col_msg, resuelto, pista_usada
            nonlocal texto_respuesta, t_mision
            t_mision = tt - t_ini
            if texto_respuesta.upper().strip() == ciudad:
                agente.acierto()
                tb = max(0, (t_rest / TMAX) * 0.5)
                pts = agente.sumar(350, vidas, tb)
                msg_ret = f"✓ CORRECTO: {ciudad} | K={k} | +{pts} pts"
                col_msg = FOSF_VERDE; resuelto = True
                if not pista_usada: logros.intentar("SIN_PISTA")
                if t_mision < 15: logros.intentar("VELOCISTA")
                logros.intentar("CIFRADOR")
                sfx.flash(FOSF_VERDE, 0.2); sfx.shake(4, 0.2)
                boom(ANCHO // 2, 400, FOSF_VERDE, 50); play("ok")
                add_float(f"+{pts}", ANCHO // 2, 350, FOSF_VERDE, 30)
                aria.decir(f"¡{ciudad} confirmada como punto de encuentro!", FOSF_VERDE)
            else:
                vidas -= 1; agente.fallo()
                sfx.shake(8, 0.3); sfx.flash(ROJO_ALERTA, 0.15)
                sfx.glitch(0.4); boom(ANCHO // 2, 400, ROJO_ALERTA, 20); play("error")
                aria.decir("Incorrecto. Relee el acertijo.", ROJO_ALERTA)
                if vidas == 0:
                    t_mision = TMAX
                    msg_ret = f"✗ SIN VIDAS. La ciudad era: {ciudad}"
                    col_msg = ROJO_ALERTA; resuelto = True
                else:
                    msg_ret = f"✗ ERROR. Relee el acertijo. Vidas: {vidas}"
                    col_msg = ROJO_ALERTA; texto_respuesta = ""

        # ── Eventos ──
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return False, t_mision, False
                if not resuelto and vidas > 0:
                    if ev.key == pygame.K_RETURN:
                        if foco == "respuesta":
                            verificar()
                    elif ev.key == pygame.K_BACKSPACE:
                        if foco == "terminal":
                            texto_terminal = texto_terminal[:-1]
                        elif foco == "respuesta":
                            texto_respuesta = texto_respuesta[:-1]
                    elif ev.key == pygame.K_TAB:
                        # Tab cambia foco entre terminal y respuesta
                        foco = "respuesta" if foco == "terminal" else "terminal"
                        play("click")
                    elif ev.unicode.isalpha() or ev.unicode.isspace():
                        if foco == "terminal" and len(texto_terminal) < 20:
                            texto_terminal += ev.unicode.lower(); play("tecla")
                        elif foco == "respuesta" and len(texto_respuesta) < 12:
                            texto_respuesta += ev.unicode.upper(); play("tecla")
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if not resuelto and vidas > 0:
                    if btn_env.collidepoint(ev.pos):
                        verificar()
                    if btn_up.collidepoint(ev.pos):
                        rueda.click_arriba()
                    if btn_dn.collidepoint(ev.pos):
                        rueda.click_abajo()
                    if btn_buscar.collidepoint(ev.pos):
                        if busquedas > 0 and texto_terminal.strip():
                            buscar_en_terminal()
                    if btn_limp_t.collidepoint(ev.pos):
                        texto_terminal = ""; terminal_resultado = ""
                        terminal_mostrar = False; play("beep")
                    if btn_pst.collidepoint(ev.pos):
                        vidas -= 1; pista_usada = True; agente.usar_pista()
                        rueda.set_k(k)
                        msg_ret = f"◈ PISTA: K = {k} (rueda ajustada)"
                        col_msg = AMBER; play("beep")
                    # ── CAMBIAR FOCO AL CLICKEAR EN LOS INPUTS ──
                    # Terminal input area
                    term_rect = pygame.Rect(35 + ox, pc_y + 114, ANCHO - 360, 30)
                    if term_rect.collidepoint(ev.pos):
                        foco = "terminal"; play("click")
                    # Respuesta input area
                    resp_rect = pygame.Rect(35 + ox, pc_y + 274, ANCHO - 360, 30)
                    if resp_rect.collidepoint(ev.pos):
                        foco = "respuesta"; play("click")
                if resuelto:
                    try:
                        if btn_sig.collidepoint(ev.pos):
                            play("mision"); return vidas > 0, t_mision, True
                    except NameError:
                        pass