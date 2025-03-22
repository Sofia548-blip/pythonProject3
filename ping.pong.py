import random
import pygame


pygame.init()


WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра Пинг-Понг")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont("comicsans", 25)


mode = 0


class Paddle:
    WIDTH = 15
    HEIGHT = 100

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 10

    def move(self, up=True):

        if up and self.y > 0:
            self.y -= self.vel
        elif not up and self.y < HEIGHT - self.HEIGHT:
            self.y += self.vel

    def draw(self, draw_screen):
        pygame.draw.rect(draw_screen, WHITE, (self.x, self.y, self.WIDTH, self.HEIGHT))


class AutoPaddle(Paddle):
    def auto_move(self, ball, difficulty):
        if ball.y < self.y + self.HEIGHT // 2 and self.y > 0:
            self.y -= self.vel * (0.2 * difficulty)
        elif ball.y > self.y + self.HEIGHT // 2 and self.y < HEIGHT - self.HEIGHT:
            self.y += self.vel * (0.2 * difficulty)


class Ball:
    RADIUS = 10

    def __init__(self, x, y, vel_x, vel_y):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y

    def move(self, paddles):
        self.x += self.vel_x
        self.y += self.vel_y

        if self.y - self.RADIUS < 0 or self.y + self.RADIUS > HEIGHT:
            self.vel_y = -self.vel_y


        for paddle in paddles:
            if self.x - self.RADIUS <= paddle.x + paddle.WIDTH and \
                    self.x + self.RADIUS >= paddle.x and \
                    self.y + self.RADIUS >= paddle.y and \
                    self.y - self.RADIUS <= paddle.y + paddle.HEIGHT:
                self.vel_x = -self.vel_x

    def draw(self, draw_screen):
        pygame.draw.circle(draw_screen, WHITE, (self.x, self.y), self.RADIUS)


def random_velocity(difficulty):
    base_speed = 5 + 2 * (difficulty - 1)
    vel_x = random.choice([base_speed, -base_speed])
    vel_y = random.choice([base_speed, -base_speed])
    return vel_x, vel_y


def redraw_game_window(left_paddle, right_paddle, ball, player_score, computer_score, paused):
    screen.fill(BLACK)
    left_paddle.draw(screen)
    right_paddle.draw(screen)
    ball.draw(screen)


    if mode == 1:
        score_text = FONT.render(f"Компьютер: {player_score}  Игрок: {computer_score}", True, WHITE)
    else:
        score_text = FONT.render(f"Игрок слева: {player_score}  Игрок справа: {computer_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    if paused:
        pause_text = FONT.render("Для продолжения игры нажмите Пробел", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
        quit_text = FONT.render("Для завершения игры нажмите клавишу Esc", True, WHITE)
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 30))

    pygame.display.update()


def start_screen():
    global mode
    screen.fill(BLACK)
    difficulty_text = FONT.render("Выберите сложность (1 - легкая, 2 - средняя, 3 - тяжелая)", True, WHITE)
    mode_text = FONT.render("Выберите режим (4 - с компьютером, 5 - с игроком)", True, WHITE)
    start_text = FONT.render("Для старта игры нажмите Enter", True, WHITE)
    screen.blit(difficulty_text, (50, 150))
    screen.blit(mode_text, (50, 200))
    screen.blit(start_text, (50, 250))
    pygame.display.update()

    choosing = True
    difficulty = 1

    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = 1
                    difficulty_text = FONT.render("Выбрана сложность: легкая", True, WHITE)
                elif event.key == pygame.K_2:
                    difficulty = 2
                    difficulty_text = FONT.render("Выбрана сложность: средняя", True, WHITE)
                elif event.key == pygame.K_3:
                    difficulty = 3
                    difficulty_text = FONT.render("Выбрана сложность: тяжелая", True, WHITE)
                elif event.key == pygame.K_4:
                    mode = 1
                    mode_text = FONT.render("Выбран режим: с компьютером", True, WHITE)
                elif event.key == pygame.K_5:
                    mode = 2
                    mode_text = FONT.render("Выбран режим: с игроком", True, WHITE)
                elif event.key == pygame.K_RETURN and mode != 0:
                    choosing = False

        screen.fill(BLACK)
        screen.blit(difficulty_text, (50, 150))
        screen.blit(mode_text, (50, 200))
        screen.blit(start_text, (50, 250))
        pygame.display.update()

    return difficulty, mode


def main():
    global mode
    difficulty, mode = start_screen()
    vel_x, vel_y = random_velocity(difficulty)
    left_paddle = AutoPaddle(5, HEIGHT // 2 - Paddle.HEIGHT // 2) if mode == 1 else (
        Paddle(5, HEIGHT // 2 - Paddle.HEIGHT // 2))
    right_paddle = Paddle(WIDTH - 5 - Paddle.WIDTH, HEIGHT // 2 - Paddle.HEIGHT // 2)
    ball = Ball(WIDTH // 2, HEIGHT // 2, vel_x, vel_y)
    player_score = 0
    computer_score = 0
    paused = False

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and paused:
                    paused = False
                    vel_x, vel_y = random_velocity(difficulty)
                    ball = Ball(WIDTH // 2, HEIGHT // 2, vel_x, vel_y)
                if event.key == pygame.K_ESCAPE:
                    run = False

        if not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                right_paddle.move(up=True)
            if keys[pygame.K_DOWN]:
                right_paddle.move(up=False)
            if mode == 2:
                if keys[pygame.K_w]:
                    left_paddle.move(up=True)
                if keys[pygame.K_s]:
                    left_paddle.move(up=False)
            elif mode == 1:
                left_paddle.auto_move(ball, difficulty)

            ball.move([left_paddle, right_paddle])


            if ball.x < 0 or ball.x > WIDTH:
                paused = True
                if ball.x < 0:
                    computer_score += 1
                else:
                    player_score += 1

        redraw_game_window(left_paddle, right_paddle, ball, player_score, computer_score, paused)

    pygame.quit()


if __name__ == "__main__":
    main()