import os
import pygame
import math  
import time
import random

def load_image(path,size=None,key=None):
    if size:
        img = pygame.transform.scale(pygame.image.load(path).convert_alpha(),size)
    else:
        img = pygame.image.load(path).convert_alpha()
    if key:
        img.set_colorkey(key)
    return img

def load_images(path,size=None, key=None):
    images = []
    for img_name in sorted(os.listdir(path)):
        images.append(load_image(path + '/' + img_name,size=size,key=key))
    return images

class Animation:
    def __init__(self, images, dur=5, loop=True):
        self.images = images
        self.dur = dur
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.dur, self.loop)

    def animation_lenght(self):
        return self.dur * len(self.images)


    def update(self):
        if not self.done:
            if self.loop:
                self.frame = (self.frame + 1) % (self.dur * len(self.images))
            else:
                self.frame = min(self.frame + 1 ,self.dur * len(self.images) -1)
                if self.frame >= self.dur * len(self.images) -1:
                    self.done = True
        return self.done
    
    def img(self):
        return self.images[int(self.frame/self.dur)]

def load_dir(path, size=None):
    dirs = {}
    for dire in sorted(os.listdir(path)):
        
        dirs[dire] = load_images(path + '/' + dire,size=size)
    return dirs

def spritesheat(sheet ,w : int,h : int, x=0,y=0 , key=(0,0,0),scale=1):
    imgs = []
    sheet = load_image(sheet)
    while x <= sheet.get_width():
        
        crop = (x,y,w,h)
        img = pygame.Surface((w,h),pygame.SRCALPHA)
        img.blit(sheet,(0,0),crop)
        img = pygame.transform.scale_by(img,scale)
        imgs.append(img)
        
        x += w
    return imgs

class HealthBar:
    def __init__(self, pos, size, reverse=False) -> None:
        self.pos = list(pos)
        self.size = list(size)
        self.reverse = reverse
        

    def render(self, surface,ratio):
        size = list(self.size)
        size[0] *= ratio
        if not self.reverse:
            pygame.draw.rect(surface,(255,0,0),(self.pos[0],self.pos[1],*self.size))
            pygame.draw.rect(surface,(0,255,0),(self.pos[0],self.pos[1],*size))
            pygame.draw.rect(surface,(0,0,0),(*self.pos,*self.size),3)
        else:
            pygame.draw.rect(surface,(255,0,0),(self.pos[0],self.pos[1],*self.size))
            pygame.draw.rect(surface,(0,255,0),(self.pos[0]+self.size[0]-size[0],self.pos[1],*size))            
            pygame.draw.rect(surface,(0,0,0),(*self.pos, *self.size),3)



def fps_counter(clock, surf, font):
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps , 1, pygame.Color("green"))
    surf.blit(fps_t,(0,0))



