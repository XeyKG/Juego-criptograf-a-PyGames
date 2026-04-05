# -*- coding: utf-8 -*-
"""
Sistema de pistas progresivas para las misiones.
Las pistas se vuelven más específicas según el número de intentos fallidos.
"""


PISTAS_CESAR = {
    1: "Recuerda: En el cifrado César, cada letra se desplaza X posiciones...",
    2: "Intenta con diferentes valores de desplazamiento. Prueba números pequeños primero.",
    3: "¿Has notado patrones en las palabras? 'THE' es muy común en inglés.",
    4: "Los números que ves al lado son pistas. Usa el más pequeño como primer intento.",
    5: "Prueba: ROT1, ROT2, ROT3... hasta que la frase tenga sentido.",
}

PISTAS_BASE64 = {
    1: "Base64 es un cifrado de sustitución bidireccional. Usa el botón AUTO-DECODIFICAR si necesitas ayuda.",
    2: "¿Las luces parpadeantes indican algo? Intenta memorizar el patrón con los números iniciales.",
    3: "Las secuencias de 4 caracteres son típicas en Base64. Busca grupos similares.",
    4: "Los caracteres especiales (+ / =) son importantes. El = aparece al final.",
    5: "Prueba decodificadores línea por línea. A veces una sección está correcta y otra no.",
}

PISTAS_HASH = {
    1: "SHA-256 es una función hash unidireccional. Pequeños cambios producen hashes completamente diferentes.",
    2: "Busca patrones: ¿Qué diferencias hay entre los hashes de 'admin' y 'Admin'?",
    3: "La contraseña correcta debería generar un hash que coincida exactamente. Revisa mayúsculas/minúsculas.",
    4: "Intenta palabras comunes primero: nombres, palabras del acertijo, números simples.",
    5: "¿Has probado variaciones? Prueba: mayúscula al inicio, números al final, caracteres especiales.",
}

PISTAS_DIFFIE = {
    1: "Diffie-Hellman permite compartir una clave sin que KRONOS la intercepte. Sigue cada paso cuidadosamente.",
    2: "Necesitas calcular expresiones matemáticas. Usa ^ o ** para potencias, y 'mod' para módulos.",
    3: "Los valores de P y G deben ser como se especifican. Verifica que uses exactamente los números correctos.",
    4: "Cada paso construye sobre el anterior. Si un cálculo falla, los siguientes también fallarán.",
    5: "La clave final debe ser un número específico. Revisa cada cálculo intermedio con cuidado.",
}


class SistemaDeRespuestasInteligentes:
    """Gestiona las pistas contextuales por misión y tipo de error."""
    
    def __init__(self):
        self.intentos_mision = {}
        self.ultimo_error = {}
    
    def registrar_intento_fallido(self, num_mision, tipo_error=None):
        """Registra un intento fallido en una misión."""
        if num_mision not in self.intentos_mision:
            self.intentos_mision[num_mision] = 0
        self.intentos_mision[num_mision] += 1
        self.ultimo_error[num_mision] = tipo_error
    
    def obtener_pista(self, num_mision):
        """Retorna una pista apropiada según el número de intentos."""
        intentos = self.intentos_mision.get(num_mision, 0)
        
        pistas_por_mision = {
            1: PISTAS_CESAR,
            2: PISTAS_BASE64,
            3: PISTAS_HASH,
            4: PISTAS_DIFFIE
        }
        
        if num_mision not in pistas_por_mision:
            return "Mantén la calma. Revisa tu respuesta cuidadosamente."
        
        pistas = pistas_por_mision[num_mision]
        
        # Limitar el índice al máximo disponible
        indice = min(intentos - 1, len(pistas) - 1)
        
        if indice < 0:
            return "Inténtalo de nuevo."
        
        return pistas.get(indice + 1, pistas[max(pistas.keys())])
    
    def obtener_pista_especifica(self, num_mision, tipo_error):
        """Retorna pistas específicas según el tipo de error."""
        pistas_errores = {
            "formato": "Verifica el formato de tu respuesta. ¿Tiene espacios o caracteres especiales?",
            "longitud": "La longitud de la respuesta es importante. Cuenta los caracteres.",
            "rango": "El valor está fuera del rango esperado. Revisa los límites.",
            "calculo": "Hay un error en el cálculo. Revisa cada paso paso a paso.",
            "mayuscula": "A veces importa si es mayúscula o minúscula. Intenta cambiarlo.",
        }
        return pistas_errores.get(tipo_error, "Revisa tu respuesta cuidadosamente.")
    
    def intentos_usados(self, num_mision):
        """Retorna cuántos intentos se han usado en una misión."""
        return self.intentos_mision.get(num_mision, 0)
    
    def limpiar(self):
        """Limpia el estado para una nueva partida."""
        self.intentos_mision = {}
        self.ultimo_error = {}


# Instancia global
pistas_inteligentes = SistemaDeRespuestasInteligentes()
