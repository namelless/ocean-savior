import pygame
import random
import math
import time
class collectable:
    def __init__(self, game, pos, speed, img, effect, delay) -> None:
        self.game = game
        self.pos = list(pos)
        self.speed = speed
        self.img = img
        self.effect = effect
        self.delay = delay
        self.time = time.time()
        self.circles = []

    def rect(self):
        return pygame.Rect(*self.pos, *self.img.get_size())
    

    def update(self, player_r, tilemap,y ):
        if time.time() - self.time > self.delay:
            return True


        if self.pos[1] > y:
            return True
        self.pos[1] += self.speed
        c = self.rect()
        if c.colliderect(player_r):
            self.game.effect(self.effect)
            self.game.sfx['pick'].play()
            return True
        for rect in list(tilemap.physics_rects_around(self.pos)):
            if c.colliderect(rect):
                c.bottom = rect.top 
            self.pos[1] = c.y

    def render(self, screen, offset=(0,0)):
        screen.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))