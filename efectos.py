# -*- coding: utf-8 -*-
"""
Efectos visuales: screen shake, flash, glitch, partículas, textos flotantes.
"""

import random
import math
import time

import pygame

from config import ANCHO, ALTO, pantalla, FOSF_VERDE, FOSF_DIM, ROJO_ALERTA, CYAN_SCAN, AMBER, BLANCO


# ═══════════════════════════════════════════════════════════════════════════════
#  SCREEN FX
# ═══════════════════════════════════════════════════════════════════════════════

class ScreenFX:
    def __init__(self):
        self.shake_x = 0
        self.shake_y = 0
        self.shake_dur = 0.0
        self.shake_str = 0
        self.flash_alpha = 0
        self.flash_col = BLANCO
        self.flash_dur = 0.0
        self.glitch_dur = 0.0
        self.glitch_lines = []
        self.vignette = True

    def shake(self, strength=8, duration=0.3):
        self.shake_str = strength
        self.shake_dur = duration

    def flash(self, col=BLANCO, duration=0.2):
        self.flash_col = col
        self.flash_alpha = 180
        self.flash_dur = duration

    def glitch(self, duration=0.5, lines=15):
        self.glitch_dur = duration
        colores = [FOSF_VERDE, ROJO_ALERTA, CYAN_SCAN, AMBER]
        self.glitch_lines = [
            (random.randint(0, ANCHO), random.randint(0, ALTO),
             random.randint(30, 300), random.randint(2, 6),
             random.choice(colores))
            for _ in range(lines)
        ]

    def update(self, dt):
        if self.shake_dur > 0:
            self.shake_dur -= dt
            self.shake_x = random.randint(-self.shake_str, self.shake_str)
            self.shake_y = random.randint(-self.shake_str, self.shake_str)
        else:
            self.shake_x = self.shake_y = 0

        if self.flash_dur > 0:
            self.flash_dur -= dt
            self.flash_alpha = max(0, min(255, int(180 * (self.flash_dur / 0.2))))
        else:
            self.flash_alpha = 0

        if self.glitch_dur > 0:
            self.glitch_dur -= dt
        else:
            self.glitch_lines = []

    def draw(self):
        if self.flash_alpha > 0:
            s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            s.fill((*self.flash_col[:3], self.flash_alpha))
            pantalla.blit(s, (0, 0))
        for lx, ly, lw, lh, lc in self.glitch_lines:
            s = pygame.Surface((lw, lh), pygame.SRCALPHA)
            s.fill((*lc, random.randint(40, 120)))
            pantalla.blit(s, (lx, ly))
        if self.vignette:
            s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            for i in range(40):
                a = int(60 * (1 - i / 40))
                pygame.draw.rect(s, (0, 0, 0, a),
                                 (i * 2, i * 2, ANCHO - i * 4, ALTO - i * 4), 3)
            pantalla.blit(s, (0, 0))


sfx = ScreenFX()


# ═══════════════════════════════════════════════════════════════════════════════
#  PARTÍCULAS
# ═══════════════════════════════════════════════════════════════════════════════

class Particle:
    __slots__ = ['x', 'y', 'vx', 'vy', 'vida', 'vida_max', 'tam', 'col', 'tipo']

    def __init__(self, x, y, col, vx=None, vy=None, vida=None, tam=None, tipo="dot"):
        self.x = float(x)
        self.y = float(y)
        self.col = col
        self.tipo = tipo
        self.vx = vx if vx is not None else random.uniform(-3, 3)
        self.vy = vy if vy is not None else random.uniform(-5, 0)
        self.vida = self.vida_max = vida or random.randint(30, 80)
        self.tam = tam or random.uniform(1.5, 4)

    def tick(self):
        self.x += self.vx
        self.y += self.vy
        if self.tipo == "spark":
            self.vy += 0.15
        elif self.tipo == "float":
            self.vy -= 0.02
        self.vida -= 1
        return self.vida > 0

    def draw(self):
        a = self.vida / self.vida_max
        c = tuple(max(0, min(255, int(x * a))) for x in self.col)
        sz = max(1, int(self.tam * a))
        if self.tipo == "spark":
            ex = int(self.x - self.vx * 2)
            ey = int(self.y - self.vy * 2)
            pygame.draw.line(pantalla, c, (ex, ey),
                             (int(self.x), int(self.y)), max(1, sz // 2))
        pygame.draw.circle(pantalla, c, (int(self.x), int(self.y)), sz)


particles = []


def boom(x, y, col, n=25, tipo="esfera"):
    for _ in range(n):
        ang = random.uniform(0, math.tau)
        vel = random.uniform(1, 7)
        t = "spark" if tipo == "esfera" else tipo
        particles.append(Particle(
            x, y, col,
            math.cos(ang) * vel, math.sin(ang) * vel,
            random.randint(40, 100), random.uniform(2, 6), t
        ))


def lluvia_data(n=2):
    for _ in range(n):
        particles.append(Particle(
            random.randint(0, ANCHO), 0,
            FOSF_DIM,
            random.uniform(-0.3, 0.3), random.uniform(2, 5),
            random.randint(60, 130), random.uniform(1, 2), "float"
        ))


def tick_particles():
    global particles
    particles = [p for p in particles if p.tick()]
    for p in particles:
        p.draw()


# ═══════════════════════════════════════════════════════════════════════════════
#  TEXTOS FLOTANTES
# ═══════════════════════════════════════════════════════════════════════════════

class FloatingText:
    def __init__(self, texto, x, y, col, tam_fuente=24, dur=2.0):
        from config import _fuente
        self.texto = texto
        self.x = x
        self.y = y
        self.col = col
        self.fuente = _fuente(tam_fuente, True)
        self.dur = dur
        self.t0 = time.time()
        self.vy = -1.5

    def alive(self):
        return time.time() - self.t0 < self.dur

    def draw(self):
        prog = (time.time() - self.t0) / self.dur
        a = max(0, 1 - prog)
        self.y += self.vy
        c = tuple(max(0, min(255, int(x * a))) for x in self.col)
        s = self.fuente.render(self.texto, True, c)
        r = s.get_rect(centerx=int(self.x), y=int(self.y))
        pantalla.blit(s, r)


floats = []


def add_float(texto, x, y, col, tam=24, dur=2.0):
    floats.append(FloatingText(texto, x, y, col, tam, dur))


def tick_floats():
    global floats
    floats = [f for f in floats if f.alive()]
    for f in floats:
        f.draw()