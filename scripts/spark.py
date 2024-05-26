import pygame
import math


class Particle:
    def __init__(self, angle, speed, pos) -> None:
        self.angle = angle
        self.speed = speed
        self.pos = list(pos)

    def update(self):
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed        

        self.speed = max(0, self.speed - 0.1)

        return not self.speed
    
    def render(self, surf):
        polygon = [
            (self.pos[0] + math.cos(self.angle) * self.speed * 3, self.pos[1] + math.sin(self.angle) * self.speed * 3),
            (self.pos[0] + math.cos(self.angle - 0.5 * math.pi) * self.speed * 0.5, self.pos[1] + math.sin(self.angle - 0.5 * math.pi) * self.speed * 0.5),
            (self.pos[0] + math.cos(self.angle + math.pi) * self.speed * 3, self.pos[1] + math.sin(self.angle + math.pi) * self.speed * 3),
            (self.pos[0] + math.cos(self.angle + math.pi * 0.5) * self.speed * 0.5, self.pos[1] + math.sin(self.angle + math.pi * 0.5) * self.speed * 0.5),
        ]

        pygame.draw.polygon(surf, (255,255,255), polygon)