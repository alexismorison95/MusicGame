import pygame
import time
import random

pygame.init()

# Display
ancho = 800
alto = 650

FPS = 60

gameDisplay = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Morris GAME')
clock = pygame.time.Clock()

obst1Img = pygame.image.load('imagenes/obstaculo/obst1.png').convert_alpha()
obst2Img = pygame.image.load('imagenes/obstaculo/obst2.png').convert_alpha()
obst3Img = pygame.image.load('imagenes/obstaculo/obst3.png').convert_alpha()
obstChocadoImg = pygame.image.load('imagenes/obstaculo/obst4.png').convert_alpha()

lineaImg = pygame.image.load('imagenes/linea/lineLargaTransparente.png').convert_alpha()

vidaImg = pygame.image.load('imagenes/corazon/corazon.png').convert_alpha()

naveImgs = [pygame.image.load('imagenes/nave/nave1.png').convert_alpha(),
            pygame.image.load('imagenes/nave/nave2.png').convert_alpha(),
            pygame.image.load('imagenes/nave/nave3.png').convert_alpha()]

musica = pygame.mixer.music.load('musica/01-run-kurt-run.mp3')


# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

columnas = [0, 160, 320, 480, 640]

# Tamanio de nave
naveAncho = 116
naveAlto = 116


# Class
class Nave:
    def __init__(self, x, y, imagen):
        self.x = x
        self.y = y
        self.imagen = imagen
    

class Obstaculo:
    def __init__(self, x, y, imagen, isCorazon, isTocado):
        self.x = x
        self.y = y
        self.imagen = imagen
        self.isCorazon = isCorazon
        self.isTocado = isTocado



# Functions
# def cars_dodged(count):
#     font = pygame.font.SysFont(None, 25)
#     text = font.render("Score: " + str(count), True, black)
#     gameDisplay.blit(text, (5, 5))


# Funcion que verifica que la nave no se salga de la pantalla..
# def verificarNave(nave):
#     if(nave.x > (ancho - naveAncho)):
#         nave.x = ancho - naveAncho
#     if(nave.x < 0):
#         nave.x = 0

# Funcion para mostrar mi nave
def mostrarNave(nave):
    gameDisplay.blit(nave.imagen, (nave.x, nave.y))

# Funcion basica para mostrar cualquier imagen
def mostrarImagen(img, x, y):
    gameDisplay.blit(img, (x, y))

# Funcion para mostrar las lineas de fondo
def mostrarLineas(linea):
    xs = [-45, 115, 275, 435, 595, 755]
    for i in range(0, 6):
        mostrarImagen(linea, xs[i], -60)

# Funcion para mostrar los FPS
def showFPS():
    font = pygame.font.SysFont(None, 25)
    fpss = str(clock.get_fps())
    text = font.render("FPS: " + fpss[0:4], True, white)
    gameDisplay.blit(text, (710, 5))

# Funcion para obtener la columna a la que pertenece un obstaculo
def obstaculoColumna(x):
    if x >= 0 and x < 160: return 0
    if x >= 160 and x < 320: return 1
    if x >= 320 and x < 480: return 2
    if x >= 480 and x < 640: return 3
    if x >= 480: return 4

# def text_objects(text, font, color):
#     textSurface = font.render(text, True, color)
#     return textSurface, textSurface.get_rect()


# def message_display(text):
#     largeText = pygame.font.Font('freesansbold.ttf', 50)
#     textSurf, textRect = text_objects(text, largeText, red)
#     textRect.center = ((width/2), (height/2))
#     gameDisplay.blit(textSurf, textRect)

#     pygame.display.update()

#     time.sleep(2)


def game_loop():

    # Reproduzco el tema cargado
    pygame.mixer.music.play(-1)

    # Variables para alternar entre los colores de los obstaculos
    color = -1
    inc = True

    # Posicion inicial de mi nave
    posNave = 2

    # Cantidad de vidas
    cantVidas = 3

    # Creo una lista de obstaculos y vidas
    obstaculos = []
    for i in range(0, 10):
        if(i % 10 == 0):
            aux = Obstaculo(random.choice(columnas) + 10, -80 * i, vidaImg, True, False)
            obstaculos.append(aux)
        else:
            aux = Obstaculo(random.choice(columnas), -80 * i, obst1Img, False, False)
            obstaculos.append(aux)

    # Cargo mi nave
    nave = Nave(340, 460, naveImgs[2])

    gameExit = False

    loops_num = 0

    while(not gameExit):

        # EVENTOS DEL TECLADO
        for event in pygame.event.get():

            if(event.type == pygame.QUIT):
                pygame.quit()
                quit()
            
            if(event.type == pygame.KEYDOWN):

                if(event.key == pygame.K_LEFT):
                    if(posNave > 0):
                        posNave -= 1
                if(event.key == pygame.K_RIGHT):
                    if(posNave < 4):
                        posNave += 1

        # FIN DE EVENTOS

        # Actualizo la posicion de mi nave a la columna correspondiente
        nave.x = columnas[posNave] + 25
        
        # Dibujo las superficies
        # Fondo negro
        gameDisplay.fill(black)

        # Dibujo las lineas de las columnas
        mostrarLineas(lineaImg)

        # Cada 20 FPS actualizo los colores de los obstaculos
        if(loops_num % (FPS * 0.2) == 0):
            if(color < 2 and inc):
                color += 1
                if(color == 2):
                    inc = False
            elif(color > 0 and not inc):
                color -= 1
                if(color == 0):
                    inc = True

        # Muestro los FPS
        showFPS()

        # Muestro los obstaculos
        for i in range(0, len(obstaculos)):

            # Primero si el obstaculo fue tocado
            if(obstaculos[i].isTocado):
                # Pregunto si toque una vida
                if(obstaculos[i].isCorazon):
                    mostrarImagen(obstaculos[i].imagen, obstaculos[i].x, obstaculos[i].y)
                # Sino quiere decir que toque un obstaculo
                else:
                    mostrarImagen(obstaculos[i].imagen, obstaculos[i].x, obstaculos[i].y)
            # Si no fue tocado asigno los colores a los obstaculos y los muestro
            elif(color == 0 and not obstaculos[i].isCorazon):
                obstaculos[i].imagen = obst1Img
                mostrarImagen(obstaculos[i].imagen, obstaculos[i].x, obstaculos[i].y)
            elif(color == 1 and not obstaculos[i].isCorazon):
                obstaculos[i].imagen = obst2Img
                mostrarImagen(obstaculos[i].imagen, obstaculos[i].x, obstaculos[i].y)
            elif(color == 2 and not obstaculos[i].isCorazon):
                obstaculos[i].imagen = obst3Img
                mostrarImagen(obstaculos[i].imagen, obstaculos[i].x, obstaculos[i].y)
            # Sino muestro el corazon
            else:
                mostrarImagen(obstaculos[i].imagen, obstaculos[i].x, obstaculos[i].y)
            
            # Aumento la componente 'y' para que se muevan
            obstaculos[i].y += 7

        # Muestro la nave
        mostrarNave(nave)


        # Verifico si hay una colision
        for i in range(0, len(obstaculos)):
            # Verifico primero si toque una vida
            if(obstaculos[i].isCorazon):
                # Verifico la componente y
                if(nave.y < obstaculos[i].y + 100 and nave.y > obstaculos[i].y - 100):
                    # Verifico la columna
                    if(posNave == obstaculoColumna(obstaculos[i].x)):
                        # Si tengo menos de 3 vidas aumento una vida
                        if(cantVidas < 3 and loops_num % (FPS * 0.3) == 0):
                            # Aumento el contador
                            cantVidas += 1
                            # TODO: Conseguir una imagen para las vidas tocadas
                            obstaculos[i].imagen = vidaImg
                            # Asigno a la vida como tocada
                            obstaculos[i].isTocado = True
                            # Actualizo la imagen de la nave
                            nave.imagen = naveImgs[cantVidas-1]

            # Sino toque un obstaculo y verifico la componente y
            elif(nave.y < obstaculos[i].y + 70 and nave.y > obstaculos[i].y - 50):
                # Verifico la columna
                if(posNave == obstaculoColumna(obstaculos[i].x) and loops_num % (FPS * 0.3) == 0):
                    # Si tengo vidas disponibles
                    if(cantVidas > 1):
                        # Decremento el contador
                        cantVidas -= 1
                        # Actualizo la imagen del obstaculo chocado
                        obstaculos[i].imagen = obstChocadoImg
                        # Lo marco como chocado
                        obstaculos[i].isTocado = True
                        # Actualizo la imagen de la nave
                        nave.imagen = naveImgs[cantVidas-1]
                    # Si no, ya no me quedan vidas
                    else:
                        game_loop()

        # Cuando los obstaculos se salen de la pantalla tengo que reiniciarlos
        # De momento es todo al azar
        for i in range(0, len(obstaculos)):
            if(obstaculos[i].y > 625):
                # Elijo la columna
                obstaculos[i].x = random.choice(columnas)
                # Lo mando para arriba
                obstaculos[i].y = -80
                # Lo marco como no chocado
                obstaculos[i].isTocado = False
                # Si es una vida reinicio la imagen
                if(obstaculos[i].isCorazon):
                    obstaculos[i].imagen = vidaImg
                # Sino, es un obstaculo, reinicio la imagen
                else:
                    obstaculos[i].imagen = obst1Img


        # Actualizo la superficie
        pygame.display.update()
        loops_num += 1
        clock.tick(FPS) # Set FPS

game_loop()
pygame.quit()
quit()