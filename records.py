# -*- coding: utf-8 -*-
"""
Sistema de guardado y carga de récords y partidas en JSON.
"""

import json
import os
import time

REC_FILE = "sombra_records.json"
PARTIDAS_FILE = "sombra_partidas.json"


def cargar_rec():
    """Carga récords desde archivo. Retorna dict por defecto si no existe."""
    if os.path.exists(REC_FILE):
        try:
            with open(REC_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "partidas": 0,
        "exitos": 0,
        "mejor_rango": "RECLUTA",
        "mejor_pts": 0,
    }


def guardar_rec(datos):
    """Guarda el dict de récords a archivo JSON."""
    try:
        with open(REC_FILE, "w", encoding="utf-8") as f:
            json.dump(datos, f)
    except Exception:
        pass


def guardar_partida(estado_partida):
    """
    Guarda el progreso actual de una partida.
    estado_partida: dict con info de la partida en progreso
    """
    try:
        partidas = {}
        if os.path.exists(PARTIDAS_FILE):
            try:
                with open(PARTIDAS_FILE, encoding="utf-8") as f:
                    partidas = json.load(f)
            except Exception:
                partidas = {}
        
        # Usar timestamp como key para tener múltiples guardos
        timestamp = int(time.time())
        partidas[str(timestamp)] = {
            "timestamp": timestamp,
            "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
            **estado_partida
        }
        
        with open(PARTIDAS_FILE, "w", encoding="utf-8") as f:
            json.dump(partidas, f, indent=2)
        
        return timestamp
    except Exception:
        return None


def cargar_partidas_disponibles():
    """Retorna lista de partidas guardadas disponibles."""
    if not os.path.exists(PARTIDAS_FILE):
        return []
    
    try:
        with open(PARTIDAS_FILE, encoding="utf-8") as f:
            partidas = json.load(f)
        
        # Convertir a lista ordenada por más reciente primero
        lista = []
        for key, datos in sorted(partidas.items(), 
                                key=lambda x: x[1].get("timestamp", 0),
                                reverse=True):
            lista.append((key, datos))
        return lista
    except Exception:
        return []


def cargar_partida(timestamp_key):
    """Carga una partida específica por su key."""
    try:
        with open(PARTIDAS_FILE, encoding="utf-8") as f:
            partidas = json.load(f)
        return partidas.get(timestamp_key)
    except Exception:
        return None


def eliminar_partida(timestamp_key):
    """Elimina una partida guardada."""
    try:
        with open(PARTIDAS_FILE, encoding="utf-8") as f:
            partidas = json.load(f)
        
        if timestamp_key in partidas:
            del partidas[timestamp_key]
            with open(PARTIDAS_FILE, "w", encoding="utf-8") as f:
                json.dump(partidas, f, indent=2)
            return True
    except Exception:
        pass
    return False