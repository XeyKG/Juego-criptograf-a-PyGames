# -*- coding: utf-8 -*-
"""
Misión 03 — SHA-256: "Identidad Fantasma"
Con acertijo + perfilador de expedientes + escáner de coincidencias.
"""

import random
import time
import pygame

from config import (
    ANCHO, ALTO, reloj, pantalla,
    FOSF_VERDE, FOSF_DIM, FOSF_DARK, AMBER, ROJO_ALERTA,
    ROJO_DIM, BLANCO, GRIS_PANEL, CYAN_SCAN, MORADO, ORO,
    F_BOLD, F_SMALL, F_TINY, F_MICRO,
)
from criptografia import sha256
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
from componentes.hash_calc import HashCalc
from escenas.teletipo import teletipo, briefing_mision


# ═══════════════════════════════════════════════════════════════════════════════
#  BASE DE DATOS: Expedientes de sospechosos
# ═══════════════════════════════════════════════════════════════════════════════
SOSPECHOSOS_DATA = {
    "MORGAN": {
        "hash_palabra": "morgan",
        "expediente": {
            "cargo": "Técnico de Comunicaciones — Nivel 4",
            "lugar": "Oficina Central — Praga",
            "antiguedad": "12 años en la agencia",
            "idiomas": "Checo nativo, inglés fluido, ruso básico",
            "ultimo_movimiento": "Viajó a Praga hace 3 días. Visto en el puente de Carlos al anochecer.",
            "nota_archivo": "Sin registros disciplinarios. Evaluación de rendimiento: sobresaliente.",
        },
        "expandido": [
            "Paseos frecuentes por el río Moldava. Aficionado a la fotografía nocturna.",
            "Acceso a la sala de comunicaciones sin autorización los domingos.",
            "Tiene contactos no documentados en la región de Bohemia.",
        ],
    },
    "REEVES": {
        "hash_palabra": "reeves",
        "expediente": {
            "cargo": "Analista de Inteligencia — Nivel 5",
            "lugar": "Sede Operativa — Berlín",
            "antiguedad": "8 años en la agencia",
            "idiomas": "Alemán nativo, inglés, francés",
            "ultimo_movimiento": "Transferido a Berlín hace 1 semana. Trabajó en la Puerta de Brandeburgo.",
            "nota_archivo": "Promovido recientemente. Tiene acceso a archivos clasificados de la Operación.",
        },
        "expandido": [
            "Especialista en redes de comunicación alemanas. Conoce la infraestructura de Berlín.",
            "Fue promovido inusualmente rápido — posiblemente sin mérito suficiente.",
            "Últimamente pidió acceso a archivos que no le correspondían.",
        ],
    },
    "CARVER": {
        "hash_palabra": "carver",
        "expediente": {
            "cargo": "Agente de Campo — Nivel 3",
            "lugar": "Base de campo — Viena",
            "antiguedad": "6 años en la agencia",
            "idiomas": "Alemán, inglés básico",
            "ultimo_movimiento": "Estacionado en Viena hace 2 semanas. Reporta actividad operacional normal.",
            "nota_archivo": "Desempeño promedio. Sin señales de actividad irregular.",
        },
        "expandido": [
            "Reporta desde una cafetería cerca de la ópera de Viena. Observación rutinaria.",
            "Su rutina es tan normal que podría ser una tapadera perfecta para operaciones encubiertas.",
            "No tiene acceso a redes de comunicación clasificadas desde su nivel.",
        ],
    },
    "BISHOP": {
        "hash_palabra": "bishop",
        "expediente": {
            "cargo": "Director Adjunto de Operaciones — Nivel 6",
            "lugar": "Sede Central — Moscú (temporal)",
            "antiguedad": "15 años en la agencia",
            "idiomas": "Ruso nativo, inglés, español",
            "ultimo_movimiento": "Llegó a Moscú hace 5 días para una reunión clasificada de alto nivel.",
            "nota_archivo": "Tiene acceso total a operaciones de alto secreto. Confianza absoluta del Director.",
        },
        "expandido": [
            "Reunión clasificada en Moscú coincidente con periodo de máxima alerta KRONOS.",
            "Su posición de alto nivel le permite operar sin supervisión. Nadie lo cuestiona.",
            "Ha sido evaluado 3 veces por contra-inteligencia. Siempre limpio.",
        ],
    },
    "HOLDEN": {
        "hash_palabra": "holden",
        "expediente": {
            "cargo": "Oficial de Seguridad — Nivel 2",
            "lugar": "Posta Perimetral — Tokio",
            "antiguedad": "3 años en la agencia",
            "idiomas": "Japonés nativo, inglés básico",
            "ultimo_movimiento": "Cumplió turno de guardia nocturno en la puerta este. Nada que reportar.",
            "nota_archivo": "Cero acceso a información clasificada. Turnos rutinarios sin incidentes.",
        },
        "expandido": [
            "Su rutina es tan normal que es invisible. Nadie lo nota ni lo cuestiona.",
            "Trabaja la puerta este de Tokio — punto de entrada menos vigilado.",
            "No tiene acceso a archivos pero conoce los horarios de todos los guardias.",
        ],
    },
    "PIERCE": {
        "hash_palabra": "pierce",
        "expediente": {
            "cargo": "Ingeniero de Sistemas — Contratista",
            "lugar": "Data Center — Zúrich",
            "antiguedad": "2 años (contratista)",
            "idiomas": "Inglés, alemán, suizo alemán",
            "ultimo_movimiento": "Instaló actualización de seguridad en los servidores principales hace 4 días.",
            "nota_archivo": "CONTRATISTA — No es empleado oficial. Sin antecedentes verificables antes de 2023.",
        },
        "expandido": [
            "Contratista reciente. No pasó verificación de contra-inteligencia completa.",
            "La actualización que instaló abrió un canal secundario no autorizado en los servidores.",
            "Tiene acceso root a TODOS los sistemas de la agencia en Zúrich.",
        ],
    },
    "LARKIN": {
        "hash_palabra": "larkin",
        "expediente": {
            "cargo": "Coordinador de Logística — Nivel 4",
            "lugar": "Almacén Regional — Lisboa",
            "antiguedad": "9 años en la agencia",
            "idiomas": "Portugués nativo, español, inglés",
            "ultimo_movimiento": "Organizó envío urgente a destino desconocido hace 6 días.",
            "nota_archivo": "Controla todas las rutas de suministro. Conoce horarios y destinos de todas las operaciones.",
        },
        "expandido": [
            "El envío urgente de hace 6 días tenía destino no registrado en el sistema oficial.",
            "Conoce todas las rutas de suministro — podría haber desviado cargos sin dejar rastro.",
            "Su red de contactos en Lisboa es extensa y no documentada completamente.",
        ],
    },
    "WESTON": {
        "hash_palabra": "weston",
        "expediente": {
            "cargo": "Cryptoanalista Senior — Nivel 5",
            "lugar": "Búnker de Cifrado — Atenas",
            "antiguedad": "11 años en la agencia",
            "idiomas": "Griego, inglés, alemán técnico",
            "ultimo_movimiento": "Trabajó en el búnker de cifrado durante 72 horas seguidas. Sin contacto externo.",
            "nota_archivo": "Único con acceso a los protocolos de cifrado originales de la agencia.",
        },
        "expandido": {
            "72 horas sin contacto externo — suficientes para copiar o transmitir documentos cifrados.",
            "Trabaja en un búnker donde nadie puede observarlo. Ubicación secreta.",
            "Es el único que conoce los algoritmos de cifrado originales de la agencia.",
        },
    },
    "CALLUM": {
        "hash_palabra": "callum",
        "expediente": {
            "cargo": "Piloto de Transporte — Nivel 3",
            "lugar": "Hangar Militar — Lisboa (temporal)",
            "antiguedad": "5 años en la agencia",
            "idiomas": "Inglés, portugués básico",
            "ultimo_movimiento": "Solicitó permiso para vuelo no programado hace 10 días. Denegado.",
            "nota_archivo": "Solicitud de vuelo no programado denegada. Motivo: 'sin autorización superior'.",
        },
        "expandido": [
            "Intentó un vuelo no autorizado — posiblemente para extraer algo o a alguien.",
            "Su solicitud fue denegada por alguien con 'autorización superior'. ¿Quién lo protege?",
            "Tiene acceso al hangar militar temporal. El vuelo denegado era hacia el extranjero.",
        ],
    },
    "DECKER": {
        "hash_palabra": "decker",
        "expediente": {
            "cargo": "Diplomático de Enlace — Agencia Externa",
            "lugar": "Embajada — París (sede permanente)",
            "antiguedad": "7 años en enlace diplomático",
            "idiomas": "Francés nativo, inglés, español, italiano, alemán",
            "ultimo_movimiento": "Reunión con contacto no identificado en café parisino. Grabado por CCTV.",
            "nota_archivo": "Sede en París pero viaja constantemente. La reunión grabada fue clasificada y borrada del CCTV.",
        },
        "expandido": [
            "Reunión en café parisino grabada por CCTV — grabación clasificada y luego borrada. ¿Por qué?",
            "Viaja constantemente entre capitales europeas. Rutas no rastreables oficialmente.",
            "Como diplomático tiene inmunidad — sus movimientos nunca son registrados por seguridad interna.",
        ],
    },
}

# Acertijos para cada sospechoso
ACERTIJOS = {
    "MORGAN":  "El fantasma del río Moldava camina entre sombras con un micrófono oculto, fotografiando lo que no debería ser visto",
    "REEVES":  "El alpinista de Brandeburgo ascendió demasiado rápido y ahora tiene las llaves de algo que no debería abrir",
    "CARVER":  "El invisible que observa óperas desde una cafetería vienesa — su rutina perfecta es su mejor disfraz",
    "BISHOP":  "El visitante temporal de Moscú fue recibido sin preguntas — nadie cuestiona al que llega con una orden del Director",
    "HOLDEN": "El guardia de la puerta este de Tokio sabe cuándo duerme sus compañeros y eligió el momento perfecto",
    "PIERCE": "El técnico externo instaló una puerta trasera en todos los servidores — sin que nadie lo notara",
    "LARKIN": "El logista de Lisboa envió un paquete a la nada — pero las rutas que conoce podrían llevar algo a algún lado",
    "WESTON": "El ermita del búnker de Atenas desapareció 72 horas con los secretos de todos — working from home",
    "CALLUM": "El piloto cuyo vuelo fue denegado tiene un protector en la sombra que bloqueó la investigación",
    "DECKER": "El diplomático de París fue grabado por cámaras que luego fueron borradas — alguien con poder lo protege",
}


def mision_hash():
    teletipo([
        ("ALERTA MÁXIMA — INFILTRADO EN LA AGENCIA", ROJO_ALERTA),
        ("", FOSF_DIM),
        ("Solo tienes un hash SHA-256 y un ACERTIJO sobre el infiltrado.", BLANCO),
        ("Usa el PERFILADOR DE EXPEDIENTES: cada sospechoso tiene datos de fondo valiosos.", FOSF_VERDE),
        ("El ESCÁNER compara tu texto con los 4 hashes a la vez — sin revelar cuál es.", CYAN_SCAN),
    ])
    briefing_mision(3, "IDENTIDAD FANTASMA", [
        "Paso 1: Lee el acertijo sobre el infiltrado con atención.",
        "Paso 2: CLIC en cada sospechoso para ver su expediente y datos de fondo.",
        "Paso 3: Usa la calculadora para verificar hashes. El escáner te indica coincidencias.",
        "Paso 4: Selecciona al infiltrado y acusa.",
    ], AMBER, 60)

    # ── Seleccionar 4 sospechosos (no siempre el mismo culpable para variedad) ──
    nombres = list(SOSPECHOSOS_DATA.keys())
    culpable = random.choice(nombres)
    otros = [n for n in nombres if n != culpable]
    random.shuffle(otros)
    opciones = [culpable] + otros[:3]
    random.shuffle(opciones)

    hash_real = sha256(culpable)
    acertijo = ACERTIJOS[culpable]

    # Preparar datos de los sospechosos
    sospechosos_info = []
    for nom in opciones:
        datos = SOSPECHOSOS_DATA[nom]
        exp = datos["expediente"]
        expandido = datos["expandido"]
        sospechosos_info.append({
            "nombre": nom,
            "hash": sha256(nom),
            "expediente": exp,
            "expandido": expandido,
            "es_culpable": (nom == culpable),
        })

    # ── Estado ──
    texto_calc = ""
    foco = "expedientes"  # "expedientes", "calculadora"
    seleccionado = -1
    vidas = 3
    breach_level = 0
    msg_ret = ""
    col_msg = BLANCO
    resuelto = False
    TMAX = 60.0
    t_ini = time.time()
    t_mision = 0.0
    pista_usada = False
    expandido_abierto = -1  # índice del expediente expandido abierto, -1 = ninguno
    escaner_resultados = []  # lista de (índice, coincide) del último escaneo

    # Calculadora
    calc = HashCalc(20, 0, 0, 0)
    calc.activo = False

    aria.decir("CLIC en los expedientes para leer sus datos de fondo. Busca pistas en el acertijo.", CYAN_SCAN, 0.5)
    aria.decir("El escáner compara tu texto con los 4 hashes sin decirte cuál coincide.", AMBER, 5)
    aria.decir("Usa la calculadora solo si necesitas verificar algo específico.", FOSF_DIM, 10)

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

        # ── Huella digital objetivo + Acertijo ──
        panel(20, 68, ANCHO - 40, 95,
              col=(25, 15, 0), borde=ROJO_ALERTA, radio=6)
        txt("◉ HUELLA DEL INFILTRADO — SHA-256:", F_SMALL, ROJO_ALERTA, 35, 73)
        pygame.draw.line(pantalla, ROJO_ALERTA, (35, 90), (ANCHO - 50, 90), 1)
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

        # Acertijo debajo del hash
        txt(f"◈ ACERTIJO DEL INFILTRADO:", F_TINY, AMBER, 35, 138)
        # Word-wrap del acertijo
        ac_lines = []
        lin = ""
        for p in acertijo.split():
            prueba = (lin + " " + p).strip()
            if F_SMALL.size(prueba)[0] < ANCHO - 70:
                lin = prueba
            else:
                ac_lines.append(lin); lin = p
        if lin:
            ac_lines.append(lin)
        for i, al in enumerate(ac_lines[:2]):
            txt(al, F_SMALL, BLANCO, 35, 155 + i * 18)

        # ── Barra de tiempo ──
        panel(20, 198, ANCHO - 40, 32, borde=FOSF_DIM, radio=4)
        txt("INFILTRADO HUYE EN:", F_MICRO, ROJO_ALERTA, 35, 202)
        barra_tiempo(180, 206, ANCHO - 230, 12, t_rest, TMAX)

        if t_rest <= 0 and not resuelto:
            vidas = 0; resuelto = True; t_mision = TMAX
            msg_ret = f"SE FUGÓ. Infiltrado: {culpable}"
            col_msg = ROJO_ALERTA; agente.fallo()
            sfx.shake(12, 0.5); sfx.flash(ROJO_ALERTA, 0.3)
            boom(ANCHO // 2, ALTO // 2, ROJO_ALERTA, 50); play("alerta")

        # ════════════════════════════════════════════════════════════════════
        #  EXPEDIENTES DE SOSPECHOSOS (2x2 grid clickeable)
        # ════════════════════════════════════════════════════════════════════
        panel(20, 238, ANCHO - 300, 330,
              col=GRIS_PANEL, borde=AMBER, radio=6)

        txt("◈ PERFILADOR DE SOSPECHOSOS — CLIC para ver expediente:",
            F_TINY, AMBER, 35, 242)
        txt("Clickea cada sospechoso para investigar su expediente completo.",
            F_TINY, FOSF_DIM, 35, 258)

        botones_sosp = []
        for i, sosp in enumerate(sospechosos_info):
            bx = 28 + (i % 2) * ((ANCHO - 320) // 2)
            by = 275 + (i // 2) * 155

            es_sel = (i == seleccionado)
            es_culp = sosp["es_culpable"]

            # Feedback visual si la calculadora coincide
            calc_coincide = (calc.texto.upper() == sosp["nombre"])
            escaner_coincide = any(idx == i for idx, c in escaner_resultados if c)

            if es_sel:
                bord = ORO
                bg = (30, 20, 0) if es_culp else (20, 15, 0)
            elif es_culp and (calc_coincide or escaner_coincide):
                bord = AMBER
                bg = (20, 15, 0)
            elif hov_rect := pygame.Rect(bx, by, (ANCHO - 320) // 2 - 4, 145).collidepoint(mouse):
                bord = FOSF_VERDE
                bg = (10, 25, 10)
            else:
                bord = FOSF_DIM
                bg = GRIS_PANEL

            exp = sosp["expediente"]
            panel(bx, by, (ANCHO - 320) // 2 - 4, 145, col=bg, borde=bord, radio=5)

            # Nombre y hash mini
            hash_mini = sosp["hash"][:16] + "..."
            sel_icon = "▶ " if es_sel else ""
            txt(f"{sel_icon}{sosp['nombre']}", F_BOLD,
                AMBER if es_sel else BLANCO, bx + 8, by + 6)
            txt(f"SHA: {hash_mini}", F_TINY, FOSF_DIM, bx + 8, by + 26)

            # Datos básicos del expediente (siempre visibles)
            txt(f"Cargo: {exp['cargo']}", F_TINY, FOSF_DIM, bx + 8, by + 42)
            txt(f"Lugar: {exp['lugar']}", F_TINY, FOSF_DIM, bx + 8, by + 56)
            txt(f"Antigüedad: {exp['antiguedad']}", F_TINY, FOSF_DIM, bx + 8, by + 70)

            # Indicadores de coincidencia
            indicadores = ""
            if calc_coincide:
                indicadores += " [HASH ✓]"
            if escaner_coincide and not calc_coincide:
                indicadores += " [SCAN ✓]"
            if es_culp and (calc_coincide or escaner_coincide):
                indicadores += " [¡ALTO!]"

            if indicadores:
                ind_col = ROJO_ALERTA if es_culp else CYAN_SCAN
                txt(indicadores, F_TINY, ind_col, bx + 8, by + 86)

            botones_sosp.append(pygame.Rect(bx, by, (ANCHO - 320) // 2 - 4, 145))

        # ── Panel expandido expandido (si hay uno abierto) ──
        if expandido_abierto >= 0:
            sosp_exp = sospechosos_info[expandido_abierto]
            exp_d = sosp["expandido"]
            ex = ANCHO - 270
            ey = 578
            panel(ex, ey, 248, 55, col=(5, 15, 5), borde=ROJO_ALERTA, radio=4)
            txt("◈ INFORME CONFIDENCIAL — ACCESO RESTRINGIDO:", F_TINY, ROJO_ALERTA, ex + 8, ey + 4)
            for j, linea in enumerate(exp_d[:3]):
                txt(linea, F_TINY, AMBER, ex + 8, ey + 18 + j * 14)
            # Botón cerrar
            btn_cerrar = boton("CERRAR", ex + 168, ey + 18, 65, 22,
                                (40, 10, 10), (80, 20, 20), mouse, F_TINY,
                                enabled=not resuelto)
        else:
            btn_cerrar = None

        # ── Botón de captura ──
        btn_capturar = None

        # ════════════════════════════════════════════════════════════════════
        #  PANEL DERECHO: Calculadora + Escáner
        # ════════════════════════════════════════════════════════════════════
        cx = ANCHO - 270
        cw = 248

        panel(cx, 68, cw, 195,
              col=(15, 10, 0), borde=MORADO, radio=6)
        txt("◈ HERRAMIENTAS DE ANÁLISIS:", F_TINY, MORADO, cx + 8, 72)

        # Sección: Calculadora de hash
        calc_activo = (foco == "calculadora" and not resuelto)
        calc_borde = FOSF_VERDE if calc_activo else FOSF_DIM
        if calc_activo:
            s_br = pygame.Surface((cw - 16, 65), pygame.SRCALPHA)
            s_br.fill((*FOSF_VERDE, 15))
            pantalla.blit(s_br, (cx + 4, 90))
        panel(cx + 4, 90, cw - 8, 65, col=(10, 18, 8), borde=calc_borde, radio=4)
        txt("◉ CALCULADORA SHA-256  {'◀ ACTIVA' if calc_activo else ''}",
            F_TINY, calc_borde, cx + 8, 94)
        input_box(texto_calc, cx + 8, 112, cw - 16,
                  activo=calc_activo,
                  placeholder="Clic aquí → escribir nombre...")
        calc.draw(target_hash="", mouse=mouse)
        btn_verif_h = boton("VERIFICAR", cx + 8, 152, cw - 16, 24,
                             (10, 25, 40), (20, 60, 90), mouse, F_TINY,
                             enabled=not resuelto and len(texto_calc.strip()) > 0)

        # Sección: Escáner de coincidencias
        panel(cx + 4, 265, cw - 8, 100, col=(10, 15, 25), borde=CYAN_SCAN, radio=4)
        txt("◉ ESCÁNER DE COINCIDENCIAS:",
            F_TINY, CYAN_SCAN, cx + 8, 269)
        txt("Compara tu texto con los 4 hashes simultáneamente.",
            F_TINY, FOSF_DIM, cx + 8, 287)

        btn_escanear = boton("◈ ESCANEAR TODO", cx + 8, 308, cw - 16, 26,
                            (10, 25, 40), (20, 60, 90), mouse, F_TINY,
                            enabled=not resuelto and len(texto_calc.strip()) > 0 and breach_level < 2)

        if breach_level >= 2:
            txt("⚠ ESCÁNER DESHABILITADO — BRECHA DE SEGURIDAD ALTA", F_TINY, ROJO_ALERTA, cx + 8, 340)

        # Resultados del escáner
        if escaner_resultados:
            txt("RESULTADO DEL ESCÁNER:", F_TINY, CYAN_SCAN, cx + 8, 340)
            for idx, coincide in escaner_resultados:
                col_r = FOSF_VERDE if coincide else ROJO_DIM
                icon = "✓ COINCIDE" if coincide else "✗ no coincide"
                txt(f"  {sospechosos_info[idx]['nombre']}: {icon}",
                    F_TINY, col_r, cx + 8, 356)
            txt("(No revela cuál es el hash objetivo — solo indica coincidencias)",
                F_TINY, FOSF_DIM, cx + 8, 374)

        # Nota sobre la calculadora
        txt("NOTA: La calculadora muestra el hash completo.",
            F_TINY, FOSF_DARK, cx + 8, 392)

        # ── Botones de acción ──
        btn_acu = boton(
            "▶ ACUSAR SELECCIONADO", cx + 8, 410, 180, 30,
            (60, 30, 0), (120, 60, 0), mouse, F_SMALL,
            enabled=not resuelto and seleccionado >= 0,
        )
        btn_pst = boton(
            "◈ PISTA (−1 vida)", cx + 8, 450, 180, 30,
            (50, 40, 0), (100, 80, 0), mouse, F_SMALL,
            enabled=not resuelto and vidas > 1 and not pista_usada,
        )
        btn_limp_c = boton(
            "LIMPIAR", cx + 8, 490, 100, 26,
            (20, 25, 20), (50, 50, 50), mouse, F_TINY, enabled=not resuelto,
        )

        # ── Mensaje de resultado ──
        if msg_ret:
            bg = (0, 35, 12) if col_msg == FOSF_VERDE else (40, 0, 0)
            panel(20, 590, ANCHO - 40, 30, col=bg, borde=col_msg, radio=4)
            txt(msg_ret, F_BOLD, col_msg, ANCHO // 2, 598, centro=True)

        if resuelto:
            btn_sig = boton("SIGUIENTE MISIÓN ▶▶",
                            ANCHO // 2 - 110, ALTO - 55, 220, 38,
                            (0, 60, 20), (0, 120, 40), mouse)

        # ── Overlay de brecha de seguridad ──
        if breach_level > 0 and not resuelto:
            alpha = 50 + breach_level * 40
            s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            s.fill((*ROJO_ALERTA, alpha))
            pantalla.blit(s, (0, 0))
            txt(f"⚠ BRECHA DE SEGURIDAD NIVEL {breach_level}/3", F_BOLD, ROJO_ALERTA,
                ANCHO // 2, 50, centro=True)

        # ── Overlays ──
        aria.actualizar(); aria.dibujar()
        indicador_progreso(2); logros.draw(); sfx.draw(); tick_floats()
        pygame.display.flip()

        # ── Abrir expediente expandido ──
        def abrir_expandido(idx):
            nonlocal expandido_abierto
            if expandido_abierto == idx:
                expandido_abierto = -1  # toggle
                play("beep")
            else:
                expandido_abierto = idx
                play("click")
                aria.decir(f"Acceso a informe confidencial del sospechoso #{idx+1}. Lectura con cuidado.", ROJO_ALERTA)

        # ── Verificar hash manual ──
        def verificar_hash():
            nonlocal msg_ret, col_msg
            nombre = texto_calc.upper().strip()
            if nombre in [s["nombre"] for s in sospechosos_info]:
                s = [s for s in sospechosos_info if s["nombre"] == nombre][0]
                h = s["hash"]
                msg_ret = f"SHA-256({nombre}) = {h[:32]}..."
                col_msg = CYAN_SCAN
            else:
                msg_ret = f"No se encuentra expediente para '{nombre}'"
                col_msg = ROJO_DIM

        # ── Escanear coincidencias ──
        def escanear_todo():
            nonlocal escaner_resultados
            query = texto_calc.strip().upper()
            if not query:
                return
            play("click")
            resultados = []
            for i, s in enumerate(sospechosos_info):
                coincide = (query in s["nombre"]
                           or query == s["nombre"]
                           or (len(query) >= 3 and query in s["expediente"]["cargo"].upper()))
            resultados.append((i, coincide))
            escaner_resultados = resultados
            if any(c for _, c in resultados):
                aria.decir("¡Coincidencia detectada! Investiga a esos sospechosos.", CYAN_SCAN)
            else:
                aria.decir("Sin coincidencias. Prueba con otra palabra.", FOSF_DIM)

        # ── Acusar ──
        def acusar():
            nonlocal vidas, msg_ret, col_msg, resuelto, t_mision, seleccionado, breach_level
            t_mision = tt - t_ini
            if seleccionado >= 0 and sospechosos_info[seleccionado]["es_culpable"]:
                agente.acierto()
                tb = max(0, (t_rest / TMAX) * 0.5)
                pts = agente.sumar(450, vidas, tb)
                msg_ret = (f"✓ INFILTRADO IDENTIFICADO: {culpable} "
                           f"| +{pts} pts")
                col_msg = FOSF_VERDE; resuelto = True
                logros.intentar("HUELLA")
                if t_mision < 20: logros.intentar("VELOCISTA")
                sfx.flash(FOSF_VERDE, 0.3); sfx.shake(6, 0.3)
                boom(ANCHO // 2, 400, FOSF_VERDE, 60); play("ok")
                add_float(f"+{pts}", ANCHO // 2, 560, FOSF_VERDE, 32)
                add_float("INFILTRADO DETENIDO", ANCHO // 2, 530, ORO, 20, 3)
                aria.decir(f"¡{culpable} arrestado! Operación exitosa.", FOSF_VERDE)
            else:
                vidas -= 1; agente.fallo()
                breach_level += 1
                sfx.shake(10, 0.4); sfx.flash(ROJO_ALERTA, 0.2)
                sfx.glitch(0.5); boom(ANCHO // 2, 400, ROJO_ALERTA, 30); play("error")
                if breach_level >= 3:
                    t_mision = TMAX
                    msg_ret = f"✗ BRECHA DE SEGURIDAD CRÍTICA. Sistema comprometido. Era: {culpable}"
                    col_msg = ROJO_ALERTA; resuelto = True
                    aria.decir("¡Brecha crítica! El infiltrado ha escapado.", ROJO_ALERTA)
                elif vidas == 0:
                    t_mision = TMAX
                    msg_ret = f"✗ AGENTE INOCENTE LIBERADO. Era: {culpable}"
                    col_msg = ROJO_ALERTA; resuelto = True
                else:
                    msg_ret = f"✗ INCORRECTO. Nivel de brecha: {breach_level}/3. Vidas: {vidas}"
                    col_msg = ROJO_ALERTA; seleccionado = -1
                    expandido_abierto = -1
                    aria.decir("Brecha de seguridad detectada. Sé más cuidadoso.", ROJO_ALERTA)

        # ── Eventos ──
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return False, t_mision, False
                if not resuelto and vidas > 0:
                    if ev.key == pygame.K_RETURN:
                        if foco == "calculadora" and texto_calc.strip():
                            verificar_hash()
                        elif foco == "expedientes" and seleccionado >= 0:
                            acusar()
                    elif ev.key == pygame.K_BACKSPACE:
                        if foco == "calculadora":
                            texto_calc = texto_calc[:-1]
                    elif ev.unicode.isalpha() and len(texto_calc) < 12:
                        if foco == "calculadora":
                            texto_calc += ev.unicode.upper(); play("tecla")
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if not resuelto and vidas > 0:
                    # Seleccionar sospechoso
                    for i, rect in enumerate(botones_sosp):
                        if rect.collidepoint(ev.pos):
                            seleccionado = i; expandido_abierto = -1
                            play("click")
                            # Si el expandido estaba abierto de otro, cerrarlo
                    # Botones de herramientas
                    if btn_verif_h.collidepoint(ev.pos):
                        if foco == "calculadora" and texto_calc.strip():
                            verificar_hash()
                    if btn_escanear.collidepoint(ev.pos):
                        if foco == "calculadora" and texto_calc.strip():
                            escanear_todo()
                    if btn_pst.collidepoint(ev.pos):
                        vidas -= 1; pista_usada = True; agente.usar_pista()
                        msg_ret = (f"◈ PISTA: {len(culpable)} letras, "
                                   f"empieza '{culpable[0]}', termina '{culpable[-1]}'")
                        col_msg = AMBER; play("beep")
                    if btn_limp_c.collidepoint(ev.pos):
                        texto_calc = ""; calc.set_texto("")
                        escaner_resultados = []; play("beep")
                    if btn_acu.collidepoint(ev.pos):
                        acusar()
                    # Abrir/cerrar expandido
                    if btn_cerrar and btn_cerrar.collidepoint(ev.pos):
                        abrir_expandido(expandido_abierto)
                    # Cambiar foco al clickear en la calculadora
                    calc_rect = pygame.Rect(cx + 8, 112, cw - 16, 30)
                    if calc_rect.collidepoint(ev.pos):
                        foco = "calculadora"; play("click")
                if resuelto:
                    try:
                        if btn_sig.collidepoint(ev.pos):
                            play("mision"); return vidas > 0, t_mision, True
                    except NameError:
                        pass