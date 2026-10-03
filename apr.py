import pygame
from random import randint

WIDTH = 800
HEIGHT = 600
FPS = 30
SPEED = 5

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)

pygame.init()
pygame.font.init()
font_t50 = pygame.sysfont.SysFont("Tahoma", 50)

clock = pygame.time.Clock()
timer = 180
pygame.time.set_timer(pygame.USEREVENT,1000)

LIVES_COUNT = 3
lives = LIVES_COUNT
score = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))

dino_images = []
dino_image_index = 0

pygame.mixer.music.load("Super_Mario.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

music_buttons = []
music_button = pygame.image.load("702139.png")
music_button = pygame.transform.scale(music_button,(64,64))
music_buttons.append(music_button)
music_button = pygame.image.load("VolumeMaxim.png")
music_button = pygame.transform.scale(music_button,(64,64))
music_buttons.append(music_button)

music_rect = music_button.get_rect()
music_rect.center = 40, 100

for i in range(1,7):
    dino_image = pygame.image.load("images/walk"+str(i)+".png")
    dino_image = pygame.transform.rotozoom(dino_image, 0, 0.7)
    dino_images.append(dino_image)

dino = dino_image.get_rect()
dino.center = (WIDTH//2, HEIGHT//2)
dino_angle = 0
dino_speed = [0,10]
dino_is_jump = False
dino_is_walk = False
dino_direction = "RIGHT"

spike_image = pygame.image.load("spike.png")
spike_image = pygame.transform.rotozoom(spike_image, 0, 0.5)
spike = spike_image.get_rect()
spike.center = 700, 385

ground = 416
cactus_image = pygame.image.load("cactus.png")
cactus_image = pygame.transform.rotozoom(cactus_image, 0, 0.5)
cactus = cactus_image.get_rect()
cactus.bottom = ground
cactus.left = 0
cactus_speed = 5

heal_image = pygame.image.load("heal.png")
heal = heal_image.get_rect()
heal.center = randint(10, WIDTH-10), randint(10, ground - 10)


coins = []
coin_image = pygame.image.load("coin.png")
for i in range(10):
    coin = coin_image.get_rect()
    coin.center = randint(10, WIDTH-10), randint(10, ground - 10)
    coins.append(coin)



back_image = pygame.image.load("background.png")
back_image = pygame.transform.scale(back_image, (WIDTH, HEIGHT))

back = pygame.image.load("background.png")
back = pygame.transform.scale(back, (WIDTH, HEIGHT))

button_start_off = pygame.image.load("go1.png")
button_start_on = pygame.image.load("go2.png")
button_start_collider = button_start_off.get_rect()
button_start_collider.center = WIDTH//2, HEIGHT//2

button_exit = pygame.image.load("exit.png")
button_exit = pygame.transform.rotozoom(button_exit, 0, 0.15)
button_exit_collider = button_start_off.get_rect()
button_exit_collider.center = WIDTH, 100

bip = pygame.mixer.Sound("coins.mp3")
bip.set_volume(0.1)

run = True
status = "START"

while run:

    while status == "START":
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and button_start_collider.collidepoint(event.pos):
                bip.play()
                status = "PLAY"
            if event.type == pygame.MOUSEBUTTONDOWN and button_exit_collider.collidepoint(event.pos):
                run = False
                status = "EXIT"

        screen.blit(back, (0, 0))

        if button_start_collider.collidepoint(pygame.mouse.get_pos()):
            screen.blit(button_start_on, button_start_collider)
        else:
            screen.blit(button_start_off, button_start_collider)
        screen.blit(button_exit, button_exit_collider)
        pygame.display.update()

    while status == "PLAY":
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
                status = "EXIT"
            if event.type == pygame.USEREVENT:
                timer -= 1
                if timer <=0:
                    status = "FINISH"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                status = "PAUSE"
                pause_screen = pygame.Surface((WIDTH, HEIGHT))
                pause_screen.fill(RED)
                pause_screen.set_alpha(5)
                pause_text = font_t50.render("Нажмите P для продолжения", True, WHITE)
                while status == "PAUSE":
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT and event.key == pygame.K_ESCAPE:
                            run = False
                            status = "EXIT"
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                            status = "PLAY"

                        screen.blit(pause_screen, (0,0))
                        screen.blit(pause_text, (75, HEIGHT//2))
                        pygame.display.update()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    dino_speed[0] = -SPEED
                    dino_is_walk = True
                    dino_direction = "LEFT"
                if event.key == pygame.K_d:
                    dino_speed[0] = SPEED
                    dino_is_walk = True
                    dino_direction = "RIGHT"
                if event.key == pygame.K_SPACE and not dino_is_jump:
                    dino.y -= 300
                    dino_is_jump = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d and dino_speed[0] > 0:
                    dino_speed[0] = 0
                    dino_is_walk = False
                if event.key == pygame.K_a and dino_speed[0] < 0:
                    dino_speed[0] = 0
                    dino_is_walk = False
            if event.type == pygame.MOUSEWHEEL:
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + event.y/10)
            if event.type == pygame.MOUSEBUTTONDOWN and music_rect.collidepoint(event.pos):
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

        dino_new_image = pygame.transform.rotozoom(dino_image, dino_angle, 1)

        cactus.x += cactus_speed
        if cactus.right >= WIDTH or cactus.left <= 0:
            cactus_speed = -cactus_speed

        dino.move_ip(dino_speed)
        if dino.bottom >= ground:
            dino.bottom = ground
            dino_is_jump = False
        if dino.colliderect(cactus):
            lives -= 1
            if lives <= 0:
                status = "FINISH"
        if dino.collidelist(coins) != -1:
            coins.pop(dino.collidelist(coins))
            if len(coins) == 0:
                status = "FINISH"
        if dino.colliderect(heal) != -1:
            SPEED = 10
        if dino.colliderect(spike):
            SPEED = 5




        screen.blit(back_image, (0,0))


        if dino_direction == "RIGHT":
            screen.blit(dino_images[dino_image_index], dino)
        if dino_direction == "LEFT":
            screen.blit(pygame.transform.flip(dino_images[dino_image_index], 1, 0), dino)

        if dino_is_walk:
            if dino_image_index < 5:
                dino_image_index += 1
            else:
                dino_image_index = 0
        screen.blit(cactus_image, cactus)
        screen.blit(spike_image, spike)
        screen.blit(heal_image, heal)


        for coin in coins:
            screen.blit(coin_image, coin)

        screen.blit(music_buttons[pygame.mixer.music.get_busy()], music_rect)

        timer_text = font_t50.render("Время: "+str(timer), True, WHITE)
        screen.blit(timer_text, (10,10))

        lives_text = font_t50.render("Жизни: " + str(lives), True, WHITE)
        screen.blit(lives_text, (550, 10))


        pygame.display.update()

    while status == "FINISH":
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and button_start_collider.collidepoint(event.pos):
                bip.play()
                status = "PLAY"
            if event.type == pygame.MOUSEBUTTONDOWN and button_exit_collider.collidepoint(event.pos):
                run = False
                status = "EXIT"


        screen.blit(back, (0, 0))

        if button_start_collider.collidepoint(pygame.mouse.get_pos()):
            screen.blit(button_start_on, button_start_collider)
        else:
            screen.blit(button_start_off, button_start_collider)
        screen.blit(button_exit, button_exit_collider)
        pygame.display.update()