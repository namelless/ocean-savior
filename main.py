import pygame
import sys
import time
import random
import math
from scripts.outline import perfect_outline
from scripts.utils import load_dir, load_images, load_image, spritesheat,HealthBar, Animation
from scripts.player import Player
from scripts.weapons import Weapon
from scripts.tilemap import Tilemap
from scripts.garbage import garbage
from scripts.pickups import collectable
from scripts.spark import Particle
class Main:
    def __init__(self):
        pygame.mixer.pre_init()
        pygame.init()
        self.font = pygame.font.SysFont("Arial" , 18 , bold = True)
        self.width = 1200
        self.height = 550
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("ocean saviour")
        with open('assets/level.txt','r') as f:

            self.highest_level = int(f.read())
        scale = 1.6
        self.particles = []
        self.level = 1
        self.assets = {
             'shotgun_fire' : Animation(spritesheat('assets/shoot.png',40,22,scale=scale),dur=6,loop=False),
             'shotgun_idle' : Animation([pygame.transform.scale_by(load_image('assets/shotgun.png'),scale)],dur=6),
             'shotgun_bullet' : pygame.transform.scale_by(load_image('assets/bullet.png'),1),
             'pistol_fire' : Animation(spritesheat('assets/pistol_shoot.png',63,32,scale=1),dur=2,loop=False),
             'pistol_idle' : Animation([pygame.transform.scale_by(load_image('assets/pistol.png'),1)],dur=6),
             'pistol_bullet' : pygame.transform.scale_by(load_image('assets/pistol_bullet.png'),1),             
             'grass' : load_images('assets/grass',size=(40,40),key=(0,0,0)),
             'player' : load_image('assets/player.png',(35,45)),
             'bag' : pygame.transform.scale_by(load_image('assets/trash_bag.png'),1.7),
             'bg' : load_image('assets/bg.png',(self.screen.get_width(),650)),
             'heal' : load_image('assets/healing.png',(32,32)),
             'reload' : load_image('assets/ammo.png',(32,32)),
             'can' : load_image('assets/can.png')
        }
        self.player = Player(self, self.screen,(200,0), y_difference=5,health=100)
        self.shotgun = Weapon(self, 'shotgun', 50, self.assets['shotgun_fire'].animation_lenght()/60, (100,100), bullet_count=5,offset=(25,35),range=300)
        self.pistol = Weapon(self, 'pistol', 50, self.assets['pistol_fire'].animation_lenght()/60, (100,100),offset=(25,35), range=700)
        self.tilemap = Tilemap(self, 40)
        self.trash = []
        self.sfx = {
            'pick' : pygame.mixer.Sound('assets/pickup.wav'),
            'pistol' : pygame.mixer.Sound('assets/pistol.mp3'),
            'shotgun' : pygame.mixer.Sound('assets/shotgun.mp3'),
        }
        self.sfx['shotgun'].set_volume(0.1)
        self.sfx['pistol'].set_volume(0.6)
        self.unlocked_trash = ['bag','can']
        self.healthbar = HealthBar((20,20),(200,20),False)
        self.gun = 0
        self.weapons = [self.shotgun]
        self.upgrades = ['health', 'dmg', 'range', 'speed', 'ammo']
        self.upgrade_dialouge = {
            'health' : f'increase Health by ',
            'dmg' : f'increase Damage by ',
            'range' : f'increase Range by ',
            'speed' : f'increase speed by ',
            'ammo' : f'increase max ammo by ',
        }
        self.unlocked_weapons = [self.pistol]
        self.tilemap.load('assets/lvl.json')
        self.collectables = []
        self.drop_loot = ['heal','reload']
        self.y = 470
        self.m_time = time.time()
        self.run()

    def reset(self):
        self.player.pos = [200,0]
        for weapon in self.unlocked_weapons:
            weapon.ammo = weapon.max_ammo
        self.player = Player(self, self.screen,(200,0), y_difference=5,health=100)
        self.shotgun = Weapon(self, 'shotgun', 50, self.assets['shotgun_fire'].animation_lenght()/60, (100,100), bullet_count=5,offset=(25,35),range=300)
        self.pistol = Weapon(self, 'pistol', 50, self.assets['pistol_fire'].animation_lenght()/60, (100,100),offset=(25,35), range=700)
        if self.level > self.highest_level:
            with open('assets/level.txt', 'w') as f:
                f.write(str(self.level))
            self.highest_level = self.level
        self.level = 1
        self.weapons = [self.shotgun]
        self.unlocked_weapons = [self.pistol]
        self.gun = 0
        
        self.trash = []

    def effect(self, effect):
        if effect[0] == 'heal':
            self.player.health = self.player.max_health
        if effect[0] == 'reload':
            for i,w in enumerate(self.unlocked_weapons):
                self.unlocked_weapons[i].ammo =  w.max_ammo
        if effect[0] == 'health':
            self.player.max_health *= (effect[1]/100 )+ 1
            self.player.health = self.player.max_health
        if effect[0] == 'dmg':
            for weapon in self.unlocked_weapons:
                weapon.dmg *= (effect[1]/100 )+ 1
        if effect[0] == 'range':
            for weapon in self.unlocked_weapons:
                weapon.range *= 3*((effect[1])/100 )+ 1

        if effect[0] == 'ammo':
            for weapon in self.unlocked_weapons:
                weapon.max_ammo *= ((effect[1]/100 )+ 1)
                weapon.max_ammo = int(weapon.max_ammo)
                weapon.ammo = weapon.max_ammo
        if effect[0] == 'speed':
            self.player.speed *= ((effect[1]*2.5)/100 )+ 1
            self.player.speed = int(self.player.speed)
        

    def run(self):
        font = pygame.font.Font('assets/squarefont/Square.ttf',32)
        sfont = pygame.font.Font('assets/squarefont/Square.ttf',28)
        camera = [0,0]
        movement = [False for i in range(4)]        
        last_frame = time.time()
        wave_l = 7
        lag = 2
        clicking = False
        count = 0
        drop_odds = 0.35
        last_garbage = 0
        upgrading = False
        paused = True
        l = False
        c_del = 20
        
        text_color = (150,30,30)
        while True:
            self.screen.fill((0,0,0))
            self.screen.blit(self.assets['bg'],(0,0))
            dt = time.time() - last_frame
            last_frame = time.time()
            
            delay = (random.randint(30,200)/10)/self.level
            weapon_switch = False
            if (self.player.rect().centerx - self.screen.get_width()/2 - camera[0])/30 > lag or (self.player.rect().centerx - self.screen.get_width()/2 - camera[0])/10 < -lag:
                camera[0] += (self.player.rect().centerx - self.screen.get_width()/2 - camera[0])/30
            if (self.player.rect().centery - self.screen.get_height()/2 - camera[1])/30 > lag or (self.player.rect().centery - self.screen.get_height()/2 - camera[1])/10 < -lag:
                camera[1] += (self.player.rect().centery - self.screen.get_height()/2 - camera[1])/30
            scroll = (int(camera[0]), int(camera[1]))
            scroll = [0,0]
            mpos = pygame.mouse.get_pos()
            if not upgrading and not paused:
                if self.level % 2 == 0 and self.weapons:
                    self.unlocked_weapons.append(self.weapons.pop())
                if time.time() - last_garbage > delay and count < self.level * wave_l:
                    count += 1
                    last_garbage = time.time()
                    mg = pygame.transform.scale_by(self.assets[random.choice(self.unlocked_trash)],1/math.sqrt(self.level))
                    self.trash.append(garbage(self,mg, self.screen, 2, sum(mg.get_size())))
                if count >= self.level * wave_l and not self.trash:
                    self.level += 1
                    count = 0
                    upgrading = True
                    l = True
                for t in self.trash:
                    self.unlocked_weapons[self.gun].bullets = t.update(self.unlocked_weapons[self.gun].bullets)
                    
                    if t.pos[1] > self.y:
                        self.player.health -= t.health//(4-math.sqrt(self.level))
                        self.trash.remove(t)
                    if t.health <= 0:
                        try:
                            self.trash.remove(t)
                        except Exception:
                            pass
                        r = random.random()
                        if r < drop_odds:
                            skill = [random.choice(self.drop_loot), random.randint(10,50)]
                            self.collectables.append(collectable(self,t.pos,t.speed,self.assets[skill[0]],skill,c_del))
                if self.player.pos[1] > self.y or self.player.health < 1:
                    self.lose()
                self.player.flip = self.unlocked_weapons[self.gun].flip
                self.player.update(self.tilemap,[movement[1] - movement[0], 0])
                self.unlocked_weapons[self.gun].update(None, mpos)

            for particle in self.particles:
                if particle.update():
                    self.particles.remove(particle)
                particle.render(self.screen)
            self.healthbar.render(self.screen, self.player.health/self.player.max_health)
            self.tilemap.render(self.screen)
            for t in self.trash:
                t.render(scroll)
            self.player.render(self.screen, scroll)
            
            self.unlocked_weapons[self.gun].render(self.screen, scroll)
            offset = 0

            for c in self.collectables:
                if c.update(self.player.rect(),self.tilemap, self.y):
                    self.collectables.remove(c)
                c.render(self.screen, scroll)

            if upgrading:
                if l:
                    u = self.upgrades.copy()
                    choices = []
                    for i in range(3):
                        choices.append((random.choice(u),random.randint(10,50)))
                        u.remove(choices[i][0])
                    l = False
                for i in range(3):

                    text = sfont.render(f"{self.upgrade_dialouge[choices[i][0]]}{choices[i][1]}%", True, text_color)
                    if choices[i][0] == 'range' or choices[i][0] == 'speed':
                        text = sfont.render(f"{self.upgrade_dialouge[choices[i][0]]}{int(choices[i][1]*2.5)}%", True, text_color)
                    pos = (80+i*380,300)
                    rect= pygame.Rect(*pos,*text.get_size())
                    perfect_outline(text,self.screen,pos,(255,255,255))
                    self.screen.blit(text,pos)
                    text = font.render(f"you have leveled up choose an upgrade", True, text_color)
                    perfect_outline(text,self.screen,(300,160),(255,255,255))
                    self.screen.blit(text,(300,160))
                    if rect.collidepoint(mpos) and clicking:
                        upgrading = False
                        self.effect(choices[i])

            for i, weapon in enumerate(self.unlocked_weapons):
                img = self.assets[f"{weapon.weapon}_idle"].img()
                img = pygame.transform.scale_by(img, 1.3)
                offset += img.get_width() + 30
                p = 1000 - len(self.unlocked_weapons) * 100
                self.screen.blit(img,(p + offset ,30))
                rect = pygame.Rect(p + offset ,30,*img.get_rect()[2:4])
                if rect.collidepoint(mpos) and clicking:
                    weapon_switch = True
                    self.gun = i
            text = font.render(f"Ammo : {str(self.unlocked_weapons[self.gun].ammo)}", True, text_color)
            self.screen.blit(text,(700,20))
            text = font.render(f"Health : {int(self.player.health)}", True, text_color)
            self.screen.blit(text,(25,50))            
            text = font.render(f"Level : {self.level}", True, text_color)
            self.screen.blit(text,(430,20))    
            if paused:
                text = font.render(f"presss W A D to move", True, text_color)
                perfect_outline(text,self.screen,(430,200),(255,255,255),(255,255,255),(255,255,255))
                self.screen.blit(text,(430,200))                    
                text = font.render(f"left click to shoot and dont let the trash pollute the ocean", True, text_color)
                perfect_outline(text,self.screen,(60,300),(255,255,255))
                self.screen.blit(text,(60,300))                    
                text = font.render(f"click anywhere to continue", True, text_color)
                perfect_outline(text,self.screen,(400,380),(255,255,255))
                self.screen.blit(text,(400,380))                                    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if paused and self.level == 1:
                        paused = False
                    if event.button == 1:
                        clicking = True  
                        if not upgrading and not paused:
                            if not weapon_switch:
                                self.unlocked_weapons[self.gun].update('fire',mpos)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        clicking = False     
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if not upgrading and not paused:
                            self.unlocked_weapons[self.gun].set_state('idle')
                            self.gun = (self.gun + 1) % len(self.unlocked_weapons)

                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        movement[1] = True
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        movement[2] = True
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if self.player.air_time < 5:
                            self.player.velocity[1] = -8
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        movement[1] = False        
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        movement[2] = False
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        movement[3] = False   
        
            self.clock.tick(60)
            pygame.display.update()


    def lose(self):
        font = pygame.font.Font('assets/squarefont/Square.ttf',32)
        bfont = pygame.font.Font('assets/squarefont/Square.ttf',33)
        text_color = (200,30,30)
        time.sleep(0.3)
        while True:

            text = font.render(f"You have lost left click to restart", True, text_color)
            perfect_outline(text,self.screen,(350,180),(255,255,255))
            self.screen.blit(text,(350,180))            
            text = font.render(f"level reached : {self.level} ", True, text_color)
            perfect_outline(text,self.screen,(350,280),(255,255,255))
            self.screen.blit(text,(350,280))            
            text = font.render(f"Highest level reached : {max(self.level,self.highest_level)} ", True, text_color)
            perfect_outline(text,self.screen,(350,380),(255,255,255))
            self.screen.blit(text,(350,380))            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.reset()

                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        self.reset()
                        self.run()
            self.clock.tick(60)
            pygame.display.update()

game = Main()