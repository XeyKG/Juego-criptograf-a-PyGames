import math
import time

import pygame

from config import (
    ANCHO, ALTO, pantalla, reloj, t,
    FOSF_VERDE, FOSF_DIM, FOSF_DARK, AMBER, AMBER_DIM,
    ROJO_ALERTA, ROJO_DIM, CYAN_SCAN, BLANCO,
    GRIS_PANEL, GRIS_BORDE, FONDO,
    F_GIANT, F_TITULO, F_GRANDE, F_MEDIA, F_SMALL,
    F_MICRO, F_BOLD, F_TINY,
)
from estado import agente


# ═══════════════════════════════════════════════════════════════════════════════
#  FONDO TERMINAL
# ═══════════════════════════════════════════════════════════════════════════════

def fondo_terminal():
    """Dibuja el fondo con scanlines y grid sutil."""
    pantalla.fill(FONDO)
    # Scanlines más sutiles para no competir con el texto
    s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    for y in range(0, ALTO, 4):
        pygame.draw.line(s, (0, 0, 0, 35), (0, y), (ANCHO, y))
    pantalla.blit(s, (0, 0))
    # Grid más sutil
    for x in range(0, ANCHO, 80):
        pygame.draw.line(pantalla, (0, 14, 4), (x, 0), (x, ALTO))
    for y in range(0, ALTO, 80):
        pygame.draw.line(pantalla, (0, 14, 4), (0, y), (ANCHO, y))


# ═══════════════════════════════════════════════════════════════════════════════
#  TEXTO
# ═══════════════════════════════════════════════════════════════════════════════

def txt(texto, fnt, col, x, y, centro=False):
    """Dibuja texto con sombra sutil para mejorar contraste sobre fondo."""
    sup = fnt.render(str(texto), True, col)
    r = sup.get_rect()
    if centro:
        r.centerx = int(x)
    else:
        r.x = int(x)
    r.y = int(y)
    # Sombra sutil para mejorar legibilidad
    sombra = fnt.render(str(texto), True, (0, 0, 0))
    sr = sombra.get_rect()
    sr.x = r.x + 1
    sr.y = r.y + 1
    pantalla.blit(sombra, sr)
    pantalla.blit(sup, r)
    return r


def txt_glow(texto, fnt, col, x, y, centro=False):
    """Texto con efecto de neón/glow más pronunciado."""
    glow = tuple(min(255, c // 2) for c in col)
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1)]:
        s = fnt.render(str(texto), True, glow)
        r = s.get_rect()
        if centro:
            r.centerx = int(x) + dx
        else:
            r.x = int(x) + dx
        r.y = int(y) + dy
        pantalla.blit(s, r)
    return txt(texto, fnt, col, x, y, centro)


# ═══════════════════════════════════════════════════════════════════════════════
#  PANEL
# ═══════════════════════════════════════════════════════════════════════════════

def panel(x, y, w, h, col=None, borde=None, radio=6, alpha=215):
    """Panel semitransparente con borde más visible."""
    col = col or GRIS_PANEL
    borde = borde or GRIS_BORDE
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (*col, alpha), (0, 0, w, h), border_radius=radio)
    pantalla.blit(s, (x, y))
    # Borde doble: interior oscuro + exterior brillante
    pygame.draw.rect(pantalla, borde, (x, y, w, h), 2, border_radius=radio)


# ═══════════════════════════════════════════════════════════════════════════════
#  BOTÓN
# ═══════════════════════════════════════════════════════════════════════════════

def boton(texto, x, y, w, h, col_n, col_h, mouse,
          fnt=None, icono="", enabled=True):
    """Botón con hover y estado disabled. Retorna Rect."""
    fnt = fnt or F_MEDIA
    r = pygame.Rect(x, y, w, h)

    if not enabled:
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(s, (*col_n, 70), (0, 0, w, h), border_radius=5)
        pantalla.blit(s, (x, y))
        pygame.draw.rect(pantalla, FOSF_DARK, r, 1, border_radius=5)
        # Texto deshabilitado con sombra
        sombra = fnt.render(icono + texto, True, (0, 0, 0))
        sr = sombra.get_rect()
        sr.centerx = x + w // 2 + 1
        sr.centery = y + h // 2 + 1
        pantalla.blit(sombra, sr)
        sup = fnt.render(icono + texto, True, FOSF_DARK)
        sr2 = sup.get_rect()
        sr2.centerx = x + w // 2
        sr2.centery = y + h // 2
        pantalla.blit(sup, sr2)
        return r

    hov = r.collidepoint(mouse)
    c = col_h if hov else col_n
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (*c, 210), (0, 0, w, h), border_radius=5)
    if hov:
        pygame.draw.rect(s, (255, 255, 255, 30), (0, 0, w, h // 2),
                         border_radius=5)
    pantalla.blit(s, (x, y))
    bord = FOSF_VERDE if hov else (80, 160, 80)
    pygame.draw.rect(pantalla, bord, r, 2, border_radius=5)
    # Texto con sombra para legibilidad
    col_txt = BLANCO if hov else (180, 220, 180)
    sombra = fnt.render(icono + texto, True, (0, 0, 0))
    sr = sombra.get_rect()
    sr.centerx = x + w // 2 + 1
    sr.centery = y + h // 2 + 1
    pantalla.blit(sombra, sr)
    sup = fnt.render(icono + texto, True, col_txt)
    sr2 = sup.get_rect()
    sr2.centerx = x + w // 2
    sr2.centery = y + h // 2
    pantalla.blit(sup, sr2)
    return r


# ═══════════════════════════════════════════════════════════════════════════════
#  INPUT BOX — más alto y más legible
# ═══════════════════════════════════════════════════════════════════════════════

def input_box(texto, x, y, w, activo=True, placeholder="", max_len=20):
    """Caja de texto con cursor parpadeante. Altura aumentada a 42px."""
    H = 42  # era 36 — más espacio para texto
    col_b = FOSF_VERDE if activo else (0, 120, 40)
    r = pygame.Rect(x, y, w, H)
    s = pygame.Surface((w, H), pygame.SRCALPHA)
    # Fondo más visible cuando activo
    fondo_col = (0, 30, 12, 230) if activo else (0, 18, 8, 200)
    pygame.draw.rect(s, fondo_col, (0, 0, w, H), border_radius=5)
    pantalla.blit(s, (x, y))
    # Borde más grueso cuando activo
    grosor = 2 if activo else 1
    pygame.draw.rect(pantalla, col_b, r, grosor, border_radius=5)
    if activo:
        # Glow exterior
        pygame.draw.rect(pantalla, (*FOSF_VERDE, 50),
                         (x - 2, y - 2, w + 4, H + 4), 1, border_radius=6)
    cur = "|" if activo and int(time.time() * 2) % 2 == 0 else ""
    if not texto and placeholder:
        txt(placeholder, F_SMALL, (0, 120, 40), x + 10, y + 11)
    else:
        txt(texto + cur, F_BOLD, FOSF_VERDE, x + 10, y + 10)


# ═══════════════════════════════════════════════════════════════════════════════
#  BARRA DE TIEMPO
# ═══════════════════════════════════════════════════════════════════════════════

def barra_tiempo(x, y, w, h, restante, maximo,
                 col_ok=FOSF_VERDE, col_warn=AMBER, col_crit=ROJO_ALERTA):
    """Barra de progreso con cambio de color según urgencia."""
    pygame.draw.rect(pantalla, GRIS_PANEL, (x, y, w, h), border_radius=3)
    ratio = max(0, restante / maximo)
    fw = int(w * ratio)
    col = col_ok if ratio > 0.5 else (col_warn if ratio > 0.25 else col_crit)
    if fw > 0:
        pygame.draw.rect(pantalla, col, (x, y, fw, h), border_radius=3)
        s = pygame.Surface((fw, h // 2), pygame.SRCALPHA)
        s.fill((255, 255, 255, 25))
        pantalla.blit(s, (x, y))
    pygame.draw.rect(pantalla, FOSF_DIM, (x, y, w, h), 1, border_radius=3)
    if ratio < 0.25 and int(t() * 8) % 2 == 0:
        pygame.draw.rect(pantalla, BLANCO, (x, y, fw, h), border_radius=3)
    # Texto del tiempo más grande y con contraste
    txt(f"{max(0, int(restante))}s", F_SMALL, col, x + w + 8, y - 1)


# ═══════════════════════════════════════════════════════════════════════════════
#  HUD SUPERIOR — rediseñado para más legibilidad
# ═══════════════════════════════════════════════════════════════════════════════

def hud_superior(mision_num, titulo, color, vidas):
    """Dibuja la barra superior con info del agente y misión. Altura: 68px."""
    H = 68  # era 55 — más espacio
    s = pygame.Surface((ANCHO, H), pygame.SRCALPHA)
    pygame.draw.rect(s, (0, 10, 3, 250), (0, 0, ANCHO, H))
    pantalla.blit(s, (0, 0))
    pygame.draw.line(pantalla, color, (0, H), (ANCHO, H), 2)

    # ── Izquierda: ID y rango ──
    rango_nombre, rango_col = agente.rango()
    txt("AGT. CIPHER", F_MICRO, FOSF_DIM, 14, 6)
    txt(rango_nombre, F_SMALL, rango_col, 14, 22)  # más grande que antes

    # Cobertura mini — segmentos más grandes
    for i in range(10):
        c = FOSF_VERDE if i < agente.cobertura // 10 else FOSF_DARK
        pygame.draw.rect(pantalla, c, (14 + i * 14, 44, 11, 14),
                         border_radius=2)
    cov_col = FOSF_VERDE if agente.cobertura > 50 else ROJO_ALERTA
    txt(f"{agente.cobertura}%", F_MICRO, cov_col, 14 + 10 * 14 + 6, 46)

    # ── Centro: misión ── 
    txt_glow(f"[ MISIÓN 0{mision_num}: {titulo} ]",
             F_BOLD, color, ANCHO // 2, 6, centro=True)
    txt("CLASIFICADO — OJOS SOLO AUTORIZADOS",
        F_MICRO, FOSF_DIM, ANCHO // 2, 30, centro=True)

    # Herramientas — espaciado mejor
    hx = ANCHO // 2 - 120
    txt(f"◉ Scanner:{agente.herramientas['scanner']}", F_MICRO, CYAN_SCAN, hx, 48)
    txt(f"◉ Acel:{agente.herramientas['acelerador']}", F_MICRO, AMBER, hx + 130, 48)
    txt(f"◉ Escudo:{agente.herramientas['escudo']}", F_MICRO, FOSF_VERDE, hx + 245, 48)

    # ── Derecha: puntos, racha, vidas ──
    txt(f"PUNTOS: {agente.pts:06d}", F_SMALL, AMBER, ANCHO - 200, 6)
    if agente.racha > 1:
        racha_col = ((255, 215, 0) if agente.racha >= 5
                     else (ROJO_ALERTA if agente.racha >= 3 else AMBER))
        txt(f"RACHA ×{agente.racha}", F_SMALL, racha_col, ANCHO - 200, 26)

    for i in range(3):
        c = FOSF_VERDE if i < vidas else ROJO_DIM
        cx = ANCHO - 185 + i * 26
        cy = 52
        pygame.draw.circle(pantalla, c, (cx, cy), 9)  # era 7
        if i < vidas:
            c_brillo = tuple(min(255, x + 70) for x in c)
            pygame.draw.circle(pantalla, c_brillo, (cx - 2, cy - 3), 4)


# ═══════════════════════════════════════════════════════════════════════════════
#  INDICADOR DE PROGRESO — más grande y claro
# ═══════════════════════════════════════════════════════════════════════════════

def indicador_progreso(mision_actual):
    """Dibuja la barra de progreso de misiones en la parte inferior. Altura: 32px."""
    nombres = ["CÉSAR", "BASE64", "SHA-256", "DIFFIE-H."]
    H = 32   # era 16 — el doble de alto
    y = ALTO - H - 4
    w = (ANCHO - 100) // 4
    for i in range(4):
        x = 50 + i * w
        completada = i < mision_actual
        actual = i == mision_actual
        col_borde = (FOSF_VERDE if completada
                     else (AMBER if actual else (0, 60, 20)))
        col_fondo = ((0, 40, 15) if completada
                     else (GRIS_PANEL if actual else FONDO))
        pygame.draw.rect(pantalla, col_fondo,
                         (x + 1, y, w - 2, H), border_radius=5)
        pygame.draw.rect(pantalla, col_borde,
                         (x + 1, y, w - 2, H), 2 if actual else 1, border_radius=5)
        if completada:
            txt("✓ " + nombres[i], F_MICRO, FOSF_VERDE,
                x + w // 2, y + 8, centro=True)
        elif actual:
            txt("▶ " + nombres[i], F_MICRO, AMBER,
                x + w // 2, y + 8, centro=True)
        else:
            txt("— " + nombres[i], F_MICRO, (0, 70, 25),
                x + w // 2, y + 8, centro=True)