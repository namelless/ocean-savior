import math, pygame, time, random


class Bullet:
    def __init__(self, angle, pos, sprite, dmg, dis=500,speed=10) -> None:
        self.angle = angle
        self.pos = list(pos)
        self.dmg = dmg
        self.range = dis
        self.distance = [0,0]
        self.sprite = sprite
        self.speed = (math.sin(math.radians(angle + 90))*speed,math.cos(math.radians(angle + 90))*speed)
        
    def rect(self):
        
        return pygame.Rect(*self.pos,*pygame.transform.rotate(self.sprite,self.angle).get_size())
    
    def update(self, tilemap):
        bullet = self.rect()


        self.distance[0] += self.speed[0]
        self.distance[1] += self.speed[1]



        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]


    def out_of_range(self) -> bool:
        return True if math.sqrt(self.distance[0]**2 + self.distance[1]**2) > self.range else False

    def render(self, screen, scroll):
        screen.blit(pygame.transform.rotate(self.sprite,self.angle),[self.pos[i] -scroll[i] for i in range(2)])

class Weapon:
    def __init__(self, game, weapon, damage, delay, pos, range=500 ,bullet_count=1, rotation=0,offset=(0,0),ammo=30) -> None:
        self.game = game
        self.dmg = damage
        self.weapon = weapon
        self.delay = delay
        self.pos = list(pos)
        self.pos = [self.pos[0] + offset[0], self.pos[1] + offset[1]]
        self.state = ''
        self.offset = offset
        self.ammo = self.max_ammo = ammo
        self.bulletc = bullet_count
        self.range = range
        self.flip = True
        self.bullets = []
        self.initial_rotation = rotation
        self.rotation = rotation
        self.animation = None
        self.last_shot = time.time()
        self.set_state('idle')

    def update_delay(self, n):
        self.game.assets[f"{self.weapon}_{self.state}"].dur += n
        self.delay = self.game.assets[f"{self.weapon}_{self.state}"].animation_lenght()/60
        self.set_state('idle')

    def set_state(self, state):
        if self.state == state:
            return
        self.state = state
        self.animation = self.game.assets[f"{self.weapon}_{self.state}"].copy()

    def rect(self):
        return pygame.Rect(*self.game.player.pos,*self.animation.img().get_size())

    def update(self, action, mpos=(0,0)):
        self.pos[0] = self.game.player.pos[0] + self.offset[0]
        self.pos[1] = self.game.player.pos[1] + self.offset[1]
        angle = math.degrees(math.atan2((mpos[1] - self.pos[1]  ),self.pos[0]  - mpos[0])+math.pi)
        self.rotation = angle - self.initial_rotation
        if action:            
            if time.time() - self.last_shot > self.delay:

                if self.ammo > 0:
                    self.set_state(action)
                if self.bulletc > 1:
                    if self.ammo > 0:
                        self.game.player.velocity[0] -= math.cos(math.radians(angle)) * self.bulletc
                        self.game.player.velocity[1] += math.sin(math.radians(angle)) * self.bulletc
                    for i in range(5):
                        if self.ammo > 0:

                            self.game.sfx[self.weapon].play()
                            self.bullets.append(Bullet(self.rotation + (i-self.bulletc//2)*random.randint(300,500)/100, self.rect().center, self.game.assets[f'{self.weapon}_bullet'], dmg=self.dmg, dis=self.range))
                            self.ammo -= 1
                            self.last_shot = time.time()
                else:
                    if self.ammo > 0:
                        self.game.player.velocity[0] -= math.cos(math.radians(angle)) * self.bulletc
                        self.game.player.velocity[1] += math.sin(math.radians(angle)) * self.bulletc
                        self.game.sfx[self.weapon].play()
                        self.bullets.append(Bullet(self.rotation , self.rect().center, self.game.assets[f'{self.weapon}_bullet'], dmg=self.dmg, dis=self.range))
                        self.ammo -= 1
                        self.last_shot = time.time()

        for bullet in self.bullets:
            if bullet.update(self.game.tilemap):
                self.bullets.remove(bullet)
            if bullet.out_of_range():
                self.bullets.remove(bullet)
            
        if self.animation.update():
            self.set_state('idle')

    def render(self, surf, camera):
        
        self.flip = False if self.rotation < 90 or self.rotation > 270 else True
        img = pygame.transform.rotate(pygame.transform.flip(self.animation.img(),False, self.flip),self.rotation)
        surf.blit(img,(self.pos[0]-img.get_width()//2 - camera[0], self.pos[1]-img.get_height()//2- camera[1]))
        for bullet in self.bullets:
            bullet.render(surf, camera)