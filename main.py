import pygame
import random
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_SPACE
pygame.init()

FPS =pygame.time.Clock()

HEIGHT = 730
WIDTH = 1250

FONT = pygame.font.SysFont('Verdana', 30)

COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

IMAGE_PATH = 'Goose'
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

#player_size = (20, 20)
player = pygame.image.load('player.png').convert_alpha()
player = pygame.transform.scale((player).convert_alpha(), (40, 60))  #pygame.Surface(player_size)
player_size = player.get_size()
#player.fill(COLOR_BLACK)
#player_rect = player.get_rect()
player_rect = pygame.Rect(0, HEIGHT // 2, *player_size)
#player_speed = [1, 1]
player_move_down = [0, 10]
player_move_right = [10, 0]
player_move_left = [-10, 0]
player_move_up = [0, -10]

enemies = []
bonuses = []
score = 0
image_index = 0

playing = True
game_over_displayed = False 


def create_enemy():
    #enemy_size = (30, 30)
    enemy = pygame.image.load('enemy.png').convert_alpha() #pygame.Surface(enemy_size)
    enemy = pygame.transform.scale(enemy, (100, 30))
    # enemy_size = enemy.get_size()
    #enemy.fill(COLOR_BLUE)
    enemy_rect = pygame.Rect(WIDTH, random.randint(enemy.get_height(), HEIGHT-enemy.get_height()), *enemy.get_size())
    enemy_move = [random.randint(-10, -5), 0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    #bonus_size = (10, 10)
    bonus = pygame.image.load('bonus.png').convert_alpha() #pygame.Surface(bonus_size)
    bonus = pygame.transform.scale(bonus, (90, 110))
    #bonus_size = bonus.get_size()
    #bonus.fill(COLOR_GREEN)
    bonus_rect = pygame.Rect(random.randint(bonus.get_width(), WIDTH-bonus.get_width()), -bonus.get_height(), *bonus.get_size())
    bonus_move = [0, random.randint(4, 6)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1800)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)



def game_over():
    game_over_text = FONT.render('Game Over', True, COLOR_BLACK)
    text_rect = game_over_text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)
    main_display.blit(game_over_text, text_rect)
    pygame.display.flip()
    #pygame.time.delay(2000)  # Затримка на 2 секунди
    #playing = False

def retryGame():
    retryGame_text = FONT.render('If you want to restart game, please press the "SPACE"', True, COLOR_BLUE)
    retry_rect = retryGame_text.get_rect()
    retry_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)
    main_display.blit(retryGame_text, retry_rect)
    pygame.display.flip()

def space_pressed():
    keys = pygame.key.get_pressed()
    return keys[pygame.K_SPACE]

def your_score():
    your_score_text = FONT.render(f'Your score is: {score}', True, COLOR_GREEN)
    your_score_rect = your_score_text.get_rect()
    your_score_rect.center = (WIDTH // 2, HEIGHT // 2 + 100)
    main_display.blit(your_score_text, your_score_rect)
    pygame.display.flip()

while playing:
    FPS.tick(500)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            create_enemy()
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            create_bonus()
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
        

    
    #main_display.fill(COLOR_BLACK)

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            your_score()
            if not game_over_displayed:
                game_over()
                game_over_displayed = True
                start_time = pygame.time.get_ticks()
                while pygame.time.get_ticks() - start_time < 5000:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            playing = False
                            break
                    retryGame()
                    pygame.display.flip()
                    pygame.time.delay(100)
                    if space_pressed():
                        player_rect = pygame.Rect(0, HEIGHT // 2, *player.get_size())
                        enemies = []
                        bonuses = []
                        score = 0
                        game_over_displayed = False
                        break
                player_rect = pygame.Rect(0, HEIGHT // 2, *player.get_size())
                enemies = []
                bonuses = []
                score = 0
                game_over_displayed = False
                


    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))
    
    main_display.blit(player, player_rect)

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
    
    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))
    
    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
print("Your score is: ", score)