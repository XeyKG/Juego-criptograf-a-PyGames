# -*- coding: utf-8 -*-
"""
Misión de entrenamiento: lecciones guiadas de criptografía con enfoque académico.
"""

import time
import base64
import hashlib
import pygame

from config import (
    ANCHO, ALTO, reloj, pantalla,
    FOSF_VERDE, FOSF_DIM, AMBER, CYAN_SCAN, MORADO, ROJO_ALERTA,
    BLANCO, GRIS_PANEL, F_GIANT, F_BOLD, F_SMALL, F_MICRO, F_TINY,
)
from ui import fondo_terminal, txt, txt_glow, panel, boton, input_box
from efectos import lluvia_data, tick_particles
from sonidos import play


def _dibujar_encabezado(titulo, descripcion):
    txt_glow(titulo, F_GIANT, AMBER, ANCHO // 2, 60, centro=True)
    txt(descripcion, F_SMALL, FOSF_DIM, ANCHO // 2, 95, centro=True)
    pygame.draw.line(pantalla, FOSF_DIM, (140, 120), (ANCHO - 140, 120), 1)


def _dibujar_tarjeta(x, y, w, h, titulo, texto, color):
    panel(x, y, w, h, col=(12, 18, 24), borde=color, radio=14, alpha=230)
    txt_glow(titulo, F_SMALL, color, x + 20, y + 16)
    txt(texto, F_MICRO, FOSF_DIM, x + 20, y + 44)


def _dibujar_explica(x, y, titulo, lineas, color):
    panel(x, y, 300, 220, col=(8, 12, 20), borde=color, radio=12, alpha=220)
    txt_glow(titulo, F_SMALL, color, x + 18, y + 14)
    for i, linea in enumerate(lineas):
        txt(linea, F_MICRO, FOSF_DIM, x + 18, y + 44 + i * 20)


def _esperar_click_fin():
    while True:
        fondo_terminal()
        lluvia_data(1)
        tick_particles()
        txt_glow("¡Excelente!", F_GIANT, FOSF_VERDE, ANCHO // 2, ALTO // 2 - 40, centro=True)
        txt("Pulsa cualquier tecla para continuar.", F_SMALL, FOSF_DIM, ANCHO // 2, ALTO // 2 + 20, centro=True)
        pygame.display.flip()
        reloj.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if ev.type == pygame.KEYDOWN or ev.type == pygame.MOUSEBUTTONDOWN:
                return


def _mostrar_panel_inicial():
    while True:
        fondo_terminal()
        lluvia_data(2)
        tick_particles()
        panel(100, 140, ANCHO - 200, ALTO - 260, col=(6, 10, 16), borde=MORADO, radio=18, alpha=240)
        txt_glow("AULA DE ENTRENAMIENTO", F_GIANT, MORADO, ANCHO // 2, 200, centro=True)
        txt("Estas lecciones explican de forma académica cada técnica.", F_SMALL, FOSF_DIM, ANCHO // 2, 240, centro=True)
        txt("Lee la teoría, prueba los ejemplos y avanza cuando estés listo.", F_MICRO, FOSF_DIM, ANCHO // 2, 268, centro=True)

        _dibujar_tarjeta(160, 330, 240, 180, "1. César", "Rotación de letras. Comprende cómo funciona el shift.", FOSF_VERDE)
        _dibujar_tarjeta(460, 330, 240, 180, "2. Base64", "Codificación reversible de bytes a texto.", CYAN_SCAN)
        _dibujar_tarjeta(760, 330, 240, 180, "3. Hash", "Huella única e irreversible de datos.", AMBER)
        _dibujar_tarjeta(1060, 330, 240, 180, "4. Diffie", "Intercambio seguro de claves sobre un canal abierto.", ROJO_ALERTA)

        txt("Pulsa ENTER para comenzar la lección 1.", F_SMALL, FOSF_DIM, ANCHO // 2, ALTO - 90, centro=True)
        pygame.display.flip()
        reloj.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                play("ok")
                return


def _texto_ayuda(texto, y):
    txt(texto, F_MICRO, FOSF_DIM, 160, y)


def leccion_cesar():
    mensaje_codificado = "URYYB JBEYQ"
    desplazamiento = "13"
    ayuda = "Ingresa un número entre 1 y 25 y luego presiona VERIFICAR."
    correcto = False

    while not correcto:
        fondo_terminal()
        lluvia_data(2)
        tick_particles()
        _dibujar_encabezado("Lección 1: Cifrado César", "El cifrado César desplaza el alfabeto una cantidad fija de posiciones.")
        panel(120, 140, 760, 520, col=(10, 14, 20), borde=FOSF_VERDE, radio=18, alpha=230)
        panel(920, 140, 300, 520, col=(8, 12, 18), borde=FOSF_VERDE, radio=18, alpha=220)

        txt("Cadena cifrada:", F_SMALL, FOSF_VERDE, 160, 170)
        txt_glow(mensaje_codificado, F_GIANT, BLANCO, 500, 220, centro=True)

        txt("Shift actual:", F_SMALL, FOSF_VERDE, 160, 280)
        input_box(desplazamiento, 280, 276, 90, activo=True)
        _texto_ayuda(ayuda, 330)

        if desplazamiento.isdigit():
            shift = int(desplazamiento) % 26
            resultado = ''.join(
                chr((ord(c) - 65 - shift) % 26 + 65) if 'A' <= c <= 'Z' else c
                for c in mensaje_codificado
            )
        else:
            resultado = "Introduce un número válido."

        txt("Resultado con el shift elegido:", F_SMALL, FOSF_VERDE, 160, 380)
        txt(resultado, F_BOLD, BLANCO, 500, 420, centro=True)

        _dibujar_explica(920, 170, "Cómo funciona", [
            "1. Cada letra se mueve X posiciones en el alfabeto.",
            "2. ROT13 usa un desplazamiento fijo de 13.",
            "3. A→N, B→O, C→P, ..., M→Z.",
            "4. Decodificar ROT13 es aplicar el mismo shift otra vez.",
            "5. Es un cifrado clásico, útil para ejemplos."
        ], FOSF_VERDE)

        txt_glow("Fórmula", F_SMALL, FOSF_VERDE, 940, 400)
        txt("C = (P + shift) mod 26", F_MICRO, FOSF_DIM, 940, 430)
        txt("P = letra original, C = letra cifrada.", F_MICRO, FOSF_DIM, 940, 450)

        mouse = pygame.mouse.get_pos()
        btn = boton("VERIFICAR", 500, 500, 180, 40, (0, 90, 50), (0, 160, 90), mouse)
        btn_hint = boton("PISTA", 500, 556, 180, 40, (20, 20, 50), (70, 70, 150), mouse)

        pygame.display.flip()
        reloj.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_BACKSPACE:
                    desplazamiento = desplazamiento[:-1]
                elif ev.key == pygame.K_RETURN:
                    if resultado == "HELLO WORLD":
                        correcto = True
                    else:
                        ayuda = "Ese shift no descifra aún. Intenta otro."
                elif ev.unicode.isdigit() and len(desplazamiento) < 2:
                    desplazamiento += ev.unicode
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btn.collidepoint(ev.pos):
                    if resultado == "HELLO WORLD":
                        correcto = True
                    else:
                        ayuda = "Ese shift no descifra aún. Intenta otro."
                        play("error")
                if btn_hint.collidepoint(ev.pos):
                    ayuda = "ROT13 es un desplazamiento de 13 posiciones. Prueba con 13 si no estás seguro."
                    play("click")

    play("ok")
    _esperar_click_fin()


def leccion_base64():
    texto_base64 = "U29tbyBjaXJjbzogSGFnYSA1MCVzaW5vcw=="
    respuesta = ""
    ayuda = "Escribe el texto decodificado y presiona VERIFICAR."
    correcto = False
    mensaje_decodificado = base64.b64decode(texto_base64).decode('utf-8')

    while not correcto:
        fondo_terminal()
        lluvia_data(2)
        tick_particles()
        _dibujar_encabezado("Lección 2: Base64", "Base64 convierte bytes binarios en texto seguro para transmisión.")
        panel(120, 140, 760, 520, col=(8, 16, 24), borde=CYAN_SCAN, radio=18, alpha=230)
        panel(920, 140, 300, 520, col=(6, 14, 22), borde=CYAN_SCAN, radio=18, alpha=220)

        txt("Cadena Base64:", F_SMALL, CYAN_SCAN, 160, 170)
        txt_glow(texto_base64, F_BOLD, BLANCO, 500, 220, centro=True)

        txt("Tu respuesta:", F_SMALL, CYAN_SCAN, 160, 280)
        input_box(respuesta, 320, 276, 520, activo=True, placeholder="Texto decodificado")
        _texto_ayuda(ayuda, 330)

        txt("Decodificación esperada:", F_SMALL, CYAN_SCAN, 160, 390)
        txt_glow(mensaje_decodificado, F_SMALL, FOSF_DIM, 500, 430, centro=True)

        _dibujar_explica(920, 170, "Teoría Base64", [
            "1. Usa 64 símbolos: A-Z, a-z, 0-9, +, /.",
            "2. Agrupa bytes en bloques de 3 (24 bits).",
            "3. Divide los 24 bits en 4 valores de 6 bits.",
            "4. Cada valor se mapea a un símbolo Base64.",
            "5. '=' se usa para rellenar cuando faltan bytes."
        ], CYAN_SCAN)

        txt_glow("Ejemplo parcial", F_SMALL, CYAN_SCAN, 940, 400)
        txt("'Som' → 01010011 01101111 01101101", F_MICRO, FOSF_DIM, 940, 430)
        txt("Divide en 6 bits y mapea cada grupo.", F_MICRO, FOSF_DIM, 940, 450)

        mouse = pygame.mouse.get_pos()
        btn = boton("VERIFICAR", 500, 500, 180, 40, (0, 70, 100), (0, 140, 220), mouse)
        btn_hint = boton("EXPLICAR", 500, 556, 180, 40, (0, 50, 80), (0, 100, 160), mouse)

        pygame.display.flip()
        reloj.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_BACKSPACE:
                    respuesta = respuesta[:-1]
                elif ev.key == pygame.K_RETURN:
                    if respuesta.strip() == mensaje_decodificado:
                        correcto = True
                    else:
                        ayuda = "Revisa los espacios y las mayúsculas de tu respuesta."
                elif ev.unicode:
                    respuesta += ev.unicode
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btn.collidepoint(ev.pos):
                    if respuesta.strip() == mensaje_decodificado:
                        correcto = True
                    else:
                        ayuda = "La respuesta no coincide. Revisa mayúsculas y espacios."
                        play("error")
                if btn_hint.collidepoint(ev.pos):
                    ayuda = "Base64 es reversible. Descifra la cadena para ver el texto original."
                    play("click")

    play("ok")
    _esperar_click_fin()


def leccion_hash():
    objetivo = "AGENTE"
    texto_hash = hashlib.sha256(objetivo.encode('utf-8')).hexdigest()
    entrada = ""
    ayuda = "Escribe la palabra correcta para obtener el hash mostrado."
    correcto = False

    while not correcto:
        fondo_terminal()
        lluvia_data(2)
        tick_particles()
        _dibujar_encabezado("Lección 3: Hash", "Un hash es una huella digital fija para cualquier entrada.")
        panel(120, 140, 760, 520, col=(10, 12, 20), borde=AMBER, radio=18, alpha=230)
        panel(920, 140, 300, 520, col=(8, 10, 18), borde=AMBER, radio=18, alpha=220)

        txt("Hash objetivo:", F_SMALL, AMBER, 160, 170)
        txt_glow(texto_hash[:48] + "...", F_TINY, BLANCO, 500, 210, centro=True)

        txt("Escribe tu texto:", F_SMALL, AMBER, 160, 280)
        input_box(entrada, 320, 276, 520, activo=True, placeholder="Intenta hallar la palabra secreta")

        if entrada:
            hash_actual = hashlib.sha256(entrada.encode('utf-8')).hexdigest()
            txt("Hash generado:", F_SMALL, FOSF_DIM, 160, 330)
            txt(hash_actual[:48] + "...", F_TINY, FOSF_DIM, 500, 370, centro=True)
        else:
            txt("Hash generado:", F_SMALL, FOSF_DIM, 160, 330)
            txt("(escribe algo para verlo)", F_TINY, FOSF_DIM, 500, 370, centro=True)

        _texto_ayuda(ayuda, 420)
        _dibujar_explica(920, 170, "Propiedades de hash", [
            "1. Determinista: misma entrada → mismo hash.",
            "2. Irreversible: no se puede recuperar el texto original.",
            "3. Efecto avalancha: un cambio cambia todo.",
            "4. Útil para verificar integridad de datos.",
            "5. SHA-256 produce 64 caracteres hex."
        ], AMBER)

        mouse = pygame.mouse.get_pos()
        btn = boton("VERIFICAR", 500, 500, 180, 40, (60, 40, 0), (140, 90, 0), mouse)
        btn_hint = boton("PISTA", 500, 556, 180, 40, (30, 30, 0), (90, 90, 0), mouse)

        pygame.display.flip()
        reloj.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_BACKSPACE:
                    entrada = entrada[:-1]
                elif ev.key == pygame.K_RETURN:
                    if entrada.upper() == objetivo:
                        correcto = True
                    else:
                        ayuda = "Prueba con una palabra corta y clara."
                elif ev.unicode:
                    entrada += ev.unicode.upper()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btn.collidepoint(ev.pos):
                    if entrada.upper() == objetivo:
                        correcto = True
                    else:
                        ayuda = "No es correcto. Observa el hash y prueba otra palabra."
                        play("error")
                if btn_hint.collidepoint(ev.pos):
                    ayuda = "La palabra secreta es AGENTE. El hash mostrado corresponde a esa entrada."
                    play("click")

    play("ok")
    _esperar_click_fin()


def leccion_diffie():
    p = 23
    g = 5
    secreto_a = "6"
    secreto_b = "15"
    respuesta = ""
    ayuda = "Calcula la clave compartida usando exponenciación modular."
    correcto = False

    def calcular_compartido(a, b):
        A = pow(g, a, p)
        B = pow(g, b, p)
        return pow(B, a, p), pow(A, b, p)

    while not correcto:
        fondo_terminal()
        lluvia_data(2)
        tick_particles()
        _dibujar_encabezado("Lección 4: Diffie-Hellman", "Diffie-Hellman permite acordar una clave sin transmitirla directamente.")
        panel(120, 140, 760, 520, col=(12, 10, 18), borde=ROJO_ALERTA, radio=18, alpha=230)
        panel(920, 140, 300, 520, col=(10, 8, 18), borde=ROJO_ALERTA, radio=18, alpha=220)

        txt("Parámetros públicos:", F_SMALL, ROJO_ALERTA, 160, 170)
        txt_glow(f"P = {p}    G = {g}", F_BOLD, BLANCO, 500, 210, centro=True)

        txt("Secreto A:", F_SMALL, ROJO_ALERTA, 160, 280)
        input_box(secreto_a, 260, 276, 90, activo=False)
        txt("Secreto B:", F_SMALL, ROJO_ALERTA, 380, 280)
        input_box(secreto_b, 480, 276, 90, activo=False)

        txt("Clave compartida:", F_SMALL, ROJO_ALERTA, 160, 340)
        input_box(respuesta, 360, 336, 310, activo=True, placeholder="Introduce K aquí")
        _texto_ayuda(ayuda, 390)
        txt("Fórmula:", F_SMALL, FOSF_DIM, 160, 420)
        txt("A = g^a mod p,  B = g^b mod p", F_MICRO, FOSF_DIM, 160, 442)
        txt("K = B^a mod p = A^b mod p", F_MICRO, FOSF_DIM, 160, 464)
        txt("Usa los valores A=6 y B=15 para esta lección.", F_MICRO, FOSF_DIM, 160, 486)

        _dibujar_explica(920, 170, "Pasos básicos", [
            "1. P y G son públicos y conocidos por todos.",
            "2. Cada participante elige un secreto privado.",
            "3. Envía solo su valor público al otro.",
            "4. Ambos calculan K por separado.",
            "5. La clave compartida queda igual para ambos."
        ], ROJO_ALERTA)

        mouse = pygame.mouse.get_pos()
        btn = boton("VERIFICAR", 500, 500, 180, 40, (80, 0, 40), (160, 0, 80), mouse)
        btn_hint = boton("EXPLICAR", 500, 556, 180, 40, (50, 0, 50), (120, 0, 120), mouse)

        pygame.display.flip()
        reloj.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_BACKSPACE:
                    respuesta = respuesta[:-1]
                elif ev.key == pygame.K_RETURN:
                    if respuesta.strip() == str(calcular_compartido(int(secreto_a), int(secreto_b))[0]):
                        correcto = True
                    else:
                        ayuda = "No coincide. Revisa la fórmula paso a paso."
                elif ev.unicode.isdigit() and len(respuesta) < 4:
                    respuesta += ev.unicode
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btn.collidepoint(ev.pos):
                    clave = calcular_compartido(int(secreto_a), int(secreto_b))[0]
                    if respuesta.strip() == str(clave):
                        correcto = True
                    else:
                        ayuda = "Clave incorrecta. Calcula primero A y B."
                        play("error")
                if btn_hint.collidepoint(ev.pos):
                    respuesta = str(calcular_compartido(int(secreto_a), int(secreto_b))[0])
                    play("click")

    play("ok")
    _esperar_click_fin()


def pantalla_final_practica(segundos):
    t0 = time.time()
    while time.time() - t0 < 4.5:
        fondo_terminal()
        lluvia_data(3)
        tick_particles()
        panel(220, 220, ANCHO - 440, ALTO - 440, col=(10, 16, 14), borde=FOSF_VERDE, radio=18, alpha=230)
        txt_glow("ENTRENAMIENTO COMPLETADO", F_GIANT, FOSF_VERDE, ANCHO // 2, ALTO // 2 - 40, centro=True)
        txt("Has repasado los fundamentos de las cuatro lecciones.", F_SMALL, FOSF_DIM, ANCHO // 2, ALTO // 2 + 20, centro=True)
        txt(f"Tiempo total de práctica: {segundos:.1f}s", F_SMALL, AMBER, ANCHO // 2, ALTO // 2 + 60, centro=True)
        pygame.display.flip()
        reloj.tick(60)


def mision_practica():
    t0 = time.time()
    _mostrar_panel_inicial()
    leccion_cesar()
    leccion_base64()
    leccion_hash()
    leccion_diffie()
    pantalla_final_practica(time.time() - t0)
    return True, time.time() - t0, None
