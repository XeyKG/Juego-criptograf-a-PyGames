# -*- coding: utf-8 -*-
"""
Chat del operador ARIA — mensajes contextuales en la esquina inferior.
"""

import time

from config import CYAN_SCAN, ANCHO, ALTO
from ui import txt, panel, F_SMALL, F_TINY


class ChatBase:
    def __init__(self):
        self.mensajes = []   # [(texto, color, tiempo_expira)]
        self.queue = []      # mensajes pendientes con delay

    def decir(self, texto, col=None, delay=0):
        """Encola un mensaje. Aparecerá tras 'delay' segundos."""
        col = col or CYAN_SCAN
        self.queue.append((texto, col, time.time() + delay))

    def actualizar(self):
        """Mueve mensajes de la cola a pantalla y limpia expirados."""
        now = time.time()
        for item in list(self.queue):
            if now >= item[2]:
                self.mensajes.append((item[0], item[1], now + 5.0))
                self.queue.remove(item)
        self.mensajes = [m for m in self.mensajes if now < m[2]]

    def dibujar(self):
        """Dibuja la burbuja de chat si hay mensajes activos."""
        if not self.mensajes:
            return
        bx, by = 8, ALTO - 115
        bw = 310
        panel(bx, by, bw, 82, col=(0, 12, 22), borde=CYAN_SCAN, alpha=200)
        txt("◈ ARIA [BASE]:", F_TINY, CYAN_SCAN, bx + 6, by + 4)
        # Último mensaje con word-wrap
        mensaje = self.mensajes[-1]
        palabras = mensaje[0].split()
        lineas = []
        linea = ""
        for p in palabras:
            prueba = (linea + " " + p).strip()
            if F_TINY.size(prueba)[0] < bw - 16:
                linea = prueba
            else:
                lineas.append(linea)
                linea = p
        if linea:
            lineas.append(linea)
        for i, l in enumerate(lineas[:3]):
            txt(l, F_TINY, mensaje[1], bx + 6, by + 18 + i * 18)


# Instancia global
aria = ChatBase()