# -*- coding: utf-8 -*-
"""
Rueda de cifrado César interactiva.
Dos anillos concéntricos: el exterior fijo y el interior rota.
"""

import math
import pygame

from config import FOSF_VERDE, FOSF_DIM, AMBER, pantalla, FOSF_DARK, ANCHO, ALTO
from ui import txt, F_TINY, F_BOLD
from sonidos import play


class RuedaCesar:
    def __init__(self, cx, cy, radio):
        self.cx = cx
        self.cy = cy
        self.radio = radio
        self.desplazamiento = 0.0
        self.target = 0
        self.animando = False
        self.abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def set_k(self, k):
        """Establece el desplazamiento objetivo con animación."""
        self.target = k
        self.animando = True

    def update(self):
        """Actualiza la animación de rotación."""
        if self.animando:
            diff = self.target - self.desplazamiento
            if abs(diff) < 0.05:
                self.desplazamiento = self.target
                self.animando = False
            else:
                self.desplazamiento += diff * 0.2

    def draw(self, palabra_cifrada="", mouse=None):
        """Dibuja la rueda completa con conexiones."""
        # Anillo exterior decorativo
        pygame.draw.circle(pantalla, FOSF_DARK,
                           (self.cx, self.cy), self.radio + 4, 2)
        radio_int_div = self.radio - self.radio // 4
        pygame.draw.circle(pantalla, FOSF_DIM,
                           (self.cx, self.cy), radio_int_div - 2, 1)

        # ── Letras del anillo exterior (fijo) ──
        for i, ch in enumerate(self.abc):
            ang = math.radians(i * 360 / 26 - 90)
            rx = self.cx + int(self.radio * math.cos(ang))
            ry = self.cy + int(self.radio * math.sin(ang))
            destacado = palabra_cifrada and ch in palabra_cifrada
            col = AMBER if destacado else FOSF_DIM
            txt(ch, F_TINY, col, rx, ry, centro=True)

        # ── Anillo interior (rota con desplazamiento) ──
        radio_int = radio_int_div
        for i, ch in enumerate(self.abc):
            ang = math.radians((i + self.desplazamiento) * 360 / 26 - 90)
            rx = self.cx + int(radio_int * math.cos(ang))
            ry = self.cy + int(radio_int * math.sin(ang))
            idx_orig = (i - int(round(self.desplazamiento))) % 26
            destacado = (palabra_cifrada
                         and self.abc[idx_orig] in palabra_cifrada)
            col = FOSF_VERDE if destacado else (80, 120, 80)
            txt(ch, F_TINY, col, rx, ry, centro=True)

        # ── Centro con K actual ──
        k_mostrar = int(round(self.desplazamiento)) % 26
        pygame.draw.circle(pantalla, (12, 18, 12), (self.cx, self.cy), 28)
        pygame.draw.circle(pantalla, FOSF_VERDE, (self.cx, self.cy), 28, 2)
        txt(f"K={k_mostrar:02d}", F_BOLD, FOSF_VERDE,
            self.cx, self.cy - 8, centro=True)
        txt("CÉSAR", F_TINY, FOSF_DIM, self.cx, self.cy + 8, centro=True)

        # ── Líneas de conexión para letras destacadas ──
        if palabra_cifrada:
            s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            for ch in set(palabra_cifrada):
                if ch.isalpha():
                    idx = ord(ch) - 65
                    ang_e = math.radians(idx * 360 / 26 - 90)
                    ex = self.cx + int(self.radio * math.cos(ang_e))
                    ey = self.cy + int(self.radio * math.sin(ang_e))
                    ang_i = math.radians(
                        (idx + self.desplazamiento) * 360 / 26 - 90)
                    ix = self.cx + int(radio_int * math.cos(ang_i))
                    iy = self.cy + int(radio_int * math.sin(ang_i))
                    pygame.draw.line(s, (*AMBER, 60), (ex, ey), (ix, iy), 1)
            pantalla.blit(s, (0, 0))

    def click_arriba(self):
        """Rota la rueda un paso hacia arriba."""
        self.target = (self.target - 1) % 26
        self.animando = True
        play("flip")

    def click_abajo(self):
        """Rota la rueda un paso hacia abajo."""
        self.target = (self.target + 1) % 26
        self.animando = True
        play("flip")