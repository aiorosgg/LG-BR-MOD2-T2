import pygame

from dino_runner.utils.constants import BG, CLOUD, ICON, RESTART, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, GAME_OVER
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager


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
        self.x_pos_cloud = 1900
        self.y_pos_cloud = 120
        self.score = 0
        self.record = 0
        self.rec = [0]
        self.death_count = 0
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

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
        self.power_up_manager.reset_power_ups()
  
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
        self.power_up_manager.update(self.score, self.game_speed, self.player)
        self.update_score()
                    
    def update_score(self):
        self.score += 0.5
        if self.score % 100 == 0:
            self.game_speed += 1
        self.text_format(22, (f"Score: {self.score:.0f}"), "#cc0000", 1000, 50)
        if self.rec[0] >= self.score:
            self.text_format(22, (f"Score: {self.score:.0f}"), "#cc0000", 1000, 50)
        else:
            self.text_format(22, (f"Score: {self.score:.0f}"), "#008000", 1000, 50)
                             
    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                self.text_format(18, (f"{self.player.type.capitalize()} enabled for {time_to_show} seconds."), "#808080", 550,30)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE
                
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill("#C0C0C0")
        self.draw_background()       
        self.cloud()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.update_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
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
    
    def cloud(self):
        image_width = CLOUD.get_width()
        self.screen.blit(CLOUD, (self.x_pos_cloud + 20, self.y_pos_cloud + 20))
        self.screen.blit(CLOUD, (self.x_pos_cloud + 200, self.y_pos_cloud + 80))
        self.screen.blit(CLOUD, (self.x_pos_cloud - 400, self.y_pos_cloud + 20))
        self.screen.blit(CLOUD, (self.x_pos_cloud - 50, self.y_pos_cloud + 110))
        self.screen.blit(CLOUD, (self.x_pos_cloud - 150, self.y_pos_cloud + 130))
        self.screen.blit(CLOUD, (self.x_pos_cloud - 300, self.y_pos_cloud + 80))
        self.screen.blit(CLOUD, (self.x_pos_cloud - 600, self.y_pos_cloud + 110))
        self.screen.blit(CLOUD, (self.x_pos_cloud - 470, self.y_pos_cloud + 130))

        if self.x_pos_cloud <= -image_width - 200:
            self.screen.blit(CLOUD, (image_width - self.x_pos_cloud +200, self.y_pos_cloud))
            self.x_pos_cloud = 1900
        self.x_pos_cloud -=  3

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.score = 0
                self.run()
                
                
    def text_format(self, size_font, format, color_hex, pos_x, pos_y):      
        font = pygame.font.Font(FONT_STYLE, size_font)
        text = font.render(format, True, (color_hex))
        text_rect = text.get_rect()        
        text_rect.center = (pos_x, pos_y)
        self.screen.blit(text, text_rect)
                
    def show_menu(self):
        self.screen.fill("#C0C0C0")
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2 
        

        if self.death_count == 0:
            self.text_format(21, (TITLE), "#2f4f4f", half_screen_width, half_screen_height + 180)
            self.screen.blit(ICON,(half_screen_width - 42, half_screen_height - 100))
            self.text_format(30, ("Press any key to start"), "#2f4f4f", half_screen_width, half_screen_height + 80)
        else:
            if self.score >= self.record:
                self.record = self.score -1
                self.rec.append(self.rec)
                self.rec.insert(0, self.record)
            self.text_format(22, (f"Record: {self.rec[0]}"), "#008000", half_screen_width, 500)
            self.screen.blit(GAME_OVER,(half_screen_width -205, 320))
            self.screen.blit(RESTART,(half_screen_width - 55, half_screen_height - 86))
            self.screen.blit(ICON,(50, half_screen_height + 180))           
            self.text_format(22, (f"Death(s): {self.death_count}"), "#cc0000", half_screen_width,430)
            self.text_format(22, ('Press any key for restart!'), "#808080", half_screen_width,378)
            self.text_format(33, (f"Score: {self.score:.0f}"), "#000000", half_screen_width -15, 160)
            self.game_speed = 20
            

        pygame.display.update()
        self.handle_events_on_menu()



            
                