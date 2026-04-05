# -*- coding: utf-8 -*-
"""
Visualización interactiva del protocolo Diffie-Hellman.
Muestra a Alice y Bob intercambiando claves con partículas animadas.
"""

import math
import time
import pygame

from config import (
    ANCHO, pantalla, NEGRO, CYAN_SCAN, AMBER, MORADO, ORO, FOSF_DIM
)
from criptografia import diffie_hellman
from ui import txt, panel, F_TINY, F_BOLD
from sonidos import play


class DHVisual:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.p = 0
        self.g = 0
        self.a = 0
        self.b = 0
        self.A = 0
        self.B = 0
        self.secreto = 0
        self.fase = 0  # 0=setup, 1=calcular, 2=intercambio, 3=secreto
        self.particles_dh = []
        self.t_fase = time.time()

    def setup(self, p, g, a_real, b_real):
        """Inicializa los parámetros del protocolo."""
        self.p = p
        self.g = g
        self.a = a_real
        self.b = b_real
        self.A, self.B, self.secreto = diffie_hellman(p, g, a_real, b_real)
        self.fase = 0
        self.particles_dh = []
        self.t_fase = time.time()

    def advance(self):
        """Avanza a la siguiente fase del protocolo."""
        self.fase = min(self.fase + 1, 3)
        self.t_fase = time.time()
        if self.fase == 1:
            play("nivel")
        if self.fase == 2:
            play("flip")
            lx = self.x + 80
            rx = self.x + self.w - 80
            cy = self.y + self.h // 2
            for _ in range(20):
                self.particles_dh.append({
                    'x': lx, 'y': cy,
                    'tx': rx, 'ty': cy,
                    'prog': 0, 'col': CYAN_SCAN
                })
                self.particles_dh.append({
                    'x': rx, 'y': cy,
                    'tx': lx, 'ty': cy,
                    'prog': 0, 'col': AMBER
                })

    def update(self):
        """Actualiza partículas de intercambio."""
        for p in self.particles_dh:
            p['prog'] = min(1.0, p['prog'] + 0.02)
        self.particles_dh = [
            p for p in self.particles_dh if p['prog'] < 1.0
        ]

    def draw(self, mouse=None):
        """Dibuja toda la visualización del protocolo."""
        panel(self.x, self.y, self.w, self.h,
              col=(8, 4, 20), borde=MORADO)

        lx = self.x + 80
        rx = self.x + self.w - 80
        cy = self.y + self.h // 2

        # Parámetros públicos
        txt(f"p = {self.p}  |  g = {self.g}",
            F_TINY, MORADO, self.x + self.w // 2, self.y + 6, centro=True)
        pygame.draw.line(pantalla, MORADO,
                         (self.x + 10, self.y + 20),
                         (self.x + self.w - 10, self.y + 20), 1)

        # ── Agente Alice (izquierda) ──
        pygame.draw.circle(pantalla, CYAN_SCAN, (lx, cy), 25)
        txt("A", F_BOLD, NEGRO, lx, cy - 8, centro=True)
        txt("ALICE", F_TINY, CYAN_SCAN, lx, cy + 30, centro=True)
        if self.fase >= 0:
            txt(f"secreto_a = {self.a}", F_TINY, CYAN_SCAN,
                lx - 40, cy + 48, centro=True)

        # ── Agente Bob (derecha) ──
        pygame.draw.circle(pantalla, AMBER, (rx, cy), 25)
        txt("B", F_BOLD, NEGRO, rx, cy - 8, centro=True)
        txt("BOB", F_TINY, AMBER, rx, cy + 30, centro=True)
        if self.fase >= 0:
            txt(f"secreto_b = {self.b}", F_TINY, AMBER,
                rx - 40, cy + 48, centro=True)

        # ── Fase 1: Claves públicas ──
        if self.fase >= 1:
            txt(f"A = g^a mod p = {self.A}", F_TINY, CYAN_SCAN,
                lx, cy - 45, centro=True)
            txt(f"B = g^b mod p = {self.B}", F_TINY, AMBER,
                rx, cy - 45, centro=True)

        # ── Partículas de intercambio ──
        for p in self.particles_dh:
            px = p['x'] + (p['tx'] - p['x']) * p['prog']
            py = (p['y'] + (p['ty'] - p['y']) * p['prog']
                  + math.sin(p['prog'] * math.pi * 4) * 20)
            pygame.draw.circle(pantalla, p['col'], (int(px), int(py)), 3)

        # ── Fase 3: Secreto compartido ──
        if self.fase >= 3:
            mid_x = (lx + rx) // 2
            s = pygame.Surface((200, 50), pygame.SRCALPHA)
            pygame.draw.rect(s, (*ORO, 40), (0, 0, 200, 50),
                             border_radius=8)
            pygame.draw.rect(s, (*ORO, 180), (0, 0, 200, 50),
                             2, border_radius=8)
            pantalla.blit(s, (mid_x - 100, cy - 25))
            txt("SECRETO COMPARTIDO", F_TINY, ORO,
                mid_x, cy - 18, centro=True)
            txt(f"= {self.secreto}", F_BOLD, ORO,
                mid_x, cy, centro=True)
            pygame.draw.line(pantalla, ORO,
                             (lx + 25, cy), (mid_x - 100, cy), 1)
            pygame.draw.line(pantalla, ORO,
                             (mid_x + 100, cy), (rx - 25, cy), 1)

        # ── Instrucción de fase actual ──
        instrucciones = [
            "Paso 1: Alice y Bob eligen secretos privados (a, b)",
            "Paso 2: Calculan claves publicas (A, B) y las comparten",
            "Paso 3: Intercambian A y B por el canal publico",
            "Paso 4: Ambos calculan el mismo secreto compartido",
        ]
        txt(instrucciones[min(self.fase, 3)], F_TINY, FOSF_DIM,
            self.x + self.w // 2, self.y + self.h - 16, centro=True)