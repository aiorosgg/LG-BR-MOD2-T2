from cgitb import text
from tkinter import font
import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager

FONT_STYLE = "freesansbold.ttf"
 

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
        self.obstacle_manager = ObstacleManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
    
    def text_style(self, size_font, format, color_r, color_g, color_b, pos_x, pos_y):      
        font = pygame.font.Font(FONT_STYLE, size_font)
        text = font.render(format, True, (color_r, color_g, color_b))
        text_rect = text.get_rect()        
        text_rect.center = (pos_x, pos_y)
        self.screen.blit(text, text_rect)
                
    def update_score(self):
        self.score += 0.5
        if self.score % 100 == 0:
            self.game_speed += 1
    
        self.text_style(22, (f"Score: {self.score:.0f}"), 0, 0, 0, 1000, 50)      
               
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.update_score()
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

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.score = 0
                self.run()
                
    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.screen.blit(ICON,(half_screen_width - 42, half_screen_height - 100))
            self.text_style(30, ("Press any key to start"), 47,79,79, half_screen_width, half_screen_height + 80)
        else:
            self.screen.blit(ICON,(half_screen_width - 52, half_screen_height - 90))
            self.text_style(22, (f"Death(s): {self.death_count}"), 204,0,0, 680,362)
            self.text_style(22, ('Press any key for restart!'), 200,0,0, 480,362)
            self.text_style(33, (f"Score: {self.score:.0f}"), 0,0,0, half_screen_width, 160)
            
            self.game_speed = 20
            

        pygame.display.update()
        self.handle_events_on_menu()