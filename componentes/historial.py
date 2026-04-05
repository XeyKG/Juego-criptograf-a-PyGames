# -*- coding: utf-8 -*-
"""
Sistema de historial de comandos para consolas interactivas.
"""


class HistorialComandos:
    """Gestiona el historial de comandos con navegación ARRIBA/ABAJO."""
    
    def __init__(self):
        self.comandos = []
        self.indice_actual = None
    
    def agregar(self, comando):
        """Agrega un comando al historial."""
        if comando and comando not in self.comandos:
            self.comandos.append(comando)
        self.indice_actual = None  # Reset cuando se agrega nuevo
    
    def anterior(self):
        """Navega al comando anterior."""
        if not self.comandos:
            return None
        
        if self.indice_actual is None:
            self.indice_actual = len(self.comandos) - 1
        elif self.indice_actual > 0:
            self.indice_actual -= 1
        
        return self.comandos[self.indice_actual]
    
    def siguiente(self):
        """Navega al comando siguiente."""
        if not self.comandos:
            return None
        
        if self.indice_actual is None:
            return None
        elif self.indice_actual < len(self.comandos) - 1:
            self.indice_actual += 1
            return self.comandos[self.indice_actual]
        else:
            self.indice_actual = None
            return ""
    
    def obtener_actual(self):
        """Obtiene el comando actual del historial."""
        if self.indice_actual is None:
            return None
        return self.comandos[self.indice_actual]
    
    def limpiar(self):
        """Limpia el historial."""
        self.comandos = []
        self.indice_actual = None
