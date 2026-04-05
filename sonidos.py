# -*- coding: utf-8 -*-
"""
Generación y reproducción de efectos de sonido.
Usa numpy si está disponible, sino desactiva audio silenciosamente.
"""

from config import AUDIO_OK

# ─── Generador de beeps ───────────────────────────────────────────────────────
def gen_beep(freq, dur_ms, vol=0.3):
    """Genera un sonido de beep a partir de parámetros."""
    if not AUDIO_OK:
        return None
    try:
        import numpy as np
        import pygame.sndarray
        sr = 22050
        n = int(sr * dur_ms / 1000)
        t = np.linspace(0, dur_ms / 1000, n, False)
        wave = np.sin(2 * np.pi * freq * t)
        env = np.exp(-t * 5)
        wave = (wave * env * vol * 32767).astype(np.int16)
        stereo = np.column_stack([wave, wave])
        return pygame.sndarray.make_sound(stereo)
    except Exception:
        return None


# ─── Diccionario de sonidos ──────────────────────────────────────────────────
SND = {}

if AUDIO_OK:
    _defs = {
        "beep":    (880, 80, 0.15),
        "error":   (180, 400, 0.25),
        "ok":      (660, 200, 0.25),
        "alerta":  (440, 600, 0.3),
        "mision":  (330, 800, 0.25),
        "tecla":   (1200, 30, 0.08),
        "click":   (2000, 20, 0.1),
        "nivel":   (520, 300, 0.2),
        "logro":   (880, 150, 0.2),
        "flip":    (600, 60, 0.12),
        "combo":   (1100, 100, 0.15),
    }
    for nombre, args in _defs.items():
        SND[nombre] = gen_beep(*args)


# ─── Reproductor ─────────────────────────────────────────────────────────────
def play(nombre):
    """Reproduce un sonido por nombre. Silencioso si no existe."""
    snd = SND.get(nombre)
    if snd:
        try:
            snd.play()
        except Exception:
            pass