import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)
GRAY = (169, 169, 169)

# Fonts
font = pygame.font.SysFont("Arial", 24)
button_font = pygame.font.SysFont("Arial", 30)

# Paddle
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
paddle_y = HEIGHT - 30
paddle_speed = 10

# Ball
BALL_RADIUS = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 3 * random.choice([1, -1])
ball_dy = -3

# Bricks
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_PADDING = 10
BRICK_OFFSET_TOP = 30
BRICK_OFFSET_LEFT = 30

def create_bricks(level):
    bricks = []
    for i in range(8):
        brick_row = []
        for j in range(10):
            brick_x = BRICK_OFFSET_LEFT + j * (BRICK_WIDTH + BRICK_PADDING)
            brick_y = BRICK_OFFSET_TOP + i * (BRICK_HEIGHT + BRICK_PADDING)
            brick_row.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))
        bricks.append(brick_row)
    return bricks

bricks = create_bricks(1)

# Game variables
score = 0
level = 1
high_score = 0

# Main loop
running = True
game_over = False

# Button
button_width = 200
button_height = 50
button_x = (WIDTH - button_width) // 2
button_y = HEIGHT // 2 + 50

def draw_button(text, x, y, width, height):
    pygame.draw.rect(win, GRAY, (x, y, width, height))
    pygame.draw.rect(win, WHITE, (x, y, width, height), 2)
    text_surface = button_font.render(text, True, WHITE)
    win.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                # Restart the game
                score = 0
                level = 1
                bricks = create_bricks(level)
                ball_x = WIDTH // 2
                ball_y = HEIGHT // 2
                ball_dx = 3 * random.choice([1, -1])
                ball_dy = -3
                game_over = False

    if not game_over:
        # Move paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x - paddle_speed > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x + PADDLE_WIDTH + paddle_speed < WIDTH:
            paddle_x += paddle_speed

        # Move ball
        ball_x += ball_dx
        ball_y += ball_dy

        # Ball collision with walls
        if ball_x - BALL_RADIUS < 0 or ball_x + BALL_RADIUS > WIDTH:
            ball_dx = -ball_dx
        if ball_y - BALL_RADIUS < 0:
            ball_dy = -ball_dy

        # Ball collision with paddle
        if (paddle_y < ball_y + BALL_RADIUS < paddle_y + PADDLE_HEIGHT and
                paddle_x < ball_x < paddle_x + PADDLE_WIDTH):
            ball_dy = -ball_dy

        # Ball collision with bricks
        for row in bricks:
            for brick in row:
                if brick.collidepoint(ball_x, ball_y):
                    ball_dy = -ball_dy
                    row.remove(brick)
                    score += 10
                    break

        # Ball out of bounds
        if ball_y + BALL_RADIUS > HEIGHT:
            game_over = True  # Game over
            if score > high_score:
                high_score = score  # Update high score

        # Check if all bricks are destroyed
        if all(not row for row in bricks):
            level += 1
            bricks = create_bricks(level)
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            ball_dx = (3 + level) * random.choice([1, -1])
            ball_dy = -(3 + level)

        # Clear screen
        win.fill(BLACK)

        # Draw paddle
        pygame.draw.rect(win, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

        # Draw ball
        pygame.draw.circle(win, RED, (ball_x, ball_y), BALL_RADIUS)

        # Draw bricks
        colors = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE]
        for i, row in enumerate(bricks):
            for brick in row:
                color = colors[i % len(colors)]
                pygame.draw.rect(win, color, brick)

        # Draw score, level, and high score
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        win.blit(score_text, (10, 10))
        win.blit(level_text, (WIDTH - 150, 10))
        win.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, 10))

        # Update display
        pygame.display.update()

        # Frame rate
        pygame.time.Clock().tick(60)
    else:
        # Game over screen
        win.fill(BLACK)
        game_over_text = font.render("Game Over!", True, WHITE)
        win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        win.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 30))
        draw_button("Retry", button_x, button_y, button_width, button_height)
        pygame.display.update()

pygame.quit()
