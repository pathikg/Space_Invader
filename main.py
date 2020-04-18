import pygame
import random
import math

# initialise pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('Background.jpg')
pygame.display.set_icon(background)

# Player
PlayerImg = pygame.image.load('Player.png')
PlayerX = 370
PlayerY = 500
PlayerX_change = 0
PlayerY_change = 0


def player(x, y):
    screen.blit(PlayerImg, (x, y))


# Enemy
# for Multiple enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(6):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 746))
    enemyY.append(random.randint(20, 215))
    enemyX_change.append(5)
    enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Bullet
# Ready State means We see the bullet on screen
# Fire bullet is moving
BulletImg = pygame.image.load('bullet.png')
BulletX = PlayerX
BulletY = 500
BulletX_change = 0
BulletY_change = 20
Bullet_state = "ready"


def Bullet(x, y):
    screen.blit(BulletImg, (x, y))


def fire_bullet(x, y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, BulletX, BulletY):
    distance = math.hypot(enemyX - BulletX, enemyY - BulletY)
    if distance < 27:
        return True
    else:
        return False


# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10


def show_score(x, y):
    scor = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(scor, (x, y))


# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over = over_font.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(over, (200, 250))


# game loop
running = True
while running:
    # screen background RGB
    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if key is pressed or released ?
        if event.type == pygame.KEYDOWN:

            # if pressed by what amount position should change ? and firing bullet
            if event.key == pygame.K_LEFT:
                PlayerX_change = -2
            if event.key == pygame.K_RIGHT:
                PlayerX_change = +2
            if event.key == pygame.K_SPACE:
                if Bullet_state is "ready":
                    BulletX = PlayerX
                    fire_bullet(BulletX, BulletY)

        # if released stop changing X coordinate
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerX_change = 0

    # Changing X coordinate
    PlayerX += PlayerX_change

    # Boundary for spaceship
    if PlayerX >= 736:
        PlayerX = 736
    elif PlayerX < 0:
        PlayerX = 0

    # Changing X coordinate of enemy
    enemyX += enemyX_change

    # Boundary for spaceship
    for i in range(6):

        # Game Over
        if enemyY[i] > 460:
            for j in range(6):
                for k in range(6):
                    enemyY[k] = 2000
            game_over_text()
            break

        # Changing X coordinate of enemy
        enemyX[i] += enemyX_change[i]

        #setting boundary
        if enemyX[i] >= 736:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] < 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], BulletX, BulletY)
        if collision:
            enemyX[i] = random.randint(0, 746)
            enemyY[i] = random.randint(15, 150)
            BulletY = 480
            Bullet_state = "ready"
            score += 1
            print(score)

        enemy(enemyX[i], enemyY[i], i)

    # for bullet
    if BulletY <= 0:
        BulletY = 500
        Bullet_state = "ready"

    if Bullet_state is "fire":
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    player(PlayerX, PlayerY)
    show_score(textX, textY)
    pygame.display.update()
