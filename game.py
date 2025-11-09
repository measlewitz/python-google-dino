import sys
import pygame
pygame.init()

screen = pygame.display.set_mode((750, 250))
screen.fill((255,255,255))
pygame.display.set_caption("Dino Game")
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont("Arial", 25, True)
text = font.render("press space-bar to start", True, (0,0,0))
label = text.get_rect(
    centerx=screen.get_rect().centerx,
    centery=screen.get_rect().top + 50
)

score = 0
def drawScore():
    timer = font.render(str(score), True, (0, 0, 0))
    timePos = timer.get_rect(right = screen.get_rect().right - 10)
    screen.blit(timer, timePos)

gameStarted = False
def on_space_press():
    global gameStarted
    if not gameStarted:
        gameStarted = True
    else:
        print("jumping")

def exit():
    pygame.quit()
    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                on_space_press()
            elif event.key == pygame.K_ESCAPE:
                exit()

    screen.fill((255,255,255))

    if not gameStarted:
        screen.blit(text, label)
    else:
        score += 1
    drawScore()

    pygame.display.flip()
    clock.tick(60)