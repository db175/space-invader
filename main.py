import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the Screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invader")
Icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(Icon)

# Player Config
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Bullet "ready" ---> cannot see "fire" ----> can see
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready"

# Enemy Config
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 200))
    enemyX_change.append(4)
    enemyY_change.append(4)

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf',32)

def game_over_text():
    over_text = font.render("GAME OVER  Score : " + str(score_value),True,(255,255,255) )
    screen.blit(over_text,(200,250))

def show_score(x, y):
    score = over_font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(x1, y1, x2, y2):
    x = math.pow((x1 - x2), 2)
    y = math.pow((y1 - y2), 2)
    distance = math.sqrt(x + y)

    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True

# For screen display
while running:

    # Color of screen in RGB , have to update the screen
    screen.fill((0, 0, 0))
    # Background
    screen.blit(background, (-550, -500))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        # To contol the Player using keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
            if event.key == pygame.K_RIGHT:
                playerX_change += 4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[i] = 20000;
            game_over_text()
            break

        if enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] = -2.5
            enemyY[i] += 4
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = 2.5
            enemyY[i] += 3

        enemyX[i] += enemyX_change[i]

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY == 0:
        bullet_state = "ready"
        bulletY = playerY

    # To set the boundary of the player
    if playerX > 736:
        playerX = 736
    if playerX < 0:
        playerX = 0

    # To set the boundary of the enemy
    # Collision
    for i in range(num_of_enemies):
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bullet_state = "ready"
            bulletY = playerY
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 200)
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()

    # Call the Player and the Enemy
    player(playerX, playerY)

    for i in range(num_of_enemies):
        enemy(enemyX[i], enemyY[i], i)

    show_score(textX, textY)
    pygame.display.update()
