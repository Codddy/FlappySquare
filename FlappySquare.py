import pygame
import sys
import random

pygame.init()

screen_width = 600
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Square")

white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)

bird_x = 50
bird_y = screen_height // 2
bird_speed = 5
jump_speed = 12

pipe_width = 50
pipe_gap = 130
pipe_speed = 5

pipes = []

clock = pygame.time.Clock()

score = 0

font = pygame.font.Font(None, 72)
score_text = font.render("{}".format(score), True, yellow)

game_state = 0

def draw_bird(x, y):
    pygame.draw.rect(screen, white, [x, y, 20, 20])

def draw_pipe(pipe_x, pipe_height):
    pygame.draw.rect(screen, white, [pipe_x, 0, pipe_width, pipe_height])
    pygame.draw.rect(screen, white, [pipe_x, pipe_height + pipe_gap, pipe_width, screen_height - pipe_height - pipe_gap])

def generate_pipe():
    pipe_height = random.randint(50, screen_height - 200)
    pipes.append({'x': screen_width, 'height': pipe_height})

generate_pipe()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_speed = -jump_speed

    if game_state == 0:  # MENU
        # Draw menu screen
        screen.fill(black)
        font_menu = pygame.font.Font(None, 48)
        menu_text = font_menu.render("Press SPACE to play", True, white)
        screen.blit(menu_text, (screen_width // 2 - menu_text.get_width() // 2, screen_height // 2))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = 1
            pipes.clear()
            bird_y = screen_height // 2
            score = 0

    elif game_state == 1:
        bird_speed += 1

        bird_y += bird_speed

        if bird_y < 0 or bird_y > screen_height - 20:
            print("Game over! Score:", score)
            game_state = 2

        bird_rect = pygame.Rect(bird_x, bird_y, 20, 20)
        for pipe in pipes:
            pipe_rect_upper = pygame.Rect(pipe['x'], 0, pipe_width, pipe['height'])
            pipe_rect_lower = pygame.Rect(pipe['x'], pipe['height'] + pipe_gap, pipe_width, screen_height - pipe['height'] - pipe_gap)

            if bird_rect.colliderect(pipe_rect_upper) or bird_rect.colliderect(pipe_rect_lower):
                print("Game over! Score:", score)
                game_state = 2

            if pipe['x'] == bird_x:
                score += 1
                print("Score:", score)
                score_text = font.render("{}".format(score), True, yellow)

        screen.fill(black)

        if not pipes or pipes[-1]['x'] < screen_width - 200:
            generate_pipe()

        for pipe in pipes:
            draw_pipe(pipe['x'], pipe['height'])
            pipe['x'] -= pipe_speed

        draw_bird(bird_x, bird_y)

        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 20))

    elif game_state == 2:
        screen.fill(black)
        font_game_over = pygame.font.Font(None, 48)
        game_over_text = font_game_over.render("Game Over", True, white)
        try_again_text = font_game_over.render("Press SPACE to try again", True, white)
        score_text_game_over = font_game_over.render("Score: {}".format(score), True, white)

        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, 100))
        screen.blit(score_text_game_over, (screen_width // 2 - score_text_game_over.get_width() // 2, 200))
        screen.blit(try_again_text, (screen_width // 2 - try_again_text.get_width() // 2, 300))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = 1
            pipes.clear()
            bird_y = screen_height // 2
            score = 0

    pygame.display.flip()
    clock.tick(30)