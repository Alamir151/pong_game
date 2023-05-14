import pygame
import random
import os

# Set up the Pygame window
WIDTH = 800
HEIGHT = 600
FPS = 60
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Set up the game
game_folder = os.path.dirname(__file__)
sound_folder = os.path.join(game_folder, "assets", "sound")
font_name = pygame.font.match_font("arial")

# Load the game assets
bounce_sound = pygame.mixer.Sound(os.path.join(sound_folder, "bounce.wav"))
score_sound = pygame.mixer.Sound(os.path.join(sound_folder, "score.mp3"))

# Define the game functions
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    screen.blit(text_surface, text_rect)

def draw_score(score, x, y):
    draw_text(str(score), 50, (255, 255, 255), x, y)

def reset_ball():
    ball_rect.centerx = WIDTH / 2
    ball_rect.centery = HEIGHT / 2
    ball_speedx = random.choice([-5, 5])
    ball_speedy = random.choice([-5, 5])
    return ball_speedx, ball_speedy

def update_score(player_score, opponent_score):
    draw_score(player_score, WIDTH / 4, 50)
    draw_score(opponent_score, WIDTH * 3 / 4, 50)

def update_player():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_rect.centery -= 5
    if keys[pygame.K_DOWN]:
        player_rect.centery += 5
    if player_rect.top < 0:
        player_rect.top = 0
    if player_rect.bottom > HEIGHT:
        player_rect.bottom = HEIGHT

def update_opponent():
    if opponent_rect.centery < ball_rect.centery:
        opponent_rect.centery += 5
    if opponent_rect.centery > ball_rect.centery:
        opponent_rect.centery -= 5
    if opponent_rect.top < 0:
        opponent_rect.top = 0
    if opponent_rect.bottom > HEIGHT:
        opponent_rect.bottom = HEIGHT

def update_ball(ball_speedx, ball_speedy, player_score, opponent_score):
    ball_rect.centerx += ball_speedx
    ball_rect.centery += ball_speedy
    if ball_rect.left <= 0:
        opponent_score += 1
        score_sound.play()
        ball_speedx, ball_speedy = reset_ball()
    if ball_rect.right >= WIDTH:
        player_score += 1
        score_sound.play()
        ball_speedx, ball_speedy = reset_ball()
    if ball_rect.top <= 0 or ball_rect.bottom >= HEIGHT:
        ball_speedy = -ball_speedy
        bounce_sound.play()
    if ball_rect.colliderect(player_rect):
        ball_speedx = -ball_speedx
        bounce_sound.play()
    if ball_rect.colliderect(opponent_rect):
        player_score += 1
        score_sound.play()
        ball_speedx = -ball_speedx
    return ball_speedx, ball_speedy, player_score, opponent_score

def show_game_over(player_score, opponent_score):
    screen.fill((0, 0, 0))
    draw_text("GAME OVER", 64, (255, 255, 255), WIDTH / 2, HEIGHT / 4)
    draw_text("Player Score: " + str(player_score), 32, (255, 255, 255), WIDTH / 2, HEIGHT / 2)
    draw_text("Opponent Score: " + str(opponent_score), 32, (255, 255, 255), WIDTH / 2, HEIGHT * 3 / 4)
    draw_text("Press any key to play again", 32, (255, 255, 255), WIDTH / 2, HEIGHT - 50)
    pygame.display.update()

    # Wait for player to press a key to restart the game
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Set up the game objects
player_rect = pygame.Rect(0, 0, 20, 100)
player_rect.centerx = 50
player_rect.centery = HEIGHT / 2
opponent_rect = pygame.Rect(0, 0, 20, 100)
opponent_rect.centerx = WIDTH - 50
opponent_rect.centery = HEIGHT / 2
ball_rect = pygame.Rect(0, 0, 20, 20)
ball_rect.centerx = WIDTH / 2
ball_rect.centery = HEIGHT / 2

# Set up the game loop
player_score = 0
opponent_score = 0
ball_speedx, ball_speedy = reset_ball()
game_over = False
running = True
while running:
    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    if not game_over:
        update_player()
        update_opponent()
        ball_speedx, ball_speedy, player_score, opponent_score = update_ball(ball_speedx, ball_speedy, player_score, opponent_score)
        if player_score == 10 or opponent_score == 10:
            game_over = True

    # Draw / render
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), player_rect)
    pygame.draw.rect(screen, "red", opponent_rect)
    pygame.draw.ellipse(screen, (255, 255, 255), ball_rect)
    update_score(player_score, opponent_score)
    pygame.display.flip()

    # Game over screen
    if game_over:
        show_game_over(player_score, opponent_score)
        player_score = 0
        opponent_score = 0
        ball_speedx, ball_speedy = reset_ball()
        game_over = False

    # Wait for the next frame
    clock.tick(FPS)

# Clean up the Pygame window
pygame.quit()