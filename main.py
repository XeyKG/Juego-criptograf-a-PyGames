# -*- coding: utf-8 -*-
"""
█████████████████████████████████████████████████████████████
█                                                           █
█          O P E R A C I Ó N   S O M B R A   v3.0         █
█                                                           █
█████████████████████████████████████████████████████████████
Punto de entrada — Ejecutar desde la raíz del proyecto:
    python main.py
"""

import sys
import os

# Asegurar que la raíz del proyecto está en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import ANCHO, ALTO
from records import cargar_rec, guardar_rec
from estado import RANGOS, agente
from logros import logros
from efectos import sfx
from sonidos import play
from escenas.inicio import pantalla_inicio
from escenas.teletipo import teletipo
from escenas.resultados import pantalla_resultados
from misiones.cesar import mision_cesar
from misiones.base64_v2 import mision_base64
from misiones.hash import mision_hash
from misiones.diffie import mision_diffie


def main():
    rec = cargar_rec()
    rec["partidas"] += 1
    guardar_rec(rec)

    while True:
        resultado = pantalla_inicio(rec)
        if resultado != "jugar":
            continue

        # ── Reset de estado para nueva partida ──────────────────
        agente.__init__()
        logros.__init__()
        resultados = []

        # ── Misión 1: Cifrado César ────────────────────────────
        ok, t, _ = mision_cesar()
        resultados.append((ok, agente.pts if ok else 0, t))
        if not ok:
            sfx.glitch(1.0)
            sfx.shake(15, 0.8)
            teletipo([
                ("OPERACIÓN FALLIDA — Identidad comprometida.", (255, 30, 30)),
                ("KRONOS ha ganado esta vez.", (0, 140, 40)),
                ("", (0, 140, 40)),
                ("Vuelve al cuartel. Reorganízate.", (255, 180, 0)),
            ])
            rec["mejor_pts"] = max(rec["mejor_pts"], agente.pts)
            guardar_rec(rec)
            pantalla_resultados(resultados)
            continue

        # ── Misión 2: Base64 ───────────────────────────────────
        ok, t, _ = mision_base64()
        pts_m2 = agente.pts - resultados[0][1] if ok else 0
        resultados.append((ok, pts_m2, t))
        if not ok:
            sfx.glitch(1.0)
            sfx.shake(15, 0.8)
            teletipo([
                ("OPERACIÓN ABORTADA — Cobertura insuficiente.", (255, 30, 30)),
                ("Has completado misiones parciales.", (0, 140, 40)),
            ])
            rec["mejor_pts"] = max(rec["mejor_pts"], agente.pts)
            guardar_rec(rec)
            pantalla_resultados(resultados)
            continue

        # ── Misión 3: SHA-256 ─────────────────────────────────
        ok, t, _ = mision_hash()
        pts_m3 = agente.pts - resultados[0][1] - resultados[1][1] if ok else 0
        resultados.append((ok, pts_m3, t))
        if not ok:
            sfx.glitch(1.0)
            sfx.shake(15, 0.8)
            teletipo([
                ("EL INFILTRADO ESCAPÓ.", (255, 30, 30)),
                ("La agencia necesita resultados.", (0, 140, 40)),
            ])
            rec["mejor_pts"] = max(rec["mejor_pts"], agente.pts)
            guardar_rec(rec)
            pantalla_resultados(resultados)
            continue

        # ── Misión 4: Diffie-Hellman ──────────────────────────
        ok, t, _ = mision_diffie()                 # ← corregido aquí
        pts_m4 = (agente.pts - resultados[0][1]
                  - resultados[1][1] - resultados[2][1] if ok else 0)
        resultados.append((ok, pts_m4, t))

        # ── Guardar récords ────────────────────────────────────
        rec["mejor_pts"] = max(rec["mejor_pts"], agente.pts)
        rango_nombre, _ = agente.rango()
        rangos_ordenados = [r[1] for r in RANGOS]
        idx_actual = rangos_ordenados.index(rango_nombre)
        idx_mejor = rangos_ordenados.index(rec["mejor_rango"])
        if idx_actual > idx_mejor:
            rec["mejor_rango"] = rango_nombre
        if all(r[0] for r in resultados):
            rec["exitos"] += 1
        guardar_rec(rec)

        # ── Pantalla final ─────────────────────────────────────
        if all(r[0] for r in resultados):
            teletipo([
                ("■■■ TRANSMISIÓN DEL DIRECTOR — MÁXIMA PRIORIDAD ■■■", (255, 215, 0)),
                ("", (0, 140, 40)),
                ("Agente CIPHER, has detenido el ataque de KRONOS.", (220, 230, 220)),
                ("El mundo no sabe lo que hiciste. Pero yo sí.", (0, 255, 70)),
                (f"Puntuación: {agente.pts:06d} — Rango: {rango_nombre}", (255, 215, 0)),
                ("Vuelve al cuartel. Hay más trabajo.", (255, 180, 0)),
            ])
            sfx.flash((255, 215, 0), 0.5)
        else:
            teletipo([
                ("OPERACIÓN INCOMPLETA", (255, 30, 30)),
                ("", (0, 140, 40)),
                ("No pudiste completar todas las misiones.", (220, 230, 220)),
                ("KRONOS avanza. Prepárate mejor.", (0, 140, 40)),
            ])

        pantalla_resultados(resultados)


if __name__ == "__main__":
    main()