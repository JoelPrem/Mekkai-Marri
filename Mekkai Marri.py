import pygame
import sys
import random


pygame.init()  # TODO: Sound

screen = pygame.display.set_mode((1600, 800))
pygame.display.set_caption("Mekkai Marri")


FPS = pygame.time.Clock()

BG = pygame.transform.scale(pygame.image.load("Data/Images/bg.png"), (1600, 800))

PLAY = pygame.image.load("Data/Images/Play_1.png")
PLAY_HOVER = pygame.image.load("Data/Images/Play_0.png")

PLATE = pygame.transform.scale(pygame.image.load("Data/Images/plate.png"), (128, 64))
plate_rect = PLATE.get_rect()


BIRYANI = pygame.image.load("Data/Images/Food/Biryani.png")
PANIPURI = pygame.image.load("Data/Images/Food/Pani Puri.png")
ROTI = pygame.image.load("Data/Images/Food/Roti.png")
SAMBAAR = pygame.image.load("Data/Images/Food/Sambaar.png")

pygame.display.set_icon(BIRYANI)

with open("Data/highscore.txt", "r") as file:
    high_score = int(file.read())


class Button:
    def __init__(self, x: int, y: int, image, scale: int, hover_button, screen, job):
        self.job = job
        self.screen = screen
        self.hover_button = hover_button
        width = image.get_width()
        height = image.get_height()
        self.scale = scale
        self.width = width
        self.height = height
        self.og_image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale))
        )
        self.image = self.og_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = pygame.transform.scale(
                self.hover_button,
                (int(self.width * self.scale), int(self.height * self.scale)),
            )
            if pygame.mouse.get_pressed()[0] == 1:
                self.job()
        else:
            self.image = self.og_image


class Food(Button):
    last = pygame.time.get_ticks()
    cooldown = 1000
    meals = []
    calories = 0

    def __init__(
        self, x: int, y: int, image, scale: int, hover_button, screen, job, calories
    ):
        super().__init__(x, y, image, scale, hover_button, screen, job)
        self.calories = calories
        Food.meals.append(self)
        Food.last = pygame.time.get_ticks()
        Food.cooldown -= Food.cooldown * 0.01

    def eat(self, pos):
        Food.meals.remove(self)
        [meal.draw() for meal in Food.meals]
        if 500 < pos[1] < 700:
            self.calories *= 2
        Food.calories += self.calories

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        pos = pygame.mouse.get_pos()
        if self.rect.colliderect(plate_rect):
            self.eat(pos)


def quit():
    pygame.quit()
    sys.exit()


def play():
    screen.fill("red")
    global idle
    idle = False


def start_over():
    pygame.mouse.set_visible(True)
    score = Food.calories
    Food.meals = []
    Food.cooldown = 1000
    Food.calories = 0
    Food.last = pygame.time.get_ticks()
    font = pygame.font.SysFont("algerian", 32)
    text = font.render(str(score), True, "white")
    h_score = font.render("High Score: " + str(high_score), True, "white")

    if score > high_score:
        with open("Data/highscore.txt", "w+") as file:
            file.write(str(score))
        h_score = font.render("You beat the High Score", True, "white")

    h_scoreRect = h_score.get_rect()
    h_scoreRect.center = (800, 550)
    textRect = text.get_rect()
    textRect.center = (800, 500)
    while True:
        screen.blit(BG, (0, 0))
        play_button.draw()
        screen.blit(text, textRect)
        screen.blit(h_score, h_scoreRect)
        pygame.display.update()
        FPS.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


def make_food():
    now = pygame.time.get_ticks()
    if now - Food.last >= Food.cooldown:
        food_type = random.choice(
            [[BIRYANI, 150], [ROTI, 100], [SAMBAAR, 90], [PANIPURI, 70]]
        )
        Food.last = now
        eat_button = Food(
            random.randint(50, 1550),
            5,
            food_type[0],
            8,
            1,
            screen,
            make_food,
            food_type[1],
        )
    for meal in Food.meals:
        meal.rect.y += 0.05 * meal.calories
        if meal.rect.y >= 780:
            start_over()

    [meal.draw() for meal in Food.meals]


def game_loop():
    pygame.mouse.set_visible(False)
    while True:
        plate_rect.center = pygame.mouse.get_pos()
        screen.blit(BG, (0, 0))

        screen.blit(PLATE, plate_rect)
        make_food()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        pygame.display.update()
        FPS.tick(30)


play_button = Button(800, 400, PLAY, 4, PLAY_HOVER, screen, game_loop)


def mekkai_marri():
    global idle
    idle = True
    while True:
        screen.blit(BG, (0, 0))
        play_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        pygame.display.update()
        FPS.tick(30)


mekkai_marri()
