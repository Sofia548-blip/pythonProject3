import pygame
import random

pygame.init()

screen_x = 1000
screen_y = 500

width = 15
height = 100
speed = 15

points_left = 0
points_right = 0

white = (255,255,255)

ball_r = 10
ball_speed = 6
ball_d = 10*2
ball_start_x = screen_x/2 - ball_r
ball_start_y = screen_y/2 - ball_r

fps = 60
mode = 0
FONT = pygame.font.SysFont("comicsans", 25)

screen = pygame.display.set_mode((screen_x, screen_y))


platform_right = pygame.Rect(screen_x-width-5,screen_y/2-height/2,width,height)
platform_left = pygame.Rect(5,screen_y/2-height/2,width,height)
ball = pygame.Rect(ball_start_x, ball_start_y, ball_d,ball_d)

dx = 1
dy = -1

font = pygame.font.Font(None, 50)

green = (0,133,35)
clock = pygame.time.Clock()

pygame.display.set_caption('Ping-Pong Pixel Game')
pause = False
game = True
while game:
    screen.fill(green)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #выход из игры
            exit()
    key = pygame.key.get_pressed()
    if (key[pygame.K_UP] and platform_right.top > 0 ):
        platform_right.top -=speed
    elif (key[pygame.K_DOWN]and platform_right.bottom < screen_y):
        platform_right.bottom += speed
    elif (key[pygame.K_w] and platform_left.top > 0):
        platform_left.top -= speed
    elif (key[pygame.K_s] and platform_left.bottom < screen_y):
        platform_left.bottom += speed


    pygame.draw.rect(screen, pygame.Color('White'), platform_right)  #создание ракеток
    pygame.draw.rect(screen, pygame.Color('White'), platform_left)
    pygame.draw.circle(screen, pygame.Color('White'), ball.center, ball_r)
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    if ball.centery < ball_r or ball.centery > screen_y:
        dy = -dy
    elif ball.colliderect(platform_left) or ball.colliderect(platform_right):
        dx = -dx

    if mode == 1:
        score_text = FONT.render(f"Компьютер: {points_right}  Игрок: {points_left}", True, green)
    else:
        score_text = FONT.render(f"Игрок слева: {points_left}  Игрок справа: {points_right}", True, green)
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 20))


def random_velocity(difficulty):
    base_speed = 5 + 2 * (difficulty - 1)  # Основная скорость изменяется в зависимости от сложности
    vel_x = random.choice([base_speed, -base_speed])  # Случайное направление по горизонтали
    vel_y = random.choice([base_speed, -base_speed])  # Случайное направление по вертикали
    return vel_x, vel_y


def redraw_game_window(left_paddle, right_paddle, ball, player_score, computer_score, paused):
    screen.fill(green)
    left_paddle.draw(screen)
    right_paddle.draw(screen)
    ball.draw(screen)

def start_screen():
    global mode
    screen.fill(green)
    difficulty_text = FONT.render("Выберите сложность (1 - легкая, 2 - средняя, 3 - тяжелая)", True, white)
    mode_text = FONT.render("Выберите режим (4 - с компьютером, 5 - с игроком)", True, white)
    start_text = FONT.render("Для старта игры нажмите Enter", True, white)
    screen.blit(difficulty_text, (50, 150))
    screen.blit(mode_text, (50, 200))
    screen.blit(start_text, (50, 250))
    pygame.display.update()

    pause_text = FONT.render("Для продолжения игры нажмите Пробел", True, white)
    screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2))
    quit_text = FONT.render("Для завершения игры нажмите клавишу Esc", True, green)
    screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 2 + 30))

    pygame.display.update()


    right_text = font.render(f'{points_right}', True, pygame.Color('White'))
    screen.blit(right_text, (screen_x - 40, 20))
    left_text = font.render(f'{points_left}', True, pygame.Color('White'))
    screen.blit(left_text, (20, 20))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

if __name__ == "__main__":
    main()

