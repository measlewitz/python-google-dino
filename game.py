import random
import sys, os
import pygame

def resource_path(path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, path)
    return path

pygame.init()
screen = pygame.display.set_mode((750, 250))
screen.fill((255,255,255))
pygame.display.set_caption("Dino Game")
pygame.display.set_icon(pygame.image.load(resource_path("sprites/jump.png")).convert_alpha())
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font(resource_path("sprites/font.ttf"), 15)

def gameOver():
    text = font.render("GAME OVER", True, (83, 83, 83))
    label = text.get_rect(
        centerx=screen.get_rect().centerx,
        centery=screen.get_rect().top + 50
    )
    screen.blit(text, label)

score = 0
highscore = 0
def drawScore(last_score=None):
    if last_score is None:
        last_score = [-1]
    if score != last_score[0]:
        timer = font.render(str(score), True, (83, 83, 83))
    timePos = timer.get_rect(
        right = screen.get_rect().right - 10,
        top = screen.get_rect().top + 5,
    )
    screen.blit(timer, timePos)

    if dead:
        global highscore
        highscore = score if highscore < score else highscore
        hi = font.render("HI " + str(highscore), True, (83, 83, 83))
        hiLabel = hi.get_rect(
            right=screen.get_rect().right - timer.get_width() - 30,
            top=screen.get_rect().top + 5
        )
        screen.blit(hi, hiLabel)

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
        self.velocity = 18
        self.gravity = 1
        self.jumping = False
        self.ducking = False

        self.stand = pygame.image.load(resource_path("sprites/stand.png")).convert_alpha()
        self.jumper = pygame.image.load(resource_path("sprites/jump.png")).convert_alpha()

        self.currentImage = 0
        self.running_sprites = []
        self.ducking_sprites = []

        self.running_sprites.append(pygame.image.load(resource_path("sprites/run1.png")).convert_alpha())
        self.running_sprites.append(pygame.image.load(resource_path("sprites/run2.png")).convert_alpha())

        self.ducking_sprites.append(pygame.image.load(resource_path("sprites/duck1.png")).convert_alpha())
        self.ducking_sprites.append(pygame.image.load(resource_path("sprites/duck2.png")).convert_alpha())

        if not gameStarted:
            self.image = self.stand
        else:
            self.image = self.running_sprites[0]
        self.mask = pygame.mask.from_surface(self.image)
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
            self.velocity = 16
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
        if self.currentImage >= 2:
            self.currentImage = 0
        self.image = self.ducking_sprites[int(self.currentImage)]

    def run(self):
        self.currentImage += 0.125
        if self.currentImage>=2:
            self.currentImage = 0
        self.image = self.running_sprites[int(self.currentImage)]

    def update(self):
        if dead:
            return
        if self.jumping:
            self.jump()
        elif self.ducking:
            self.duck()
        elif gameStarted:
            self.run()

cloudImage = pygame.image.load(resource_path("sprites/cloud.png")).convert_alpha()
cloudY = [50,75,100,125,150]
class cloud(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = cloudImage
        self.x = x
        self.y = random.choices(cloudY, (50,40,30,20,10))[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        if dead:
            return
        self.rect.x -= 1
        global clouds
        if self.rect.x <= -50:
            cloud_sprites.remove(self)
            clouds -= 1

cacti = []
for i in range(1,7):
    cacti.append(pygame.image.load(resource_path(f"sprites/cacti/cactus{i}.png")).convert_alpha())
class cactus(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.x = x
        self.y = 190
        self.image = random.choice(cacti)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.x -= speed
        self.rect = self.image.get_rect(center=(self.x, self.y))
        global obstacles
        if self.x <= -50:
            obstacle_sprites.remove(self)
            obstacles -= 1

pteroImages = []
pteroImages.append(pygame.image.load(resource_path("sprites/bird1.png")).convert_alpha())
pteroImages.append(pygame.image.load(resource_path("sprites/bird2.png")).convert_alpha())
pteroY = [150,165,190]
class pterodactyl(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.x = x
        self.y = random.choices(pteroY, (15,35,50))[0]
        self.yBalanced = True
        self.image = pteroImages[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.currentImage = 0
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def animate(self):
        self.currentImage += 0.025
        if self.currentImage >= 2:
            self.currentImage = 0
            self.yBalanced = True
        elif self.currentImage >= 1:
            self.yBalanced = False
        self.new_image(int(self.currentImage))

    def new_image(self, value):
        if self.image != pteroImages[value]:
            self.image = pteroImages[value]
            if self.yBalanced:
                self.y += 6
            else:
                self.y -= 6


    def update(self):
        if dead:
            return
        self.animate()
        self.x -= speed
        self.rect = self.image.get_rect(center=(self.x, self.y))
        global obstacles
        if self.x <= -50:
            obstacle_sprites.remove(self)
            obstacles -= 1

xPos = 100
dino_sprites = pygame.sprite.Group()
obstacle_sprites = pygame.sprite.Group()
cloud_sprites = pygame.sprite.Group()

trex = dino()
dino_sprites.add(trex)

obstacles = 0
obstacleTimer = 0
obstacleCooldown = 1000

clouds = 0
cloudTimer = 0
cloudCooldown = 3000

ground = pygame.image.load(resource_path("sprites/ground.png")).convert_alpha()
cover_length = 1201
cover_pos = xPos

deadImage = pygame.image.load(resource_path("sprites/dead.png")).convert_alpha()

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
                    trex = dino()
                    dino_sprites.empty()
                    dino_sprites.add(trex)
                    obstacle_sprites.empty()
                    dead = False

                    obstacles = 0
                    clouds = 0
                    speed = 5
                    score = 0

            elif event.key == pygame.K_DOWN:
                if gameStarted and not dead and not trex.jumping:
                    trex.ducking = True
                    trex.rect.centery = trex.y + 17
            elif event.key == pygame.K_ESCAPE:
                exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN and not dead:
                trex.ducking = False
                trex.rect.centery = trex.y

    if pygame.sprite.spritecollide(trex, obstacle_sprites, False, pygame.sprite.collide_mask):
        dead = True
        speed = 0
        trex.image = deadImage

    screen.fill((255,255,255))

    xPos -= speed
    if not dead and gameStarted:
        score += 1
    elif dead:
        gameOver()
    if score % 100 == 0 and gameStarted and not dead:
        speed = round(speed + 0.1, 1)
        if obstacleCooldown >= 255:
            obstacleCooldown -= 5

    screen.blit(ground, (xPos, 200))
    screen.blit(ground, (xPos + 1200, 200))
    if xPos <= -1200:
        xPos = 0

    ground_cover = pygame.draw.rect(screen, (255, 255, 255), (cover_pos, 200, cover_length, 15))
    if(cover_length <= 1200):
        cover_length -= 10
        cover_pos += 10

    if gameStarted and not dead:
        if clouds < 3 and pygame.time.get_ticks() - cloudTimer >= cloudCooldown:
            rand = random.randint(1, 25)
            if rand == 1:
                cloudTimer = pygame.time.get_ticks()
                clouds += 1
                clowd = cloud(800)
                cloud_sprites.add(clowd)

        if obstacles < 3 and pygame.time.get_ticks() - obstacleTimer >= obstacleCooldown:
            rand = random.randint(1,100)
            if rand in range(1,15):
                obstacleTimer = pygame.time.get_ticks()
                obstacles += 1
                cact = cactus(800)
                obstacle_sprites.add(cact)
            elif rand in range(16, 22):
                obstacleTimer = pygame.time.get_ticks()
                obstacles += 1
                ptero = pterodactyl(800)
                obstacle_sprites.add(ptero)

    cloud_sprites.update()
    cloud_sprites.draw(screen)
    obstacle_sprites.update()
    obstacle_sprites.draw(screen)
    dino_sprites.update()
    dino_sprites.draw(screen)
    drawScore()

    pygame.display.flip()
    clock.tick(60)