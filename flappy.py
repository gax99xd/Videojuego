import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuraciones de la pantalla
ANCHO = 400
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Flappy Pygame")
reloj = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL_CIELO = (135, 206, 235)
VERDE = (34, 139, 34)
AMARILLO = (255, 215, 0)

# Configuraciones del juego
GRAVEDAD = 0.5
FUERZA_SALTO = -8
VELOCIDAD_TUBOS = 4
ESPACIO_ENTRE_TUBOS = 150

class Pajaro:
    def __init__(self):
        self.x = 50
        self.y = ALTO // 2
        self.velocidad = 0
        self.tamano = 30
        self.rect = pygame.Rect(self.x, self.y, self.tamano, self.tamano)

    def saltar(self):
        self.velocidad = FUERZA_SALTO

    def mover(self):
        self.velocidad += GRAVEDAD
        self.y += self.velocidad
        self.rect.y = self.y

    def dibujar(self):
        pygame.draw.rect(pantalla, AMARILLO, self.rect)

class Tubo:
    def __init__(self):
        self.x = ANCHO
        self.ancho = 60
        self.alto_superior = random.randint(50, 350)
        self.alto_inferior = ALTO - self.alto_superior - ESPACIO_ENTRE_TUBOS
        
        self.rect_sup = pygame.Rect(self.x, 0, self.ancho, self.alto_superior)
        self.rect_inf = pygame.Rect(self.x, ALTO - self.alto_inferior, self.ancho, self.alto_inferior)
        self.pasado = False

    def mover(self):
        self.x -= VELOCIDAD_TUBOS
        self.rect_sup.x = self.x
        self.rect_inf.x = self.x

    def dibujar(self):
        pygame.draw.rect(pantalla, VERDE, self.rect_sup)
        pygame.draw.rect(pantalla, VERDE, self.rect_inf)

def mostrar_texto(texto, fuente, color, x, y):
    superficie = fuente.render(texto, True, color)
    rectangulo = superficie.get_rect(center=(x, y))
    pantalla.blit(superficie, rectangulo)

def juego():
    pajaro = Pajaro()
    tubos = []
    puntos = 0
    fuente = pygame.font.SysFont("Arial", 36, bold=True)
    
    # Temporizador para crear tubos nuevos
    TIEMPO_TUBOS = pygame.USEREVENT
    pygame.time.set_timer(TIEMPO_TUBOS, 1500)

    jugando = True
    while jugando:
        # 1. Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pajaro.saltar()
            if evento.type == TIEMPO_TUBOS:
                tubos.append(Tubo())

        # 2. Lógica y movimiento
        pajaro.mover()

        for tubo in tubos:
            tubo.mover()
            
            # Comprobar colisiones
            if pajaro.rect.colliderect(tubo.rect_sup) or pajaro.rect.colliderect(tubo.rect_inf):
                jugando = False
            
            # Puntuación
            if not tubo.pasado and tubo.x < pajaro.x:
                puntos += 1
                tubo.pasado = True

        # Eliminar tubos que salen de la pantalla
        tubos = [tubo for tubo in tubos if tubo.x + tubo.ancho > 0]

        # Comprobar límites de pantalla (suelo y techo)
        if pajaro.y > ALTO or pajaro.y < 0:
            jugando = False

        # 3. Dibujar en pantalla
        pantalla.fill(AZUL_CIELO)
        pajaro.dibujar()
        for tubo in tubos:
            tubo.dibujar()
            
        mostrar_texto(str(puntos), fuente, BLANCO, ANCHO // 2, 50)

        pygame.display.update()
        reloj.tick(60) # 60 FPS

    # Pantalla de fin de juego
    pantalla.fill(NEGRO)
    mostrar_texto("¡JUEGO TERMINADO!", fuente, BLANCO, ANCHO // 2, ALTO // 2 - 50)
    mostrar_texto(f"Puntos: {puntos}", fuente, BLANCO, ANCHO // 2, ALTO // 2 + 10)
    mostrar_texto("Presiona ESPACIO para reiniciar", pygame.font.SysFont("Arial", 20), BLANCO, ANCHO // 2, ALTO // 2 + 70)
    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    juego() # Reiniciar juego

# Iniciar el juego
juego()