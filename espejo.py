import pygame
import random
import sys
import math
import os

# Inicializar pygame
pygame.init()

# Configuración de pantalla responsive
info_pantalla = pygame.display.Info()
ANCHO = min(info_pantalla.current_w, 900)
ALTO = min(info_pantalla.current_h, 700)
if ANCHO < 400 or ALTO < 300:
    ANCHO = max(400, info_pantalla.current_w)
    ALTO = max(300, info_pantalla.current_h)

pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("Cazador de Monstruos Mágico")
reloj = pygame.time.Clock()

# Colores
NEGRO = (10, 5, 20)
DORADO = (255, 215, 0)
AZUL_MAGICO = (50, 150, 255)
BLANCO = (245, 240, 250)
VIOLETA = (180, 130, 255)
ROJO_OSCURO = (100, 20, 20)

# Fuentes (tamaño responsive)
tamano_fuente = max(20, min(ANCHO // 20, 36))
tamano_grande = max(40, min(ANCHO // 10, 72))
fuente = pygame.font.Font(None, tamano_fuente)
fuente_grande = pygame.font.Font(None, tamano_grande)

# Variables del juego
vidas = 3
puntuacion = 0
max_puntuacion = 999
game_over = False
monstruos = []
disparos = []
tiempo_vida_monstruo = 2.5  # segundos al inicio
tiempo_entre_spawn = 0.6  # segundos entre apariciones
spawn_timer = 0

# Cargar imagen del monstruo (el usuario puede cambiarla)
def cargar_imagen_monstruo(ruta="monstruo.png"):
    """Intenta cargar una imagen. Si no existe, crea un monstruo dibujado"""
    if os.path.exists(ruta):
        try:
            imagen = pygame.image.load(ruta)
            # Escalar a tamaño adecuado
            tamano = max(60, min(ANCHO // 6, 100))
            imagen = pygame.transform.scale(imagen, (tamano, tamano))
            return imagen, True
        except:
            print(f"No se pudo cargar {ruta}, usando monstruo dibujado")
            return None, False
    else:
        print(f"No se encontró {ruta}. Crea un archivo 'monstruo.png' en la misma carpeta")
        print("o usa el monstruo dibujado automáticamente.")
        return None, False

# Intentar cargar imagen personalizada
imagen_monstruo, usar_imagen = cargar_imagen_monstruo("monstruo.png")

class Monstruo:
    def __init__(self, x, y, tiempo_vida):
        self.x = x
        self.y = y
        self.tiempo_vida = tiempo_vida
        self.tiempo_creacion = pygame.time.get_ticks() / 1000.0
        self.activo = True
        self.tamano = max(60, min(ANCHO // 6, 100))
        
    def esta_vivo(self, tiempo_actual):
        return (tiempo_actual - self.tiempo_creacion) < self.tiempo_vida
    
    def dibujar(self, superficie, tiempo_actual):
        if usar_imagen and imagen_monstruo:
            # Dibujar imagen del monstruo
            rect_imagen = imagen_monstruo.get_rect(center=(int(self.x), int(self.y)))
            superficie.blit(imagen_monstruo, rect_imagen)
            
            # Barra de vida (opcional pero útil)
            resto = self.tiempo_vida - (tiempo_actual - self.tiempo_creacion)
            porcentaje = max(0, resto / self.tiempo_vida)
            ancho_barra = self.tamano
            alto_barra = 6
            x_barra = self.x - ancho_barra // 2
            y_barra = self.y - self.tamano // 2 - 10
            
            pygame.draw.rect(superficie, (50, 50, 50), (x_barra, y_barra, ancho_barra, alto_barra))
            if porcentaje > 0.6:
                color_barra = (50, 200, 100)
            elif porcentaje > 0.3:
                color_barra = (255, 215, 0)
            else:
                color_barra = (200, 50, 50)
            pygame.draw.rect(superficie, color_barra, (x_barra, y_barra, ancho_barra * porcentaje, alto_barra))
        else:
            # Monstruo dibujado (alternativa)
            resto = self.tiempo_vida - (tiempo_actual - self.tiempo_creacion)
            if resto < 0.5 and int(tiempo_actual * 10) % 2 == 0:
                color_cuerpo = (255, 50, 50)
            else:
                color_cuerpo = (139, 69, 19)hjgjgh
            
            # Cuerpo
            pygame.draw.circle(superficie, color_cuerpo, (int(self.x), int(self.y)), self.tamano // 2)
            # Ojos
            tam_ojo = self.tamano // 5
            offset = self.tamano // 4
            pygame.draw.circle(superficie, BLANCO, (int(self.x - offset), int(self.y - offset)), tam_ojo)
            pygame.draw.circle(superficie, BLANCO, (int(self.x + offset), int(self.y - offset)), tam_ojo)
            pygame.draw.circle(superficie, NEGRO, (int(self.x - offset + 2), int(self.y - offset)), tam_ojo // 2)
            pygame.draw.circle(superficie, NEGRO, (int(self.x + offset + 2), int(self.y - offset)), tam_ojo // 2)
            # Boca
            pygame.draw.arc(superficie, NEGRO, 
                           (self.x - self.tamano//3, self.y - self.tamano//6, 
                            self.tamano*2//3, self.tamano//2), 
                           0.1, math.pi - 0.1, 3)
            # Cuernos
            puntos1 = [(self.x - self.tamano//3, self.y - self.tamano//2),
                      (self.x - self.tamano//2, self.y - self.tamano//1.5),
                      (self.x - self.tamano//4, self.y - self.tamano//2)]
            puntos2 = [(self.x + self.tamano//3, self.y - self.tamano//2),
                      (self.x + self.tamano//2, self.y - self.tamano//1.5),
                      (self.x + self.tamano//4, self.y - self.tamano//2)]
            pygame.draw.polygon(superficie, (101, 67, 33), puntos1)
            pygame.draw.polygon(superficie, (101, 67, 33), puntos2)
            
            # Barra de vida
            porcentaje = resto / self.tiempo_vida
            ancho_barra = self.tamano
            alto_barra = 6
            x_barra = self.x - ancho_barra // 2
            y_barra = self.y - self.tamano // 2 - 10
            pygame.draw.rect(superficie, (50, 50, 50), (x_barra, y_barra, ancho_barra, alto_barra))
            if porcentaje > 0.6:
                color_barra = (50, 200, 100)
            elif porcentaje > 0.3:
                color_barra = (255, 215, 0)
            else:
                color_barra = (200, 50, 50)
            pygame.draw.rect(superficie, color_barra, (x_barra, y_barra, ancho_barra * porcentaje, alto_barra))
    
    def colisiona_con_punto(self, px, py):
        distancia = math.sqrt((px - self.x)**2 + (py - self.y)**2)
        return distancia < self.tamano // 2

class Hechizo:
    def __init__(self, origen_x, origen_y, destino_x, destino_y):
        self.pos = [origen_x, origen_y]
        self.destino = (destino_x, destino_y)
        self.velocidad = 15
        self.activo = True
        
    def mover(self):
        dx = self.destino[0] - self.pos[0]
        dy = self.destino[1] - self.pos[1]
        distancia = max(1, math.sqrt(dx**2 + dy**2))
        if distancia < self.velocidad:
            self.activo = False
        else:
            self.pos[0] += (dx / distancia) * self.velocidad
            self.pos[1] += (dy / distancia) * self.velocidad
    
    def dibujar(self, superficie):
        # Efecto de hechizo brillante
        pygame.draw.circle(superficie, AZUL_MAGICO, (int(self.pos[0]), int(self.pos[1])), 10)
        pygame.draw.circle(superficie, BLANCO, (int(self.pos[0]), int(self.pos[1])), 4)
        pygame.draw.circle(superficie, VIOLETA, (int(self.pos[0]), int(self.pos[1])), 7, 2)

def mostrar_texto(texto, color, x, y, tamano="normal"):
    if tamano == "grande":
        superficie = fuente_grande.render(texto, True, color)
    else:
        superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=(x, y))
    pantalla.blit(superficie, rect)

def spawn_monstruo():
    x = random.randint(60, ANCHO - 60)
    y = random.randint(60, ALTO - 60)
    return Monstruo(x, y, tiempo_vida_monstruo)

def perder_vida():
    global vidas, game_over
    vidas -= 1
    if vidas <= 0:
        game_over = True

def actualizar_juego(tiempo_actual):
    global monstruos, disparos, puntuacion, spawn_timer, tiempo_vida_monstruo, tiempo_entre_spawn
    
    # Actualizar dificultad (más rápida)
    # El tiempo de vida baja de 2.5s a 0.4s
    tiempo_vida_monstruo = max(0.4, 2.5 - (puntuacion / 350))
    # Los monstruos aparecen más rápido: de 0.6s a 0.2s
    tiempo_entre_spawn = max(0.3, 1.0 - (puntuacion / 1800))
    
    # Spawn de monstruos
    spawn_timer += 1.54 / 60.0
    if spawn_timer >= tiempo_entre_spawn and len(monstruos) < 15:
        monstruos.append(spawn_monstruo())
        spawn_timer = 0
    
    # Mover hechizos
    for hechizo in disparos[:]:
        hechizo.mover()
        if not hechizo.activo:
            disparos.remove(hechizo)
    
    # Verificar colisiones hechizo-monstruo
    for hechizo in disparos[:]:
        for monstruo in monstruos[:]:
            if monstruo.colisiona_con_punto(hechizo.pos[0], hechizo.pos[1]):
                if monstruo in monstruos:
                    monstruos.remove(monstruo)
                    puntuacion = min(puntuacion + 1, max_puntuacion)
                if hechizo in disparos:
                    disparos.remove(hechizo)
                break
    
    # Verificar monstruos que expiran
    monstruos_vivos = []
    for monstruo in monstruos:
        if monstruo.esta_vivo(tiempo_actual):
            monstruos_vivos.append(monstruo)
        else:
            perder_vida()
    monstruos = monstruos_vivos

#Imagen de nave en el centro 
def cargar_imagen_nave(ruta="nave.png"):
    """Intenta cargar una imagen para la nave. Si no existe, se dibuja una nave simple."""
    if os.path.exists(ruta):
        try:
            imagen = pygame.image.load(ruta)
            tamano = max(80, min(ANCHO // 5, 150))
            imagen = pygame.transform.scale(imagen, (tamano, tamano))
            return imagen
        except:
            print(f"No se pudo cargar {ruta}, usando nave dibujada")
            return None
    else:
        print(f"No se encontró {ruta}. Crea un archivo 'nave.png' en la misma carpeta")
        print("o usa la nave dibujada automáticamente.")
        return None, False
    
imagen_nave, usar_imagen= cargar_imagen_nave("nave.png")





def dibujar():
    pantalla.fill(NEGRO)
    
    # Fondo místico
    for _ in range(100):
        x = random.randint(0, ANCHO)
        y = random.randint(0, ALTO)
        pygame.draw.circle(pantalla, (80, 60, 120), (x, y), 1)
    
    # Círculo mágico en el centro (efecto visual)
    centro_x, centro_y = ANCHO // 2, ALTO // 2
    for i in range(3):
        radio = 100 + i * 30
        alpha = pygame.time.get_ticks() / 1000.0
        color = (100 + int(50 * math.sin(alpha)), 50, 150)
        pygame.draw.circle(pantalla, color, (centro_x, centro_y), radio, 2)
    
    # Dibujar hechizos
    for hechizo in disparos:
        hechizo.dibujar(pantalla)
    
    # Dibujar monstruos
    tiempo_actual = pygame.time.get_ticks() / 1000.0
    for monstruo in monstruos:
        monstruo.dibujar(pantalla, tiempo_actual)
    
    #Dibujar nave
    

    # UI
    mostrar_texto(f"Puntuación: {puntuacion}", DORADO, ANCHO // 6, 30)
    mostrar_texto(f"Vidas: {vidas}", AZUL_MAGICO, ANCHO - ANCHO // 6, 30)
    
    # Instrucción
    if not game_over:
        mostrar_texto("¡Toca en cualquier lugar para lanzar hechizos!", VIOLETA, ANCHO // 2, ALTO - 30, "normal")
    
    if game_over:
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        pantalla.blit(s, (0, 0))
        
        mostrar_texto("JUEGO TERMINADO", DORADO, ANCHO//2, ALTO//2 - 60, "grande")
        mostrar_texto(f"Puntuación final: {puntuacion}", BLANCO, ANCHO//2, ALTO//2, "normal")
        
        if puntuacion >= 700:
            msg = "¡MAESTRO CAZADOR! ✨"
        elif puntuacion >= 400:
            msg = "¡Excelentes reflejos mágicos!"
        elif puntuacion >= 150:
            msg = "¡Buen trabajo! Sigue practicando."
        else:
            msg = "No te rindas, el mundo mágico te necesita."
        mostrar_texto(msg, VIOLETA, ANCHO//2, ALTO//2 + 50, "normal")
        
        mostrar_texto("Presiona R para reiniciar", AZUL_MAGICO, ANCHO//2, ALTO - 50, "normal")
    
    pygame.display.flip()

def reiniciar_juego():
    global vidas, puntuacion, monstruos, disparos, game_over, spawn_timer
    vidas = 3
    puntuacion = 0
    monstruos = []
    disparos = []
    game_over = False
    spawn_timer = 0

# Bucle principal
jugando = True
while jugando:
    tiempo_actual = pygame.time.get_ticks() / 1000.0
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        
        # Disparar con clic/toque en cualquier lugar
        if evento.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Lanzar hechizo desde el centro hacia el punto tocado
            hechizo = Hechizo(ANCHO//2, ALTO//2, mouse_x, mouse_y)
            disparos.append(hechizo)
        
        # Para dispositivos táctiles
        if evento.type == pygame.FINGERDOWN and not game_over:
            x = evento.x * ANCHO
            y = evento.y * ALTO
            hechizo = Hechizo(ANCHO//2, ALTO//2, x, y)
            disparos.append(hechizo)
        
        # Teclado
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                reiniciar_juego()
            if evento.key == pygame.K_ESCAPE:
                jugando = False
    
    if not game_over:
        actualizar_juego(tiempo_actual)
    
    dibujar()
    reloj.tick(60)

pygame.quit()
sys.exit()