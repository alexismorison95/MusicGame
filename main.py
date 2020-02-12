import pygame
import time
import random

pygame.init()

# Display
width = 800
height = 600

FPS = 60

gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption('Music Ship')
clock = pygame.time.Clock()

square1 = pygame.image.load('imagenes/square3.png').convert_alpha()
square2 = pygame.image.load('imagenes/square4.png').convert_alpha()
square3 = pygame.image.load('imagenes/square5.png').convert_alpha()
square4 = pygame.image.load('imagenes/square7.png').convert_alpha()
square5 = pygame.image.load('imagenes/square6.png').convert_alpha()

line = pygame.image.load('imagenes/lineLarga2.png').convert_alpha()

heart = pygame.image.load('imagenes/heart3.png').convert_alpha()
heart2 = pygame.image.load('imagenes/heart8.png').convert_alpha()

music = pygame.mixer.music.load('musica/03-run-kurt-run-.mp3')


# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

blockColor = (53, 115, 255)

squareXs = [0, 160, 320, 480, 640]

# Tamanio de nave
naveSizeWidth = 116
naveSizeHeight = 116


# Class
class MyShip:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
    

class Square:
    def __init__(self, x, y, image1, heart, touch):
        self.x = x
        self.y = y
        self.image1 = image1
        self.heart = heart
        self.touch = touch



# Functions
# def cars_dodged(count):
#     font = pygame.font.SysFont(None, 25)
#     text = font.render("Score: " + str(count), True, black)
#     gameDisplay.blit(text, (5, 5))


# Imprimir las vidas en la navecita
def loadShip():
    shapeImage = pygame.image.load('imagenes/ship.png').convert_alpha()
    ship = MyShip(340, 460, shapeImage)
    
    return ship


def verificarShip(ship):
    if(ship.x > (width - naveSizeWidth)):
        ship.x = width - naveSizeWidth
    if(ship.x < 0):
        ship.x = 0

def showShip(ship):
    gameDisplay.blit(ship.image, (ship.x, ship.y))

def showImages(img, x, y):
    gameDisplay.blit(img, (x, y))

def showLines(line):
    xs = [-45, 115, 275, 435, 595, 755]
    for i in range(0, 6):
        showImages(line, xs[i], -60)


def showFPS():
    font = pygame.font.SysFont(None, 25)
    fpss = str(clock.get_fps())
    text = font.render("FPS: " + fpss[0:4], True, white)
    gameDisplay.blit(text, (710, 5))

# squareXs = [0, 160, 320, 480, 640]
def squarePos(x):
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


# def crash():
#     message_display('You Crashed')

#     return True


def game_loop():

    pygame.mixer.music.play(-1)

    color = -1
    inc = True

    pos_ship = 2
    lives = 3

    # squareXs = [0, 160, 320, 480, 640]
    squares = []
    for i in range(0, 10):
        if(i % 10 == 0):
            hr = Square(random.choice(squareXs) + 10, -80 * i, heart2, True, False)
            squares.append(hr)
        else:
            sq = Square(random.choice(squareXs), -80 * i, square1, False, False)
            squares.append(sq)

    showLines(line)

    hearts = [heart, heart, heart]

    #showImages(square, x_square, y_square)

    ship = loadShip()

    gameExit = False

    loops_num = 0

    while(not gameExit):

        for event in pygame.event.get():

            if(event.type == pygame.QUIT):
                pygame.quit()
                quit()
            
            if(event.type == pygame.KEYDOWN):

                if(event.key == pygame.K_LEFT):
                    if(pos_ship > 0):
                        pos_ship -= 1
                if(event.key == pygame.K_RIGHT):
                    if(pos_ship < 4):
                        pos_ship += 1


            # if(event.type == pygame.KEYUP):

            #     if(event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
            #         x_change = 0


        # FIN DE EVENTOS

        # Actualizo la posicion de mi auto
        ship.x = squareXs[pos_ship] + 25
        
        # Dibujo la superficie
        gameDisplay.fill(black)

        showLines(line)

        if(loops_num % (FPS * 0.2) == 0):
            if(color < 2 and inc):
                color += 1
                if(color == 2):
                    inc = False
            elif(color > 0 and not inc):
                color -= 1
                if(color == 0):
                    inc = True

        showFPS()

        for i in range(0, len(squares)):

            if(squares[i].touch):
                if(squares[i].heart):
                    showImages(squares[i].image1, squares[i].x, squares[i].y)
                else:
                    showImages(squares[i].image1, squares[i].x, squares[i].y)
            elif(color == 0 and not squares[i].heart):
                squares[i].image1 = square1
                showImages(squares[i].image1, squares[i].x, squares[i].y)
            elif(color == 1 and not squares[i].heart):
                squares[i].image1 = square2
                showImages(squares[i].image1, squares[i].x, squares[i].y)
            elif(color == 2 and not squares[i].heart):
                squares[i].image1 = square3
                showImages(squares[i].image1, squares[i].x, squares[i].y)
            else:
                showImages(squares[i].image1, squares[i].x, squares[i].y)
            
            squares[i].y += 7

        showShip(ship)

        for i in range(0, lives):
            showImages(hearts[i], 30*i, 0)


        # Verifico si hay una colision
        for i in range(0, len(squares)):
            if(squares[i].heart):
                if(ship.y < squares[i].y + 100 and ship.y > squares[i].y - 100):
                    if(pos_ship == squarePos(squares[i].x)):
                        if(lives < 3 and loops_num % (FPS * 0.3) == 0):
                            lives += 1
                            squares[i].image1 = heart
                            squares[i].touch = True
            elif(ship.y < squares[i].y + 70 and ship.y > squares[i].y - 50):
                if(pos_ship == squarePos(squares[i].x) and loops_num % (FPS * 0.3) == 0):
                    if(lives > 1):
                        lives -= 1
                        squares[i].image1 = square5
                        squares[i].touch = True
                        #time.sleep(1)
                    else:
                        game_loop()


        for i in range(0, len(squares)):
            if(squares[i].y > 600):
                squares[i].x = random.choice(squareXs)
                squares[i].y = -80
                squares[i].touch = False
                if(squares[i].heart):
                    squares[i].image1 = heart2
                else:
                    squares[i].image1 = square1


        # Actualizo la superficie
        pygame.display.update()
        loops_num += 1
        clock.tick(FPS) # FPS

game_loop()
pygame.quit()
quit()