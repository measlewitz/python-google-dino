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
def drawScore(last_score=[-1]):
    if score != last_score[0]:
        timer = font.render(str(score), True, (0, 0, 0))
    timePos = timer.get_rect(right = screen.get_rect().right - 10)
    screen.blit(timer, timePos)

def exit():
    pygame.quit()
    sys.exit()

gameStarted = False
dead = False
speed = 0

class dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 122
        self.y = 189
        self.velocity = 17
        self.gravity = 1
        self.jumping = False
        self.ducking = False

        self.stand = pygame.image.load("sprites/stand.png").convert_alpha()
        self.jumper = pygame.image.load("sprites/jump.png").convert_alpha()

        self.currentImage = 0
        self.running_sprites = []
        self.ducking_sprites = []

        self.running_sprites.append(pygame.image.load("sprites/run1.png").convert_alpha())
        self.running_sprites.append(pygame.image.load("sprites/run2.png").convert_alpha())

        self.ducking_sprites.append(pygame.image.load("sprites/duck1.png").convert_alpha())
        self.ducking_sprites.append(pygame.image.load("sprites/duck2.png").convert_alpha())

        if not gameStarted:
            self.image = self.stand
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def jump(self):
        if not self.jumping:
            self.image = self.jumper
        self.jumping = True
        self.y -= self.velocity
        self.velocity -= self.gravity
        if self.velocity <= 0:
            self.gravity += 1
        if self.y >= 189:
            self.y = 189
            self.jumping = False
            self.velocity = 15
            self.gravity = 1
            global gameStarted
            global speed
            if not gameStarted:
                gameStarted = True
                speed = 5
        self.rect.centery = self.y

    def duck(self):
        self.ducking = True
        self.currentImage += 0.125
        if (self.currentImage >= 2):
            self.currentImage = 0
        self.image = self.ducking_sprites[int(self.currentImage)]

    def run(self):
        self.currentImage += 0.125
        if(self.currentImage>=2):
            self.currentImage = 0
        self.image = self.running_sprites[int(self.currentImage)]

    def update(self):
        if self.jumping:
            self.jump()
        elif self.ducking:
            self.duck()
        elif gameStarted:
            self.run()

class cloud(pygame.sprite.Sprite):
    pass

class cactus(pygame.sprite.Sprite):
    pass

class pterodactyl(pygame.sprite.Sprite):
    pass

xPos = 100
sprites = pygame.sprite.Group()

trex = dino()
sprites.add(trex)

ground = pygame.image.load("sprites/ground.png").convert_alpha()
cover_length = 1201
cover_pos = xPos

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if not dead and not trex.ducking:
                    if not gameStarted:
                        cover_length -= 1
                    trex.jump()
                else:
                    speed = 5
            elif event.key == pygame.K_DOWN:
                if gameStarted and not dead and not trex.jumping:
                    trex.ducking = True
                    trex.rect.centery = trex.y + 17
            elif event.key == pygame.K_ESCAPE:
                exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                trex.ducking = False
                trex.rect.centery = trex.y

    screen.fill((255,255,255))

    xPos -= speed
    if not gameStarted:
        screen.blit(text, label)
    else:
        score += 1
    if score % 100 == 0 and gameStarted and not dead:
        speed = round(speed + 0.1, 1)

    screen.blit(ground, (xPos, 200))
    screen.blit(ground, (xPos + 1200, 200))
    if xPos <= -1200:
        xPos = 0

    ground_cover = pygame.draw.rect(screen, (255, 255, 255), (cover_pos, 200, cover_length, 15))
    if(cover_length <= 1200):
        cover_length -= 10
        cover_pos += 10

    drawScore()
    sprites.update()
    sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)