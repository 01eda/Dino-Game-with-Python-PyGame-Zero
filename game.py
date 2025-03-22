import pgzrun 
import random
import time

WIDTH = 800
HEIGHT = 600

class Game:
    def __init__(self):
        self.background_x = 0
        self.ground1_x = 0
        self.game_over = False
        self.game_started = False
        self.sound_on = True
        self.game_won = False
        self.score = 0
        self.WINNING_SCORE = 3  
        self.CROUCH_OFFSET = 20
        self.music_button = Actor('music_on', (700, 50))
        self.start_music()

    def start_music(self):
        if self.sound_on:
            sounds.music.stop()
            sounds.music.play(-1)
            sounds.music.set_volume(0.5)

    def toggle_music(self):
        self.sound_on = not self.sound_on
        if self.sound_on:
            sounds.music.stop()
            sounds.music.play(-1)
            self.music_button.image = 'music_on'
        else:
            sounds.music.stop()
            self.music_button.image = 'music_off'

    def restart(self):
        self.game_over = False
        self.game_won = False
        self.game_started = True
        self.score = 0

        bird.actor.x = 900
        snail.actor.x = 900
        coin.x = 900

        dino.actor.y = HEIGHT - 170  
        dino.velocity_y = 0
        dino.is_jumping = False
        dino.is_crouching = False

        if self.sound_on:
            self.start_music()


class Dino:
    def __init__(self):
        self.idle_images = ['pink_stand', 'pink_walk1']
        self.jump_image = 'pink_jump'
        self.crouch_image = 'pink_duck'
        self.y = HEIGHT - 170
        self.actor = Actor(self.idle_images[0], (100, self.y))
        self.velocity_y = 0
        self.is_jumping = False
        self.is_crouching = False
        self.GRAVITY = 0.5
        self.JUMP_STRENGTH = -15

    def update(self):
        self.velocity_y += self.GRAVITY
        self.actor.y += self.velocity_y

        if self.actor.y > HEIGHT - 170:
            self.actor.y = HEIGHT - 170
            self.velocity_y = 0
            self.is_jumping = False

        if self.is_jumping:
            self.actor.image = self.jump_image
        elif self.is_crouching:
            self.actor.image = self.crouch_image
            self.actor.y = HEIGHT - 180 + game.CROUCH_OFFSET
        else:
            self.actor.image = self.idle_images[int(time.time() * 10) % len(self.idle_images)]
            self.actor.y = HEIGHT - 170

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = self.JUMP_STRENGTH
            self.is_jumping = True
            if game.sound_on:
                sounds.jump.play()

    def crouch(self, state):
        self.is_crouching = state

class AnimatedObject:
    def __init__(self, images, position):
        self.images = images
        self.actor = Actor(self.images[0], position)

    def update(self):
        self.actor.image = self.images[int(time.time() * 10) % len(self.images)]

game = Game()
dino = Dino()
planet = Actor('planet', (650, 100))

bird = AnimatedObject(['bee', 'bee_move'], (900, 375))
snail = AnimatedObject(['snail', 'snail_move'], (900, HEIGHT - 150))
coin = Actor('coin', (900, 420))

BACKGROUND_SPEED = 2
GROUND_SPEED = 2

def update():
    global game
    if game.game_started and not game.game_over and not game.game_won:
        game.background_x -= BACKGROUND_SPEED
        if game.background_x <= -WIDTH:
            game.background_x = 0

        game.ground1_x -= GROUND_SPEED
        if game.ground1_x <= -WIDTH:
            game.ground1_x = 0

        dino.update()
        bird.update()
        snail.update()

        bird.actor.x -= 5 + random.randint(-1, 1)
        snail.actor.x -= 3 + random.randint(-1, 1)
        coin.x -= 4 + random.randint(-1, 1)

        if bird.actor.x < -50:
            bird.actor.x = random.randint(900, 1500)
        if snail.actor.x < -50:
            snail.actor.x = random.randint(1600, 2200)
        if coin.x < -50:
            coin.x = random.randint(1200, 1800)

        if dino.actor.colliderect(coin):
            game.score += 1
            coin.x = random.randint(900, 1200)
            if game.sound_on:
                sounds.coin.play()

        if game.score >= game.WINNING_SCORE:
            game.game_won = True

        if dino.actor.colliderect(snail.actor) or dino.actor.colliderect(bird.actor):
            game.game_over = True

def draw():
    screen.clear()
    if not game.game_started:
        screen.fill("white")
        screen.draw.text("START", center=(400, 250), color="black", fontsize=50)
        screen.draw.text("EXIT", center=(400, 350), color="black", fontsize=50)
        game.music_button.draw()
    elif game.game_over:
        screen.fill("white")
        screen.draw.text("GAME OVER", center=(400, 200), color="red", fontsize=60)
        screen.draw.text(f"Final Score: {game.score}", center=(400, 250), color="black", fontsize=40)
        screen.draw.text("RESTART", center=(400, 350), color="black", fontsize=50)
        game.music_button.draw()
    elif game.game_won:
        screen.fill("green")
        screen.draw.text("KAZANDIN!", center=(400, 200), color="yellow", fontsize=60)
        screen.draw.text(f"Final Score: {game.score}", center=(400, 250), color="black", fontsize=40)
        screen.draw.text("RESTART", center=(400, 350), color="black", fontsize=50)
        game.music_button.draw()
    else:
        screen.blit('background', (game.background_x, 0))
        screen.blit('background', (game.background_x + WIDTH, 0))
        screen.blit('ground1', (game.ground1_x, HEIGHT - 150))
        screen.blit('ground1', (game.ground1_x + WIDTH, HEIGHT - 150))
        planet.draw()
        dino.actor.draw()
        bird.actor.draw()
        snail.actor.draw()
        coin.draw()
        screen.draw.text(f"Score: {game.score}", (10, 10), color="white")

def on_mouse_down(pos):
    if not game.game_started:
        if 350 <= pos[0] <= 450 and 225 <= pos[1] <= 275:
            game.game_started = True
            if game.sound_on:
                game.start_music()
        elif 350 <= pos[0] <= 450 and 325 <= pos[1] <= 375:
            exit()
        elif game.music_button.collidepoint(pos):
            game.toggle_music()
    elif game.game_over or game.game_won:
        if 350 <= pos[0] <= 450 and 325 <= pos[1] <= 375:
            game.restart()
        elif game.music_button.collidepoint(pos):
            game.toggle_music()

def on_key_down(key):
    if key == keys.UP:
        dino.jump()
    elif key == keys.DOWN:
        dino.crouch(True)

def on_key_up(key):
    if key == keys.DOWN:
        dino.crouch(False)

pgzrun.go()
