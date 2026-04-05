# -*- coding: utf-8 -*-
"""
Funciones criptográficas puras.
Sin dependencias del proyecto.
"""

import base64
import hashlib


def cesar(txt, k):
    """Cifra texto con desplazamiento César."""
    r = ""
    for c in txt.upper():
        r += chr((ord(c) - 65 + k) % 26 + 65) if c.isalpha() else c
    return r


def desc_cesar(txt, k):
    """Descifra texto César."""
    return cesar(txt, -k)


def b64enc(s):
    """Codifica texto a Base64."""
    return base64.b64encode(s.encode()).decode()


def b64dec(s):
    """Decodifica Base64 a texto. Retorna 'ERROR' si falla."""
    try:
        return base64.b64decode(s.encode()).decode()
    except Exception:
        return "ERROR"


def sha256(s):
    """Calcula hash SHA-256 de un texto."""
    return hashlib.sha256(s.encode()).hexdigest()


def diffie_hellman(p, g, a, b):
    """
    Simula intercambio Diffie-Hellman.
    Retorna (A, B, secreto_compartido).
    """
    A = pow(g, a, p)
    B = pow(g, b, p)
    return A, B, pow(B, a, p)