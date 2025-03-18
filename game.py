import pgzrun
import random
import time

WIDTH = 800
HEIGHT = 600

background_x = 0
ground1_x = 0

planet = Actor('planet', (650, 100))

BACKGROUND_SPEED = 2
GROUND_SPEED = 2

# Dino karakteri
idle_images = ['pink_stand', 'pink_walk1']
jump_image = 'pink_jump'
crouch_image = 'pink_duck'

dino_y = HEIGHT - 170
dino = Actor(idle_images[0], (100, dino_y))
dino.velocity_y = 0

GRAVITY = 0.5
JUMP_STRENGTH = -15

# Engeller ve Nesneler
bird = Actor('bee', (900, 375))
snail_y = HEIGHT - 150
snail = Actor('snail', (900, snail_y))
coin = Actor('coin', (900, 420))

is_jumping = False
is_crouching = False
score = 0
game_over = False
game_started = False
sound_on = True

CROUCH_OFFSET = 20

coin_sound = sounds.coin
jump_sound = sounds.jump

# Müzik butonu
music_button = Actor('music_on', (700, 50))

def start_music():
    if sound_on:
        sounds.music.stop()
        sounds.music.play(-1)
        sounds.music.set_volume(0.5)

def toggle_music():
    global sound_on
    sound_on = not sound_on
    if sound_on:
        sounds.music.stop()
        sounds.music.play(-1)
        music_button.image = 'music_on'
    else:
        sounds.music.stop()
        music_button.image = 'music_off'

def update():
    global background_x, ground1_x, game_over, is_jumping, is_crouching, score

    if game_started and not game_over:
        background_x -= BACKGROUND_SPEED
        if background_x <= -WIDTH:
            background_x = 0

        ground1_x -= GROUND_SPEED
        if ground1_x <= -WIDTH:
            ground1_x = 0

        dino.velocity_y += GRAVITY
        dino.y += dino.velocity_y

        if dino.y > HEIGHT - 170:
            dino.y = HEIGHT - 170
            dino.velocity_y = 0
            is_jumping = False

        bird.x -= 5 + random.randint(-1, 1)
        snail.x -= 3 + random.randint(-1, 1)
        coin.x -= 4 + random.randint(-1, 1)

        if bird.x < -50:
            while True:
                bird.x = random.randint(900, 1500)
                if abs(bird.x - snail.x) > 400:
                    break

        if snail.x < -50:
            while True:
                snail.x = random.randint(1600, 2200)
                if abs(snail.x - bird.x) > 400:
                    break

        if coin.x < -50:
            while True:
                coin.x = random.randint(1200, 1800)
                if abs(coin.x - bird.x) > 400 and abs(coin.x - snail.x) > 400:
                    break

        if is_jumping:
            dino.image = jump_image
        elif is_crouching:
            dino.image = crouch_image
            dino.y = HEIGHT - 180 + CROUCH_OFFSET
        else:
            dino.image = idle_images[int(time.time() * 10) % len(idle_images)]
            dino.y = HEIGHT - 170

        if dino.colliderect(coin):
            score += 1
            coin.x = random.randint(900, 1200)
            if sound_on:
                coin_sound.play()

        if dino.colliderect(snail) or dino.colliderect(bird):
            game_over = True

def draw():
    screen.clear()
    if not game_started:
        screen.fill("white")
        screen.draw.text("START", center=(400, 250), color="black", fontsize=50)
        screen.draw.text("EXIT", center=(400, 350), color="black", fontsize=50)
        music_button.pos = (700, 50)
        music_button.draw()
    elif game_over:
        screen.fill("white")
        screen.draw.text("GAME OVER", center=(400, 200), color="red", fontsize=60)
        screen.draw.text(f"Final Score: {score}", center=(400, 250), color="black", fontsize=40)
        screen.draw.text("RESTART", center=(400, 350), color="black", fontsize=50)
        music_button.pos = (700, 450)
        music_button.draw()
    else:
        screen.blit('background', (background_x, 0))
        screen.blit('background', (background_x + WIDTH, 0))
        screen.blit('ground1', (ground1_x, HEIGHT - 150))
        screen.blit('ground1', (ground1_x + WIDTH, HEIGHT - 150))
        planet.draw()
        dino.draw()
        bird.draw()
        snail.draw()
        coin.draw()
        screen.draw.text(f"Score: {score}", (10, 10), color="white")

def on_mouse_down(pos):
    global game_started, game_over, score
    if not game_started:
        if 350 <= pos[0] <= 450 and 225 <= pos[1] <= 275:
            game_started = True
            start_music()
        elif 350 <= pos[0] <= 450 and 325 <= pos[1] <= 375:
            exit()
        elif music_button.collidepoint(pos):
            toggle_music()
    elif game_over:
        if 350 <= pos[0] <= 450 and 325 <= pos[1] <= 375:
            game_over = False
            game_started = True
            score = 0
            bird.x = 900
            snail.x = 900
            coin.x = 900
            start_music()
        elif music_button.collidepoint(pos):
            toggle_music()

def on_key_down(key):
    global is_jumping, is_crouching, dino
    if key == keys.UP and not is_jumping:
        dino.velocity_y = JUMP_STRENGTH
        is_jumping = True
        if sound_on:
            jump_sound.play()
    elif key == keys.DOWN:
        is_crouching = True

def on_key_up(key):
    global is_crouching
    if key == keys.DOWN:
        is_crouching = False

pgzrun.go()
