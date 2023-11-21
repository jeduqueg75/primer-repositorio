import pygame
import random
import math
from pygame import mixer, Surface, SurfaceType

#iniciar pygame

pygame.init()
#crear pantalla
pantalla = pygame.display.set_mode((800, 600))

#titulo e icono
pygame.display.set_caption("space invader 1.0")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("espacio (1).jpg")


#agrgar sonido
mixer.music.load("MusicaFondo.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)


# variables del jugador
img_jugador = pygame.image.load("cohete1.png")
jugador_x = 368
jugador_y= 500
jugador_x_cambio = 0


# variables del alien
img_alien = []
alien_x = []
alien_y= []
alien_x_cambio = []
alien_y_cambio = []
cantidad_alien = 8

for a in range(cantidad_alien):
    img_alien.append(pygame.image.load("monstruo1.png"))
    alien_x.append(random.randint(0,736))
    alien_y.append(random.randint(50,200))
    alien_x_cambio.append(0.8)
    alien_y_cambio.append(30)



# variables de bala
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y= 500
bala_x_cambio = 0
bala_y_cambio = 1.3
bala_visible     = False

#score
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

#texto final juego
texto_fin = pygame.font.Font('freesansbold.ttf', 40)

def texto_final():
    mi_texto_final = texto_fin.render("***GAME OVER***", True, (255, 255, 255))
    pantalla.blit(mi_texto_final, (240, 280))

#funcion ver score

def mostrar_puntaje(x,y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x,y))

#funcion jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

#funcion alien
def alien(x, y, ene):
    pantalla.blit(img_alien[ene], (x, y))

def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x+16, y+10))


#funcion detectar impacto
def hay_impacto(x_1, y_1, x_2, y_2 ):
    distancia = math.sqrt(math.pow(x_2-x_1, 2)+(math.pow(y_2-y_1,2)))
    if distancia <27:
        return True
    else:
        return False


#loop juego
se_ejecuta = True
while se_ejecuta:

    #pantalla RBG
    pantalla.blit(fondo, (0,0))

    #iterar eventos
    for evento in pygame.event.get():

        #cerrar pantalla
        if evento.type == pygame.QUIT:
            se_ejecuta = False


        #presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.3
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.3
            if evento.key == pygame.K_SPACE:
                sonido_disparo = mixer.Sound("disparo.mp3")
                sonido_disparo.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

        #levantar flecha
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    #modificar posición jugador
    jugador_x += jugador_x_cambio

    #limites de la nave jugador
    if jugador_x <= 0:
        jugador_x  = 0

    elif jugador_x >= 736:
        jugador_x = 736

    #modificar posición enemigo
    for e in range(cantidad_alien):

        #fin del juego
        if alien_y[e] > 480:
            for k in range(cantidad_alien):
                alien_y[k] = 1000
            texto_final()
            break

        alien_x[e] += alien_x_cambio[e]

        #limites de la nave alien

        if alien_x[e] <= 0:
            alien_x_cambio[e]  = 0.5
            alien_y[e] += alien_y_cambio[e]

        elif alien_x[e] >= 736:
            alien_x_cambio[e] += -0.5
            alien_y[e] += alien_y_cambio[e]


        impacto = hay_impacto(alien_x[e], alien_y[e], bala_x, bala_y)

        if impacto:
            sonido_impacto= mixer.Sound("Golpe.mp3")
            sonido_impacto.play()
            bala_y = 500
            bala_visible = False
            puntaje +=1


            alien_x[e] = random.randint(0, 736)
            alien_y[e] = random.randint(50, 200)

        alien(alien_x[e], alien_y[e], e)

    #movimiento de la bala

    if bala_y <=-64:
        bala_y = 500
        bala_visible = False
    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    #impacto


    jugador(jugador_x, jugador_y)

    mostrar_puntaje(texto_x, texto_y)

    #actualizar pantalla
    pygame.display.update()

