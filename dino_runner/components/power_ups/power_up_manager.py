from random import randint
import pygame

from dino_runner.components.power_ups.shield_hemmer import Shield, Hammer


class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appers = 0
    
    def generate_power_up(self, score):
        if len(self.power_ups) == 0 and self.when_appers == score:
            self.power = randint(0, 1)
            self.when_appers += randint(200, 300)
            if self.power == 0:
                self.power_ups.append(Shield())
            else:
                self.power_ups.append(Hammer()) 
                
    def update(self, score, game_speed, player):
        self.generate_power_up(score)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                if self.power == 0:
                    player.hammer = False
                    player.shield = True
                else:
                    player.hammer = False
                    player.shield = True
                player.shield = True
                player.has_power_up = True
                player.type = power_up.type
                player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                self.power_ups.remove(power_up)
                
                    
    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appers = randint(200, 1000)