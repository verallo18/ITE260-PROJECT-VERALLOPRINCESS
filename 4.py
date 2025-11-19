import pygame, sys, random

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

# Bird settings
bird_x, bird_y, bird_radius = 50, HEIGHT // 2, 15
bird_vel, gravity, jump = 0, 0.3, -8

# Pipe settings
pipe_w, pipe_gap, pipe_speed, pipes = 60, 200, 3, []

# Game state
score, game_over, game_started = 0, False, False

def create_pipe():
    gap_y = random.randint(100, HEIGHT - 100)
    return {"x": WIDTH, "top": gap_y - pipe_gap//2, "bottom": gap_y + pipe_gap//2, "scored": False}

def reset():
    global bird_y, bird_vel, pipes, score, game_over, game_started
    bird_y, bird_vel, pipes, score, game_over, game_started = HEIGHT//2, 0, [], 0, False, False

def collision():
    if bird_y - bird_radius <= 0 or bird_y + bird_radius >= HEIGHT:
        return True
    for p in pipes:
        if bird_x + bird_radius > p["x"] and bird_x - bird_radius < p["x"] + pipe_w:
            if bird_y - bird_radius < p["top"] or bird_y + bird_radius > p["bottom"]:
                return True
    return False

def draw_text(text, size, color, y):
    surf = font.render(text, True, color)
    screen.blit(surf, ((WIDTH - surf.get_width())//2, y))

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                if not game_started: game_started = True
                elif not game_over: bird_vel = jump
            if e.key == pygame.K_r: reset()

    if not game_started:
        screen.fill((0,0,0))
        draw_text("FLAPPY BIRD", 32, (255,255,0), HEIGHT//2-60)
        draw_text("Press SPACE to Start", 32, (255,255,255), HEIGHT//2)
        pygame.display.update(); clock.tick(60); continue

    if game_over:
        screen.fill((0,0,0))
        draw_text("GAME OVER! Press R", 32, (255,50,50), HEIGHT//2-20)
        draw_text(f"Score: {score}", 32, (255,255,255), HEIGHT//2+30)
        pygame.display.update(); clock.tick(60); continue

    # Bird physics
    bird_vel += gravity
    bird_y += bird_vel

    # Pipes
    if not pipes or pipes[-1]["x"] < WIDTH-200: pipes.append(create_pipe())
    for p in pipes:
        p["x"] -= pipe_speed
        if not p["scored"] and p["x"] + pipe_w < bird_x: score+=1; p["scored"]=True
    pipes = [p for p in pipes if p["x"] + pipe_w > 0]

    if collision(): game_over = True

    # Draw
    screen.fill((135,206,235))
    for p in pipes:
        pygame.draw.rect(screen,(0,200,0),(p["x"],0,pipe_w,p["top"]))
        pygame.draw.rect(screen,(0,200,0),(p["x"],p["bottom"],pipe_w,HEIGHT-p["bottom"]))
    pygame.draw.circle(screen,(255,255,0),(bird_x,int(bird_y)),bird_radius)
    screen.blit(font.render(str(score),True,(255,255,255)),(10,10))

    pygame.display.update()
    clock.tick(60)
