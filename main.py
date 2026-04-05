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
from records import cargar_rec, guardar_rec, guardar_partida
from estado import RANGOS, agente
from logros import logros
from efectos import sfx
from sonidos import play
import config
from escenas.inicio import pantalla_inicio
from escenas.selectormodo import pantalla_seleccionar_modo
from escenas.teletipo import teletipo
from escenas.resultados import pantalla_resultados
from escenas.victoria import pantalla_victoria, pantalla_acceso_negado, pantalla_carga_mision
from misiones.cesar import mision_cesar
from misiones.base64_v2 import mision_base64
from misiones.hash import mision_hash
from misiones.diffie import mision_diffie
from misiones.practica import mision_practica


def verificar_logros_mision(num_mision, ok, pts, tiempo):
    """Desbloquea logros según el desempeño en una misión."""
    if not ok:
        return
    
    logros.intentar("PRIMERA_SANGRE")
    
    # Logros por misión
    nombres_logros = {
        1: "CIFRADOR",
        2: "DECODIFICADOR", 
        3: "HUELLA",
        4: "PROTOCOLO"
    }
    
    nombres_rapidos = {
        1: ("CESAR_RAPIDO", 15),
        2: ("BASE64_RAPIDO", 12),
        3: ("HASH_RAPIDO", 20),
        4: ("DH_RAPIDO", 30)
    }
    
    nombres_perfecto = {
        1: "CESAR_PERFECTO",
        2: "BASE64_PERFECTO",
        3: "HASH_PERFECTO",
        4: "DH_PERFECTO"
    }
    
    # Desbloquear logro de dominio
    if num_mision in nombres_logros:
        logros.intentar(nombres_logros[num_mision])
    
    # Desbloquear logro de velocidad
    if num_mision in nombres_rapidos:
        logro_id, umbral = nombres_rapidos[num_mision]
        if tiempo < umbral:
            logros.intentar(logro_id)
    
    # Desbloquear logro de precisión (sin errores)
    if num_mision in nombres_perfecto and agente.sin_errores:
        logros.intentar(nombres_perfecto[num_mision])


def guardar_estado_partida(misiones_completadas):
    """Guarda el estado actual de la partida."""
    estado = {
        "modo_practica": config.MODO_PRACTICA,
        "misiones_completadas": misiones_completadas,
        "puntos_acumulados": agente.pts,
        "resultados": [],  # Podría extenderse con más detalles
    }
    return guardar_partida(estado)


def main():
    rec = cargar_rec()
    rec["partidas"] += 1
    guardar_rec(rec)

    while True:
        resultado = pantalla_inicio(rec)
        
        if resultado == "jugar":
            # Nueva partida
            # ─ Seleccionar modo de juego ──────────────────────────────
            modo = pantalla_seleccionar_modo()
            if modo is None:
                continue  # Volver al menú
            
            config.MODO_PRACTICA = (modo == "practica")

            if config.MODO_PRACTICA:
                mision_practica()
                continue

            # ── Reset de estado para nueva partida ──────────────────
            agente.__init__()
            logros.__init__()
            resultados = []
            misiones_completadas = 0
            
        elif isinstance(resultado, tuple) and resultado[0] == "cargar":
            # Cargar partida
            partida_data = resultado[1]
            config.MODO_PRACTICA = partida_data.get("modo_practica", False)
            
            agente.__init__()
            logros.__init__()
            
            # Restaurar estado
            resultados = partida_data.get("resultados", [])
            misiones_completadas = partida_data.get("misiones_completadas", 0)
            agente.pts = partida_data.get("puntos_acumulados", 0)
            
        else:
            continue

        # ── Misión 1: Cifrado César ────────────────────────────
        ok, t, _ = mision_cesar()
        resultados.append((ok, agente.pts if ok else 0, t))
        if not ok:
            pantalla_acceso_negado(1)
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
        
        verificar_logros_mision(1, ok, t, agente.sin_errores)
        pantalla_victoria(1, resultados[0][1], t)
        guardar_estado_partida(1)  # Guardar progreso
        pantalla_carga_mision(2)

        # ── Misión 2: Base64 ───────────────────────────────────
        ok, t, _ = mision_base64()
        pts_m2 = agente.pts - resultados[0][1] if ok else 0
        resultados.append((ok, pts_m2, t))
        if not ok:
            pantalla_acceso_negado(2)
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
        
        verificar_logros_mision(2, ok, t, agente.sin_errores)
        pantalla_victoria(2, pts_m2, t)
        guardar_estado_partida(2)  # Guardar progreso
        pantalla_carga_mision(3)

        # ── Misión 3: SHA-256 ─────────────────────────────────
        ok, t, _ = mision_hash()
        pts_m3 = agente.pts - resultados[0][1] - resultados[1][1] if ok else 0
        resultados.append((ok, pts_m3, t))
        if not ok:
            pantalla_acceso_negado(3)
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
        
        verificar_logros_mision(3, ok, t, agente.sin_errores)
        pantalla_victoria(3, pts_m3, t)
        guardar_estado_partida(3)  # Guardar progreso
        pantalla_carga_mision(4)

        # ── Misión 4: Diffie-Hellman ──────────────────────────
        ok, t, _ = mision_diffie()
        pts_m4 = (agente.pts - resultados[0][1]
                  - resultados[1][1] - resultados[2][1] if ok else 0)
        resultados.append((ok, pts_m4, t))
        
        if not ok:
            pantalla_acceso_negado(4)
        else:
            verificar_logros_mision(4, ok, t, agente.sin_errores)
            pantalla_victoria(4, pts_m4, t)
            # Partida completada, no guardar en punto de carga

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