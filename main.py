import pygame
import sys
import math
import random
import time
from pygame.locals import *
from pygame import mixer

pygame.init()  # initialization
WINDOW_SIZE = (800, 600)
display = pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF)
clock = pygame.time.Clock()
wall_image = pygame.image.load("images/wall.png")
bullet_image = pygame.image.load("images/fire.png")
cannon_image = pygame.image.load("images/cannon.png")
explosion_images = [pygame.image.load("images/explosion0.png"), pygame.image.load("images/explosion1.png"),
                    pygame.image.load("images/explosion2.png"), pygame.image.load("images/explosion3.png"),
                    pygame.image.load("images/explosion4.png"), pygame.image.load("images/explosion5.png"),
                    pygame.image.load("images/explosion6.png")]
blood_images = [pygame.image.load("images/blood_0.png"),pygame.image.load("images/blood_1.png"),
                pygame.image.load("images/blood_2.png"),pygame.image.load("images/blood_3.png")]

player_pistol = pygame.image.load("images/player_pistol.png")  # player images
player_shotgun = pygame.image.load("images/player_shotgun.png")
player_rifle = pygame.image.load("images/player_rifle.png")
player_rocket = pygame.image.load("images/player_rocket.png")
cursor_image = pygame.image.load("images/aim.png")  # cursur image
police_pistol = pygame.image.load("images/police_pistol.png")  # Police Images
police_shotgun = pygame.image.load("images/police_shotgun.png")
police_rifle = pygame.image.load("images/police_rifle.png")
police_car = pygame.image.load("images/car.png")
police_rocket = pygame.image.load("images/police_rocket.png")
police_shield = pygame.image.load("images/police_shield.png")
tutorial_image = pygame.image.load("images/tutorial.png")

reload_sound = mixer.Sound("sounds/pistol_reload.wav")
explosion_sound= mixer.Sound("sounds/explosion.wav")
launcher_sound = mixer.Sound("sounds/launcher_sound.mp3")
shotgun_sound = mixer.Sound("sounds/shotgun_sound.wav")
rifle_sound = mixer.Sound("sounds/rifle_sound.wav")
sniper_sound = mixer.Sound("sounds/sniper_sound.wav")
dead_sound = mixer.Sound("sounds/dead_sound.wav")
siren_sound = mixer.Sound("sounds/police_siren.wav")
police_death_sound_0 = mixer.Sound("sounds/police_death_0.wav")
police_death_sound_1 = mixer.Sound("sounds/police_death_1.wav")

UI_font = pygame.font.SysFont(None, 40)
menu_font = pygame.font.SysFont(None, 40)
title_font = pygame.font.SysFont(None, 100)
timer_font = pygame.font.SysFont(None, 20)

# Player Character
class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = 5
        self.ammo = 6
        self.start_time = pygame.time.get_ticks()
        self.cooldown = 2500
        self.animation_count = 0
        self.moving_right = False
        self.moving_left = False
        self.hit_box = (self.x + 20, self.y, 28, 60)
        self.pistol_mode = True
        self.rifle_mode = False
        self.rocket_mode = False
        self.shotgun_mode = False
        self.sound_count = 0

    def character_rotation(self, display):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        angle = (180 / math.pi) * - math.atan2(rel_y, rel_x)
        playerangle = (180 / math.pi) * math.atan2(rel_x, rel_y)
        if self.pistol_mode:
            player_walk_image = pygame.transform.rotate(pygame.transform.scale(player_pistol, (128, 168)), playerangle)
            #print("P")
        elif self.rifle_mode:
            player_walk_image = pygame.transform.rotate(pygame.transform.scale(player_rifle, (128, 168)), playerangle)
        elif self.shotgun_mode:
            player_walk_image = pygame.transform.rotate(pygame.transform.scale(player_shotgun, (128, 168)), playerangle)
            #print("S")
        elif self.rocket_mode:
            player_walk_image = pygame.transform.rotate(pygame.transform.scale(player_rocket, (128, 168)), playerangle)

        #player_walk_image = pygame.transform.rotate(pygame.transform.scale(player_pistol, (128, 168)), playerangle)
        player_pos = (self.x - player_walk_image.get_rect().width / 2,
                      self.y - player_walk_image.get_rect().height / 2)
        display.blit(player_walk_image, player_pos)

        self.hit_box = (self.x - 20, self.y - 15, 28, 28)  # hitbox update
        #pygame.draw.rect(display, (255, 0, 0), self.hit_box, 2)  # display hitbox

    def hit(self):
        self.hp -= 1

    def reload(self):
        if self.sound_count == 0:
            reload_sound = mixer.Sound("sounds/pistol_reload.wav")
            reload_sound.play()
            self.sound_count += 1

        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= self.cooldown:
            self.ammo = 6
            self.sound_count = 0
            self.start_time = pygame.time.get_ticks()

    def main_act(self, display):
        self.character_rotation(display)

        self.moving_right = False
        self.moving_left = False


        # pygame.draw.rect(display, (255,0,0), (self.x, self.y, self.width, self.height))


# Player Bullet
class Bullet:
    def __init__(self, x, y, mouse_x, mouse_y, speed):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = speed
        self.angle = math.atan2(y - mouse_y, x - mouse_x)
        self.x_velocity = math.cos(self.angle) * self.speed
        self.y_velocity = math.sin(self.angle) * self.speed
        self.rel_x, self.rel_y = self.mouse_x - self.x, self.mouse_y - self.y
        self.bullet_angle = (180 / math.pi) * math.atan2(self.rel_x, self.rel_y)

    def main(self, display):
        self.x -= int(self.x_velocity)
        self.y -= int(self.y_velocity)

        # if self.owner:
        #   pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 5)
        # else:
        #   pygame.draw.circle(display, (255, 0, 0), (self.x, self.y), 5)
        bullet_image_2 = pygame.transform.rotate(pygame.transform.scale(bullet_image, (32, 32)), self.bullet_angle)
        bullet_pos = (self.x - bullet_image_2.get_rect().width / 2,
                      self.y - bullet_image_2.get_rect().height / 2)
        display.blit(bullet_image_2, bullet_pos)

# Projectile Classes
class EnemyBullet:
    def __init__(self, x, y, mouse_x, mouse_y, speed):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = speed
        self.angle = math.atan2(y - mouse_y, x - mouse_x)
        self.x_velocity = math.cos(self.angle) * self.speed
        self.y_velocity = math.sin(self.angle) * self.speed
        self.rel_x, self.rel_y = self.mouse_x - self.x, self.mouse_y - self.y
        self.bulletangle = (180 / math.pi) * math.atan2(self.rel_x, self.rel_y)

    def main(self, display):
        self.x -= int(self.x_velocity)
        self.y -= int(self.y_velocity)

        # if self.owner:
        #   pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 5)
        # else:
        #   pygame.draw.circle(display, (255, 0, 0), (self.x, self.y), 5)
        bullet_image_2 = pygame.transform.rotate(pygame.transform.scale(bullet_image, (32, 32)), self.bulletangle)
        bullet_pos = (self.x - bullet_image_2.get_rect().width / 2 - display_scroll[0],
                      self.y - bullet_image_2.get_rect().height / 2 - display_scroll[1])
        display.blit(bullet_image_2, bullet_pos)

class EnemyCannon:
    def __init__(self, x, y, mouse_x, mouse_y, speed):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = speed
        self.angle = math.atan2(y - mouse_y, x - mouse_x)
        self.x_velocity = math.cos(self.angle) * self.speed
        self.y_velocity = math.sin(self.angle) * self.speed
        self.rel_x, self.rel_y = self.mouse_x - self.x, self.mouse_y - self.y
        self.bulletangle = (180 / math.pi) * math.atan2(self.rel_x, self.rel_y)

    def main(self, display):
        self.x -= int(self.x_velocity)
        self.y -= int(self.y_velocity)

        # if self.owner:
        #   pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 5)
        # else:
        #   pygame.draw.circle(display, (255, 0, 0), (self.x, self.y), 5)
        bullet_image_2 = pygame.transform.rotate(pygame.transform.scale(cannon_image, (32, 32)), self.bulletangle)
        bullet_pos = (self.x - bullet_image_2.get_rect().width / 2 - display_scroll[0],
                      self.y - bullet_image_2.get_rect().height / 2 - display_scroll[1])
        display.blit(bullet_image_2, bullet_pos)


class Cannon:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 30
        self.angle = math.atan2(y - mouse_y, x - mouse_x)
        self.x_velocity = math.cos(self.angle) * self.speed
        self.y_velocity = math.sin(self.angle) * self.speed
        self.rel_x, self.rel_y = self.mouse_x - self.x, self.mouse_y - self.y
        self.bulletangle = (180 / math.pi) * math.atan2(self.rel_x, self.rel_y)

    def main(self, display):
        self.x -= int(self.x_velocity)
        self.y -= int(self.y_velocity)

        # if self.owner:
        #   pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 5)
        # else:
        #   pygame.draw.circle(display, (255, 0, 0), (self.x, self.y), 5)
        cannon_image_2 = pygame.transform.rotate(pygame.transform.scale(cannon_image, (32, 32)), self.bulletangle)
        cannon_pos = (self.x - cannon_image_2.get_rect().width / 2,
                      self.y - cannon_image_2.get_rect().height / 2)
        display.blit(cannon_image_2, cannon_pos)


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_count = 0

    def main(self, display):
        position = (self.x - display_scroll[0], self.y - display_scroll[1])

        self.animation_count += 1
        display.blit(pygame.transform.scale(explosion_images[self.animation_count // 4], (64, 64)), position)
        if self.animation_count == 27:
            explosions.pop(explosions.index(self))

            self.animation_count = 0

class Blood:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_count = 0

    def main(self, display):
        position = (self.x - display_scroll[0] - 45, self.y - display_scroll[1] - 45)

        self.animation_count += 1
        display.blit(pygame.transform.scale(blood_images[self.animation_count // 4], (128, 128)), position)
        if self.animation_count == 15:
            bloods.pop(bloods.index(self))

            self.animation_count = 0


# Enemy Class
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.reset_offset = 0
        self.offset_x = random.randrange(-300, 300)
        self.offset_y = random.randrange(-300, 300)
        self.hp = 3
        self.hit_box = (self.x - display_scroll[0], self.y - display_scroll[1], 20, 20)
        self.bullets = []
        self.shootdelay = 0
        self.shootdelayadd = 0.02

    def shoot(self, player_x, player_y):
        enemy_bullets.append(EnemyBullet(self.x, self.y,
                                        player_x + display_scroll[0], player_y + display_scroll[1], 10))

    def hit(self):

        self.hp -= 1

    def cannonhit(self):

        self.hp -= 10

    def main(self, display):
        player_x, player_y = player.x, player.y
        rel_x, rel_y = player_x - (self.x - display_scroll[0]), player_y - (self.y - display_scroll[1])
        # angle = (180 / math.pi) * - math.atan2(rel_y, rel_x)
        policeangle = (180 / math.pi) * math.atan2(rel_x, rel_y)

        if self.reset_offset == 0:
            self.offset_x = random.randrange(-300, 300)
            self.offset_y = random.randrange(-300, 300)
            self.reset_offset = random.randrange(120, 150)
        else:
            self.reset_offset -= 1

        if player_x + self.offset_x > self.x - display_scroll[0]:
            self.x += 2

        elif player_x + self.offset_x < self.x - display_scroll[0]:
            self.x -= 2

        if player_y + self.offset_y > self.y - display_scroll[1]:
            self.y += 2
        elif player_y + self.offset_y < self.y - display_scroll[1]:
            self.y -= 2

        if self.shootdelay >= 1:
            self.shoot(player_x, player_y)

            self.shootdelay = 0

        # display.blit(pygame.transform.scale(police_pistol, (128,168)),
        #            (self.x - display_scroll[0], self.y - display_scroll[1]))
        police_walk_image = pygame.transform.rotate(pygame.transform.scale(police_pistol, (128, 168)), policeangle)
        police_pos = (self.x - police_walk_image.get_rect().width / 2 - display_scroll[0],
                      self.y - police_walk_image.get_rect().height / 2 - display_scroll[1])
        display.blit(police_walk_image, police_pos)

        self.hit_box = (self.x - display_scroll[0] - 20, self.y - display_scroll[1] - 20, 50, 50)
        #pygame.draw.rect(display, (255, 0, 0), self.hit_box, 2)

        self.shootdelay += self.shootdelayadd


class Enemy_rifle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.reset_offset = 0
        self.offset_x = random.randrange(-300, 300)
        self.offset_y = random.randrange(-300, 300)
        self.hp = 3
        self.hit_box = (self.x - display_scroll[0], self.y - display_scroll[1], 10, 10)
        self.bullets = []
        self.shootdelay = 0
        self.shootdelayadd = 0.02

    def shoot(self, player_x, player_y):
        enemy_bullets.append(
            EnemyBullet(self.x, self.y, player_x + display_scroll[0], player_y + display_scroll[1], 12))

    def hit(self):

        self.hp -= 1

    def cannonhit(self):

        self.hp -= 10

    def main(self, display):
        player_x, player_y = player.x, player.y
        rel_x, rel_y = player_x - (self.x - display_scroll[0]), player_y - (self.y - display_scroll[1])
        # angle = (180 / math.pi) * - math.atan2(rel_y, rel_x)
        policeangle = (180 / math.pi) * math.atan2(rel_x, rel_y)

        if self.reset_offset == 0:
            self.offset_x = random.randrange(-300, 300)
            self.offset_y = random.randrange(-300, 300)
            self.reset_offset = random.randrange(120, 150)
        else:
            self.reset_offset -= 1

        if player_x + self.offset_x > self.x - display_scroll[0]:
            self.x += 2

        elif player_x + self.offset_x < self.x - display_scroll[0]:
            self.x -= 2

        if player_y + self.offset_y > self.y - display_scroll[1]:
            self.y += 2
        elif player_y + self.offset_y < self.y - display_scroll[1]:
            self.y -= 2

        if math.pow(player_y - (self.y - display_scroll[1]), 2) + math.pow(player_x - (self.x - display_scroll[0]),
                                                                           2) < 100000:  # attack range
            if self.shootdelay >= 0.5:
                self.shoot(player_x, player_y)
                self.shootdelay = 0

        # display.blit(pygame.transform.scale(police_pistol, (128,168)),
        #            (self.x - display_scroll[0], self.y - display_scroll[1]))
        police_walk_image = pygame.transform.rotate(pygame.transform.scale(police_rifle, (128, 168)), policeangle)
        police_pos = (self.x - police_walk_image.get_rect().width / 2 - display_scroll[0],
                      self.y - police_walk_image.get_rect().height / 2 - display_scroll[1])
        display.blit(police_walk_image, police_pos)

        self.hit_box = (self.x - display_scroll[0] - 20, self.y - display_scroll[1] - 20, 50, 50)
        #pygame.draw.rect(display, (255, 0, 0), self.hit_box, 2)

        self.shootdelay += self.shootdelayadd


class Enemy_shotgun:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.reset_offset = 0
        self.offset_x = random.randrange(-300, 300)
        self.offset_y = random.randrange(-300, 300)
        self.hp = 3
        self.hit_box = (self.x - display_scroll[0], self.y - display_scroll[1], 10, 10)
        self.bullets = []
        self.shootdelay = 0
        self.shootdelayadd = 0.02

    def shoot(self, player_x, player_y):
        enemy_bullets.append(EnemyBullet(self.x, self.y,
                                        player_x + display_scroll[0], player_y + display_scroll[1], 10))
        enemy_bullets.append(EnemyBullet(self.x, self.y,
                                        player_x + display_scroll[0] + 10, player_y + display_scroll[1] + 10, 10))
        enemy_bullets.append(EnemyBullet(self.x, self.y,
                                        player_x + display_scroll[0] - 10, player_y + display_scroll[1] - 10, 10))
        enemy_bullets.append(EnemyBullet(self.x, self.y,
                                        player_x + display_scroll[0] + 10, player_y + display_scroll[1] - 10, 10))

    def hit(self):
        self.hp -= 1

    def cannonhit(self):
        self.hp -= 10

    def main(self, display):
        player_x, player_y = player.x, player.y
        rel_x, rel_y = player_x - (self.x - display_scroll[0]), player_y - (self.y - display_scroll[1])
        # angle = (180 / math.pi) * - math.atan2(rel_y, rel_x)
        policeangle = (180 / math.pi) * math.atan2(rel_x, rel_y)

        if self.reset_offset == 0:
            self.offset_x = random.randrange(-300, 300)
            self.offset_y = random.randrange(-300, 300)
            self.reset_offset = random.randrange(120, 150)
        else:
            self.reset_offset -= 1

        if player_x + self.offset_x > self.x - display_scroll[0]:
            self.x += 3

        elif player_x + self.offset_x < self.x - display_scroll[0]:
            self.x -= 3

        if player_y + self.offset_y > self.y - display_scroll[1]:
            self.y += 3
        elif player_y + self.offset_y < self.y - display_scroll[1]:
            self.y -= 3

        if self.shootdelay >= 2:
            self.shoot(player_x, player_y)
            self.shootdelay = 0

        # display.blit(pygame.transform.scale(police_pistol, (128,168)),
        #            (self.x - display_scroll[0], self.y - display_scroll[1]))
        police_walk_image = pygame.transform.rotate(pygame.transform.scale(police_shotgun, (128, 168)), policeangle)
        police_pos = (self.x - police_walk_image.get_rect().width / 2 - display_scroll[0],
                      self.y - police_walk_image.get_rect().height / 2 - display_scroll[1])
        display.blit(police_walk_image, police_pos)

        self.hit_box = (self.x - display_scroll[0] - 20, self.y - display_scroll[1] - 20, 50, 50)
        #pygame.draw.rect(display, (255, 0, 0), self.hit_box, 2)

        self.shootdelay += self.shootdelayadd


class Enemy_rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.reset_offset = 0
        self.offset_x = random.randrange(-300, 300)
        self.offset_y = random.randrange(-300, 300)
        self.hp = 3
        self.hit_box = (self.x - display_scroll[0], self.y - display_scroll[1], 10, 10)
        self.bullets = []
        self.shootdelay = 0
        self.shootdelayadd = 0.02

    def shoot(self, player_x, player_y):
        enemy_cannons.append(EnemyCannon(self.x, self.y,
                                        player_x + display_scroll[0], player_y + display_scroll[1], 10))
        launcher_sound.play()

    def hit(self):

        self.hp -= 1

    def cannonhit(self):

        self.hp -= 10

    def main(self, display):
        player_x, player_y = player.x, player.y
        rel_x, rel_y = player_x - (self.x - display_scroll[0]), player_y - (self.y - display_scroll[1])
        # angle = (180 / math.pi) * - math.atan2(rel_y, rel_x)
        policeangle = (180 / math.pi) * math.atan2(rel_x, rel_y)

        if self.reset_offset == 0:
            self.offset_x = random.randrange(-300, 300)
            self.offset_y = random.randrange(-300, 300)
            self.reset_offset = random.randrange(120, 150)
        else:
            self.reset_offset -= 1

        if player_x + self.offset_x > self.x - display_scroll[0]:
            self.x += 2

        elif player_x + self.offset_x < self.x - display_scroll[0]:
            self.x -= 2

        if player_y + self.offset_y > self.y - display_scroll[1]:
            self.y += 2
        elif player_y + self.offset_y < self.y - display_scroll[1]:
            self.y -= 2

        if self.shootdelay >= 5:
            self.shoot(player_x, player_y)
            self.shootdelay = 0

        # display.blit(pygame.transform.scale(police_pistol, (128,168)),
        #            (self.x - display_scroll[0], self.y - display_scroll[1]))
        police_walk_image = pygame.transform.rotate(pygame.transform.scale(police_rocket, (128, 168)), policeangle)
        police_pos = (self.x - police_walk_image.get_rect().width / 2 - display_scroll[0],
                      self.y - police_walk_image.get_rect().height / 2 - display_scroll[1])
        display.blit(police_walk_image, police_pos)

        self.hit_box = (self.x - display_scroll[0] - 20, self.y - display_scroll[1] - 20, 55, 55)
        #pygame.draw.rect(display, (255, 0, 0), self.hit_box, 2)

        self.shootdelay += self.shootdelayadd


class Enemy_shield:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.reset_offset = 0
        self.offset_x = random.randrange(-100, 100)
        self.offset_y = random.randrange(-100, 100)
        self.hp = 1
        self.hit_box = (self.x - display_scroll[0], self.y - display_scroll[1], 10, 10)
        self.bullets = []
        self.shootdelay = 0
        self.shootdelayadd = 0.02

    def shoot(self, player_x, player_y):
        enemy_bullets.append(EnemyBullet(self.x, self.y,
                                        player_x + display_scroll[0], player_y + display_scroll[1], 10))

    def hit(self):
        print(self.hp)
        self.hp -= 1

    def cannonhit(self):

        self.hp -= 10

    def main(self, display):
        player_x, player_y = player.x, player.y
        rel_x, rel_y = player_x - (self.x - display_scroll[0]), player_y - (self.y - display_scroll[1])
        # angle = (180 / math.pi) * - math.atan2(rel_y, rel_x)
        policeangle = (180 / math.pi) * math.atan2(rel_x, rel_y)

        if self.reset_offset == 0:
            self.offset_x = random.randrange(-300, 300)
            self.offset_y = random.randrange(-300, 300)
            self.reset_offset = random.randrange(120, 150)
        else:
            self.reset_offset -= 1

        if player_x + self.offset_x > self.x - display_scroll[0]:
            self.x += 2

        elif player_x + self.offset_x < self.x - display_scroll[0]:
            self.x -= 2

        if player_y + self.offset_y > self.y - display_scroll[1]:
            self.y += 2
        elif player_y + self.offset_y < self.y - display_scroll[1]:
            self.y -= 2

        if self.shootdelay >= 1:
            self.shoot(player_x, player_y)
            print("shoot")
            self.shootdelay = 0

        # display.blit(pygame.transform.scale(police_pistol, (128,168)),
        #            (self.x - display_scroll[0], self.y - display_scroll[1]))
        police_walk_image = pygame.transform.rotate(pygame.transform.scale(police_shield, (128, 168)), policeangle)
        police_pos = (self.x - police_walk_image.get_rect().width / 2 - display_scroll[0],
                      self.y - police_walk_image.get_rect().height / 2 - display_scroll[1])
        display.blit(police_walk_image, police_pos)

        self.hit_box = (self.x - display_scroll[0] - 20, self.y - display_scroll[1] - 20, 60, 60)
        #pygame.draw.rect(display, (255, 0, 0), self.hit_box, 2)

        self.shootdelay += self.shootdelayadd


class Item:
    def __init__(self, x, y, weapon):
        self.x = x
        self.y = y
        self.item_shotgun_images = [pygame.image.load("images/item_shotgun_0.png"),
                                    pygame.image.load("images/item_shotgun_1.png")]
        self.item_rifle_images = [pygame.image.load("images/item_rifle_0.png"),
                                    pygame.image.load("images/item_rifle_1.png")]
        self.item_rocket_images = [pygame.image.load("images/item_rocket_0.png"),
                                    pygame.image.load("images/item_rocket_1.png")]
        self.animation_count = 0
        self.weapon = weapon

    def main(self, display):
        position = (self.x - display_scroll[0] - 50, self.y - display_scroll[1] - 50)

        if self.animation_count + 1 == 16:
            self.animation_count = 0

        self.animation_count += 1

        if self.weapon == 0: #shotgun
            display.blit(pygame.transform.scale(self.item_shotgun_images[self.animation_count // 8], (64, 64)),
                         position)
        if self.weapon == 1: #rifle
            display.blit(pygame.transform.scale(self.item_rifle_images[self.animation_count // 8], (86, 86)),
                         position)
        if self.weapon == 2: #rocket
            display.blit(pygame.transform.scale(self.item_rocket_images[self.animation_count // 8], (86, 86)),
                         position)


        #display.blit(pygame.transform.scale(self.item_shotgun_images[self.animation_count // 8], (64, 64)), position)

class Corpse:
    def __init__(self, x, y, corpse_type):
        self.x = x
        self.y = y
        self.police_corpse_0 = pygame.image.load("images/police_corpse_0.png")
        self.police_corpse_1 = pygame.image.load("images/police_corpse_1.png")
        self.police_corpse_2 = pygame.image.load("images/police_corpse_2.png")
        self.rocket_corpse_0 = pygame.image.load("images/police_rocket_corpse_0.png")
        self.rocket_corpse_1 = pygame.image.load("images/police_rocket_corpse_1.png")
        self.shield_corpse_0 = pygame.image.load("images/police_shield_corpse_0.png")

        self.animation_count = 0
        self.corpse_type = corpse_type
        self.random_corpse = random.randint(0,3)


    def main(self, display):
        position = (self.x - display_scroll[0] - 50, self.y - display_scroll[1] - 50)


        if self.animation_count + 1 == 16:
            self.animation_count = 0

        self.animation_count += 1

        if self.corpse_type == 0: #pistol, shotgun
            if self.random_corpse == 0:
                display.blit(pygame.transform.scale(self.police_corpse_0, (128,128)), position)
            elif self.random_corpse == 1:
                display.blit(pygame.transform.scale(self.police_corpse_1, (128,128)), position)
            else:
                display.blit(pygame.transform.scale(self.police_corpse_2, (128,128)), position)
        if self.corpse_type == 1: #rocket
            if self.random_corpse == 0:
                display.blit(pygame.transform.scale(self.rocket_corpse_0, (128,128)), position)
            else:
                display.blit(pygame.transform.scale(self.rocket_corpse_1, (128,128)), position)

        if self.corpse_type == 2: #shield
            display.blit(pygame.transform.scale(self.shield_corpse_0, (128, 128)), position)

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def main(self, display):
        position = (self.x - display_scroll[0], self.y - display_scroll[1])
        collide_point = pygame.Rect(position[0], position[1], 250, 350)
        if collide_point.collidepoint((player.x, player.y)):
            if player.hp != 0:
                sniper_sound.play()
                player.hp = 0


        car_image = pygame.transform.scale(police_car, (270,350))
        #pygame.draw.rect(display, (255, 0, 0), collide_point, 2)

        display.blit(car_image, position)

class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def main(self, display):
        position = (self.x - display_scroll[0], self.y - display_scroll[1])
        collide_point = pygame.Rect(position[0], position[1], 400, 25)
        if collide_point.collidepoint((player.x, player.y)):
            if player.hp != 0:
                sniper_sound.play()
                player.hp = 0

        wallimage = pygame.transform.scale(wall_image, (384, 96))
        #pygame.draw.rect(display, (255, 0, 0), collide_point, 2)

        display.blit(wallimage, position)
# In game UI
class GameUI:
    def __init__(self, player, level, points):
        self.points = points
        self.player = player
        self.level = level

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def draw_UI(self):
        text_points = "Points : " + str(self.points)
        text_hp = "HP : " + str(player.hp)
        text_level = "Level " + str(self.level)
        text_ammo = "Ammo : " + str(player.ammo)
        self.draw_text(text_points, UI_font, (255, 255, 255), display, 40, 40)
        self.draw_text(text_hp, UI_font, (255, 255, 255), display, 40, 80)
        self.draw_text(text_ammo, UI_font, (255,255,255), display, 40, 120)
        self.draw_text(text_level, UI_font, (255, 255, 255), display, 350, 40)


# Mouse cursor
class Cursor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def main(self, display):
        self.x, self.y = pygame.mouse.get_pos()
        display.blit(cursor_image, (self.x - 5, self.y- 5))


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False


def main_menu():
    menu_sound = mixer.Sound("sounds/menu_theme.mp3")
    menu_sound.play(loops=-1)
    while True:

        display.fill((255, 200, 50))
        draw_text('Six Shot Loaded', title_font, (255, 255, 255), display, 120, 100)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(350, 300, 100, 50)

        button_2 = pygame.Rect(350, 400, 100, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                menu_sound.stop()
                return True

        if button_2.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(display, (255, 0, 0), button_1)
        pygame.draw.rect(display, (255, 0, 0), button_2)
        display.blit(menu_font.render("Start", True, (255, 200, 50)), (368, 310))
        display.blit(menu_font.render("Exit", True, (255, 200, 50)), (370, 410))
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
level = 1
point = 0
mouse_cursur = Cursor(100, 200)
game_ui = GameUI(player, level, 0)
display_scroll = [0, 0]
player_bullets = []  # dealing with player bullets
player_cannons = []
items = []
enemy_corpses = []
enemy_bullets = []  # dealing with enemy bullets
enemy_cannons = []
enemies = []
enemies_rifle = []
enemies_shotgun = []
enemies_rocket = []
enemies_shield = []
enemy_spawn_spot = [(1000, 400), (-1000, 400), (400, -1000), (400, 1000)]

explosions = []
bloods = []
main_theme = mixer.Sound("sounds/game_theme_1.wav")  # Main Theme

siren_sound.play()
main_theme.play(loops= -1)
pistol_sound = mixer.Sound("sounds/pistol_shot_1.wav")
cars = [Car(1000, -1100), Car(1000, -750), Car(1000, -400), Car(1000, -50), Car(1000, 300), Car(1000, 650),
        Car(1000, 1000),
        Car(-1000, -1100), Car(-1000, -750), Car(-1000, -400), Car(-1000, -50), Car(-1000, 300), Car(-1000, 650),
        Car(-1000, 1000), Car(-1000, 1350), Car(-1000, 1350)]
walls = [Wall(684, -1100),Wall(300,-1100),Wall(-84,-1100),Wall(-468,-1100),Wall(-852,-1100),
         Wall(684, 1100),Wall(300,1100),Wall(-84,1100),Wall(-468,1100),Wall(-852,1100)]

start_ticks = pygame.time.get_ticks()
spawn_delay = 0
spawn_shield_delay = 0
spawn_delay_add = 0.01
reload_delay = 3
reload_delay_add = 0.01
is_reloading = False
is_dead = False

while True:
    pygame.mouse.set_visible(False)
    random_number_1 = random.randint(0, 3)
    random_number_2 = random.randint(0, 3)
    random_number_3 = random.randint(0, 3)
    random_number_4 = random.randint(0, 3)
    spawn_spot_1_x, spawn_spot_1_y = enemy_spawn_spot[random_number_1]
    spawn_spot_2_x, spawn_spot_2_y = enemy_spawn_spot[random_number_2]
    spawn_spot_3_x, spawn_spot_3_y = enemy_spawn_spot[random_number_3]
    spawn_spot_4_x, spawn_spot_4_y = enemy_spawn_spot[random_number_4]
    display.fill((200, 164, 0))  # fill display with color
    display.blit(pygame.transform.scale(tutorial_image,(512, 512)), (150 - display_scroll[0],150 - display_scroll[1]))

    for wall in walls:
        wall.main(display)
    for car in cars:
        car.main(display)




    mouse_x, mouse_y = pygame.mouse.get_pos()
    game_ui = GameUI(player, level, point )

    angle = math.atan2(mouse_y - (player.y + 32), mouse_x - (player.x + 26))  # angle(between mouse and player)


    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # Timer set


    if int(elapsed_time) == 15:  # Level change
        level = 2

    elif int(elapsed_time) == 30:
        level = 3
    elif int(elapsed_time) == 45:
        level = 4
    elif int (elapsed_time) == 60:
        level = 5

    if player.hp >= 1:
        if level == 1:
            if spawn_delay >= 2.5:
                enemies.append(Enemy(spawn_spot_1_x, spawn_spot_1_y))
                spawn_delay = 0
        elif level == 2:
            if spawn_delay >= 5 and elapsed_time < 25:
                enemies.append(Enemy(spawn_spot_1_x, spawn_spot_1_y))
                enemies_rifle.append(Enemy_rifle(spawn_spot_2_x, spawn_spot_2_y))
                spawn_delay = 0
        elif level == 3:
            if spawn_delay >= 5 and elapsed_time < 36:
                enemies.append(Enemy(spawn_spot_3_x, spawn_spot_3_y))
                enemies_rifle.append(Enemy_rifle(spawn_spot_1_x, spawn_spot_1_y))
                enemies_shotgun.append(Enemy_shotgun(spawn_spot_2_x, spawn_spot_2_y))
                spawn_delay = 0
        elif level == 4:
            if spawn_delay >= 5 and elapsed_time < 52:
                enemies.append(Enemy(spawn_spot_4_x, spawn_spot_4_y))
                enemies_rifle.append(Enemy_rifle(spawn_spot_2_x, spawn_spot_2_y))
                enemies_shotgun.append(Enemy_shotgun(spawn_spot_3_x, spawn_spot_3_y))
                enemies_rocket.append(Enemy_rocket(spawn_spot_1_x, spawn_spot_1_y))
                spawn_delay = 0
        elif level == 5:
            if spawn_delay >= 5:
                enemies.append(Enemy(spawn_spot_4_x, spawn_spot_4_y))
                enemies_rifle.append(Enemy_rifle(spawn_spot_3_x, spawn_spot_3_y))
                enemies_shotgun.append(Enemy_shotgun(spawn_spot_2_x, spawn_spot_2_y))
                enemies_rocket.append(Enemy_rocket(spawn_spot_1_x, spawn_spot_1_y))
                spawn_delay = 0
            if spawn_shield_delay >= 10:
                enemies_shield.append(Enemy_shield(spawn_spot_4_x, spawn_spot_4_y))
                spawn_shield_delay = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if player.hp >= 1:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if player.pistol_mode:
                        if player.ammo >= 1:
                            player.ammo -= 1
                            pistol_sound.play()
                            player_bullets.append(Bullet(player.x - 25, player.y, mouse_x, mouse_y, 20))
                    elif player.shotgun_mode:
                        shotgun_sound.play()
                        player_bullets.append(Bullet(player.x - 25, player.y, mouse_x, mouse_y + 10, 15))
                        player_bullets.append(Bullet(player.x - 25, player.y, mouse_x - 10, mouse_y, 15))
                        player_bullets.append(Bullet(player.x - 25, player.y, mouse_x + 10, mouse_y, 15))
                        player_bullets.append(Bullet(player.x - 25, player.y, mouse_x - 10, mouse_y + 10, 15))
                        player_bullets.append(Bullet(player.x - 25, player.y, mouse_x - 5, mouse_y + 15, 15))

                        player.shotgun_mode = False
                        player.pistol_mode = True
                    elif player.rocket_mode:
                        launcher_sound.play()
                        player_cannons.append(Cannon(player.x - 25, player.y, mouse_x, mouse_y))
                        player.rocket_mode = False
                        player.pistol_mode = True
                    elif player.rifle_mode:
                        rifle_sound.play()
                        player_bullets.append(Bullet(player.x - 25, player.y, mouse_x, mouse_y, 50))
                        player.rifle_mode = False
                        player.pistol_mode = True



    keys = pygame.key.get_pressed()  # scrolling movement.

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

    if keys[pygame.K_r] and player.ammo == 0 and not is_reloading:
        reload_sound.play()
        is_reloading = True
        reload_delay = 0


    if 2 <= reload_delay <= 2.01:
        player.ammo = 6
        print("RRRRRRRRR")
        is_reloading = False




    for bullet in player_bullets:
        for enemy in enemies:
            if bullet.y - 10 < enemy.hit_box[1] + enemy.hit_box[3] and bullet.y + 10 > enemy.hit_box[1]:
                if bullet.x + 10 > enemy.hit_box[0] and bullet.x - 10 < enemy.hit_box[0] + enemy.hit_box[2]:
                    bloods.append(Blood(enemy.x, enemy.y))
                    enemy.hit()
                    player_bullets.pop(player_bullets.index(bullet))
        for enemy in enemies_rifle:
            if bullet.y - 10 < enemy.hit_box[1] + enemy.hit_box[3] and bullet.y + 10 > enemy.hit_box[1]:
                if bullet.x + 10 > enemy.hit_box[0] and bullet.x - 10 < enemy.hit_box[0] + enemy.hit_box[2]:
                    bloods.append(Blood(enemy.x, enemy.y))
                    enemy.hit()
                    player_bullets.pop(player_bullets.index(bullet))
        for enemy in enemies_shotgun:
            if bullet.y - 10 < enemy.hit_box[1] + enemy.hit_box[3] and bullet.y + 10 > enemy.hit_box[1]:
                if bullet.x + 10 > enemy.hit_box[0] and bullet.x - 10 < enemy.hit_box[0] + enemy.hit_box[2]:
                    bloods.append(Blood(enemy.x, enemy.y))
                    enemy.hit()
                    player_bullets.pop(player_bullets.index(bullet))
        for enemy in enemies_rocket:
            if bullet.y - 10 < enemy.hit_box[1] + enemy.hit_box[3] and bullet.y + 10 > enemy.hit_box[1]:
                if bullet.x + 10 > enemy.hit_box[0] and bullet.x - 10 < enemy.hit_box[0] + enemy.hit_box[2]:
                    bloods.append(Blood(enemy.x, enemy.y))
                    enemy.hit()
                    player_bullets.pop(player_bullets.index(bullet))
        for enemy in enemies_shield:
            if bullet.y - 15 < enemy.hit_box[1] + enemy.hit_box[3] and bullet.y + 15 > enemy.hit_box[1]:
                if bullet.x + 15 > enemy.hit_box[0] and bullet.x - 15 < enemy.hit_box[0] + enemy.hit_box[2]:

                    #enemy.hit()
                    player_bullets.pop(player_bullets.index(bullet))
        bullet.main(display)

    for cannon in player_cannons:
        for enemy in enemies:
            if cannon.y - 5 < enemy.hit_box[1] + enemy.hit_box[3] and cannon.y + 5 > enemy.hit_box[1]:
                if cannon.x + 5 > enemy.hit_box[0] and cannon.x - 5 < enemy.hit_box[0] + enemy.hit_box[2]:
                    enemy.cannonhit()
                    explosions.append(Explosion(enemy.x, enemy.y))
                    explosion_sound.play()
                    player_cannons.pop(player_cannons.index(cannon))

        for enemy in enemies_rifle:
            if cannon.y - 5 < enemy.hit_box[1] + enemy.hit_box[3] and cannon.y + 5 > enemy.hit_box[1]:
                if cannon.x + 5 > enemy.hit_box[0] and cannon.x - 5 < enemy.hit_box[0] + enemy.hit_box[2]:
                    enemy.cannonhit()
                    explosions.append(Explosion(enemy.x, enemy.y))
                    explosion_sound.play()
                    player_cannons.pop(player_cannons.index(cannon))
        for enemy in enemies_shotgun:
            if cannon.y - 5 < enemy.hit_box[1] + enemy.hit_box[3] and cannon.y + 5 > enemy.hit_box[1]:
                if cannon.x + 5 > enemy.hit_box[0] and cannon.x - 5 < enemy.hit_box[0] + enemy.hit_box[2]:
                    enemy.cannonhit()
                    explosions.append(Explosion(enemy.x, enemy.y))
                    explosion_sound.play()
                    player_cannons.pop(player_cannons.index(cannon))
        for enemy in enemies_rocket:
            if cannon.y - 5 < enemy.hit_box[1] + enemy.hit_box[3] and cannon.y + 5 > enemy.hit_box[1]:
                if cannon.x + 5 > enemy.hit_box[0] and cannon.x - 5 < enemy.hit_box[0] + enemy.hit_box[2]:
                    enemy.cannonhit()
                    player_cannons.pop(player_cannons.index(cannon))
                    explosion_sound.play()
        for enemy in enemies_shield:
            if cannon.y - 5 < enemy.hit_box[1] + enemy.hit_box[3] and cannon.y + 5 > enemy.hit_box[1]:
                if cannon.x + 5 > enemy.hit_box[0] and cannon.x - 5 < enemy.hit_box[0] + enemy.hit_box[2]:
                    enemy.cannonhit()
                    player_cannons.pop(player_cannons.index(cannon))
                    explosion_sound.play()

        cannon.main(display)

    for bullet in enemy_bullets:
        if bullet.y - 5 - display_scroll[1] < player.hit_box[1] + player.hit_box[3] and bullet.y + 5 - \
                display_scroll[1] > player.hit_box[1]:
            if bullet.x + 5 - display_scroll[0] > player.hit_box[0] and bullet.x - 5 - display_scroll[0] < \
                    player.hit_box[0] + player.hit_box[2]:
                player.hit()
                enemy_bullets.pop(enemy_bullets.index(bullet))
        bullet.main(display)

    for cannon in enemy_cannons:
        if cannon.y - 5 - display_scroll[1] < player.hit_box[1] + player.hit_box[3] and cannon.y + 5 - \
                display_scroll[1] > player.hit_box[1]:
            if cannon.x + 5 - display_scroll[0] > player.hit_box[0] and cannon.x - 5 - display_scroll[0] < \
                    player.hit_box[0] + player.hit_box[2]:
                player.hit()
                explosions.append(Explosion(player.x + display_scroll[0], player.y + display_scroll[1]))
                enemy_cannons.pop(enemy_cannons.index(cannon))
        cannon.main(display)

    for enemy in enemies:
        if enemy.hp > 0:
            enemy.main(display)
        else:
            enemy_corpses.append(Corpse(enemy.x, enemy.y, 0))
            police_death_sound_0.play()
            enemies.pop(enemies.index(enemy))
            point += 1  # + 1 point


    for enemy in enemies_rifle:
        if enemy.hp > 0:
            enemy.main(display)
        else:
            items.append(Item(enemy.x, enemy.y, 1))
            enemy_corpses.append(Corpse(enemy.x, enemy.y, 0))
            police_death_sound_0.play()
            enemies_rifle.pop(enemies_rifle.index(enemy))
            point += 1  # + 1 point

    for enemy in enemies_shotgun:
        if enemy.hp > 0:
            enemy.main(display)
        else:
            items.append(Item(enemy.x, enemy.y, 0))
            enemy_corpses.append(Corpse(enemy.x, enemy.y, 0))
            police_death_sound_1.play()
            enemies_shotgun.pop(enemies_shotgun.index(enemy))
            point += 1  # + 1 point

    for enemy in enemies_rocket:
        if enemy.hp > 0:
            enemy.main(display)
        else:
            items.append(Item(enemy.x, enemy.y, 2))
            enemy_corpses.append(Corpse(enemy.x, enemy.y, 1))
            police_death_sound_0.play()
            enemies_rocket.pop(enemies_rocket.index(enemy))
            point += 1  # + 1 point

    for enemy in enemies_shield:
        if enemy.hp > 0:
            enemy.main(display)
        else:
            enemy_corpses.append(Corpse(enemy.x, enemy.y, 2))
            police_death_sound_1.play()
            enemies_shield.pop(enemies_shield.index(enemy))
            game_ui.points += 1  # + 1 point


    # shotgunitem.main(display)
    for explosion in explosions:
        for enemy in enemies:
            if explosion.y - 150 < enemy.hit_box[1] + enemy.hit_box[3] and explosion.y + 150 > enemy.hit_box[1]:
                if explosion.x + 150 > enemy.hit_box[0] and explosion.x - 150 < enemy.hit_box[0] + enemy.hit_box[2]:
                    enemy.cannonhit()
        for enemy in enemies_shotgun:
            if explosion.y - 150 < enemy.hit_box[1] + enemy.hit_box[3] and explosion.y + 150 > enemy.hit_box[1]:
                if explosion.x + 150 > enemy.hit_box[0] and explosion.x - 150 < enemy.hit_box[0] + enemy.hit_box[2]:
                    enemy.cannonhit()
        for enemy in enemies_rifle:
            if explosion.y - 150 < enemy.hit_box[1] + enemy.hit_box[3] and explosion.y + 150 > enemy.hit_box[1]:
                if explosion.x + 150 > enemy.hit_box[0] and explosion.x - 150 < enemy.hit_box[0] + enemy.hit_box[2]:
                    enemy.cannonhit()
        for enemy in enemies_rocket:
            if explosion.y - 150 < enemy.hit_box[1] + enemy.hit_box[3] and explosion.y + 150 > enemy.hit_box[1]:
                if explosion.x + 150 > enemy.hit_box[0] and explosion.x - 150 < enemy.hit_box[0] + enemy.hit_box[2]:
                    enemy.cannonhit()
        for enemy in enemies_shield:
            if explosion.y - 150 < enemy.hit_box[1] + enemy.hit_box[3] and explosion.y + 150 > enemy.hit_box[1]:
                if explosion.x + 150 > enemy.hit_box[0] and explosion.x - 150 < enemy.hit_box[0] + enemy.hit_box[2]:
                    enemy.cannonhit()
        explosion.main(display)

    for item in items:
        if (item.x - 50 - display_scroll[0] < player.x < item.x + 50 - display_scroll[0]):
            if (item.y - 50 - display_scroll[1] < player.y < item.y + 50 - display_scroll[1]):
                print("Hhgg")
                if item.weapon == 0:
                    player.shotgun_mode = True
                    player.pistol_mode = False
                if item.weapon == 1:
                    player.rifle_mode = True
                    player.pistol_mode = False
                if item.weapon == 2:
                    player.rocket_mode = True
                    player.pistol_mode = False

                items.pop(items.index(item))
        item.main(display)

    for corpse in enemy_corpses:
        corpse.main(display)

    for blood in bloods:
        blood.main(display)

    spawn_delay += spawn_delay_add  # add static value in spawn_delay every frame
    spawn_shield_delay += spawn_delay_add
    reload_delay += reload_delay_add


    game_ui.draw_UI()

    timer = timer_font.render("    " + str(int(elapsed_time)), True, (255, 255, 255))
    display.blit(timer, (370, 70))

    player.main_act(display)

    mouse_cursur.main(display)  # display mouse cursur
    if player.hp <= 0:
        if is_dead == False:
            dead_sound.play()
            is_dead = True

        display.fill((0, 0, 0))
        gameover_text = UI_font.render("Game Over", True, (255, 0, 0))
        display.blit(gameover_text, (300, 250))

    clock.tick(60)
    # elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    # timer = font.render("Timer = " + str(int(elapsed_time)), True, (255, 255, 255))
    # display.blit(timer, (0, 100))
    pygame.display.update()
