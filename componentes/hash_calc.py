# -*- coding: utf-8 -*-
"""
Calculadora de hash SHA-256 interactiva.
El usuario escribe y ve el hash calcularse carácter por carácter.
"""

import time
import math
import pygame

from config import ANCHO, FOSF_VERDE, AMBER, ROJO_DIM, FOSF_DIM
from criptografia import sha256
from ui import txt, panel, F_TINY, F_BOLD, F_SMALL



class HashCalc:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.texto = ""
        self.hash_resultado = ""
        self.chars_visibles = 0
        self.t_hash = time.time()
        self.activo = False
        self.match = False

    def set_texto(self, t):
        """Actualiza el texto y recalcula el hash."""
        self.texto = t
        self.hash_resultado = sha256(t) if t else ""
        self.chars_visibles = 0
        self.t_hash = time.time()
        self.match = False

    def set_target(self, target_hash):
        """Verifica si el hash actual coincide con el objetivo."""
        if self.hash_resultado and self.hash_resultado == target_hash:
            self.match = True
        else:
            self.match = False

    def update(self):
        """Anima la aparición del hash carácter por carácter."""
        if (self.hash_resultado
                and self.chars_visibles < len(self.hash_resultado)):
            if time.time() - self.t_hash > 0.015:
                self.chars_visibles = min(
                    self.chars_visibles + 2, len(self.hash_resultado))
                self.t_hash = time.time()

    def draw(self, target_hash="", mouse=None):
        """Dibuja la calculadora completa."""
        from config import pantalla
        panel(self.x, self.y, self.w, self.h, col=(15, 10, 0), borde=AMBER)
        txt("◉ CALCULADORA SHA-256 — Escribe para verificar:",
            F_TINY, AMBER, self.x + 8, self.y + 5)

        # Input visual
        ir = pygame.Rect(self.x + 8, self.y + 22, self.w - 16, 30)
        if ir.w > 0 and ir.h > 0:
            s = pygame.Surface((ir.w, ir.h), pygame.SRCALPHA)
            pygame.draw.rect(s, (0, 25, 8, 220), (0, 0, ir.w, ir.h),
                             border_radius=3)
            pantalla.blit(s, ir.topleft)
        cur = "|" if self.activo and int(time.time() * 2) % 2 == 0 else ""
        txt(self.texto + cur, F_BOLD, FOSF_VERDE, ir.x + 6, ir.y + 6)
        bord = FOSF_VERDE if self.activo else FOSF_DIM
        pygame.draw.rect(pantalla, bord, ir, 1, border_radius=3)

        # Hash resultado animado
        if self.hash_resultado:
            visible = self.hash_resultado[:self.chars_visibles]
            col_h = FOSF_VERDE if self.match else AMBER
            txt(visible[:32], F_TINY, col_h, self.x + 8, self.y + 56)
            if len(visible) > 32:
                txt(visible[32:], F_TINY, col_h, self.x + 8, self.y + 70)

        # Indicador de coincidencia
        if self.match:
            txt("✓ ¡COINCIDENCIA DETECTADA!", F_SMALL, FOSF_VERDE,
                self.x + self.w // 2, self.y + self.h - 18, centro=True)
            if self.w > 0 and self.h > 0:
                s = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
                a = int(30 * abs(math.sin(time.time() * 4)))
                pygame.draw.rect(s, (*FOSF_VERDE, a), (0, 0, self.w, self.h),
                                 border_radius=6)
                pantalla.blit(s, (self.x, self.y))

        # Hash objetivo de referencia
        if target_hash:
            txt(f"OBJETIVO: {target_hash[:32]}", F_TINY, ROJO_DIM,
                self.x + 8, self.y + self.h - 18)