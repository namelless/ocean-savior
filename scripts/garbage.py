import pygame, random, time, math
from scripts.spark import Particle
class garbage:
    def __init__(self, game, img, screen, speed, health) -> None:
        self.game = game
        self.speed = speed
        self.screen = screen
        self.health = health
        self.pos = [random.randint(100, self.screen.get_width()-100), -100]
        self.img = img
    def rect(self):
        return pygame.Rect(*self.pos,*self.img.get_size())
    
    def update(self, bullets):
        trash = self.rect()
        self.pos[1] += self.speed
        for bullet in bullets:
            if trash.colliderect(bullet.rect()):
                self.health -= bullet.dmg
                bullets.remove(bullet)
                for i in range(5):
                    self.game.particles.append(Particle(math.radians(bullet.angle) + math.pi + (random.random()-0.5)/2, 2+ random.random()*2 ,bullet.pos))

        return bullets


    def render(self, offset=(0,0)):
        self.screen.blit(self.img,(self.pos[0] - offset[0], self.pos[1] - offset[1]))