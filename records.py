# -*- coding: utf-8 -*-
"""
Sistema de guardado y carga de récords en JSON.
"""

import json
import os

REC_FILE = "sombra_records.json"


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