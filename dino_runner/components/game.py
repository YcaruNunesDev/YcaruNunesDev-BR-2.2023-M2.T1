import pygame

from dino_runner.utils.constants import *
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.score = 0
        self.death_count = 0

        self.player = Dinosaur()
        self.obstacle_maneger = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()        

    def run(self):
        # Game loop: events - update - draw
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.playing = True
        self.score = 0 # Reseta a pontuação
        self.game_speed = 20 # Reseta a velocidade do jogo
        self.obstacle_maneger.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_maneger.update(self)
        self.update_score()
        self.power_up_manager.update(self)

    def update_score(self):
        self.score += 1
        if self.player.type == SPIDER_SENSE_TYPE:
            self.game_speed = 20
        elif self.score % 100 == 0:
            self.game_speed += 2
        

    def draw(self):
        self.clock.tick(FPS)
        self.screen.blit(FUNDO, (0, -100)) # "#FFFFFFF"
        self.draw_background()
        self.draw_score()
        self.player.draw(self.screen)
        self.obstacle_maneger.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.draw_power_up_time()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
       self.draw_text(f"score: {self.score}", (1000, 50))

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                 self.draw_text(f'{self.player.type.capitalize()} ENABLED FOR {time_to_show} SECONDS',(500,50))
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def  handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.draw_text("Press any key to start", (half_screen_width, half_screen_height))
        else:
            self.screen.blit(ICON, (half_screen_width - 35, half_screen_height - 130)) ## mostra mensagem de "Press any key to restart"
            self.draw_text("Press any key to restart", (half_screen_width, half_screen_height))
            self.draw_text(f"You score: {self.score}", (half_screen_width, half_screen_height + 50)) ## mostrar score atingido
            self.draw_text(f"Deaths: {self.death_count}", (half_screen_width, half_screen_height + 100))   ## mostra death_count
            pygame.mixer.music.fadeout(500)

        pygame.display.update()

        self.handle_events_on_menu()

   
    def draw_text(self,
                 text,text_rect,
                  font_size=35,
                  font_style = FONT_STYLE[0],
                  font_color = (255, 0, 0)
                  ):
        font = pygame.font.Font(font_style, font_size)
        self.text = font.render(f'{text}', True, (font_color))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = text_rect
        self.screen.blit(self.text, self.text_rect)
        