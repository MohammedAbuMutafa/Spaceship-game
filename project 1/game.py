import sys
import time
import pygame
import random
import os
import math
from pygame.locals import *
pygame.init()
WIDTH,HEIGHT= 900,1000
FPS= 144
VEL=2
SCORE_FONT=pygame.font.SysFont('comicsans', 40)
WIN= pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First game")
SPACESHIP_IMG= pygame.image.load(os.path.join("Assets", "spaceship_yellow.png")) #use os so it works in all operating systems.
SPACESHIP_IMG= pygame.transform.rotate(pygame.transform.scale(SPACESHIP_IMG,(60,50)),180)
ENEMY_SPACESHIP_IMG= pygame.image.load(os.path.join("Assets", "spaceship_red.png")) #use os so it works in all operating systems.
ENEMY_SPACESHIP_IMG= pygame.transform.rotate(pygame.transform.scale(ENEMY_SPACESHIP_IMG,(60,50)),360)
BOSS_IMG= pygame.image.load(os.path.join("Assets", "boss1.png"))
BOSS_IMG= pygame.transform.rotate(pygame.transform.scale(BOSS_IMG,(440,240)),360)
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/shoot.wav')
BULLET_VEL = 7
MAX_BULLETS = 5
SPACESHIP_HIT = pygame.USEREVENT + 1
ENEMY_HIT = pygame.USEREVENT + 2

BORDER = pygame.Rect(0, 700, 900, 10)
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.gif')), (WIDTH, HEIGHT))

def draw_window(spaceship,enemy,spaceship_bullets,score,tries,boss,boss_bullets):
    WIN.fill((255,255,255))
    WIN.blit(SPACE, (0, 0))
    WIN.blit(SPACESHIP_IMG,(spaceship.x, spaceship.y))

    score_text=SCORE_FONT.render(
        "Score: " + str(score), 1, (255,255,255))
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 10, 900))
    Tries=SCORE_FONT.render(
        "Tries: " + str(tries), 1, (255,255,255))
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 10, 900))
    pygame.draw.rect(WIN, (0,0,0), BORDER)
    for i in enemy:
        WIN.blit(ENEMY_SPACESHIP_IMG,(i.x, i.y))
    for bullet in spaceship_bullets:
        pygame.draw.rect(WIN, (255,255,0), bullet)
    for bullet in boss_bullets:
        pygame.draw.rect(WIN, (255,255,0), bullet)
    if score>10:
        WIN.blit(BOSS_IMG,(boss.x, boss.y))
    if boss.y <160 and score>10:
        boss.y+= 2
    pygame.display.update()
    



def handle_bullets(enemy_bullets, spaceship_bullets, enemy, spaceship,score,boss_bullets):
    for bullet in spaceship_bullets:
        bullet.y -= BULLET_VEL
        if enemy[0].colliderect(bullet):
            pygame.event.post(pygame.event.Event(ENEMY_HIT))
            enemy.remove(enemy[0])
            spaceship_bullets.remove(bullet)
        if len(enemy) >= 2 and enemy[1].colliderect(bullet):
            spaceship_bullets.remove(bullet)
            enemy.remove(enemy[1])
        if len(enemy) >= 3 and enemy[2].colliderect(bullet):
            pygame.event.post(pygame.event.Event(ENEMY_HIT))
            spaceship_bullets.remove(bullet)
            enemy.remove(enemy[2])
        elif bullet.y < 0:
            spaceship_bullets.remove(bullet)

    for bullet in enemy_bullets:
        bullet.x -= BULLET_VEL
        if pygame.sprite.collide_rect(spaceship,bullet):
            pygame.event.post(pygame.event.Event(SPACESHIP_HIT))
            enemy_bullets.remove(bullet)
        elif bullet.x < 0:
            enemy_bullets.remove(bullet)
    for bullet in boss_bullets:
        bullet.y += BULLET_VEL
        if spaceship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SPACESHIP_HIT))
            boss_bullets.remove(bullet)
        elif bullet.x < 0:
            boss_bullets.remove(bullet)
def spaceship_move(keys_pressed,spaceship):
        if keys_pressed[pygame.K_a] and spaceship.x - 5 > 0:
            spaceship.x-=5 
        if keys_pressed[pygame.K_d] and spaceship.x + 5 + spaceship.width < WIDTH:
            spaceship.x+=5 
        if keys_pressed[pygame.K_w] and spaceship.y - 5 >0:
            spaceship.y-=5 
        if keys_pressed[pygame.K_s] and spaceship.y + 5 + spaceship.height < HEIGHT:
            spaceship.y+=5 
def enemy_move(enemy):
    enemy[0].y +=1
    enemy[1].y +=1
    if len(enemy) >=3:
        enemy[2].y +=1
    if enemy[0].y >= HEIGHT:
        enemy.remove(enemy[0])
    


def make_enemy():
    enemy = pygame.Rect(random.randint(0, 900) ,0, 60,50)
    return enemy

def boss_movement(boss,score):
    global VEL
    if score > 10 and boss.y>=160:
        boss.x+= VEL
    if score> 10 and boss.y>=160 and boss.x == 450:
        VEL=-2
    if score> 10 and boss.y>=160 and boss.x == 0:
        VEL=2

def main():
    spaceship= pygame.Rect(450-60,800,60,50)
    enemy_bullets = []
    spaceship_bullets = []
    boss_bullets=[]

    score=0
    tries=0
    enemy=[make_enemy(),make_enemy(),make_enemy()]
    counter=0
    clock=pygame.time.Clock()
    list = [10,20,30, 40, 50]
    run = True
    boss = pygame.Rect(220,-200, 60,50)
    while run:
        boss_movement(boss,score)
        enemy_move(enemy)
        if len(enemy) < 3:
            enemy.append(make_enemy())
        clock.tick(FPS) #usually 60
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run= False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(spaceship_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(spaceship.x + spaceship.width, spaceship.y + spaceship.height//2 - 2, 10, 5)
                    BULLET_HIT_SOUND.play()
                    spaceship_bullets.append(bullet)
        counter+=1
        if counter % 300==0 and score>10:
            bullet = pygame.Rect(boss.x + boss.width +150 + random.randrange(-200,200), boss.y + boss.height//2 +80, 10, 5)
            boss_bullets.append(bullet)
            bullet = pygame.Rect(boss.x + boss.width +150 + random.randrange(-200,200), boss.y + boss.height//2 +80, 10, 5)
            boss_bullets.append(bullet)
            bullet = pygame.Rect(boss.x + boss.width +150 + random.randrange(-200,200), boss.y + boss.height//2 +80, 10, 5)
            boss_bullets.append(bullet)
            bullet = pygame.Rect(boss.x + boss.width +150 + random.randrange(-200,200), boss.y + boss.height//2 +80, 10, 5)
            boss_bullets.append(bullet)
            BULLET_HIT_SOUND.play()
   


        if event.type== ENEMY_HIT:
            score+=1
        
            

        keys_pressed=pygame.key.get_pressed()
        spaceship_move(keys_pressed,spaceship)
        handle_bullets(enemy_bullets, spaceship_bullets, enemy, spaceship,score,boss_bullets)
        draw_window(spaceship,enemy,spaceship_bullets,score,tries,boss,boss_bullets)

        
        


    pygame.quit()

if __name__ == "__main__":
    main()