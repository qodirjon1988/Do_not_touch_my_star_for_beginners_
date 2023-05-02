import pygame
import random

# Ekranning o'lchami
WIDTH = 600
HEIGHT = 600

# Ranglar
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# O'yin yorliqlari
FONT_NAME = 'arial'
FONT_SIZE = 40

# Yulduzcha sinfi
class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('star.jpg').convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)

# O'yin sinfi
class Game:
    def __init__(self):
        # Pygame ni boshlash
        pygame.init()
        pygame.mixer.init()
        # Ekranni ochish
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Don't touch my star")
        # Clock
        self.clock = pygame.time.Clock()
        # Yulduzlar to'plami
        self.stars = pygame.sprite.Group()
        # O'yin yorliqlari
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        # O'yin holati
        self.game_over = False
        self.score = 0
        # Zvonok
        self.sound = pygame.mixer.Sound('game_song.m4a')
        # O'yin boshlanishi
        self.start_game()

    # O'yin boshlanishi
    def start_game(self):
        # Yulduzlar to'plamini yaratish
        for i in range(10):
            star = Star()
            self.stars.add(star)
        # O'yin boshlanish holatini tiklash
        self.game_over = False
        self.score = 0

    # O'yin tugatilishi
    def game_over_screen(self):
        self.screen.fill(BLACK)
        game_over_text = self.font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (WIDTH / 2, HEIGHT / 2)
        self.screen.blit(game_over_text, game_over_rect)
        score_text = self.font.render("Score: " + str(self.score), True, YELLOW)
        score_rect = score_text.get_rect()
        score_rect.center = (WIDTH / 2, HEIGHT / 2 + game_over_rect.height)
        self.screen.blit(score_text, score_rect)
        # Restart va Quit tugmachalari
        restart_text = self.font.render("Restart", True, WHITE)
        restart_rect = restart_text.get_rect()
        restart_rect.center = (WIDTH / 2, HEIGHT / 2 + game_over_rect.height + score_rect.height * 2)
        pygame.draw.rect(self.screen, YELLOW, (restart_rect.x - 10, restart_rect.y - 10, restart_rect.width + 20, restart_rect.height + 20))
        self.screen.blit(restart_text, restart_rect)
        quit_text = self.font.render("Quit", True, WHITE)
        quit_rect = quit_text.get_rect()
        quit_rect.center = (WIDTH / 2, HEIGHT / 2 + game_over_rect.height + score_rect.height * 3)
        pygame.draw.rect(self.screen, YELLOW, (quit_rect.x - 10, quit_rect.y - 10, quit_rect.width + 20, quit_rect.height + 20))
        self.screen.blit(quit_text, quit_rect)
        pygame.display.flip()
        # Qayta boshlash yoki chiqish
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if restart_rect.collidepoint(x, y):
                        self.start_game()
                        return
                    elif quit_rect.collidepoint(x, y):
                        pygame.quit()
                        exit()

    # O'yinni boshqarish
    def run(self):
        while True:
            self.clock.tick(60)

        # Inputlar
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Yulduzlar va qo'l sinfi yig'indisi
        all_sprites = pygame.sprite.Group()
        all_sprites.add(self.stars)

        # Yulduzlar ko'rsatish
        self.screen.fill(BLACK)
        all_sprites.draw(self.screen)

        # Yulduzcha qo'lga tegish
        hits = pygame.sprite.spritecollide(self.hand, self.stars, True)
        for hit in hits:
            self.score += 1
            self.sound.play()
            star = Star()
            self.stars.add(star)

        # Skor ko'rsatish
        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Qo'l boshqa qo'llarga tegishi
        pos = pygame.mouse.get_pos()
        self.hand.rect.x = pos[0]
        self.hand.rect.y = pos[1]
        if pygame.sprite.spritecollide(self.hand, self.stars, False):
            self.game_over = True

        # O'yin tugatilishi
        if self.game_over:
            self.game_over_screen()

        # Ekranni yangilash
        pygame.display.flip()
