import pygame
import random
import os

pygame.init()

# File paths for images and high score
b_image_path = r"C:\Users\Aaryan\Desktop\CODE\Projects\New folder\re.png"
player_image_path = r"C:\Users\Aaryan\Desktop\CODE\Projects\New folder\pngegg (1).png"
target_image_path = r"C:\Users\Aaryan\Desktop\CODE\Projects\New folder\ENEMY.png"
bullet_image_path = r"C:\Users\Aaryan\Desktop\CODE\Projects\New folder\fIRE.png"
high_score_file = 'high_score.txt'

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("First Project")
font = pygame.font.Font(None, 30)

def load_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, 'r') as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return 0
    return 0

def save_high_score(score):
    with open(high_score_file, 'w') as file:
        file.write(str(score))

def game_over_screen(score, HC):
    screen.fill((0, 0, 0))
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {HC}", True, (255, 255, 255))
    play_again_text = font.render("Press R to Play Again or Q to Quit", True, (255, 255, 255))
    
    screen.blit(game_over_text, (350, 150))
    screen.blit(score_text, (350, 200))
    screen.blit(high_score_text, (350, 250))
    screen.blit(play_again_text, (250, 350))
    
    pygame.display.update()

def gameLoop():
    running = True
    game_started = False
    player_x = 400
    player_y = 400
    player_speed = 5
    bullet_speed = 10
    bullets = []
    targets = []
    clock = pygame.time.Clock()
    score = 0
    HC = load_high_score()
    target_spawn_timer = 0
    target_spawn_interval = 500  # milliseconds
    b_image = pygame.image.load(b_image_path).convert_alpha()
    player_image = pygame.image.load(player_image_path).convert_alpha()
    target_image = pygame.image.load(target_image_path).convert_alpha()
    bullet_image = pygame.image.load(bullet_image_path).convert_alpha()
    
    while running:
        while True:  # Game loop with play again or quit option
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Restart the game
                        gameLoop()
                        return
                    if event.key == pygame.K_q:
                        # Quit the game
                        pygame.quit()
                        return

            game_over_screen(score, HC)
            clock.tick(15)
        
        # Handle input and update game state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bullets.append([player_x + 20, player_y])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < 780:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < 480:
            player_y += player_speed

        for bullet in bullets:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Generate new targets
        target_spawn_timer += clock.get_time()
        if target_spawn_timer >= target_spawn_interval:
            target_spawn_timer %= target_spawn_interval
            target_x = random.randint(0, 780)
            target_y = -40
            targets.append([target_x, target_y, target_image])

        # Update target positions
        for target in targets:
            target[1] += random.randint(1, 5)

        # Remove targets that go off the screen
        targets = [target for target in targets if target[1] < 480]
        # High Score and Score
        if score > HC:
            HC = score
            save_high_score(HC)
        # Check for collisions
        for i, target in enumerate(targets):
            for bullet in bullets:
                bullet_rect = pygame.Rect(bullet[0], bullet[1], 10, 10)
                target_rect = pygame.Rect(target[0], target[1], target[2].get_width(), target[2].get_height())
                if bullet_rect.colliderect(target_rect):
                    targets.remove(target)
                    bullets.remove(bullet)
                    score += 1
                    break
        
        # Check for collisions between player and targets
        player_rect = pygame.Rect(player_x, player_y, player_image.get_width(), player_image.get_height())
        for target in targets:
            target_rect = pygame.Rect(target[0], target[1], target[2].get_width(), target[2].get_height())
            if player_rect.colliderect(target_rect):
                # Game over
                print("Game over")
                print('Score:', score)
                # Display game over screen and handle restart or quit
                game_over_screen(score, HC)
                pygame.display.update()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                # Restart the game
                                gameLoop()
                                return
                            if event.key == pygame.K_q:
                                # Quit the game
                                pygame.quit()
                                return
                    clock.tick(15)
                break
        
        # Images in the Game
        screen.blit(b_image, (0, 0))
        screen.blit(player_image, (player_x, player_y))
        for bullet in bullets:
            bullet_rect = pygame.Rect(bullet[0] - bullet_image.get_width() / 2, bullet[1] - bullet_image.get_height() / 2, bullet_image.get_width(), bullet_image.get_height())
            screen.blit(bullet_image, bullet_rect)
        for target in targets:
            screen.blit(target[2], (target[0], target[1]))

        # Render the score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        high_score_text = font.render(f"High Score: {HC}", True, (255, 255, 255))
        
        screen.blit(high_score_text, (10, 50))
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

def main():
    gameLoop()

main()
