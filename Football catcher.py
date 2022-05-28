# KidsCanCode - Game Development with Pygame video series
# Shmup game - part 2
# Video link: https://www.youtube.com/watch?v=-5GNbL33hz0
# Enemy sprites
from platform import machine
from stringprep import b1_set
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

over = 0
# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 50
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT-10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(1, 8)
        self.speedx = random.randint(-3, 3)
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < 0 or self.rect.right > WIDTH:
            self.rect.x = random.randint(0, WIDTH)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(1, 8)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ball_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 40
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(1, 8)
        self.speedx = random.randint(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT-50 or self.rect.left < 0 or self.rect.right > WIDTH:
            self.rect.x = random.randint(0, WIDTH)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(1, 8)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "FOOTBALL CATCHER", 40, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move. Catch footballs and take points", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Avoid catching bombs. If you catch bombs,", 22,
              WIDTH / 2, 325)
    draw_text(screen, "it will explode the ground.", 22,
              WIDTH / 2, 350)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


# Load all game graphics
background = pygame.image.load(path.join(img_dir, 'ground.jpg')).convert()
background_rect = background.get_rect()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
player_img = pygame.image.load(path.join(img_dir, "keeper.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
ball_img = pygame.image.load(path.join(img_dir, "ball.png")).convert()
enemy_img = pygame.image.load(path.join(img_dir, "enemy.png")).convert()

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
# Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'catch.wav'))
enemy_sound = pygame.mixer.Sound(path.join(snd_dir, 'enemy.wav'))
enemy_sound.set_volume(1000000)
pygame.mixer.music.load(path.join(snd_dir, 'music.wav'))
pygame.mixer.music.set_volume(0.4)


pygame.mixer.music.play(loops=-1)
# Game loop
game_over = True
running = True
while running:
    if game_over:
        pygame.time.wait(1000)
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(2):
            en = Enemy()
            all_sprites.add(en)
            enemy_group.add(en)
        ball_group = pygame.sprite.Group()
        for i in range(6):
            b = Ball()
            all_sprites.add(b)
            ball_group.add(b)
        score = 0

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()


# check to see if a bullet hit a mob
    hits = pygame.sprite.spritecollide(player, ball_group, False, False,)
    for hit in hits:
        b.rect.x = random.randint(0, WIDTH)
        b.rect.y = random.randint(-100, -40)
        b.speedy = random.randint(1, 8)
        b.speedx = random.randint(-3, 3)
        # pygame.time.wait(1000)
        score += 1
        shoot_sound.play()

        #b = Ball()
        # all_sprites.add(b)
        # ball_group.add(b)

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(
        player, enemy_group, False, pygame.sprite.collide_circle)
    if hits:
        enemy_sound.play()
        expl = Explosion(en.rect.center, 'lg')
        en.rect.x = 0
        all_sprites.add(expl)
        game_over = True

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
