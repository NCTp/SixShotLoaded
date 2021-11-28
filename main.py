import pygame
import sys
import math
import random
from pygame.locals import *
from pygame import mixer
pygame.init()  # initialization
WINDOW_SIZE = (800, 600)
display = pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF)
clock = pygame.time.Clock()

player_image = pygame.image.load("222.png")
player_pistol = pygame.image.load("images/player_pistol.png")
font = pygame.font.SysFont(None, 20)



class Player:  # Player Character
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.moving_right = False
        self.moving_left = False
        self.hit_box = (self.x + 20, self.y, 28, 60)

    def character_rotation(self, display):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        angle = (180 / math.pi) * - math.atan2(rel_y, rel_x)
        playerangle = (180 / math.pi) * math.atan2(rel_x, rel_y)

        player_walk_image = pygame.transform.rotate(pygame.transform.scale(player_pistol, (128, 168)), playerangle)
        player_pos = (self.x - player_walk_image.get_rect().width / 2,
                      self.y - player_walk_image.get_rect().height / 2)
        display.blit(player_walk_image, player_pos)

        self.hit_box = (self.x - 20, self.y - 15, 28, 28)  # hitbox update
        pygame.draw.rect(display, (255, 0, 0), self.hit_box, 2)  # display hitbox

    def main_act(self, display):
        self.character_rotation(display)

        self.moving_right = False
        self.moving_left = False

        # pygame.draw.rect(display, (255,0,0), (self.x, self.y, self.width, self.height))


class PlayerBullet:  # Player Bullet
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 30
        self.angle = math.atan2(y - mouse_y, x - mouse_x)
        self.x_velocity = math.cos(self.angle) * self.speed
        self.y_velocity = math.sin(self.angle) * self.speed

    def main(self, display):
        self.x -= int(self.x_velocity)
        self.y -= int(self.y_velocity)
        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 5)


class Enemy:  # Enemy Class
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_images = [pygame.image.load("slime_animation_0.png"), pygame.image.load("slime_animation_1.png"),
                                 pygame.image.load("slime_animation_2.png"), pygame.image.load("slime_animation_3.png")]
        self.animation_count = 0
        self.reset_offset = 0
        self.offset_x = random.randrange(-150, 150)
        self.offset_y = random.randrange(-150, 150)
        self.hp = 3
        self.hit_box = (self.x - display_scroll[0], self.y - display_scroll[1], 28, 30)

    def hit(self):
        print(self.hp)
        self.hp -= 1

    def main(self, display):
        if self.animation_count == 15:
            self.animation_count = 0
        self.animation_count += 1

        if self.reset_offset == 0:
            self.offset_x = random.randrange(-150, 150)
            self.offset_y = random.randrange(-150, 150)
            self.reset_offset = random.randrange(120, 150)
        else:
            self.reset_offset -= 1

        if player.x + self.offset_x > self.x - display_scroll[0]:
            self.x += 1
        elif player.x + self.offset_x < self.x - display_scroll[0]:
            self.x -= 1

        if player.y + self.offset_y > self.y - display_scroll[1]:
            self.y += 1
        elif player.y + self.offset_y < self.y - display_scroll[1]:
            self.y -= 1

        display.blit(pygame.transform.scale(self.animation_images[self.animation_count // 4], (32, 30)),
                     (self.x - display_scroll[0], self.y - display_scroll[1]))
        self.hit_box = (self.x - display_scroll[0], self.y - display_scroll[1], 28, 30)
        pygame.draw.rect(display, (255, 0, 0), self.hit_box, 2)

class cursor:  # Mouse Cursor
    def __init__(self,x,y):
        self.x = x
        self.y = y

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False

def main_menu():
    menu_sound = mixer.Sound("sounds/menu_theme.mp3")
    menu_sound.play(loops = -1)
    while True:
        display.fill((0, 0, 0))
        draw_text('Main Menu', font, (255, 255, 255), display, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50,100,200,50)

        button_2 = pygame.Rect(50,200,200,50)
        if button_1.collidepoint((mx,my)):
            if click:
                menu_sound.stop()
                return True

        if button_2.collidepoint((mx,my)):
            if click:
                pass


        pygame.draw.rect(display, (255,0,0), button_1)
        pygame.draw.rect(display, (255,0,0), button_2)
        display.blit(font.render("Start", True, (255,255,255)), (50,100))
        display.blit(font.render("Option", True, (255,255,255)), (50,200))
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(60)

main_menu()

player = Player(400, 300, 32, 32)  # player initiation
display_scroll = [0, 0]
player_bullets = []  # dealing with many bullets
enemies = [Enemy(300, 400), Enemy(200, 300)]
sound = mixer.Sound("sounds/game_theme_1.wav") # Main Theme
sound.play(loops = 0)
while True:
    display.fill((24, 164, 86))  # fill display with color
    mouse_x, mouse_y = pygame.mouse.get_pos()
    angle = math.atan2(mouse_y - (player.y + 32), mouse_x - (player.x + 26))  # angle(between mouse and player)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player_bullets.append(PlayerBullet(player.x - 25, player.y, mouse_x, mouse_y))

    keys = pygame.key.get_pressed()  # scrolling movement.
    # pygame.draw.rect(display, (255,255,255), (100 - display_scroll[0], 100 - display_scroll[1], 16, 16))
    if keys[pygame.K_a]:  # movement codes
        display_scroll[0] -= 5
        player.moving_left = True
        for bullet in player_bullets:
            bullet.x += 5
    if keys[pygame.K_d]:
        display_scroll[0] += 5
        player.moving_right = True
        for bullet in player_bullets:
            bullet.x -= 5
    if keys[pygame.K_w]:
        display_scroll[1] -= 5
        for bullet in player_bullets:
            bullet.y += 5
    if keys[pygame.K_s]:
        display_scroll[1] += 5
        for bullet in player_bullets:
            bullet.y -= 5

    player.main_act(display)

    for bullet in player_bullets:
        for enemy in enemies:
            if bullet.y - 5 < enemy.hit_box[1] + enemy.hit_box[3] and bullet.y + 5 > enemy.hit_box[1]:
                if bullet.x + 5 > enemy.hit_box[0] and bullet.x - 5 < enemy.hit_box[0] + enemy.hit_box[2]:
                    enemy.hit()
                    player_bullets.pop(player_bullets.index(bullet))

        bullet.main(display)
    for enemy in enemies:
        if enemy.hp > 0:
            enemy.main(display)

    clock.tick(60)
    pygame.display.update()
