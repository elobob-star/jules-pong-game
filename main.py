import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Game Objects Sizes
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15

# Speeds
INITIAL_BALL_SPEED_X = 5
INITIAL_BALL_SPEED_Y = 5
PADDLE_SPEED = 7
AI_SPEED = 6
SPEED_MULTIPLIER = 1.05
MAX_SPEED = 15

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Classic Pong")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.score = 0

    def move(self, y_change):
        self.rect.y += y_change
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.reset()

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed_x = INITIAL_BALL_SPEED_X * random.choice((1, -1))
        self.speed_y = INITIAL_BALL_SPEED_Y * random.choice((1, -1))

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Bounce off top and bottom walls
        if self.rect.top <= 0:
            self.rect.top = 0
            self.y = float(self.rect.y)
            self.speed_y *= -1
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.y = float(self.rect.y)
            self.speed_y *= -1

    def increase_speed(self):
        # Increase speed while maintaining direction
        if abs(self.speed_x) < MAX_SPEED:
            self.speed_x *= SPEED_MULTIPLIER
        if abs(self.speed_y) < MAX_SPEED:
            self.speed_y *= SPEED_MULTIPLIER

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)

def main():
    player = Paddle(30, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ai = Paddle(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()

    paused = False
    game_over = False
    winner = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        # Reset game
                        player.score = 0
                        ai.score = 0
                        ball.reset()
                        game_over = False
                        winner = ""
                    else:
                        paused = not paused

        if not paused and not game_over:
            # Player Movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player.move(-PADDLE_SPEED)
            if keys[pygame.K_s]:
                player.move(PADDLE_SPEED)

            # AI Movement (Simple AI that tracks the ball)
            if ai.rect.centery < ball.rect.centery:
                ai.move(AI_SPEED)
            elif ai.rect.centery > ball.rect.centery:
                ai.move(-AI_SPEED)

            # Ball Movement
            ball.move()

            # Collision with Paddles
            if ball.rect.colliderect(player.rect) and ball.speed_x < 0:
                ball.rect.left = player.rect.right
                ball.x = float(ball.rect.x)
                ball.speed_x *= -1
                ball.increase_speed()
            elif ball.rect.colliderect(ai.rect) and ball.speed_x > 0:
                ball.rect.right = ai.rect.left
                ball.x = float(ball.rect.x)
                ball.speed_x *= -1
                ball.increase_speed()

            # Scoring
            if ball.rect.left <= 0:
                ai.score += 1
                ball.reset()
            elif ball.rect.right >= WIDTH:
                player.score += 1
                ball.reset()

            # Check Win Condition
            if player.score >= 10:
                game_over = True
                winner = "Player"
            elif ai.score >= 10:
                game_over = True
                winner = "AI"

        # Drawing
        screen.fill(BLACK)

        # Draw dashed center line
        for y in range(0, HEIGHT, 40):
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 2, y, 4, 20))

        player.draw(screen)
        ai.draw(screen)
        ball.draw(screen)

        # Draw Scores
        player_text = font.render(str(player.score), True, WHITE)
        screen.blit(player_text, (WIDTH // 4 - player_text.get_width() // 2, 20))

        ai_text = font.render(str(ai.score), True, WHITE)
        screen.blit(ai_text, (WIDTH * 3 // 4 - ai_text.get_width() // 2, 20))

        if paused:
            pause_text = font.render("PAUSED", True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

        if game_over:
            over_text = font.render(f"{winner} Wins!", True, WHITE)
            restart_text = small_font.render("Press SPACE to Restart", True, WHITE)
            screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
